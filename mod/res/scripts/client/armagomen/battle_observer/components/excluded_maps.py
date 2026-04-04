from armagomen._constants import EXCLUDED_MAPS, MAIN
from armagomen.battle_observer.i18n.exluded_maps import EXCLUDED_MAPS_BY_LANG
from armagomen.utils.common import delayedCall
from armagomen.utils.dialogs import ExcludedMapsDialog
from armagomen.utils.events import g_events
from constants import PREMIUM_TYPE, PremiumConfigs
from gui.ClientUpdateManager import g_clientUpdateManager
from gui.game_control.wot_plus.utils import getExcludedMapsPromoData
from gui.impl.pub.dialog_window import DialogButtons
from gui.shared.event_dispatcher import showMapsBlacklistView
from helpers import dependency
from PlayerEvents import g_playerEvents
from renewable_subscription_common.schema import renewableSubscriptionsConfigSchema
from renewable_subscription_common.settings_constants import RS_TIER
from skeletons.gui.app_loader import GuiGlobalSpaceID, IAppLoader
from skeletons.gui.game_control import IGameSessionController, IWotPlusController
from skeletons.gui.lobby_context import ILobbyContext
from skeletons.gui.shared import IItemsCache
from wg_async import wg_async, wg_await

SERVER_SETTINGS_DIFF_KEYS = (
    PremiumConfigs.IS_PREFERRED_MAPS_ENABLED,
    PremiumConfigs.PREFERRED_MAPS
)


class ExcludedMapsProcessor(object):
    gameSession = dependency.descriptor(IGameSessionController)
    wotPlus = dependency.descriptor(IWotPlusController)
    appLoader = dependency.descriptor(IAppLoader)
    itemsCache = dependency.descriptor(IItemsCache)
    lobbyContext = dependency.descriptor(ILobbyContext)

    def __init__(self):
        self.__enabled = False
        self.__isPremium = False
        self.__dialog = None
        self.appLoader.onGUISpaceEntered += self.onGUISpaceEntered
        self.appLoader.onGUISpaceLeft += self.onGUISpaceLeft
        g_events.onModSettingsChanged += self._onModSettingsChanged
        g_clientUpdateManager.addCallbacks({'preferredMaps': self.__onPreferredMapsChanged})

    def fini(self):
        self.appLoader.onGUISpaceEntered -= self.onGUISpaceEntered
        self.appLoader.onGUISpaceLeft -= self.onGUISpaceLeft
        g_events.onModSettingsChanged -= self._onModSettingsChanged
        g_clientUpdateManager.removeObjectCallbacks(self)

    @property
    def isLobby(self):
        return self.appLoader.getSpaceID() == GuiGlobalSpaceID.LOBBY

    @property
    def _serverSettings(self):
        return self.lobbyContext.getServerSettings()

    def onGUISpaceEntered(self, spaceID):
        if spaceID != GuiGlobalSpaceID.LOBBY:
            return
        self.__isPremium = self.itemsCache.items.stats.isActivePremium(PREMIUM_TYPE.PLUS)
        self._serverSettings.onServerSettingsChange += self.__onServerSettingsChanged
        self.gameSession.onPremiumNotify += self.__onPremiumNotify
        self.wotPlus.onDataChanged += self.__onWotPlusChanged
        g_playerEvents.onConfigModelUpdated += self._onConfigModelUpdated
        self.__update()

    def onGUISpaceLeft(self, spaceID):
        if spaceID != GuiGlobalSpaceID.LOBBY:
            return
        self.__isPremium = False
        if self.__dialog is not None:
            self.__dialog = None
        self._serverSettings.onServerSettingsChange -= self.__onServerSettingsChanged
        self.gameSession.onPremiumNotify -= self.__onPremiumNotify
        self.wotPlus.onDataChanged -= self.__onWotPlusChanged
        g_playerEvents.onConfigModelUpdated -= self._onConfigModelUpdated

    def __onPreferredMapsChanged(self, _):
        if self.isLobby:
            self.__update()

    def _onConfigModelUpdated(self, gpKey):
        if renewableSubscriptionsConfigSchema.gpKey == gpKey:
            self.__update()

    def _onModSettingsChanged(self, name, data):
        if name == MAIN.NAME and MAIN.EXCLUDED_MAP_SLOTS_NOTIFICATION in data:
            if self.__enabled != data[MAIN.EXCLUDED_MAP_SLOTS_NOTIFICATION]:
                self.__enabled = data[MAIN.EXCLUDED_MAP_SLOTS_NOTIFICATION]
                if self.isLobby:
                    self.__update()

    def __onServerSettingsChanged(self, diff):
        if any(key in diff for key in SERVER_SETTINGS_DIFF_KEYS):
            self.__update()

    def __onPremiumNotify(self, isPremium, *args):
        if isPremium != self.__isPremium:
            self.__isPremium = isPremium
            self.__update()

    def __onWotPlusChanged(self, data):
        if RS_TIER in data:
            self.__update()

    @staticmethod
    def __getLocalizedMessage(availableSlots):
        return EXCLUDED_MAPS_BY_LANG[EXCLUDED_MAPS.MESSAGE] % availableSlots

    @wg_async
    def __showDialog(self, message):
        self.__dialog = ExcludedMapsDialog()
        dialog = yield wg_await(self.__dialog.show(EXCLUDED_MAPS_BY_LANG[EXCLUDED_MAPS.HEADER], message))
        if dialog.result == DialogButtons.RESEARCH:
            showMapsBlacklistView()
        self.__dialog = None

    @delayedCall(3.0)
    def __update(self):
        if not self.__enabled or self.__dialog is not None or not self._serverSettings.isPreferredMapsEnabled():
            return
        mapsConfig = self._serverSettings.getPreferredMapsConfig()
        # usedSlots = sum(1 for mapId, _ in self.itemsCache.items.stats.getMapsBlackList() if mapId > 0)
        usedSlots = len(self.itemsCache.items.stats.getMapsBlackList())
        isWotPlusAcc, wotPlusSlots = getExcludedMapsPromoData()
        totalSlots = sum([
            mapsConfig['defaultSlots'],
            mapsConfig['premiumSlots'] if self.__isPremium else 0,
            wotPlusSlots if isWotPlusAcc else 0
        ])

        if usedSlots < totalSlots:
            self.__showDialog(self.__getLocalizedMessage(totalSlots - usedSlots))


excluded_maps = ExcludedMapsProcessor()


def fini():
    excluded_maps.fini()

from armagomen._constants import EXCLUDED_MAPS, MAIN
from armagomen.battle_observer.i18n.exluded_maps import EXCLUDED_MAPS_BY_LANG
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.dialogs import ExcludedMapsDialog
from constants import PREMIUM_TYPE, PremiumConfigs, RENEWABLE_SUBSCRIPTION_CONFIG
from gui.impl.pub.dialog_window import DialogButtons
from gui.shared.event_dispatcher import showMapsBlacklistView
from helpers import dependency
from skeletons.gui.app_loader import GuiGlobalSpaceID, IAppLoader
from skeletons.gui.game_control import IGameSessionController, IWotPlusController
from skeletons.gui.lobby_context import ILobbyContext
from skeletons.gui.shared import IItemsCache
from wg_async import wg_async, wg_await

SERVER_SETTINGS_DIFF_KEYS = (
    PremiumConfigs.IS_PREFERRED_MAPS_ENABLED,
    PremiumConfigs.PREFERRED_MAPS,
    RENEWABLE_SUBSCRIPTION_CONFIG
)


class ExcludedMapsProcessor(object):
    gameSession = dependency.descriptor(IGameSessionController)
    wotPlus = dependency.descriptor(IWotPlusController)
    appLoader = dependency.descriptor(IAppLoader)
    itemsCache = dependency.descriptor(IItemsCache)
    lobbyContext = dependency.descriptor(ILobbyContext)

    def __init__(self):
        self.__enabled = user_settings.main[MAIN.EXCLUDED_MAP_SLOTS_NOTIFICATION]
        self.__isPremium = False
        self.__isDialogVisible = False
        self.appLoader.onGUISpaceEntered += self.onGUISpaceEntered
        self.appLoader.onGUISpaceLeft += self.onGUISpaceLeft
        user_settings.onModSettingsChanged += self._onModSettingsChanged

    def fini(self):
        self.appLoader.onGUISpaceEntered -= self.onGUISpaceEntered
        self.appLoader.onGUISpaceLeft -= self.onGUISpaceLeft
        user_settings.onModSettingsChanged -= self._onModSettingsChanged

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
        self.__update()

    def onGUISpaceLeft(self, spaceID):
        if spaceID != GuiGlobalSpaceID.LOBBY:
            return
        self.__isPremium = False
        self.__isDialogVisible = False
        self._serverSettings.onServerSettingsChange -= self.__onServerSettingsChanged
        self.gameSession.onPremiumNotify -= self.__onPremiumNotify
        self.wotPlus.onDataChanged -= self.__onWotPlusChanged

    def _onModSettingsChanged(self, data, name):
        if name == MAIN.NAME:
            self.__enabled = data[MAIN.EXCLUDED_MAP_SLOTS_NOTIFICATION]
            self.__update()

    def __onServerSettingsChanged(self, diff):
        if any(key in diff for key in SERVER_SETTINGS_DIFF_KEYS):
            self.__update()

    def __onPremiumNotify(self, isPremium, *args):
        if isPremium != self.__isPremium:
            self.__isPremium = isPremium
            self.__update()

    def __onWotPlusChanged(self, data):
        if 'isEnabled' in data:
            self.__update()

    @staticmethod
    def __getLocalizedMessage(availableSlots):
        return EXCLUDED_MAPS_BY_LANG[EXCLUDED_MAPS.MESSAGE] % availableSlots

    @wg_async
    def __showDialog(self, message):
        self.__isDialogVisible = True
        header = EXCLUDED_MAPS_BY_LANG[EXCLUDED_MAPS.HEADER]
        dialog = yield wg_await(ExcludedMapsDialog().showExcludedMapsDialog(header, message))
        if dialog.result == DialogButtons.RESEARCH:
            showMapsBlacklistView()
        self.__isDialogVisible = False

    def __update(self):
        if not self.__enabled or self.__isDialogVisible or not self._serverSettings.isPreferredMapsEnabled():
            return
        mapsConfig = self._serverSettings.getPreferredMapsConfig()
        usedSlots = sum(int(mapId > 0) for mapId, _ in self.itemsCache.items.stats.getMapsBlackList())
        totalSlots = sum([
            mapsConfig['defaultSlots'],
            mapsConfig['premiumSlots'] if self.__isPremium else 0,
            mapsConfig['wotPlusSlots'] if self.wotPlus.isEnabled() and self._serverSettings.isWotPlusExcludedMapEnabled() else 0
        ])
        if usedSlots < totalSlots:
            self.__showDialog(self.__getLocalizedMessage(totalSlots - usedSlots))


excluded_maps = ExcludedMapsProcessor()


def fini():
    excluded_maps.fini()

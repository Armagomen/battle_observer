from armagomen._constants import EXCLUDED_MAPS, MAIN
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.battle_observer.settings.hangar.i18n import localization
from armagomen.utils.common import logDebug
from armagomen.utils.dialogs import ExcludedMapsDialog
from armagomen.utils.events import g_events
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
        self.__isHangar = False
        self.__isPremium = False
        self.__isDialogDeferred = True
        self.__isDialogVisible = False
        self.appLoader.onGUISpaceEntered += self.init
        self.appLoader.onGUISpaceLeft += self.fini
        g_events.onHangarLoaded += self.onHangarLoaded

    @property
    def _serverSettings(self):
        return self.lobbyContext.getServerSettings()

    def init(self, spaceID):
        if spaceID != GuiGlobalSpaceID.LOBBY:
            return
        self.__isPremium = self.itemsCache.items.stats.isActivePremium(PREMIUM_TYPE.PLUS)
        self._serverSettings.onServerSettingsChange += self.__onServerSettingsChanged
        self.gameSession.onPremiumNotify += self.__onPremiumNotify
        self.wotPlus.onDataChanged += self.__onWotPlusChanged

    def fini(self, spaceID):
        if spaceID != GuiGlobalSpaceID.LOBBY:
            return
        self.__isHangar = False
        self.__isPremium = False
        self.__isDialogDeferred = True
        self.__isDialogVisible = False
        self._serverSettings.onServerSettingsChange -= self.__onServerSettingsChanged
        self.gameSession.onPremiumNotify -= self.__onPremiumNotify
        self.wotPlus.onDataChanged -= self.__onWotPlusChanged

    def onHangarLoaded(self, isHangar):
        self.__isHangar = isHangar
        if isHangar and self.__isDialogDeferred:
            self.__update()
            self.__isDialogDeferred = False

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
        return localization[EXCLUDED_MAPS.NAME][EXCLUDED_MAPS.MESSAGE] % availableSlots

    @wg_async
    def __showDialog(self, message):
        self.__isDialogVisible = True
        header = localization[EXCLUDED_MAPS.NAME][EXCLUDED_MAPS.HEADER]
        dialog = yield wg_await(ExcludedMapsDialog().showExcludedMapsDialog(header, message))
        if dialog.result == DialogButtons.RESEARCH:
            showMapsBlacklistView()
        self.__isDialogVisible = False

    def __update(self):
        if not settings.main[MAIN.EXCLUDED_MAP_SLOTS_NOTIFICATION]:
            return
        if self.__isDialogVisible:
            return
        if not self.__isHangar:
            self.__isDialogDeferred = True
            return
        if not self._serverSettings.isPreferredMapsEnabled():
            return
        mapsConfig = self._serverSettings.getPreferredMapsConfig()
        defaultSlots = mapsConfig['defaultSlots']
        premiumSlots = mapsConfig['premiumSlots']
        wotPlusSlots = mapsConfig['wotPlusSlots'] if self._serverSettings.isWotPlusExcludedMapEnabled() else 0
        mapsBlacklist = self.itemsCache.items.stats.getMapsBlackList()
        maps = [(mapId, selectedTime) for mapId, selectedTime in mapsBlacklist if mapId > 0]
        usedSlots = len(maps)
        totalSlots = defaultSlots
        isPremiumAcc = self.itemsCache.items.stats.isActivePremium(PREMIUM_TYPE.PLUS)
        isWotPlusAcc = self.wotPlus.isEnabled()
        if isPremiumAcc:
            totalSlots += premiumSlots
        if isWotPlusAcc:
            totalSlots += wotPlusSlots
        if usedSlots < totalSlots:
            availableSlots = totalSlots - usedSlots
            message = self.__getLocalizedMessage(availableSlots)
            self.__showDialog(message)


excluded_maps = ExcludedMapsProcessor()

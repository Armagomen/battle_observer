from armagomen.battle_observer.settings.default_settings import settings
from armagomen.battle_observer.settings.hangar.i18n import localization
from armagomen._constants import MAIN, EXCLUDED_MAPS
from armagomen.utils.dialogs import ExcludedMapsDialog
from wg_async import wg_async, wg_await
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.framework.entities.View import ViewKey
from gui.shared.event_dispatcher import showMapsBlacklistView
from gui.shared.personality import ServicesLocator
from gui.impl.pub.dialog_window import DialogButtons
from skeletons.gui.app_loader import GuiGlobalSpaceID
from skeletons.gui.game_control import IGameSessionController, IWotPlusController
from constants import PremiumConfigs, PREMIUM_TYPE, RENEWABLE_SUBSCRIPTION_CONFIG
from helpers import dependency

SERVER_SETTINGS_DIFF_KEYS = (
    PremiumConfigs.IS_PREFERRED_MAPS_ENABLED,
    PremiumConfigs.PREFERRED_MAPS,
    RENEWABLE_SUBSCRIPTION_CONFIG
)

def isInHangarView():
    app = ServicesLocator.appLoader.getApp()
    if app is not None and app.containerManager is not None:
        viewKey = ViewKey(VIEW_ALIAS.LOBBY_HANGAR)
        hangarView = app.containerManager.getViewByKey(viewKey)
        if hangarView is not None:
            return True
    return False

class ExcludedMapsProcessor(object):
    gameSession = dependency.descriptor(IGameSessionController)
    wotPlus = dependency.descriptor(IWotPlusController)

    def __init__(self):
        self.__isPremium = False
        self.__isDialogVisible = False
        self.__isDialogRequested = False

    def init(self):
        self.__isPremium = ServicesLocator.itemsCache.items.stats.isActivePremium(PREMIUM_TYPE.PLUS)
        self.__update()
        ServicesLocator.lobbyContext.getServerSettings().onServerSettingsChange += self.__onServerSettingsChanged
        self.gameSession.onPremiumNotify += self.__onPremiumNotify
        self.wotPlus.onDataChanged += self.__onWotPlusChanged

    def fini(self):
        self.__isPremium = False
        self.__isDialogVisible = False
        self.__isDialogRequested = False
        ServicesLocator.lobbyContext.getServerSettings().onServerSettingsChange -= self.__onServerSettingsChanged
        self.gameSession.onPremiumNotify -= self.__onPremiumNotify
        self.wotPlus.onDataChanged -= self.__onWotPlusChanged

    def __onServerSettingsChanged(self, diff):
        if not any(key in diff for key in SERVER_SETTINGS_DIFF_KEYS):
            return
        self.__update()

    def __onPremiumNotify(self, isPremium, *args):
        if isPremium != self.__isPremium:
            self.__isPremium = isPremium
            self.__update()

    def __onWotPlusChanged(self, data):
        if 'isEnabled' not in data:
            return
        self.__update()

    def __onViewLoaded(self, view, *args, **kwargs):
        alias = view.getAlias()
        if alias != VIEW_ALIAS.LOBBY_HANGAR:
            return
        app = ServicesLocator.appLoader.getApp()
        if app is not None and app.loaderManager is not None:
            app.loaderManager.onViewLoaded -= self.__onViewLoaded
        if self.__isDialogRequested:
            self.__update()
            self.__isDialogRequested = False

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
        serverSettings = ServicesLocator.lobbyContext.getServerSettings()
        if not serverSettings.isPreferredMapsEnabled():
            return
        mapsConfig = serverSettings.getPreferredMapsConfig()
        defaultSlots = mapsConfig['defaultSlots']
        premiumSlots = mapsConfig['premiumSlots']
        wotPlusSlots = mapsConfig['wotPlusSlots'] if serverSettings.isWotPlusExcludedMapEnabled() else 0
        mapsBlacklist = ServicesLocator.itemsCache.items.stats.getMapsBlackList()
        maps = [(mapId, selectedTime) for mapId, selectedTime in mapsBlacklist if mapId > 0]
        usedSlots = len(maps)
        totalSlots = defaultSlots
        isPremiumAcc = ServicesLocator.itemsCache.items.stats.isActivePremium(PREMIUM_TYPE.PLUS)
        isWotPlusAcc = self.wotPlus.isEnabled()
        if isPremiumAcc:
            totalSlots += premiumSlots
        if isWotPlusAcc:
            totalSlots += wotPlusSlots
        if usedSlots < totalSlots:
            if not isInHangarView():
                app = ServicesLocator.appLoader.getApp()
                if app is not None and app.loaderManager is not None:
                    app.loaderManager.onViewLoaded += self.__onViewLoaded
                self.__isDialogRequested = True
                return
            availableSlots = totalSlots - usedSlots
            message = self.__getLocalizedMessage(availableSlots)
            self.__showDialog(message)

excluded_maps = ExcludedMapsProcessor()

def __onGUISpaceEntered(spaceID):
    if spaceID != GuiGlobalSpaceID.LOBBY:
        return
    excluded_maps.init()

ServicesLocator.appLoader.onGUISpaceEntered += __onGUISpaceEntered

def __onGUISpaceLeft(spaceID):
    if spaceID != GuiGlobalSpaceID.LOBBY:
        return
    excluded_maps.fini()

ServicesLocator.appLoader.onGUISpaceLeft += __onGUISpaceLeft

from armagomen.utils.keys_listener import g_keysListener, MAIN
from armagomen.utils.logging import logDebug, logError
from armagomen.utils.online import user_login, user_logout
from helpers import dependency
from skeletons.connection_mgr import IConnectionManager
from skeletons.gui.app_loader import GuiGlobalSpaceID, IAppLoader
from wg_async import wg_async


class Core(object):
    connectionMgr = dependency.descriptor(IConnectionManager)
    appLoader = dependency.descriptor(IAppLoader)

    def __init__(self, modVersion):
        self.version = modVersion
        self.userID = None
        self.userName = None
        self.components = {}
        self.settings = None
        self.hangar_settings = None
        self.connectionMgr.onLoggedOn += self._onLoggedOn
        self.connectionMgr.onDisconnected += self._onDisconnected

    def showBanned(self, spaceID):
        if spaceID == GuiGlobalSpaceID.LOBBY:
            from armagomen.utils.dialogs import BannedDialog
            dialog = BannedDialog()
            dialog.showDialog(self.userID, self.userName)
            self.appLoader.onGUISpaceEntered -= self.showBanned

    @staticmethod
    def extractDatabaseID(token):
        try:
            return int(str(token).split(":")[0])
        except (IndexError, ValueError, TypeError):
            return None

    @wg_async
    def _onLoggedOn(self, responseData):
        logDebug("_onLoggedOn: {}", responseData)
        self._onDisconnected()
        self.userID = self.extractDatabaseID(responseData.get('token2'))
        self.userName = responseData.get('name')
        if self.userID:
            result = yield user_login(self.userID, self.userName, self.version)
            if result:
                self.appLoader.onGUISpaceEntered += self.showBanned

    def _onDisconnected(self):
        if self.userID:
            user_logout(self.userID)
            self.userID = None
            self.userName = None

    def start(self):
        from armagomen.battle_observer.components import loadComponents
        from armagomen.battle_observer.settings import settings_loader
        from armagomen.utils.common import isReplay

        is_replay = isReplay()
        settings_loader.readConfig()
        self.components = loadComponents(is_replay)
        self.registerBattleObserverPackages(is_replay)
        g_keysListener.init(settings_loader.settings.main)
        settings_loader.updateAllSettings()
        self.settings = settings_loader.settings
        if not is_replay:
            try:
                from gui.modsListApi import g_modsListApi
                from gui.vxSettingsApi import vxSettingsApi, vxSettingsApiEvents
            except Exception as error:
                from armagomen.battle_observer.settings.hangar.loading_error import LoadingError
                from debug_utils import LOG_CURRENT_EXCEPTION
                LoadingError(repr(error))
                LOG_CURRENT_EXCEPTION()
                logError("Settings Api Not Loaded")
            else:
                from armagomen.battle_observer.settings.hangar import SettingsInterface
                self.hangar_settings = SettingsInterface(settings_loader, self.version, g_modsListApi, vxSettingsApi, vxSettingsApiEvents)

    def fini(self):
        from armagomen.utils.common import cleanupObserverUpdates, cleanupUpdates, clearClientCache
        if self.settings.main[MAIN.AUTO_CLEAR_CACHE]:
            clearClientCache()
        cleanupObserverUpdates()
        cleanupUpdates()
        for component in self.components.itervalues():
            if hasattr(component, "fini"):
                component.fini()
        g_keysListener.fini()
        if self.hangar_settings is not None:
            self.hangar_settings.fini()
        self._onDisconnected()
        self.connectionMgr.onLoggedOn -= self._onLoggedOn
        self.connectionMgr.onDisconnected -= self._onDisconnected

    @staticmethod
    def registerBattleObserverPackages(is_replay):
        from armagomen._constants import BATTLES_RANGE
        from gui.override_scaleform_views_manager import g_overrideScaleFormViewsConfig
        from gui.Scaleform.required_libraries_config import BATTLE_REQUIRED_LIBRARIES, LOBBY_REQUIRED_LIBRARIES

        if not is_replay:
            LOBBY_REQUIRED_LIBRARIES.append('modBattleObserverHangar.swf')
            g_overrideScaleFormViewsConfig.lobbyPackages.append("armagomen.battle_observer.lobby")
        BATTLE_REQUIRED_LIBRARIES.append('modBattleObserver.swf')
        for guiType in BATTLES_RANGE:
            packages = g_overrideScaleFormViewsConfig.battlePackages.setdefault(guiType, [])
            packages.append("armagomen.battle_observer.battle")

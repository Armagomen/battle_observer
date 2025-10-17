from armagomen._constants import BATTLES_RANGE, MAIN
from armagomen.utils.events import g_events
from armagomen.utils.keys_listener import g_keysListener
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
        self.autoClearCache = False
        self.hangar_settings = None
        self.error_dialog = None
        self.connectionMgr.onLoggedOn += self._onLoggedOn
        g_events.onModSettingsChanged += self.onModSettingsChanged

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
        if responseData.get("isDemoAccount", False):
            return
        userID = self.extractDatabaseID(responseData.get('token2'))
        if self.userID != userID:
            self.logout()
            self.userID = userID
            self.userName = responseData.get('name')
            result = yield user_login(self.userID, self.userName, self.version)
            if result:
                self.appLoader.onGUISpaceEntered += self.showBanned

    def logout(self):
        if self.userID is not None:
            user_logout(int(self.userID))

    def start(self):
        from armagomen.battle_observer.components import loadComponents
        from armagomen.battle_observer.settings import user_settings
        from armagomen.battle_observer.settings.loader import SettingsLoader
        from armagomen.battle_observer.settings.loading_error import ErrorMessages
        from armagomen.utils.common import isReplay

        self.error_dialog = ErrorMessages()
        settings_loader = SettingsLoader(user_settings, self.error_dialog)
        settings_loader.readConfig()
        is_replay = isReplay()
        self.components = loadComponents(is_replay)
        self.registerBattleObserverPackages(is_replay)
        g_keysListener.init(user_settings)
        settings_loader.updateAllSettings()

        if not is_replay:
            try:
                from gui.modsListApi import g_modsListApi
                from gui.vxSettingsApi import vxSettingsApi, vxSettingsApiEvents
                from armagomen.battle_observer.settings.hangar import SettingsInterface
                api = (g_modsListApi, vxSettingsApi, vxSettingsApiEvents)
            except Exception as error:
                from debug_utils import LOG_CURRENT_EXCEPTION
                self.error_dialog.messages.add(repr(error))
                LOG_CURRENT_EXCEPTION()
                logError("Settings Api Not Loaded: {}", repr(error))
            else:
                self.hangar_settings = SettingsInterface(settings_loader, self.version, api)

    def onModSettingsChanged(self, name, data):
        if name == MAIN.NAME:
            self.autoClearCache = data[MAIN.AUTO_CLEAR_CACHE]

    def fini(self):
        self.logout()
        from armagomen.utils.common import cleanupObserverUpdates, cleanupUpdates, clearClientCache
        if self.autoClearCache:
            clearClientCache()
        cleanupObserverUpdates()
        cleanupUpdates()
        for component in self.components.values():
            getattr(component, 'fini', lambda: None)()
        g_keysListener.fini()
        if self.hangar_settings is not None:
            self.hangar_settings.fini()
        if self.error_dialog is not None:
            self.error_dialog.fini()
        self.connectionMgr.onLoggedOn -= self._onLoggedOn
        g_events.onModSettingsChanged -= self.onModSettingsChanged

    @staticmethod
    def registerBattleObserverPackages(is_replay):
        from gui.override_scaleform_views_manager import g_overrideScaleFormViewsConfig
        from gui.Scaleform.required_libraries_config import BATTLE_REQUIRED_LIBRARIES

        if not is_replay:
            from gui.Scaleform.required_libraries_config import LOBBY_REQUIRED_LIBRARIES
            g_overrideScaleFormViewsConfig.lobbyPackages.append("armagomen.battle_observer.lobby")
            LOBBY_REQUIRED_LIBRARIES.append('modBattleObserverHangar.swf')

        BATTLE_REQUIRED_LIBRARIES.append('modBattleObserver.swf')
        for guiType in BATTLES_RANGE:
            packages = g_overrideScaleFormViewsConfig.battlePackages.setdefault(guiType, [])
            packages.append("armagomen.battle_observer.battle")

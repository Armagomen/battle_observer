class Core(object):

    def __init__(self, modVersion):
        from armagomen.battle_observer.components import loadComponents
        from armagomen.battle_observer.settings import settings_loader
        from armagomen.utils.common import isReplay
        from armagomen.utils.keys_listener import g_keysListener

        is_replay = isReplay()
        loadComponents(is_replay)
        self.registerBattleObserverPackages(is_replay)
        g_keysListener.init(settings_loader.settings.main)
        settings_loader.readConfig()
        if not is_replay:
            try:
                from gui.modsListApi import g_modsListApi
                from gui.vxSettingsApi import vxSettingsApi, vxSettingsApiEvents
            except Exception as error:
                from armagomen.battle_observer.settings.hangar.loading_error import LoadingError
                from armagomen.utils.logging import logError
                from debug_utils import LOG_CURRENT_EXCEPTION
                LoadingError(repr(error))
                LOG_CURRENT_EXCEPTION()
                logError("Settings Api Not Loaded")
            else:
                from armagomen.battle_observer.settings.hangar import SettingsInterface
                self.hangar_settings = SettingsInterface(settings_loader, modVersion, g_modsListApi, vxSettingsApi,
                                                         vxSettingsApiEvents)

    @staticmethod
    def registerBattleObserverPackages(is_replay):
        from armagomen._constants import BATTLES_RANGE
        from gui.override_scaleform_views_manager import g_overrideScaleFormViewsConfig
        from gui.Scaleform.required_libraries_config import BATTLE_REQUIRED_LIBRARIES, LOBBY_REQUIRED_LIBRARIES

        if not is_replay:
            LOBBY_REQUIRED_LIBRARIES.insert(0, 'modBattleObserverHangar.swf')
            g_overrideScaleFormViewsConfig.lobbyPackages.append("armagomen.battle_observer.lobby")
        BATTLE_REQUIRED_LIBRARIES.insert(0, 'modBattleObserver.swf')
        for guiType in BATTLES_RANGE:
            packages = g_overrideScaleFormViewsConfig.battlePackages.setdefault(guiType, [])
            packages.append("armagomen.battle_observer.battle")


def onFini():
    from armagomen.battle_observer.components import components
    from armagomen.battle_observer.settings import user_settings
    from armagomen.utils.common import cleanupObserverUpdates, cleanupUpdates, clearClientCache
    if user_settings.main["clear_cache_automatically"]:
        clearClientCache()
    cleanupObserverUpdates()
    cleanupUpdates()
    for component in components.itervalues():
        if hasattr(component, "fini"):
            component.fini()
    from armagomen.utils.keys_listener import g_keysListener
    g_keysListener.fini()

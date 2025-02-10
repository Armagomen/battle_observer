class Core(object):

    def __init__(self, modVersion, Thread):
        from armagomen.battle_observer.settings import settings_loader
        from armagomen.battle_observer.components import loadComponents
        from armagomen.utils.keys_listener import g_keysListener
        from armagomen.utils.common import isReplay

        is_replay = isReplay()
        self.registerBattleObserverPackages(is_replay)
        g_keysListener.init()
        loadComponents(is_replay)
        settings_loader.readConfig()
        if not is_replay:
            from armagomen.battle_observer.settings.hangar import SettingsInterface
            hangar_settings = Thread(target=SettingsInterface, args=(settings_loader, modVersion),
                                     name="Battle_Observer_SettingsInterface")
            hangar_settings.daemon = True
            hangar_settings.start()

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
    from armagomen.battle_observer.settings import user_settings
    from armagomen.utils.common import cleanupObserverUpdates, cleanupUpdates, clearClientCache
    if user_settings.main["clear_cache_automatically"]:
        clearClientCache()
    cleanupObserverUpdates()
    cleanupUpdates()
    from armagomen.battle_observer.components import components
    for name, component in components.iteritems():
        if hasattr(component, "fini"):
            component.fini()
    from armagomen.utils.keys_listener import g_keysListener
    g_keysListener.fini()

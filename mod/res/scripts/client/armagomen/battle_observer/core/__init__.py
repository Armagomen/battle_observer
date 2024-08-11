import logging


class Core(object):

    def __init__(self, modVersion, Thread):
        from armagomen.battle_observer.settings import settings_loader
        from armagomen.battle_observer.components import loadComponents
        from armagomen.utils.common import isReplay

        logging.disable(logging.WARNING)
        self.registerBattleObserverPackages()
        self.components = loadComponents()
        if not isReplay():
            from armagomen.battle_observer.settings.hangar import SettingsInterface
            hangar_settings = Thread(target=SettingsInterface, args=(settings_loader, modVersion),
                                     name="Battle_Observer_SettingsInterface")
            hangar_settings.daemon = True
            hangar_settings.start()

    @staticmethod
    def registerBattleObserverPackages():
        from armagomen._constants import BATTLES_RANGE
        from gui.override_scaleform_views_manager import g_overrideScaleFormViewsConfig
        from gui.Scaleform.required_libraries_config import BATTLE_REQUIRED_LIBRARIES, LOBBY_REQUIRED_LIBRARIES
        BATTLE_REQUIRED_LIBRARIES.append('modBattleObserver.swf')
        LOBBY_REQUIRED_LIBRARIES.append('modBattleObserverHangar.swf')
        for guiType in BATTLES_RANGE:
            g_overrideScaleFormViewsConfig.battlePackages[guiType].append("armagomen.battle_observer.battle")
        g_overrideScaleFormViewsConfig.lobbyPackages.append("armagomen.battle_observer.lobby")


def onFini():
    from armagomen.battle_observer.settings import user_settings
    from armagomen.utils.common import cleanupObserverUpdates, cleanupUpdates, clearClientCache
    if user_settings.main["clear_cache_automatically"]:
        clearClientCache()
    cleanupObserverUpdates()
    cleanupUpdates()

from armagomen.utils.logging import logInfo


class Core(object):

    def __init__(self, modVersion):
        logInfo('MOD START LOADING: v{}', modVersion)
        try:
            import logging
            from threading import Thread
            from armagomen.battle_observer.core.updater import Updater
            update = Thread(target=Updater, args=(modVersion,), name="Battle_Observer_update")
            update.start()
            update.join(timeout=60.0)

            from armagomen.battle_observer.components import loadComponents
            from armagomen.battle_observer.settings.loader import SettingsLoader
            from armagomen.battle_observer.settings.hangar.hangar_settings import SettingsInterface
            from sys import version
            from realm import CURRENT_REALM
        except Exception as err:
            from debug_utils import LOG_CURRENT_EXCEPTION
            LOG_CURRENT_EXCEPTION()
            self.error(repr(err))
        else:
            logging.disable(logging.WARNING)
            logInfo('Launched at python v{} region={}', version, CURRENT_REALM)
            self.registerBattleObserverPackages()
            loadComponents()
            hangar_settings = Thread(target=SettingsInterface, args=(SettingsLoader(), modVersion),
                                     name="Battle_Observer_SettingsInterface")
            hangar_settings.daemon = True
            hangar_settings.start()

    @staticmethod
    def error(error_message):
        from armagomen.utils.logging import logError
        from armagomen.battle_observer.core.loading_error import LoadingError
        logError(error_message)
        LoadingError(error_message)

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


def onFini(modVersion):
    from armagomen.battle_observer.settings import user_settings
    from armagomen.utils.common import cleanupObserverUpdates, cleanupUpdates, clearClientCache
    if user_settings.main["clear_cache_automatically"]:
        clearClientCache()
    cleanupObserverUpdates()
    cleanupUpdates()
    logInfo('MOD SHUTTING DOWN: v{}', modVersion)

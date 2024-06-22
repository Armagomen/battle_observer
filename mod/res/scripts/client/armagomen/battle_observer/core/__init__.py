import logging

from armagomen._constants import BATTLES_RANGE
from armagomen.battle_observer.core.current_vehicle_data import CurrentVehicleCachedData
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import cleanupObserverUpdates, cleanupUpdates, clearClientCache, gameVersion
from armagomen.utils.logging import logInfo
from gui.override_scaleform_views_manager import g_overrideScaleFormViewsConfig
from gui.Scaleform.required_libraries_config import BATTLE_REQUIRED_LIBRARIES, LOBBY_REQUIRED_LIBRARIES

cachedVehicleData = CurrentVehicleCachedData()


def error(error_message):
    from armagomen.utils.logging import logError
    from armagomen.battle_observer.core.loading_error import LoadingError
    logError(error_message)
    LoadingError(error_message)


def onInit(modVersion, current_realm):
    logInfo('MOD START LOADING: v{} - {}', modVersion, gameVersion)
    try:
        from armagomen.battle_observer.core.updater import Updater
        Updater(modVersion)

        from armagomen.battle_observer.components import loadComponents
        from armagomen.battle_observer.settings.loader import SettingsLoader
        from armagomen.battle_observer.settings.hangar.hangar_settings import SettingsInterface
        from sys import version
    except Exception as err:
        from debug_utils import LOG_CURRENT_EXCEPTION
        LOG_CURRENT_EXCEPTION()
        error(repr(err))
    else:
        logging.disable(logging.WARNING)
        logInfo('Launched at python v{} region={}', version, current_realm)
        registerBattleObserverPackages()
        loadComponents()
        settings_loader = SettingsLoader()
        SettingsInterface(settings_loader, modVersion)


def onFini(modVersion):
    if user_settings.main["clear_cache_automatically"]:
        clearClientCache()
    cleanupObserverUpdates()
    cleanupUpdates()
    logInfo('MOD SHUTTING DOWN: v{} - {}', modVersion, gameVersion)


def registerBattleObserverPackages():
    BATTLE_REQUIRED_LIBRARIES.append('modBattleObserver.swf')
    LOBBY_REQUIRED_LIBRARIES.append('modBattleObserverHangar.swf')
    for guiType in BATTLES_RANGE:
        g_overrideScaleFormViewsConfig.battlePackages[guiType].append("armagomen.battle_observer.battle")
    g_overrideScaleFormViewsConfig.lobbyPackages.append("armagomen.battle_observer.lobby")

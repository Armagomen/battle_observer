import logging

from armagomen._constants import BATTLES_RANGE, SWF
from armagomen.battle_observer.core.current_vehicle_data import CurrentVehicleCachedData
from armagomen.utils.common import clearClientCache, cleanupUpdates, logInfo, gameVersion, cleanupObserverUpdates
from gui.override_scaleform_views_manager import g_overrideScaleFormViewsConfig

cachedVehicleData = CurrentVehicleCachedData()


def error(error_message):
    from armagomen.utils.common import logError
    from armagomen.battle_observer.core.loading_error import LoadingError
    logError(error_message)
    LoadingError(error_message)


def onInit(modVersion, current_realm):
    logInfo('MOD START LOADING: v{} - {}'.format(modVersion, gameVersion))
    if current_realm == "RU":
        return error("not supported region")
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
        logInfo('Launched at python v{} region={}'.format(version, current_realm))
        registerBattleObserverPackages()
        loadComponents(current_realm)
        settings_loader = SettingsLoader()
        SettingsInterface(settings_loader, modVersion)


def onFini(modVersion):
    clearClientCache()
    cleanupObserverUpdates()
    cleanupUpdates()
    logInfo('MOD SHUTTING DOWN: v{} - {}'.format(modVersion, gameVersion))


def registerBattleObserverPackages():
    for guiType in BATTLES_RANGE:
        g_overrideScaleFormViewsConfig.battlePackages[guiType].extend(SWF.BATTLE_PACKAGES)
    g_overrideScaleFormViewsConfig.lobbyPackages.extend(SWF.LOBBY_PACKAGES)

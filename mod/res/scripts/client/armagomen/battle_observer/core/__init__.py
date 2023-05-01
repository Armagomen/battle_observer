from armagomen.battle_observer.core.current_vehicle_data import CurrentVehicleCachedData
from armagomen.battle_observer.core.view_settings import ViewSettings, registerBattleObserverPackages
from armagomen.utils.common import clearClientCache, cleanupUpdates, logInfo, logError, gameVersion, \
    cleanupObserverUpdates

cachedVehicleData = CurrentVehicleCachedData()
viewSettings = ViewSettings()


def startLoadingMod(modVersion, current_realm):
    error_message = ""
    if current_realm == "RU":
        return "not supported region"
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
        error_message = repr(err)
    else:
        logInfo('Launched at python v{} region={}'.format(version, current_realm))
        registerBattleObserverPackages()
        loadComponents(current_realm)
        settings_loader = SettingsLoader()
        SettingsInterface(settings_loader, modVersion)
    if error_message:
        logError(error_message)
    return error_message


def onInit(modVersion, current_realm):
    logInfo('MOD START LOADING: v{} - {}'.format(modVersion, gameVersion))
    errorMessage = startLoadingMod(modVersion, current_realm)
    if errorMessage:
        from armagomen.battle_observer.core.loading_error import LoadingError
        return LoadingError(errorMessage)


def onFini(modVersion):
    clearClientCache()
    cleanupObserverUpdates()
    cleanupUpdates()
    logInfo('MOD SHUTTING DOWN: v{} - {}'.format(modVersion, gameVersion))

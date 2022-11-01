from armagomen.battle_observer.core.current_vehicle_data import CurrentVehicleCachedData
from armagomen.battle_observer.core.view_settings import ViewSettings, registerBattleObserverPackages
from armagomen.utils.common import isFileValid, clearClientCache, cleanupUpdates, logInfo, logError, gameVersion, \
    cleanupObserverUpdates
from constants import AUTH_REALM

cachedVehicleData = CurrentVehicleCachedData()
viewSettings = ViewSettings()
componentsLoader = None
hangarSettings = None


def startLoadingMod(modVersion):
    errorMessage = ""
    try:
        from armagomen.battle_observer.core.updater import Updater
        Updater(modVersion)

        from armagomen.battle_observer.components import ComponentsLoader
        from armagomen.battle_observer.settings.loader import SettingsLoader
        from armagomen.battle_observer.settings.hangar.hangar_settings import SettingsInterface
        from sys import version
    except Exception as err:
        from debug_utils import LOG_CURRENT_EXCEPTION
        LOG_CURRENT_EXCEPTION()
        errorMessage = repr(err)
    else:
        if isFileValid(modVersion):
            global componentsLoader, hangarSettings
            logInfo('Launched at python v{} region={}'.format(version, AUTH_REALM))
            registerBattleObserverPackages()
            componentsLoader = ComponentsLoader()
            settings_loader = SettingsLoader()
            hangarSettings = SettingsInterface(settings_loader, modVersion)
        else:
            URL = 'https://github.com/Armagomen/battle_observer/releases/latest'
            errorMessage = 'ERROR: file armagomen.battleObserver_{}.wotmod is not valid, mod locked, please ' \
                           'install mod from official source: {}'.format(modVersion, URL)
    if errorMessage:
        logError(errorMessage)
    return errorMessage


def onInit(modVersion):
    logInfo('MOD START LOADING: v{} - {}'.format(modVersion, gameVersion))
    cachedVehicleData.init()
    errorMessage = startLoadingMod(modVersion)
    if errorMessage:
        from armagomen.battle_observer.core.loading_error import LoadingError
        return LoadingError(errorMessage)


def onFini(modVersion):
    cachedVehicleData.fini()
    clearClientCache()
    cleanupObserverUpdates()
    cleanupUpdates()
    logInfo('MOD SHUTTING DOWN: v{} - {}'.format(modVersion, gameVersion))

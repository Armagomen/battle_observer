from armagomen.utils.common import isFileValid, clearClientCache, cleanupUpdates, logInfo, logError, gameVersion, \
    cleanupObserverUpdates


loadError = False
viewSettings = None
componentsLoader = None
hangarSettings = None


def startLoadingMod(modVersion):
    global loadError
    errorMessage = ""

    try:
        from armagomen.battle_observer.components import ComponentsLoader
        from armagomen.battle_observer.core.view_settings import ViewSettings
        from armagomen.battle_observer.settings.hangar.hangar_settings import SettingsInterface
        from armagomen.battle_observer.settings.loader import SettingsLoader
        from sys import version
    except Exception as err:
        from debug_utils import LOG_CURRENT_EXCEPTION
        LOG_CURRENT_EXCEPTION()
        loadError = True
        errorMessage = repr(err)
    else:
        if isFileValid(modVersion):
            global viewSettings, componentsLoader, hangarSettings
            logInfo('Launched at python v{}'.format(version))
            logInfo('MOD START LOADING: v{} - {}'.format(modVersion, gameVersion))
            viewSettings = ViewSettings()
            componentsLoader = ComponentsLoader()
            settings_loader = SettingsLoader()
            hangarSettings = SettingsInterface(settings_loader, modVersion)
        else:
            loadError = True
            URL = 'https://github.com/Armagomen/battle_observer/releases/latest'
            errorMessage = 'ERROR: file armagomen.battleObserver_{}.wotmod is not valid, mod locked, please ' \
                           'install mod from official source: {}'.format(modVersion, URL)
            logError(errorMessage)
    return errorMessage


def onInit(modVersion):
    errorMessage = startLoadingMod(modVersion)
    if loadError:
        from armagomen.battle_observer.core.loading_error import LoadingError
        return LoadingError(errorMessage)


def onFini(modVersion):
    clearClientCache()
    cleanupObserverUpdates()
    cleanupUpdates()
    if not loadError:
        logInfo('MOD SHUTTING DOWN: v{} - {}'.format(modVersion, gameVersion))

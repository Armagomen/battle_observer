__version__ = "1.38.8"

from helpers import getShortClientVersion

loadError = False
errorMessage = ""
shortClientVersion = getShortClientVersion()

try:
    from armagomen.utils.common import isFileValid, clearClientCache, cleanupUpdates, logInfo, logError
    from gui.modsListApi import g_modsListApi
    from gui.vxSettingsApi import vxSettingsApi, vxSettingsApiEvents
except ImportError as err:
    errorMessage = repr(err)
    logError(errorMessage)
    loadError = True
else:
    if isFileValid(__version__):
        from sys import version as python_version
        from armagomen.battle_observer.core.view_settings import ViewSettings
        from armagomen.battle_observer.core.update.worker import UpdateMain
        from armagomen.battle_observer.components import ComponentsLoader
        from armagomen.battle_observer.settings.loader import SettingsLoader
        from armagomen.battle_observer.settings.hangar.hangar_settings import SettingsInterface

        logInfo("Launched at python v{}".format(python_version))
        logInfo('MOD START LOADING: v{} - {}'.format(__version__, shortClientVersion))
        update = UpdateMain(__version__)
        _view_settings = ViewSettings()
        componentsLoader = ComponentsLoader()
        settings_loader = SettingsLoader()
        hangar_settings = SettingsInterface(g_modsListApi, vxSettingsApi, vxSettingsApiEvents,
                                            settings_loader, __version__)
    else:
        loadError = True
        errorMessage = "ERROR: file armagomen.battleObserver_{}.wotmod is not valid, mod locked, please " \
                       "install mod from official site".format(__version__)
        logError(errorMessage)


def init():
    if loadError:
        from armagomen.battle_observer.core.loading_error import LoadingError
        return LoadingError(errorMessage)


def fini():
    if loadError:
        return
    clearClientCache()
    cleanupUpdates()
    logInfo('MOD SHUTTING DOWN: v{} - {}'.format(__version__, shortClientVersion))

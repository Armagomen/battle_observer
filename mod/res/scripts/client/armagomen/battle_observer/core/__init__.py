import sys

from armagomen.constants import MESSAGES
from armagomen.utils.common import logWarning, isFileValid, clearClientCache, cleanupUpdates, logInfo

__version__ = "1.38.5"
loadError = False
errorMessage = ""

try:
    from gui.modsListApi import g_modsListApi
    from gui.vxSettingsApi import vxSettingsApi, vxSettingsApiEvents
except ImportError as err:

    errorMessage = repr(err)
    logWarning(errorMessage)
    loadError = True
else:
    if isFileValid(__version__):
        from armagomen.battle_observer.core.view_settings import ViewSettings
        from armagomen.battle_observer.core.update.worker import UpdateMain
        from armagomen.battle_observer.components import ComponentsLoader
        from armagomen.battle_observer.settings.loader import SettingsLoader
        from armagomen.battle_observer.settings.hangar.hangar_settings import SettingsInterface

        logInfo("Launched at python " + sys.version)
        logInfo('MOD {0}: {1}'.format(MESSAGES.START, __version__))
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
        logWarning(errorMessage)


def init():
    if loadError:
        from armagomen.battle_observer.core.loading_error import LoadingError
        return LoadingError(errorMessage)


def fini():
    if loadError:
        return
    clearClientCache()
    cleanupUpdates()
    logInfo('MOD {0}: {1}'.format(MESSAGES.FINISH, __version__))

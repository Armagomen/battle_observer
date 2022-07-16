__version__ = "1.38.5"
loadError = False
errorMessage = ""
try:
    from gui.modsListApi import g_modsListApi
    from gui.vxSettingsApi import vxSettingsApi, vxSettingsApiEvents
except ImportError as err:
    from armagomen.utils.common import logWarning

    errorMessage = repr(err)
    logWarning(errorMessage)
    loadError = True
else:
    from armagomen.utils.common import isFileValid

    if isFileValid(__version__):
        from armagomen.battle_observer.settings.default_settings import settings
        from armagomen.battle_observer.core.view_settings import ViewSettings
        from armagomen.battle_observer.core.observer_core import ObserverCore
        from armagomen.battle_observer.components import ComponentsLoader
        from armagomen.battle_observer.settings.config_loader import ConfigLoader
        from armagomen.battle_observer.settings.hangar.hangar_settings import ConfigInterface

        m_core = ObserverCore(__version__)
        _view_settings = ViewSettings(settings)
        componentsLoader = ComponentsLoader()
        c_Loader = ConfigLoader(settings)
        configInterface = ConfigInterface(g_modsListApi, vxSettingsApi, vxSettingsApiEvents, settings, c_Loader,
                                          __version__)
    else:
        loadError = True
        errorMessage = "ERROR: file armagomen.battleObserver_{}.wotmod is not valid, mod locked, please " \
                       "install mod from official site".format(__version__)


def init():
    if loadError:
        from armagomen.battle_observer.core.loading_error import LoadingError
        return LoadingError(errorMessage)


def fini():
    if loadError:
        return
    m_core.onExit(settings)

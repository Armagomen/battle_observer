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
    from armagomen.battle_observer.settings.default_settings import settings
    from armagomen.battle_observer.core.battle.settings import ViewSettings
    from armagomen.battle_observer.core.observer_core import ObserverCore
    from armagomen.battle_observer.components import ComponentsLoader
    from armagomen.battle_observer.core.battle.battle_core import BattleCore
    from armagomen.battle_observer.settings.config_loader import ConfigLoader
    from armagomen.battle_observer.settings.hangar.hangar_settings import ConfigInterface

    view_settings = ViewSettings(settings)
    m_core = ObserverCore()
    if m_core.isFileValid:
        componentsLoader = ComponentsLoader()
        componentsLoader.start()
        m_core.start()
        b_core = BattleCore(settings)
        c_Loader = ConfigLoader(settings)
        configInterface = ConfigInterface(g_modsListApi, vxSettingsApi, vxSettingsApiEvents, settings, c_Loader)


def init():
    if loadError:
        from armagomen.battle_observer.core.loading_error import LoadingError
        return LoadingError(errorMessage)


def fini():
    if loadError:
        return
    m_core.onExit(settings)

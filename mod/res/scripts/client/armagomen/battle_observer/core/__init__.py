from armagomen.utils.common import logWarning

try:
    from gui.modsListApi import g_modsListApi
    from gui.vxSettingsApi import vxSettingsApi, vxSettingsApiEvents
except ImportError as err:
    logWarning("%s: Settings API not found, mod not loaded, please install api packages" % repr(err))
else:
    from armagomen.battle_observer.core.battle import BattleCore, ViewSettings
    from armagomen.battle_observer.core.observer_core import ObserverCore
    from armagomen.battle_observer.settings.config_loader import ConfigLoader
    from armagomen.battle_observer.settings.default_settings import settings
    from armagomen.battle_observer.settings.hangar.hangar_settings import ConfigInterface
    from armagomen.utils.keys_parser import HotKeysParser

    c_Loader = ConfigLoader(settings)
    m_core = ObserverCore()
    view_settings = ViewSettings(settings)
    b_core = BattleCore(settings)
    keysParser = HotKeysParser(settings)
    configInterface = ConfigInterface(g_modsListApi, vxSettingsApi, vxSettingsApiEvents, settings, c_Loader)

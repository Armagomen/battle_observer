from .battle import BattleCache, BattleCore, ViewSettings
from .config import Config, ConfigLoader
from .inject_flash import InjectFlash
from .observer_core import ObserverCore
from .update import UpdateMain
from .utils import HotKeysParser, Loader

cfg = Config()
cache = BattleCache()
m_core = ObserverCore()
c_Loader = ConfigLoader(cfg, cache)
b_core = BattleCore(cfg, cache)
v_settings = ViewSettings(cfg, b_core)
keysParser = HotKeysParser(cfg)
m_Loader = Loader()
g_update = UpdateMain(m_core)
flash = InjectFlash()

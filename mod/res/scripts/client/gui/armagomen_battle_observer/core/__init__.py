from .battle import BattleCache, BattleCore, ViewSettings
from .config import Config, ConfigLoader
from .inject_flash import InjectFlash
from .observer_core import ObserverCore
from .update import UpdateMain
from .utils import HotKeysParser
from ..no_flash_components import Loader

cfg = Config()
cache = BattleCache()
c_Loader = ConfigLoader(cfg, cache)
m_Loader = Loader()
m_core = ObserverCore(cfg, cache, c_Loader, m_Loader)
b_core = BattleCore(cfg, cache)
v_settings = ViewSettings(cfg)
keysParser = HotKeysParser(cfg)
flash = InjectFlash()

from armagomen.battle_observer.core.battle import BattleCore, ViewSettings
from armagomen.battle_observer.core.config import Config, ConfigLoader
from armagomen.battle_observer.core.inject_flash import InjectFlash
from armagomen.battle_observer.core.observer_core import ObserverCore
from armagomen.battle_observer.core.utils import HotKeysParser

cfg = Config()
c_Loader = ConfigLoader(cfg)
m_core = ObserverCore(c_Loader)
b_core = BattleCore(cfg)
v_settings = ViewSettings(cfg)
keysParser = HotKeysParser(cfg)
flash = InjectFlash()

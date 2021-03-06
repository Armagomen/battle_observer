from armagomen.battle_observer.core.battle import BattleCore, ViewSettings
from armagomen.battle_observer.core.config.config import Config
from armagomen.battle_observer.core.config.config_loader import ConfigLoader
from armagomen.battle_observer.core.inject_flash import InjectFlash
from armagomen.battle_observer.core.observer_core import ObserverCore
from armagomen.utils.keys_parser import HotKeysParser

config = Config()
c_Loader = ConfigLoader(config)
m_core = ObserverCore(c_Loader)
b_core = BattleCore(config)
v_settings = ViewSettings(config)
keysParser = HotKeysParser(config)
flash = InjectFlash()

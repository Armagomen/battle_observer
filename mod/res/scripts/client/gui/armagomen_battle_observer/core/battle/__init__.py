from .battle_cache import BattleCache
from .battle_core import _BattleCore
from .settings import ViewSettings

__all__ = ["cache", "b_core", "v_settings"]

cache = BattleCache()
b_core = _BattleCore(cache)
v_settings = ViewSettings(b_core)

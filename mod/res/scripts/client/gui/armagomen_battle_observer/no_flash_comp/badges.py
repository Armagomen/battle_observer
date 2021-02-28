from gui.battle_control.arena_info import settings
from gui.battle_control.arena_info.arena_vos import VehicleArenaInfoVO
from ..core import cfg
from ..core.bo_constants import MAIN, ANOTHER, GLOBAL
from ..core.utils import overrideMethod

_PLAYER_STATUS = settings.PLAYER_STATUS


@overrideMethod(VehicleArenaInfoVO)
def new_VehicleArenaInfoVO(init, vInfoVo, *args, **kwargs):
    if kwargs:
        if cfg.main[MAIN.HIDE_BADGES] and ANOTHER.BADGES in kwargs:
            kwargs[ANOTHER.BADGES] = None
        if cfg.main[MAIN.SHOW_ANONYMOUS] and ANOTHER.ACCOUNT_DBID in kwargs:
            if kwargs[ANOTHER.ACCOUNT_DBID] == GLOBAL.ZERO:
                kwargs[ANOTHER.IS_TEAM_KILLER] = _PLAYER_STATUS.IS_TEAM_KILLER
                if cfg.main[MAIN.CHANGE_ANONYMOUS_NAME] and ANOTHER.NAME in kwargs:
                    kwargs[ANOTHER.NAME] = cfg.main[MAIN.ANONYMOUS_STRING]
        if cfg.main[MAIN.HIDE_CLAN_ABBREV] and ANOTHER.CLAN_DBID in kwargs and ANOTHER.CLAN_ABBR in kwargs:
            kwargs[ANOTHER.CLAN_DBID] = GLOBAL.FIRST
            kwargs[ANOTHER.CLAN_ABBR] = GLOBAL.EMPTY_LINE
    return init(vInfoVo, *args, **kwargs)

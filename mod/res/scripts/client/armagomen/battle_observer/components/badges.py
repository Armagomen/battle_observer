from armagomen.battle_observer.core import settings
from armagomen.bo_constants import MAIN, ANOTHER, GLOBAL
from armagomen.utils.common import overrideMethod
from gui.battle_control.arena_info import settings as arena_settings
from gui.battle_control.arena_info.arena_vos import VehicleArenaInfoVO

_PLAYER_STATUS = arena_settings.PLAYER_STATUS


@overrideMethod(VehicleArenaInfoVO)
def new_VehicleArenaInfoVO(init, vInfoVo, *args, **kwargs):
    if kwargs:
        if settings.main[MAIN.HIDE_BADGES] and ANOTHER.BADGES in kwargs:
            kwargs[ANOTHER.BADGES] = None
        if settings.main[MAIN.SHOW_ANONYMOUS] and ANOTHER.ACCOUNT_DBID in kwargs:
            if kwargs[ANOTHER.ACCOUNT_DBID] == GLOBAL.ZERO:
                kwargs[ANOTHER.IS_TEAM_KILLER] = _PLAYER_STATUS.IS_TEAM_KILLER
                if settings.main[MAIN.CHANGE_ANONYMOUS_NAME] and ANOTHER.NAME in kwargs:
                    kwargs[ANOTHER.NAME] = settings.main[MAIN.ANONYMOUS_STRING]
        if settings.main[MAIN.HIDE_CLAN_ABBREV] and ANOTHER.CLAN_DBID in kwargs and ANOTHER.CLAN_ABBR in kwargs:
            kwargs[ANOTHER.CLAN_DBID] = GLOBAL.FIRST
            kwargs[ANOTHER.CLAN_ABBR] = GLOBAL.EMPTY_LINE
    return init(vInfoVo, *args, **kwargs)

from armagomen.battle_observer.core import viewSettings
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import MAIN, ANOTHER, GLOBAL
from armagomen.utils.common import overrideMethod
from gui.battle_control.arena_info.arena_vos import VehicleArenaInfoVO
from gui.battle_control.arena_info.settings import PLAYER_STATUS

BOT_START_SWITCH = ":"


@overrideMethod(VehicleArenaInfoVO)
def new_VehicleArenaInfoVO(init, vInfoVo, *args, **kwargs):
    if kwargs:
        if settings.main[MAIN.HIDE_BADGES] and ANOTHER.BADGES in kwargs:
            kwargs[ANOTHER.BADGES] = None
        if settings.main[MAIN.SHOW_ANONYMOUS] and ANOTHER.ACCOUNT_DBID in kwargs:
            if kwargs[ANOTHER.ACCOUNT_DBID] == GLOBAL.ZERO:
                if not viewSettings.isWTREnabled():
                    kwargs[ANOTHER.IS_TEAM_KILLER] = PLAYER_STATUS.IS_TEAM_KILLER
                if settings.main[MAIN.CHANGE_ANONYMOUS_NAME] and ANOTHER.NAME in kwargs and \
                        not kwargs[ANOTHER.NAME].startswith(BOT_START_SWITCH):
                    kwargs[ANOTHER.NAME] = kwargs[ANOTHER.FAKE_NAME] = settings.main[MAIN.ANONYMOUS_STRING]
        if settings.main[MAIN.HIDE_CLAN_ABBREV] and ANOTHER.CLAN_DBID in kwargs and ANOTHER.CLAN_ABBR in kwargs:
            kwargs[ANOTHER.CLAN_DBID] = GLOBAL.FIRST
            kwargs[ANOTHER.CLAN_ABBR] = GLOBAL.EMPTY_LINE
    return init(vInfoVo, *args, **kwargs)
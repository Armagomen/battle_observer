from armagomen.battle_observer.core import settings, view_settings
from armagomen.constants import MAIN, ANOTHER, GLOBAL, STATISTICS
from armagomen.utils.common import overrideMethod
from gui.battle_control.arena_info import settings as arena_settings
from gui.battle_control.arena_info.arena_vos import VehicleArenaInfoVO

_PLAYER_STATUS = arena_settings.PLAYER_STATUS


def getStatisticEnabled():
    return settings.statistics[GLOBAL.ENABLED] and settings.statistics[STATISTICS.STATISTIC_ENABLED]


@overrideMethod(VehicleArenaInfoVO)
def new_VehicleArenaInfoVO(init, vInfoVo, *args, **kwargs):
    if view_settings.notEpicBattle() and kwargs:
        if settings.main[MAIN.HIDE_BADGES] and ANOTHER.BADGES in kwargs:
            kwargs[ANOTHER.BADGES] = None
        if settings.main[MAIN.SHOW_ANONYMOUS] and ANOTHER.ACCOUNT_DBID in kwargs:
            if kwargs[ANOTHER.ACCOUNT_DBID] == GLOBAL.ZERO:
                if not getStatisticEnabled():
                    kwargs[ANOTHER.IS_TEAM_KILLER] = _PLAYER_STATUS.IS_TEAM_KILLER
                if settings.main[MAIN.CHANGE_ANONYMOUS_NAME] and ANOTHER.NAME in kwargs and \
                        not kwargs[ANOTHER.NAME].startswith(GLOBAL.BOT_START_SWITCH):
                    kwargs[ANOTHER.NAME] = kwargs[ANOTHER.FAKE_NAME] = settings.main[MAIN.ANONYMOUS_STRING]
        if settings.main[MAIN.HIDE_CLAN_ABBREV] and ANOTHER.CLAN_DBID in kwargs and ANOTHER.CLAN_ABBR in kwargs:
            kwargs[ANOTHER.CLAN_DBID] = GLOBAL.FIRST
            kwargs[ANOTHER.CLAN_ABBR] = GLOBAL.EMPTY_LINE
    return init(vInfoVo, *args, **kwargs)

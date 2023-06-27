# coding=utf-8

from armagomen._constants import MAIN, ANOTHER, GLOBAL
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.utils.common import overrideMethod
from gui.battle_control.arena_info.arena_vos import VehicleArenaInfoVO, PlayerInfoVO
from helpers import getClientLanguage

ANONYMOUS_TRANSLATE = "Анонімний" if getClientLanguage() == "uk" else "Anonymous"


@overrideMethod(VehicleArenaInfoVO)
def new_VehicleArenaInfoVO(init, vInfoVo, *args, **kwargs):
    if kwargs:
        if settings.main[MAIN.HIDE_BADGES] and ANOTHER.BADGES in kwargs:
            kwargs[ANOTHER.BADGES] = None
            kwargs[ANOTHER.OVERRIDDEN_BADGE] = None
        if settings.main[MAIN.SHOW_ANONYMOUS] and ANOTHER.ACCOUNT_DBID in kwargs:
            if kwargs[ANOTHER.ACCOUNT_DBID] == GLOBAL.ZERO:
                kwargs[ANOTHER.NAME] = kwargs[ANOTHER.FAKE_NAME] = ANONYMOUS_TRANSLATE
        if settings.main[MAIN.HIDE_CLAN_ABBREV] and ANOTHER.CLAN_ABBR in kwargs:
            kwargs[ANOTHER.CLAN_ABBR] = GLOBAL.EMPTY_LINE
    return init(vInfoVo, *args, **kwargs)


@overrideMethod(PlayerInfoVO, "update")
def new_update_VehicleArenaInfoVO(update, pInfoVo, **kwargs):
    if kwargs:
        if settings.main[MAIN.SHOW_ANONYMOUS] and ANOTHER.ACCOUNT_DBID in kwargs:
            if kwargs[ANOTHER.ACCOUNT_DBID] == GLOBAL.ZERO:
                kwargs[ANOTHER.NAME] = kwargs[ANOTHER.FAKE_NAME] = ANONYMOUS_TRANSLATE
        if settings.main[MAIN.HIDE_CLAN_ABBREV] and ANOTHER.CLAN_ABBR in kwargs:
            kwargs[ANOTHER.CLAN_ABBR] = GLOBAL.EMPTY_LINE
    return update(pInfoVo, **kwargs)

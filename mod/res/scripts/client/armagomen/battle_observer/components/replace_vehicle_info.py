# coding=utf-8

from armagomen._constants import ANOTHER, GLOBAL, MAIN
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import overrideMethod, xvmInstalled
from gui.battle_control.arena_info.arena_vos import VehicleArenaInfoVO
from helpers import getClientLanguage

# IMG_TAG_EYE_ICON = " <IMG SRC=\"img://gui/maps/icons/library/icon_eye.png\" width=\"16\" height=\"13\" vspace=\"-2\"/>"
ANONYMOUS_TRANSLATE = "Анонімно" if getClientLanguage().lower() == "uk" else "Anonymous"
EMPTY_BADGES = ([], [])


@overrideMethod(VehicleArenaInfoVO)
@overrideMethod(VehicleArenaInfoVO, "update")
def new_VehicleArenaInfoVO(base, *args, **kwargs):
    if kwargs:
        if user_settings.main[MAIN.HIDE_BADGES] and ANOTHER.BADGES in kwargs:
            kwargs[ANOTHER.BADGES] = EMPTY_BADGES
            kwargs[ANOTHER.OVERRIDDEN_BADGE] = GLOBAL.ZERO
        if not xvmInstalled and user_settings.main[MAIN.SHOW_ANONYMOUS] and ANOTHER.ACCOUNT_DBID in kwargs:
            if kwargs[ANOTHER.ACCOUNT_DBID] == GLOBAL.ZERO:
                kwargs[ANOTHER.NAME] = ANONYMOUS_TRANSLATE
        if user_settings.main[MAIN.HIDE_CLAN_ABBREV] and ANOTHER.CLAN_ABBR in kwargs:
            kwargs[ANOTHER.CLAN_ABBR] = GLOBAL.EMPTY_LINE
        if user_settings.main[MAIN.HIDE_PRESTIGE_BATTLE_WIDGET] and ANOTHER.PRESTIGE_LEVEL in kwargs:
            kwargs[ANOTHER.PRESTIGE_LEVEL] = kwargs[ANOTHER.PRESTIGE_GRADE_MARK_ID] = None
    return base(*args, **kwargs)

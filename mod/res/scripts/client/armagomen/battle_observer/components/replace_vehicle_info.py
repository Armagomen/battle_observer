# coding=utf-8

from armagomen._constants import ANOTHER, GLOBAL, MAIN
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import overrideMethod
from gui.battle_control.arena_info.arena_vos import VehicleArenaInfoVO
from helpers import getClientLanguage

ANONYMOUS_TRANSLATE = {
    "uk": "Анонімно",
    "pl": "Anonimowo",
    "de": "Anonym",
    "en": "Anonymous",
    "fr": "Anonyme"
}.get(getClientLanguage().lower(), "Anonymous")
EMPTY_BADGES = ([], [])


@overrideMethod(VehicleArenaInfoVO)
@overrideMethod(VehicleArenaInfoVO, "update")
def new_VehicleArenaInfoVO(base, *args, **kwargs):
    if kwargs:
        if user_settings.main[MAIN.HIDE_BADGES] and ANOTHER.BADGES in kwargs:
            kwargs[ANOTHER.BADGES] = EMPTY_BADGES
            kwargs[ANOTHER.OVERRIDDEN_BADGE] = 0
        if user_settings.main[MAIN.SHOW_ANONYMOUS] and ANOTHER.ACCOUNT_DBID in kwargs and kwargs[ANOTHER.ACCOUNT_DBID] == 0:
            kwargs[ANOTHER.NAME] = ANONYMOUS_TRANSLATE
        if user_settings.main[MAIN.HIDE_CLAN_ABBREV] and ANOTHER.CLAN_ABBR in kwargs:
            kwargs[ANOTHER.CLAN_ABBR] = GLOBAL.EMPTY_LINE
        if user_settings.main[MAIN.HIDE_PRESTIGE_BATTLE_WIDGET] and ANOTHER.PRESTIGE_LEVEL in kwargs:
            kwargs[ANOTHER.PRESTIGE_LEVEL] = kwargs[ANOTHER.PRESTIGE_GRADE_MARK_ID] = None
    return base(*args, **kwargs)

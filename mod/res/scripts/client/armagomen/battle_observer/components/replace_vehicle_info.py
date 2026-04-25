# coding=utf-8

from armagomen._constants import ANOTHER, GLOBAL, MAIN
from armagomen.battle_observer.settings import IBOSettingsLoader
from armagomen.utils.common import overrideMethod
from gui.battle_control.arena_info.arena_vos import VehicleArenaInfoVO
from helpers import dependency, getClientLanguage

ANONYMOUS_TRANSLATE = {
    "uk": "Анонімно",
    "pl": "Anonimowo",
    "de": "Anonym",
    "ru": "Анонимно",
}.get(getClientLanguage(), "Anonymous")
EMPTY_BADGES = ([], [])

mainSettings = dependency.instance(IBOSettingsLoader).getSetting(MAIN.NAME)

@overrideMethod(VehicleArenaInfoVO)
@overrideMethod(VehicleArenaInfoVO, "update")
def new_VehicleArenaInfoVO(base, *args, **kwargs):
    if kwargs:
        if mainSettings[MAIN.HIDE_BADGES] and ANOTHER.BADGES in kwargs:
            kwargs[ANOTHER.BADGES] = EMPTY_BADGES
            kwargs[ANOTHER.OVERRIDDEN_BADGE] = 0
        if mainSettings[MAIN.SHOW_ANONYMOUS] and ANOTHER.ACCOUNT_DBID in kwargs and kwargs[ANOTHER.ACCOUNT_DBID] == 0:
            kwargs[ANOTHER.NAME] = ANONYMOUS_TRANSLATE
        if mainSettings[MAIN.HIDE_CLAN_ABBREV] and ANOTHER.CLAN_ABBR in kwargs:
            kwargs[ANOTHER.CLAN_ABBR] = GLOBAL.EMPTY_LINE
    return base(*args, **kwargs)

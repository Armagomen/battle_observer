from PlayerEvents import g_playerEvents
from gui.battle_control.arena_info import settings
from gui.battle_control.arena_info.arena_vos import VehicleArenaInfoVO, VehicleTypeInfoVO
from messenger.gui.Scaleform.data.contacts_data_provider import _ContactsCategories
from messenger.storage import storage_getter
from ..core.bo_constants import MAIN, ANOTHER, GLOBAL
from ..core.config import cfg
from ..core.core import overrideMethod

_PLAYER_STATUS = settings.PLAYER_STATUS
_cache = {ANOTHER.FRIEND_LIST: set(), ANOTHER.ACCOUNT_DBID: GLOBAL.ZERO}


def onGuiCacheSyncCompleted(ctx):
    users = storage_getter(ANOTHER.USERS)().getList(_ContactsCategories().getCriteria())
    for user in users:
        if not user.isIgnored():
            _cache[ANOTHER.FRIEND_LIST].add(user._userID)
    _cache[ANOTHER.ACCOUNT_DBID] = ctx.get(ANOTHER.DBID, GLOBAL.ZERO)


g_playerEvents.onGuiCacheSyncCompleted += onGuiCacheSyncCompleted


@overrideMethod(VehicleArenaInfoVO)
def new_VehicleArenaInfoVO(old, vInfoVo, vehicleID, **kwargs):
    if kwargs:
        if cfg.main[MAIN.HIDE_BADGES]:
            kwargs[ANOTHER.BADGES] = None
        if cfg.main[MAIN.SHOW_ANONYMOUS] and kwargs[ANOTHER.ACCOUNT_DBID] == GLOBAL.ZERO:
            kwargs[ANOTHER.IS_TEAM_KILLER] = _PLAYER_STATUS.IS_TEAM_KILLER
            if cfg.main[MAIN.CHANGE_ANONYMOUS_NAME]:
                kwargs[ANOTHER.NAME] = cfg.main[MAIN.ANONYMOUS_STRING]
        if cfg.main[MAIN.HIDE_CLAN_ABBREV]:
            kwargs[ANOTHER.CLAN_DBID] = GLOBAL.FIRST
            kwargs[ANOTHER.CLAN_ABBR] = GLOBAL.EMPTY_LINE
    old(vInfoVo, vehicleID, **kwargs)
    if kwargs:
        if cfg.main[MAIN.SHOW_FRIENDS] and _cache[ANOTHER.ACCOUNT_DBID] > GLOBAL.ZERO:
            if not vInfoVo.vehicleType.isPremiumIGR:
                friends = _cache[ANOTHER.FRIEND_LIST]
                isPlayer = _cache[ANOTHER.ACCOUNT_DBID] == kwargs[ANOTHER.ACCOUNT_DBID]
                vInfoVo.vehicleType.isPremiumIGR = kwargs[ANOTHER.ACCOUNT_DBID] in friends or isPlayer


@overrideMethod(VehicleTypeInfoVO, "__setVehicleData")
def new_VehicleTypeInfoVO__setVehicleData(old, vTypeVo, vehicleDescr=None):
    old_isPremiumIGR = False
    if hasattr(vTypeVo, "isPremiumIGR"):
        old_isPremiumIGR = vTypeVo.isPremiumIGR
    old(vTypeVo, vehicleDescr=vehicleDescr)
    if vehicleDescr is not None and hasattr(vTypeVo, "isPremiumIGR") and old_isPremiumIGR:
        vTypeVo.isPremiumIGR = old_isPremiumIGR

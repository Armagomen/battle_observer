from PlayerEvents import g_playerEvents
from gui.battle_control.arena_info.arena_vos import VehicleTypeInfoVO
from messenger.gui.Scaleform.data.contacts_data_provider import _ContactsCategories
from messenger.storage import storage_getter

from armagomen.battle_observer.core import cfg
from armagomen.battle_observer.core.bo_constants import MAIN, ANOTHER, GLOBAL
from armagomen.battle_observer.core.utils.common import overrideMethod

_cache = {ANOTHER.FRIEND_LIST: set(), ANOTHER.ACCOUNT_DBID: GLOBAL.ZERO}


def onGuiCacheSyncCompleted(ctx):
    users = storage_getter(ANOTHER.USERS)().getList(_ContactsCategories().getCriteria())
    for user in users:
        if not user.isIgnored():
            _cache[ANOTHER.FRIEND_LIST].add(user._userID)
    _cache[ANOTHER.ACCOUNT_DBID] = ctx.get(ANOTHER.DBID, GLOBAL.ZERO)


g_playerEvents.onGuiCacheSyncCompleted += onGuiCacheSyncCompleted


@overrideMethod(VehicleTypeInfoVO)
def new_VehicleArenaInfoVO(init, vTypeVo, *args, **kwargs):
    if cfg.main[MAIN.SHOW_FRIENDS]:
        init(vTypeVo, *args, **kwargs)
        if kwargs and _cache[ANOTHER.ACCOUNT_DBID] > GLOBAL.ZERO:
            if not vTypeVo.isPremiumIGR and ANOTHER.ACCOUNT_DBID in kwargs:
                friends = _cache[ANOTHER.FRIEND_LIST]
                isPlayer = _cache[ANOTHER.ACCOUNT_DBID] == kwargs[ANOTHER.ACCOUNT_DBID]
                vTypeVo.isPremiumIGR = kwargs[ANOTHER.ACCOUNT_DBID] in friends or isPlayer
    else:
        return init(vTypeVo, *args, **kwargs)


@overrideMethod(VehicleTypeInfoVO, "update")
def new_VehicleTypeInfoVO_update(update, vTypeVo, *args, **kwargs):
    if cfg.main[MAIN.SHOW_FRIENDS]:
        isPremiumIGR = getattr(vTypeVo, "isPremiumIGR", False)
        result = update(vTypeVo, *args, **kwargs)
        if kwargs.get('vehicleType') is not None and hasattr(vTypeVo, "isPremiumIGR") and isPremiumIGR:
            vTypeVo.isPremiumIGR = isPremiumIGR
        return result
    return update(vTypeVo, *args, **kwargs)

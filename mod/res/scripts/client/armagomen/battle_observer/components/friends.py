from collections import namedtuple

from PlayerEvents import g_playerEvents
from armagomen.battle_observer.core import viewSettings
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import MAIN, ANOTHER, GLOBAL
from armagomen.utils.common import overrideMethod
from gui.battle_control.arena_info.arena_vos import VehicleTypeInfoVO
from messenger.gui.Scaleform.data.contacts_data_provider import _ContactsCategories
from messenger.storage import storage_getter

Cache = namedtuple("Cache", "friends databaseID")
_cache = Cache(set(), GLOBAL.ZERO)


def onGuiCacheSyncCompleted(ctx):
    users = storage_getter(ANOTHER.USERS)().getList(_ContactsCategories().getCriteria())
    friends = set(user for user in users if not user.isIgnored())
    database_id = ctx.get(ANOTHER.DBID, GLOBAL.ZERO)
    global _cache
    _cache = Cache(friends, database_id)


g_playerEvents.onGuiCacheSyncCompleted += onGuiCacheSyncCompleted


@overrideMethod(VehicleTypeInfoVO)
def new_VehicleArenaInfoVO(init, vTypeVo, *args, **kwargs):
    if not viewSettings.gui.isInEpicRange() and settings.main[MAIN.SHOW_FRIENDS]:
        init(vTypeVo, *args, **kwargs)
        if kwargs and _cache.databaseID > GLOBAL.ZERO and not vTypeVo.isPremiumIGR and ANOTHER.ACCOUNT_DBID in kwargs:
            isPlayer = _cache.databaseID == kwargs[ANOTHER.ACCOUNT_DBID]
            vTypeVo.isPremiumIGR = kwargs[ANOTHER.ACCOUNT_DBID] in _cache.friends or isPlayer
    else:
        return init(vTypeVo, *args, **kwargs)


@overrideMethod(VehicleTypeInfoVO, "update")
def new_VehicleTypeInfoVO_update(update, vTypeVo, *args, **kwargs):
    if not viewSettings.gui.isInEpicRange() and settings.main[MAIN.SHOW_FRIENDS]:
        isPremiumIGR = getattr(vTypeVo, "isPremiumIGR", False)
        result = update(vTypeVo, *args, **kwargs)
        if kwargs.get('vehicleType') is not None and hasattr(vTypeVo, "isPremiumIGR") and isPremiumIGR:
            vTypeVo.isPremiumIGR = isPremiumIGR
        return result
    return update(vTypeVo, *args, **kwargs)

from armagomen._constants import ANOTHER, MAIN
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import isReplay, overrideMethod
from gui.battle_control.arena_info.arena_vos import VehicleTypeInfoVO
from messenger.gui.Scaleform.data.contacts_data_provider import _ContactsCategories
from messenger.storage import storage_getter
from PlayerEvents import g_playerEvents

_cache = set()


def onGuiCacheSyncCompleted(ctx):
    _cache.clear()
    users = storage_getter(ANOTHER.USERS)().getList(_ContactsCategories().getCriteria())
    _cache.update(user._userID for user in users if not user.isIgnored())


g_playerEvents.onGuiCacheSyncCompleted += onGuiCacheSyncCompleted


def showFriends():
    return user_settings.main[MAIN.SHOW_FRIENDS] and not isReplay()


@overrideMethod(VehicleTypeInfoVO)
def new_VehicleArenaInfoVO(init, vTypeVo, *args, **kwargs):
    init(vTypeVo, *args, **kwargs)
    if showFriends():
        vTypeVo.isPremiumIGR |= kwargs.get(ANOTHER.ACCOUNT_DBID) in _cache


@overrideMethod(VehicleTypeInfoVO, "update")
def new_VehicleTypeInfoVO_update(update, vTypeVo, *args, **kwargs):
    if showFriends():
        result = update(vTypeVo, *args, **kwargs)
        if hasattr(vTypeVo, "isPremiumIGR"):
            vTypeVo.isPremiumIGR |= kwargs.get(ANOTHER.ACCOUNT_DBID) in _cache
        return result
    return update(vTypeVo, *args, **kwargs)


def fini():
    global onGuiCacheSyncCompleted
    g_playerEvents.onGuiCacheSyncCompleted -= onGuiCacheSyncCompleted

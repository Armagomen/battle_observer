from armagomen._constants import ANOTHER, MAIN
from armagomen.battle_observer.settings import IBOSettingsLoader
from armagomen.utils.common import isReplay, overrideMethod
from gui.battle_control.arena_info.arena_vos import VehicleTypeInfoVO
from helpers import dependency
from messenger.gui.Scaleform.data.contacts_data_provider import _ContactsCategories
from messenger.storage import storage_getter
from PlayerEvents import g_playerEvents


class Friends(object):
    settingsLoader = dependency.descriptor(IBOSettingsLoader)

    def __init__(self):
        self._cache = set()
        g_playerEvents.onGuiCacheSyncCompleted += self._onGuiCacheSyncCompleted
        overrideMethod(VehicleTypeInfoVO)(self.new_VehicleTypeInfoVO)
        overrideMethod(VehicleTypeInfoVO, "update")(self.new_VehicleTypeInfoVO_update)

    def _onGuiCacheSyncCompleted(self, *args, **kwargs):
        self._cache.clear()
        users = storage_getter(ANOTHER.USERS)().getList(_ContactsCategories().getCriteria())
        self._cache.update(user._userID for user in users if not user.isIgnored())

    def showFriends(self):
        return self.settingsLoader.getSetting(MAIN.NAME, MAIN.SHOW_FRIENDS) and not isReplay()

    def new_VehicleTypeInfoVO(self, init, vTypeVo, *args, **kwargs):
        init(vTypeVo, *args, **kwargs)
        if self.showFriends():
            vTypeVo.isPremiumIGR |= kwargs.get(ANOTHER.ACCOUNT_DBID) in self._cache

    def new_VehicleTypeInfoVO_update(self, update, vTypeVo, *args, **kwargs):
        if self.showFriends():
            result = update(vTypeVo, *args, **kwargs)
            if hasattr(vTypeVo, "isPremiumIGR"):
                vTypeVo.isPremiumIGR |= kwargs.get(ANOTHER.ACCOUNT_DBID) in self._cache
            return result
        return update(vTypeVo, *args, **kwargs)

    def fini(self):
        g_playerEvents.onGuiCacheSyncCompleted -= self._onGuiCacheSyncCompleted


friends = Friends()


def fini():
    friends.fini()

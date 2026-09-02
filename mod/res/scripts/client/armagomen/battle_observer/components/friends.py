from armagomen._constants import ANOTHER, MAIN
from armagomen.battle_observer.settings import IBOSettingsLoader
from armagomen.utils.common import overrideMethod
from gui.battle_control.arena_info.arena_vos import VehicleTypeInfoVO
from helpers import dependency
from messenger.proto.shared_find_criteria import FriendsFindCriteria
from messenger.storage import MessengerStorageDescriptor, UsersStorage
from PlayerEvents import g_playerEvents


class Friends(object):
    settingsLoader = dependency.descriptor(IBOSettingsLoader)
    __usersStorage = MessengerStorageDescriptor(UsersStorage)

    def __init__(self):
        self._cache = set()
        g_playerEvents.onGuiCacheSyncCompleted += self._onGuiCacheSyncCompleted
        overrideMethod(VehicleTypeInfoVO)(self.new_VehicleTypeInfoVO)
        overrideMethod(VehicleTypeInfoVO, "update")(self.new_VehicleTypeInfoVO_update)

    def _onGuiCacheSyncCompleted(self, *args, **kwargs):
        self._cache.clear()
        friends = self.__usersStorage.getList(FriendsFindCriteria())
        self._cache.update(user._userID for user in friends if not user.isIgnored())

    def showFriends(self):
        return self.settingsLoader.getSetting(MAIN.NAME, MAIN.SHOW_FRIENDS)

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

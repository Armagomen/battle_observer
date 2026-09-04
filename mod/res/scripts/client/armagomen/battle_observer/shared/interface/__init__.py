from wg_async import wg_async


class IBOKeysListener(object):
    __slots__ = ()

    def fini(self):
        raise NotImplementedError

    def registerComponent(self, keyFunction, keyList=None):
        raise NotImplementedError


class IBOPiercingRandomizer(object):

    def fini(self):
        raise NotImplementedError

    def updateRandomization(self, vehicle):
        raise NotImplementedError


class IBOPlayersDamageController(object):
    __slots__ = ()

    def fini(self):
        raise NotImplementedError

    def getPlayerDamage(self, vehicleID):
        raise NotImplementedError


class IStatisticsDataLoader(object):

    def requestStatisticsFromApi(self, DBIDs):
        raise NotImplementedError

    def fini(self):
        pass


class IViewSettings(object):

    def fini(self):
        pass

    def invalidateComponents(self):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def registerViewComponents(self):
        raise NotImplementedError

    @property
    def battlePages(self):
        raise NotImplementedError


class IBOCurrentVehicleCachedData(object):
    __slots__ = ()

    def fini(self):
        raise NotImplementedError

    def onVehicleChanged(self):
        raise NotImplementedError

    @property
    def efficiencyAvgData(self):
        raise NotImplementedError

    @property
    def default(self):
        raise NotImplementedError


class IBOOnline(object):
    __slots__ = ()

    def fini(self):
        raise NotImplementedError

    @wg_async
    def user_login(self, user_id, name, version):
        raise NotImplementedError

    @wg_async
    def user_logout(self, user_id, attempt=0):
        raise NotImplementedError

    @wg_async
    def get_stats_by_region(self):
        raise NotImplementedError

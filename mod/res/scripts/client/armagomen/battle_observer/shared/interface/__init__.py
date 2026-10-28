class IBOKeysListener(object):
    __slots__ = ()

    def fini(self):
        raise NotImplementedError

    def registerComponent(self, keyFunction, keyList=None):
        raise NotImplementedError


class IShotResultHelper(object):

    def fini(self):
        raise NotImplementedError

    def updateRandomization(self, vehicle):
        raise NotImplementedError

    def getMinMaxPiercingPower(self, power):
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


class IBOCurrentVehicleCachedData(object):
    __slots__ = ()

    def __init__(self):
        super(IBOCurrentVehicleCachedData, self).__init__()

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

    def user_login(self, user_id, name, version):
        raise NotImplementedError

    def user_logout(self, user_id, attempt=0):
        raise NotImplementedError

    def get_stats_by_region(self):
        raise NotImplementedError

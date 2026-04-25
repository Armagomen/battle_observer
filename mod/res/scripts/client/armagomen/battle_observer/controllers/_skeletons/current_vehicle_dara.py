class IBOCurrentVehicleCachedData(object):
    __slots__ = ()

    def init(self):
        raise NotImplementedError

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

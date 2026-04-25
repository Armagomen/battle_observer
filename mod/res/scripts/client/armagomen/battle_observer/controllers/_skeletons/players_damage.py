class IBOPlayersDamageController(object):
    __slots__ = ()

    def init(self):
        raise NotImplementedError

    def fini(self):
        raise NotImplementedError

    def getPlayerDamage(self, vehicleID):
        raise NotImplementedError

class IPiercingRandomizer(object):

    def init(self):
        raise NotImplementedError

    def fini(self):
        raise NotImplementedError

    def updateRandomization(self, vehicle):
        raise NotImplementedError

    @property
    def confines(self):
        raise NotImplementedError

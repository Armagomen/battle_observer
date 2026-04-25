class IBOKeysListener(object):
    __slots__ = ()

    def init(self):
        raise NotImplementedError

    def fini(self):
        raise NotImplementedError

    def registerComponent(self, keyFunction, keyList=None):
        raise NotImplementedError

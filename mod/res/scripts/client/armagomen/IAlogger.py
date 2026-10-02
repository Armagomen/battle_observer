class IALogger(object):
    __slots__ = ()

    def fini(self):
        raise NotImplementedError

    @property
    def is_debug(self):
        raise NotImplementedError

    def set_debug(self, value):
        raise NotImplementedError

    def setModName(self, mod_name):
        raise NotImplementedError

    def logError(self, message, *args, **kwargs):
        raise NotImplementedError

    def logInfo(self, message, *args, **kwargs):
        raise NotImplementedError

    def logDebug(self, message, *args, **kwargs):
        raise NotImplementedError

    def logWarning(self, message, *args, **kwargs):
        raise NotImplementedError

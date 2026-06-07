import traceback
from inspect import getmro

from BigWorld import logDebug, logError, logInfo, logWarning


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


class _ALogger(IALogger):
    EMPTY_WARN = "!!! WARNING !!! - Empty string detected. Check first argument in call function at: File '{}', line {}, in {}, code {}"
    __slots__ = ("__is_debug", "__mod_name")

    def __init__(self):
        self.__is_debug = False
        self.__mod_name = "BATTLE_OBSERVER"
        self.logInfo("Initializing BO logger")

    @property
    def is_debug(self):
        return self.__is_debug

    def set_debug(self, value):
        update = self.__is_debug != value
        if update:
            self.__is_debug = value
        return update and value

    def fini(self):
        self.logInfo("Finished BO logger")

    @staticmethod
    def get_full_function_path(func):
        module_name = func.__module__
        func_name = func.__name__

        if hasattr(func, "im_class"):
            for cls in getmro(func.im_class):
                if func_name in cls.__dict__:
                    class_name = cls.__name__
                    return "{}.{}.{}".format(module_name, class_name, func_name)

        return "{}.{}".format(module_name, func_name)

    def _formatMessage(self, message, *args, **kwargs):
        if not isinstance(message, basestring):
            message = str(message)
        if not message:
            return self.EMPTY_WARN.format(*traceback.extract_stack()[-3])
        elif args or kwargs:
            return message.format(*args, **kwargs)
        return message

    def logError(self, message, *args, **kwargs):
        logError(self.__mod_name, self._formatMessage(message, *args, **kwargs), None)

    def logInfo(self, message, *args, **kwargs):
        logInfo(self.__mod_name, self._formatMessage(message, *args, **kwargs), None)

    def logDebug(self, message, *args, **kwargs):
        if self.__is_debug:
            if "func" in kwargs:
                kwargs["func"] = self.get_full_function_path(kwargs["func"])
            logDebug(self.__mod_name, self._formatMessage(message, *args, **kwargs), None)

    def logWarning(self, message, *args, **kwargs):
        logWarning(self.__mod_name, self._formatMessage(message, *args, **kwargs), None)

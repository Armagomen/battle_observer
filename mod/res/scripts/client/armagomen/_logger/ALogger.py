import logging

from . import IALogger


class ALogger(IALogger):
    EMPTY_WARN = "!!! WARNING !!! - Empty string detected. Check first argument in call function at: File '{}', line {}, in {}, code {}"
    __slots__ = ("__is_debug", "logger")

    def __init__(self, name):
        self.__is_debug = False
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
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
            from inspect import getmro
            for cls in getmro(func.im_class):
                if func_name in cls.__dict__:
                    class_name = cls.__name__
                    return "{}.{}.{}".format(module_name, class_name, func_name)

        return "{}.{}".format(module_name, func_name)

    def _formatMessage(self, message, *args, **kwargs):
        if not isinstance(message, basestring):
            message = str(message)
        if not message:
            from traceback import extract_stack
            return self.EMPTY_WARN.format(*extract_stack()[-3])
        elif args or kwargs:
            return message.format(*args, **kwargs)
        return message

    def logError(self, message, *args, **kwargs):
        """
        :type message: str
        """
        self.logger.error(self._formatMessage(message, *args, **kwargs))

    def logInfo(self, message, *args, **kwargs):
        """
        :type message: str
        """
        self.logger.info(self._formatMessage(message, *args, **kwargs))

    def logDebug(self, message, *args, **kwargs):
        """
        :type message: str
        """
        if self.__is_debug:
            if "func" in kwargs:
                kwargs["func"] = self.get_full_function_path(kwargs["func"])
            self.logger.info(self._formatMessage(message, *args, **kwargs))

    def logWarning(self, message, *args, **kwargs):
        self.logger.warning(self._formatMessage(message, *args, **kwargs))

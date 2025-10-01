import traceback
from inspect import getmro

import BigWorld

MOD_NAME = "BATTLE_OBSERVER"
DEBUG = "DEBUG_MODE"
EMPTY_WARN = "!!! WARNING !!! - Empty string detected. Check first argument in call function at: File '{}', line {}, in {}, code {}"
IS_DEBUG = False


def setDebug(value):
    global IS_DEBUG
    if IS_DEBUG != value:
        IS_DEBUG = value


def get_full_function_path(func):
    module_name = func.__module__
    func_name = func.__name__

    if hasattr(func, "im_class"):
        for cls in getmro(func.im_class):
            if func_name in cls.__dict__:
                class_name = cls.__name__
                return "{}.{}.{}".format(module_name, class_name, func_name)

    return "{}.{}".format(module_name, func_name)


def _formatMessage(message, *args, **kwargs):
    if not isinstance(message, str):
        message = str(message)
    if not message:
        return EMPTY_WARN.format(*traceback.extract_stack()[-3])
    elif args or kwargs:
        return message.format(*args, **kwargs)
    return message


def logError(message, *args, **kwargs):
    BigWorld.logError(MOD_NAME, _formatMessage(message, *args, **kwargs), None)


def logInfo(message, *args, **kwargs):
    BigWorld.logInfo(MOD_NAME, _formatMessage(message, *args, **kwargs), None)


def logDebug(message, *args, **kwargs):
    if IS_DEBUG:
        if "func" in kwargs:
            kwargs["func"] = get_full_function_path(kwargs["func"])
        BigWorld.logDebug(MOD_NAME, _formatMessage(message, *args, **kwargs), None)


def logWarning(message, *args, **kwargs):
    BigWorld.logWarning(MOD_NAME, _formatMessage(message, *args, **kwargs), None)

import BigWorld

MOD_NAME = "BATTLE_OBSERVER"
DEBUG = "DEBUG_MODE"
IS_DEBUG = False


def setDebug(value):
    global IS_DEBUG
    IS_DEBUG = value


def _formatMessage(message, *args, **kwargs):
    if not isinstance(message, basestring):
        message = str(message)
    if args or kwargs:
        return message.format(*args, **kwargs)
    return message


def logError(message, *args, **kwargs):
    BigWorld.logError(MOD_NAME, _formatMessage(message, *args, **kwargs), None)


def logInfo(message, *args, **kwargs):
    BigWorld.logInfo(MOD_NAME, _formatMessage(message, *args, **kwargs), None)


def logDebug(message, *args, **kwargs):
    if IS_DEBUG:
        BigWorld.logDebug(MOD_NAME, _formatMessage(message, *args, **kwargs), None)


def logWarning(message, *args, **kwargs):
    BigWorld.logWarning(MOD_NAME, _formatMessage(message, *args, **kwargs), None)

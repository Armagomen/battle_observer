import BigWorld

MOD_NAME = "BATTLE_OBSERVER"
DEBUG = "DEBUG_MODE"


def _formatMessage(message, *args, **kwargs):
    message = unicode(str(message), "utf-8", "ignore")
    if args or kwargs:
        return message.format(*args, **kwargs)
    return message


def logError(message, *args, **kwargs):
    BigWorld.logError(MOD_NAME, _formatMessage(message, *args, **kwargs), None)


def logInfo(message, *args, **kwargs):
    BigWorld.logInfo(MOD_NAME, _formatMessage(message, *args, **kwargs), None)


def logDebug(message, *args, **kwargs):
    BigWorld.logDebug(MOD_NAME, _formatMessage(message, *args, **kwargs), None)


def logWarning(message, *args, **kwargs):
    BigWorld.logWarning(MOD_NAME, _formatMessage(message, *args, **kwargs), None)

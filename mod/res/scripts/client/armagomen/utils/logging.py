import BigWorld

from armagomen.battle_observer.settings import user

MOD_NAME = "BATTLE_OBSERVER"
DEBUG = "DEBUG_MODE"


def logError(message, *args, **kwargs):
    BigWorld.logError(MOD_NAME, str(message).format(*args, **kwargs), None)


def logInfo(message):
    BigWorld.logInfo(MOD_NAME, str(message), None)


def logDebug(message, *args, **kwargs):
    if user.main[DEBUG]:
        BigWorld.logDebug(MOD_NAME, str(message).format(*args, **kwargs), None)


def logWarning(message):
    BigWorld.logWarning(MOD_NAME, str(message), None)

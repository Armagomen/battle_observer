import BigWorld
import Math

from .bo_constants import MOD_NAME


def getPlayer():
    return BigWorld.player()


def getTarget():
    return BigWorld.target()


def getEntity(entity_id):
    return BigWorld.entity(entity_id)


def setMaxFrameRate(fps):
    BigWorld.wg_setMaxFrameRate(fps)


def callback(*args, **kwargs):
    return BigWorld.callback(*args, **kwargs)


def cancelCallback(*args, **kwargs):
    return BigWorld.cancelCallback(*args, **kwargs)


def logError(msg):
    BigWorld.logError(MOD_NAME, msg, None)


def logInfo(msg):
    BigWorld.logInfo(MOD_NAME, msg, None)


def logWarning(msg):
    BigWorld.logWarning(MOD_NAME, msg, None)


def getPreferencesFilePath():
    return BigWorld.wg_getPreferencesFilePath()


def restartGame():
    BigWorld.savePreferences()
    BigWorld.worldDrawEnabled(False)
    BigWorld.restartGame()


def openWebBrowser(url):
    BigWorld.wg_openWebBrowser(url)


def vector3(x, y, z):
    return Math.Vector3(x, y, z)
import os

import BigWorld
import Math
import ResMgr

MOD_NAME = "BATTLE_OBSERVER"


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


def getCurrentModPath():
    p = os.path
    cwd = os.getcwdu() if p.supports_unicode_filenames else os.getcwd()
    if any(x in cwd for x in ("win32", "win64")):
        cwd = p.split(cwd)[0]
    for sec in ResMgr.openSection(p.join(cwd, 'paths.xml'))['Paths'].values():
        if './mods/' in sec.asString:
            return p.split(p.realpath(p.join(cwd, p.normpath(sec.asString))))
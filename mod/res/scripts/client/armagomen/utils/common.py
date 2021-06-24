import locale
import os
from collections import namedtuple
from string import printable

import BigWorld
import Math
import ResMgr

from BattleReplay import isPlaying, isLoading
from Event import SafeEvent
from armagomen.constants import MOD_NAME


def isReplay():
    return isPlaying() or isLoading()


def getPlayer():
    return BigWorld.player()


def getTarget():
    return BigWorld.target()


def getEntity(entity_id):
    return BigWorld.entity(entity_id)


def setMaxFrameRate(fps):
    BigWorld.wg_setMaxFrameRate(fps + 1)
    BigWorld.savePreferences()


def callback(*args, **kwargs):
    return BigWorld.callback(*args, **kwargs)


def cancelCallback(*args, **kwargs):
    return BigWorld.cancelCallback(*args, **kwargs)


def logError(message):
    BigWorld.logError(MOD_NAME, str(message), None)


def logInfo(message):
    BigWorld.logInfo(MOD_NAME, str(message), None)


def logWarning(message):
    BigWorld.logWarning(MOD_NAME, str(message), None)


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


def overrideMethod(wg_class, method_name="__init__"):
    """
    :type wg_class: class object
    :type method_name: unicode default __init__
    """
    class_name = wg_class.__name__
    if not hasattr(wg_class, method_name):
        if method_name.startswith("__"):
            full_name = "_{0}{1}".format(class_name, method_name)
            if hasattr(wg_class, full_name):
                method_name = full_name
            elif hasattr(wg_class, method_name[1:]):
                method_name = method_name[1:]

    def outer(new_method):
        old_method = getattr(wg_class, method_name, None)
        if old_method is not None and callable(old_method):
            def override(*args, **kwargs):
                return new_method(old_method, *args, **kwargs)

            setattr(wg_class, method_name, override)
        else:
            logError("{0} in {1} is not callable or undefined".format(method_name, class_name))
        return new_method

    return outer


def checkDecoder(_string):
    for char in _string:
        if char not in printable:
            return locale.getpreferredencoding()
    return None


def convertDictToNamedtuple(dictionary):
    """
    :rtype: namedtuple
    :type dictionary: dict
    """
    return namedtuple(dictionary.__name__, dictionary.keys())(**dictionary)


class Events(object):

    def __init__(self):
        self.onArmorChanged = SafeEvent()
        self.onMarkerColorChanged = SafeEvent()
        self.onDispersionAngleChanged = SafeEvent()


events = Events()

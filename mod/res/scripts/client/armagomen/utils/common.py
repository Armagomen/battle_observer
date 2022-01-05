import codecs
import json
import locale
import math
import os
from collections import namedtuple
from colorsys import hsv_to_rgb
from shutil import rmtree
from string import printable

import BigWorld
import Math
import ResMgr

from BattleReplay import isPlaying, isLoading
from helpers.http import openUrl

MOD_NAME = "BATTLE_OBSERVER"


def isReplay():
    return isPlaying() or isLoading()


def getPlayer():
    return BigWorld.player()


def getTarget():
    return BigWorld.target()


def getEntity(entity_id):
    return BigWorld.entity(entity_id)


def getDistanceTo(targetPos):
    return getPlayer().position.distTo(targetPos)


def setMaxFrameRate(fps):
    BigWorld.wg_setMaxFrameRate(fps + 1)
    BigWorld.savePreferences()


def callback(delay, function):
    return BigWorld.callback(delay, function)


def cancelCallback(callbackID):
    return BigWorld.cancelCallback(callbackID)


def logError(message):
    BigWorld.logError(MOD_NAME, str(message), None)


def logInfo(message):
    BigWorld.logInfo(MOD_NAME, str(message), None)


def logDebug(message):
    BigWorld.logDebug(MOD_NAME, str(message), None)


def logWarning(message):
    BigWorld.logWarning(MOD_NAME, str(message), None)


preferencesDir = None


def getPreferencesDir():
    global preferencesDir
    if preferencesDir is None:
        normpath = os.path.normpath(unicode(BigWorld.wg_getPreferencesFilePath(), 'utf-8', errors='ignore'))
        preferencesDir = os.path.split(normpath)[0]
    return preferencesDir


def restartGame():
    BigWorld.restartGame()


def openWebBrowser(url):
    BigWorld.wg_openWebBrowser(url)


def vector3(x, y, z):
    return Math.Vector3(x, y, z)


modPathCache = None


def getCurrentModPath():
    global modPathCache
    if modPathCache is None:
        cwd = os.getcwdu() if os.path.supports_unicode_filenames else os.getcwd()
        if any(x in cwd for x in ("win32", "win64")):
            cwd = os.path.split(cwd)[0]
        cleanupUpdates(cwd)
        for sec in ResMgr.openSection(os.path.join(cwd, 'paths.xml'))['Paths'].values():
            if './mods/' in sec.asString:
                modPathCache = os.path.split(os.path.realpath(os.path.join(cwd, os.path.normpath(sec.asString))))
    return modPathCache


def cleanupUpdates(cwd):
    path = os.path.join(cwd, "updates")
    # Gather directory contents
    if not os.path.exists(path):
        return os.makedirs(path)
    ignored = set()
    section = ResMgr.openSection(os.path.join(cwd, 'game_info.xml'))
    if section['game']['upcoming_patches']:
        for value in section['game']['upcoming_patches'].values():
            ignored.update(val.asString.split("\\")[0] for val in value.values())
    contents = [os.path.join(path, i) for i in os.listdir(path) if i not in ignored]
    # Iterate and remove each item in the appropriate manner
    if contents:
        for i in contents:
            os.unlink(i) if os.path.isfile(i) or os.path.islink(i) else rmtree(i, ignore_errors=True)


def removeDirs(normpath, name=None):
    if os.path.exists(normpath):
        rmtree(normpath, ignore_errors=True, onerror=None)
        if name is not None:
            logInfo('CLEANING CACHE: {0}'.format(name))


def clearClientCache(category=None):
    path = getPreferencesDir()
    dirs = (
        "account_caches", "battle_results", "clan_cache", "custom_data", "dossier_cache", "messenger_cache",
        "storage_cache", "tutorial_cache", "veh_cmp_cache", "web_cache", "profile"
    )
    if category is None:
        for dirName in dirs:
            removeDirs(os.path.join(path, dirName), dirName)
    else:
        removeDirs(os.path.join(path, category), category)
    cleanupObserverUpdates()


def encodeData(data):
    """encode dict keys/values to utf-8."""
    if isinstance(data, dict):
        return {encodeData(key): encodeData(value) for key, value in data.iteritems()}
    elif isinstance(data, list):
        return [encodeData(element) for element in data]
    elif isinstance(data, basestring):
        return data.encode('utf-8')
    else:
        return data


def openJsonFile(path):
    """Gets a dict from JSON."""
    try:
        with open(path, 'r') as dataFile:
            return encodeData(json.load(dataFile, encoding='utf-8-sig'))
    except Exception:
        with codecs.open(path, 'r', 'utf-8-sig') as dataFile:
            return encodeData(json.loads(dataFile.read(), encoding='utf-8-sig'))


def writeJsonFile(path, data):
    """Creates a new json file in a folder or replace old."""
    with open(path, 'w') as dataFile:
        json.dump(data, dataFile, skipkeys=True, ensure_ascii=False, indent=2, sort_keys=True)


def getObserverCachePath():
    path = os.path.join(getPreferencesDir(), "battle_observer")
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def getCrewPath():
    path = os.path.join(getObserverCachePath(), "crew_ignored.json")
    if not os.path.isfile(path):
        writeJsonFile(path, {"vehicles": []})
    return path


def getUpdatePath():
    path = os.path.join(getObserverCachePath(), "update")
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def cleanupObserverUpdates():
    root = getUpdatePath()
    for filename in os.listdir(root):
        filePath = os.path.join(root, filename)
        if os.path.isfile(filePath):
            os.unlink(filePath)


ignored_vehicles = set(openJsonFile(getCrewPath()).get("vehicles"))


def addVehicleToCache(vehicle):
    ignored_vehicles.add(vehicle)
    writeJsonFile(getCrewPath(), {"vehicles": sorted(ignored_vehicles)})


def overrideMethod(wg_class, method_name="__init__"):
    """
    wg_class: class object
    method_name: unicode default __init__
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
    return namedtuple(dictionary.__name__, dictionary.keys())(**dictionary)


def convertNamedtupleToDict(named):
    return dict(named._asdict())


COLOR = namedtuple("COLOR", ("PURPLE", "GREEN", "MULTIPLIER", "TEMPLATE"))(0.8333, 0.3333, 255, "#{:02X}{:02X}{:02X}")


def percentToRGB(percent, saturation=0.5, brightness=1.0):
    """percent is float number in range 0 - 2.4 purple, or 1.0 green"""
    normalized_percent = min(COLOR.PURPLE, percent * COLOR.GREEN)
    tuple_values = hsv_to_rgb(normalized_percent, saturation, brightness)
    r, g, b = (int(math.ceil(i * COLOR.MULTIPLIER)) for i in tuple_values)
    return COLOR.TEMPLATE.format(r, g, b)


def urlResponse(url):
    response = openUrl(url)
    responseData = response.getData()
    if responseData is not None:
        return json.loads(responseData, encoding="utf-8-sig")
    return responseData


def parseColorToHex(color, asInt=False):
    color = "0x" + color[1:]
    return int(color, 16) if asInt else color

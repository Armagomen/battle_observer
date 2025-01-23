import json
import locale
import os
import shutil
from collections import namedtuple
from colorsys import hsv_to_rgb
from functools import partial
from io import open as _open
from threading import Thread

import BigWorld
import ResMgr

from armagomen.utils.logging import logDebug, logError, logInfo
from BattleReplay import isLoading, isPlaying
from external_strings_utils import unicode_from_utf8
from gui.Scaleform.daapi.view.battle.shared.formatters import normalizeHealth
from helpers.http import openUrl

CONFIG_DIR = "mod_battle_observer"
MOD_CACHE = "battle_observer"
UTF_8 = 'utf-8'


def isReplay():
    return isPlaying() or isLoading()


def getPlayer():
    return BigWorld.player()


def getTarget():
    return BigWorld.target()


def getEntity(entity_id):
    return BigWorld.entities.get(entity_id)


def addCallback(delay, callMethod, *args, **kwargs):
    return BigWorld.callback(delay, partial(callMethod, *args, **kwargs) if args or kwargs else callMethod)


def cancelCallback(callbackID):
    return BigWorld.cancelCallback(callbackID)


def getPreferencesDir():
    preferences_file_path = unicode_from_utf8(BigWorld.wg_getPreferencesFilePath())[1]
    return os.path.normpath(os.path.dirname(preferences_file_path))


preferencesDir = getPreferencesDir()


def restartGame():
    BigWorld.restartGame()


def closeClient():
    BigWorld.quit()


def openWebBrowser(url):
    BigWorld.wg_openWebBrowser(url)


cwd = os.getcwdu() if os.path.supports_unicode_filenames else os.getcwd()


def getCurrentModsPath():
    for sec in ResMgr.openSection(os.path.join(cwd, 'paths.xml'))['Paths'].values():
        if './mods/' in sec.asString:
            return os.path.split(os.path.realpath(os.path.join(cwd, os.path.normpath(sec.asString))))


modsPath, gameVersion = getCurrentModsPath()
configsPath = os.path.join(modsPath, "configs")
if not os.path.exists(configsPath):
    os.makedirs(configsPath)


def setCurrentConfigPath(configs_path):
    config_path = None
    for dir_name in os.listdir(configs_path):
        full_path = os.path.join(configs_path, dir_name)
        if os.path.isdir(full_path):
            if dir_name == CONFIG_DIR:
                config_path = full_path
                break
            else:
                config_path = setCurrentConfigPath(full_path)
    return config_path


currentConfigPath = setCurrentConfigPath(configsPath)

if currentConfigPath is None:
    currentConfigPath = os.path.join(configsPath, CONFIG_DIR)
    if not os.path.exists(currentConfigPath):
        os.makedirs(currentConfigPath)


def removeDirs(path):
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True, onerror=None)
        return True
    return False


def cleanupUpdates():
    path = os.path.join(cwd, "updates")
    # Gather directory contents
    if not os.path.exists(path):
        return os.makedirs(path)
    ignored = set()
    section = ResMgr.openSection(os.path.join(cwd, 'game_info.xml'))
    if section['game']['upcoming_patches']:
        for value in section['game']['upcoming_patches'].values():
            ignored.update(val.asString.split("\\")[0] for val in value.values())
    for _link in os.listdir(path):
        if _link in ignored:
            continue
        link = os.path.join(path, _link)
        os.unlink(link) if os.path.isfile(link) or os.path.islink(link) else removeDirs(link)
        logInfo("CLEARING THE UPDATE FOLDER: {}", link)


def clearClientCache():
    exclude_cache_dirs = ["game_loading_cache"]
    game_cache_dirs = [x for x in os.listdir(preferencesDir) if "_cache" in x and x not in exclude_cache_dirs]
    for dirName in game_cache_dirs:
        if removeDirs(os.path.join(preferencesDir, dirName)):
            logInfo("CLEANING CLIENT CACHE FOLDER: {}", dirName)


def encodeData(data):
    """encode dict keys/values to utf-8."""
    if isinstance(data, dict):
        return {encodeData(key): encodeData(value) for key, value in data.iteritems()}
    elif isinstance(data, list):
        return [encodeData(element) for element in data]
    elif isinstance(data, (str, unicode)):
        return data.encode(UTF_8)
    else:
        return data


def openJsonFile(path):
    """Gets a dict from JSON."""
    if os.path.exists(path):
        with _open(path, 'r', encoding=UTF_8) as dataFile:
            try:
                return encodeData(json.load(dataFile, encoding=UTF_8))
            except ValueError:
                return encodeData(json.loads(dataFile.read(), encoding=UTF_8))


def writeJsonFile(path, data):
    """Creates a new json file in a folder or replace old."""
    with _open(path, 'w', encoding=UTF_8) as dataFile:
        dataFile.write(unicode(json.dumps(data, skipkeys=True, ensure_ascii=False, indent=2, sort_keys=True)))


def getObserverCachePath():
    old_path = os.path.join(preferencesDir, MOD_CACHE)
    new_path = os.path.join(preferencesDir, "mods", MOD_CACHE)
    if os.path.exists(old_path):
        shutil.copytree(old_path, new_path)
        shutil.rmtree(old_path, ignore_errors=True)
    elif not os.path.exists(new_path):
        os.makedirs(new_path)
    return new_path


def isXvmInstalled():
    xfw = os.path.exists(os.path.join(modsPath, gameVersion, 'com.modxvm.xfw'))
    xvm = os.path.exists(os.path.join(cwd, 'res_mods', 'mods', 'xfw_packages', 'xvm_main'))
    return xfw and xvm


xvmInstalled = isXvmInstalled()


def getUpdatePath():
    path = os.path.join(getObserverCachePath(), "update")
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def cleanupObserverUpdates():
    root = getUpdatePath()
    for filename in os.listdir(root):
        path = os.path.join(root, filename)
        if os.path.isfile(path):
            os.unlink(path)


def openIgnoredVehicles():
    path = os.path.join(getObserverCachePath(), "crew_ignored.json")
    if not os.path.exists(path):
        writeJsonFile(path, {"vehicles": []})
        return set()
    return set(openJsonFile(path).get("vehicles"))


def updateIgnoredVehicles(vehicles):
    path = os.path.join(getObserverCachePath(), "crew_ignored.json")
    writeJsonFile(path, {"vehicles": sorted(vehicles)})


base_before_override = {}


def overrideMethod(wg_class, method_name="__init__"):
    """
    wg_class: class object
    method_name: Unicode, default __init__
    """
    class_name = wg_class.__name__
    if not hasattr(wg_class, method_name):
        if method_name.startswith("__") and method_name != "__init__":
            full_name = "_{0}{1}".format(class_name, method_name)
            if hasattr(wg_class, full_name):
                method_name = full_name
            elif hasattr(wg_class, method_name[1:]):
                method_name = method_name[1:]

    def outer(new_method):
        full_name_with_class = "{0}.{1}".format(class_name, method_name)
        if full_name_with_class in base_before_override:
            return new_method
        old_method = getattr(wg_class, method_name, None)
        if old_method is not None and callable(old_method):
            base_before_override[full_name_with_class] = old_method
            setattr(wg_class, method_name, lambda *args, **kwargs: new_method(old_method, *args, **kwargs))
            logDebug("overrideMethod: Set override to {}.{} >> {func}", class_name, method_name, func=new_method)
        else:
            logError("overrideMethod: {} has not attr {}, or not callable", class_name, method_name)
        return new_method

    return outer


def cancelOverride(wg_class, method_name):
    class_name = wg_class.__name__
    if method_name.startswith("__"):
        method_name = "_{0}{1}".format(class_name, method_name)
    full_name_with_class = class_name + "." + method_name
    if full_name_with_class in base_before_override:
        setattr(wg_class, method_name, base_before_override.pop(full_name_with_class))
        logDebug("cancelOverrode: override {} removed", full_name_with_class)


def convertDictToNamedtuple(dictionary):
    return namedtuple(dictionary.__name__, dictionary.keys())(**dictionary)


def percentToRGB(percent, saturation=0.5, brightness=1.0, **kwargs):
    """Percent, float number in range 0-2.4 purple, or 1.0 green."""
    # Adjusted for purple and green positions
    position = min(0.8333, percent * 0.3333)
    r, g, b = (int(i * 255) for i in hsv_to_rgb(position, saturation, brightness))
    return "#{:02X}{:02X}{:02X}".format(r, g, b)


def urlResponse(url):
    response = openUrl(url, 10.0)
    response_data = response.getData()
    if response_data is not None:
        return encodeData(json.loads(response_data, encoding=UTF_8))
    return response_data


def parseColorToHex(color, asInt=False):
    color = "0x" + color[1:]
    return int(color, 16) if asInt else color


def getPercent(param_a, param_b):
    if param_b <= 0:
        return 0.0
    return float(normalizeHealth(param_a)) / param_b


def fetchURL(url, callback, timeout=10.0, method='GET', postData=''):
    headers = {"User-Agent": "Battle-Observer-App"}
    th = Thread(target=BigWorld.fetchURL, args=(url, callback, headers, timeout, method, postData), name="fetchURL")
    th.start()
    th.join(timeout + 2)


locale.locale_encoding_alias["cp65001"] = UTF_8


def getEncoding():
    coding = locale.getpreferredencoding()
    if coding in locale.locale_encoding_alias:
        return locale.locale_encoding_alias[coding]
    return coding


ENCODING_LOCALE = getEncoding()
ENCODING_ERRORS = "ignore"

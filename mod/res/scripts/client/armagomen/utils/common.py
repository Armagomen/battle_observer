import json
import locale
import math
import os
from collections import namedtuple
from colorsys import hsv_to_rgb
from functools import partial
from io import open as _open
from shutil import rmtree

import BigWorld
import ResMgr

from BattleReplay import isPlaying, isLoading
from armagomen.battle_observer.settings.default_settings import settings
from external_strings_utils import unicode_from_utf8
from gui.Scaleform.daapi.view.battle.shared.formatters import normalizeHealth
from helpers.http import openUrl
from uilogging.core.core_constants import HTTP_DEFAULT_TIMEOUT

MOD_NAME = "BATTLE_OBSERVER"
DEBUG = "DEBUG_MODE"
CONFIG_DIR = "mod_battle_observer"
UTF_8 = 'utf-8'


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


def distanceToEntityVehicle(entityID):
    entity_vehicle = getEntity(entityID)
    if entity_vehicle is not None:
        return getDistanceTo(entity_vehicle.position)
    return 0.0


def callback(delay, callMethod, *args, **kwargs):
    return BigWorld.callback(delay, partial(callMethod, *args, **kwargs) if args or kwargs else callMethod)


def cancelCallback(callbackID):
    return BigWorld.cancelCallback(callbackID)


def logError(message, *args, **kwargs):
    BigWorld.logError(MOD_NAME, str(message).format(*args, **kwargs), None)


def logInfo(message):
    BigWorld.logInfo(MOD_NAME, str(message), None)


def logDebug(message, *args, **kwargs):
    if settings.main[DEBUG]:
        BigWorld.logDebug(MOD_NAME, str(message).format(*args, **kwargs), None)


def logWarning(message):
    BigWorld.logWarning(MOD_NAME, str(message), None)


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
        os.unlink(link) if os.path.isfile(link) or os.path.islink(link) else rmtree(link, ignore_errors=True)
        logInfo("cleanup updates: {}".format(link))


def removeDirs(path, name=None):
    if os.path.exists(path):
        rmtree(path, ignore_errors=True, onerror=None)
        if name is not None:
            logInfo('CLEANING CACHE: {0}'.format(name))


def clearClientCache(category=None):
    if not settings.main["clear_cache_automatically"]:
        return
    dirs = (
        "account_caches", "battle_results", "clan_cache", "custom_data", "dossier_cache", "messenger_cache",
        "storage_cache", "tutorial_cache", "veh_cmp_cache", "web_cache", "profile"
    )
    if category is None:
        for dirName in dirs:
            removeDirs(os.path.join(preferencesDir, dirName), dirName)
    else:
        removeDirs(os.path.join(preferencesDir, category), category)


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
    path = os.path.join(preferencesDir, "battle_observer")
    if not os.path.exists(path):
        os.makedirs(path)
    return path


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
        filePath = os.path.join(root, filename)
        if os.path.isfile(filePath):
            os.unlink(filePath)


def openIgnoredVehicles():
    path = os.path.join(getObserverCachePath(), "crew_ignored.json")
    if not os.path.exists(path):
        writeJsonFile(path, {"vehicles": []})
        return set()
    return set(openJsonFile(path).get("vehicles"))


def updateIgnoredVehicles(vehicles):
    path = os.path.join(getObserverCachePath(), "crew_ignored.json")
    writeJsonFile(path, {"vehicles": sorted(vehicles)})


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
            logError("overrideMethod error: {} in {} is not callable or undefined in {}", method_name, class_name,
                     new_method.__name__)
        return new_method

    return outer


def convertDictToNamedtuple(dictionary):
    return namedtuple(dictionary.__name__, dictionary.keys())(**dictionary)


COLOR = namedtuple("COLOR", ("PURPLE", "GREEN", "MULTIPLIER", "TEMPLATE"))(0.8333, 0.3333, 255, "#{:02X}{:02X}{:02X}")


def percentToRGB(percent, saturation=0.5, brightness=1.0, **kwargs):
    """Percent is float number in range 0 - 2.4 purple, or 1.0 green."""
    normalized_percent = min(COLOR.PURPLE, percent * COLOR.GREEN)
    tuple_values = hsv_to_rgb(normalized_percent, saturation, brightness)
    # r, g, b = (int(math.ceil(i * COLOR.MULTIPLIER)) for i in tuple_values)
    return COLOR.TEMPLATE.format(*(int(math.ceil(i * COLOR.MULTIPLIER)) for i in tuple_values))


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


def fetchURL(url, callback_function):
    logDebug(url)
    BigWorld.fetchURL(url, callback_function, {"User-Agent": "Battle-Observer-App"}, HTTP_DEFAULT_TIMEOUT, 'GET')


locale.locale_encoding_alias["cp65001"] = UTF_8


def getEncoding():
    coding = locale.getpreferredencoding()
    if coding in locale.locale_encoding_alias:
        return locale.locale_encoding_alias[coding]
    return coding


ENCODING_LOCALE = getEncoding()
ENCODING_ERRORS = "ignore"

MOD_PACKS = ["Ukrainian_Viking_ModPack"]


def isDonateMessageEnabled():
    for mod_pack in MOD_PACKS:
        if os.path.exists(os.path.join(cwd, mod_pack)):
            return False
    return True

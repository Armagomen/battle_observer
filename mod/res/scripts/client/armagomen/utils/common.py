# coding=utf-8
import json
import locale
import os
import shutil
from collections import namedtuple
from colorsys import hsv_to_rgb
from functools import partial
from io import open as _open

import BigWorld
import ResMgr

from armagomen.utils.logging import logDebug, logError, logInfo
from BattleReplay import isLoading, isPlaying
from external_strings_utils import unicode_from_utf8
from gui.Scaleform.daapi.view.battle.shared.formatters import normalizeHealth

CONFIG_DIR = "mod_battle_observer"
MOD_CACHE = "battle_observer"
UTF_8 = "utf-8"

MinMax = namedtuple("MinMax", ("min", "max"))


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


def save():
    BigWorld.savePreferences()
    BigWorld.worldDrawEnabled(False)


def restartGame():
    save()
    try:
        import WGC
        WGC.notifyRestart()
    except ImportError:
        import LGC
        LGC.notifyRestart()
    BigWorld.restartGame()


def closeClient():
    save()
    BigWorld.quit()


def disconnect():
    BigWorld.disconnect()


def openWebBrowser(url):
    BigWorld.wg_openWebBrowser(url)


CWD = os.getcwdu() if os.path.supports_unicode_filenames else os.getcwd()
MODS_PATH = os.path.join(CWD, "mods")


def getGameVersion():
    full_version = ResMgr.openSection('../version.xml').readString('version')
    for name in ResMgr.openSection(MODS_PATH).keys():
        if name in full_version:
            return name
    return full_version.split('#')[0].strip()[2:]


GAME_VERSION = getGameVersion()
CONFIGS_PATH = os.path.join(MODS_PATH, "configs")
if not os.path.exists(CONFIGS_PATH):
    os.makedirs(CONFIGS_PATH)


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


currentConfigPath = setCurrentConfigPath(CONFIGS_PATH)

if currentConfigPath is None:
    currentConfigPath = os.path.join(CONFIGS_PATH, CONFIG_DIR)
    if not os.path.exists(currentConfigPath):
        os.makedirs(currentConfigPath)


def removeDirs(path):
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True, onerror=None)
        return True
    return False


def cleanupUpdates():
    path = os.path.join(CWD, "updates")
    if not os.path.exists(path):
        os.makedirs(path)
        return
    listDir = os.listdir(path)
    if listDir:
        ignored = set()
        section = ResMgr.openSection(os.path.join(CWD, 'game_info.xml'))
        if section['game']['upcoming_patches']:
            ignored.update(val.asString.split("\\")[0] for value in section['game']['upcoming_patches'].values() for val in value.values())
        for name in ignored.symmetric_difference(listDir):
            full_path = os.path.join(path, name)
            os.unlink(full_path) if os.path.isfile(full_path) or os.path.islink(full_path) else removeDirs(full_path)
            logInfo("CLEARING THE UPDATE FOLDER: {}", full_path)


def clearClientCache():
    exclude_cache_dirs = ["game_loading_cache"]
    game_cache_dirs = [x for x in os.listdir(preferencesDir) if "_cache" in x and x not in exclude_cache_dirs]
    for dirName in game_cache_dirs:
        if removeDirs(os.path.join(preferencesDir, dirName)):
            logInfo("CLEANING CLIENT CACHE FOLDER: {}", dirName)


def encodeData(data):
    """encode dict keys/values to utf-8."""
    if isinstance(data, dict):
        return {encodeData(key): encodeData(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [encodeData(element) for element in data]
    elif isinstance(data, (str, unicode)):
        return data.encode(UTF_8)
    else:
        return data


def openJsonFile(path):
    """Gets a dict from JSON."""
    if not os.path.exists(path):
        return {}
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


IS_XVM_INSTALLED = os.path.exists(os.path.join(MODS_PATH, GAME_VERSION, 'com.modxvm.xfw')) and os.path.exists(
    os.path.join(CWD, 'res_mods', 'mods', 'xfw_packages', 'xvm_main'))


def getUpdatePath():
    path = os.path.join(getObserverCachePath(), "update")
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def cleanupObserverUpdates():
    root = getUpdatePath()
    for filename in os.listdir(root):
        if filename == "cleanup.bat":
            continue
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


def find_similar_attr_name(obj, target_name):
    attrs = dir(obj)
    if target_name in attrs:
        return target_name
    for name in attrs:
        if target_name in name:
            logDebug("{} {}", target_name, name)
            return name
    logError("overrideError: method '{}' do not find in '{}'", target_name, str(obj))
    return None


def overrideMethod(wg_class, _method_name="__init__"):
    """
    wg_class: class object
    method_name: Unicode, default __init__
    """
    method_name = find_similar_attr_name(wg_class, _method_name)

    def outer(new_method):
        if method_name is None:
            return new_method
        class_name = getattr(wg_class, '__name__', wg_class.__class__.__name__)
        full_name_with_class = "{0}.{1}*{2}".format(class_name, method_name, new_method.__name__)
        if full_name_with_class in base_before_override:
            logDebug("overrideMethod: {} already added to storage", full_name_with_class)
            return new_method
        old_method = getattr(wg_class, method_name)
        if callable(old_method):
            base_before_override[full_name_with_class] = old_method
            setattr(wg_class, method_name, lambda *args, **kwargs: new_method(old_method, *args, **kwargs))
            logDebug("overrideMethod: Set override to {}.{} >> {func}", class_name, method_name, func=new_method)
        else:
            logError("overrideMethod: {}.{} is not callable", class_name, method_name)
        return new_method

    return outer


def cancelOverride(wg_class, _method_name, replaced_name):
    method_name = find_similar_attr_name(wg_class, _method_name)
    if method_name is not None:
        class_name = getattr(wg_class, '__name__', wg_class.__class__.__name__)
        full_name_with_class = "{0}.{1}*{2}".format(class_name, method_name, replaced_name)
        if full_name_with_class in base_before_override:
            setattr(wg_class, method_name, base_before_override.pop(full_name_with_class))
            logDebug("cancelOverride: override {} removed", full_name_with_class)


def toggleOverride(obj, method_name, func, enable):
    if enable:
        overrideMethod(obj, method_name)(func)
    else:
        cancelOverride(obj, method_name, func.__name__)


def convertDictToNamedtuple(dictionary):
    return namedtuple(dictionary.__name__, dictionary.keys())(**dictionary)


def percentToRGB(percent, saturation=0.5, brightness=1.0, color_blind=False):
    """
    Returns a HEX color code based on percent.
    If color_blind=True, uses a smooth gradient: blue → green (no yellow).
    Args:
        percent (float): Value between 0.0 and 1.0.
        saturation (float): Saturation level (default: 0.5).
        brightness (float): Brightness level (default: 1.0).
        color_blind (bool): Enables color-blind-safe gradient if True.
    Returns:
        str: HEX color string.
    """
    if color_blind:
        # Blue → Green
        hue = 0.666 + (-0.333 * percent)
    else:
        hue = min(0.8333, percent * 0.3333)

    r, g, b = (int(i * 255) for i in hsv_to_rgb(hue, saturation, brightness))
    return "#{:02X}{:02X}{:02X}".format(r, g, b)


def parseColorToHex(color, asInt=False):
    """
    Converts color string to hex string or integer.
    Accepts formats: '#RRGGBB', '0xRRGGBB', 'RRGGBB', even longer strings.
    Compatible with Python 2.7. Falls back to 0xFAFAFA or 16448250 on error.
    """
    hex_part = 16448250
    try:
        hex_part = int(color.replace("#", "").replace("0x", "").upper()[:6], 16)
    except Exception as error:
        logError(error)
    return hex_part if asInt else hex(hex_part)


def getPercent(param_a, param_b):
    if param_b <= 0:
        return 0.0
    return float(normalizeHealth(param_a)) / param_b


def getEncoding():
    custom_locale_encoding_alias = {
        "cp65001": UTF_8,
        "utf8": UTF_8,
        "win1251": "cp1251",
        "euro": "ISO8859-15",
        "latin1": "ISO8859-1",
        "english": "ISO8859-1"
    }
    locale.locale_encoding_alias.update(custom_locale_encoding_alias)
    coding = locale.getpreferredencoding()
    normalized = locale.locale_encoding_alias.get(coding)
    if normalized:
        return normalized
    if "." in coding:
        suffix = coding.split(".")[-1].lower()
        normalized_suffix = locale.locale_encoding_alias.get(suffix)
        if normalized_suffix:
            return normalized_suffix
    return coding


ENCODING_LOCALE = getEncoding()
ENCODING_ERRORS = "ignore"

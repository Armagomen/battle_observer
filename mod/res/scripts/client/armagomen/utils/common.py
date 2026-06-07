# coding=utf-8
import functools
import importlib
import os
from collections import namedtuple
from colorsys import hsv_to_rgb

import BigWorld
import ResMgr
from armagomen import IALogger
from gui.shared.utils.TimeInterval import TimeInterval as _TimeInterval
from helpers import dependency
from skeletons.gui.impl import IGuiLoader

CONFIG_DIR = 'mod_battle_observer'
MOD_CACHE = 'battle_observer'
UTF_8 = 'utf-8'


def joinAndNormalizePath(*args):
    return os.path.abspath(os.path.join(*args))


__mods_dir = next(value for value in ResMgr.openSection('../paths.xml/Paths/').readStrings('Path') if '/mods/' in value)
VERSIONED_MODS_DIR = joinAndNormalizePath(__mods_dir)
MODS_DIR = os.path.dirname(VERSIONED_MODS_DIR)

MinMax = namedtuple('MinMax', ('min', 'max'))

IS_COMMON_TEST = ResMgr.openSection('../game_info.xml/game/').readString('id', '') == 'WOT.CT.PRODUCTION'
IS_XVM_INSTALLED = os.path.exists(joinAndNormalizePath(__mods_dir, 'com.modxvm.xfw')) and os.path.exists(
    joinAndNormalizePath('./res_mods/mods/xfw_packages/xvm_main'))


def addCallback(delay, callMethod, *args, **kwargs):
    return BigWorld.callback(delay, functools.partial(callMethod, *args, **kwargs) if args or kwargs else callMethod)


def cancelCallback(callbackID):
    return BigWorld.cancelCallback(callbackID)


def delayedCall(delay):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return addCallback(delay, func, *args, **kwargs)

        return wrapper

    return decorator


def getPreferencesDir():
    from external_strings_utils import unicode_from_utf8
    preferences_file_path = unicode_from_utf8(BigWorld.wg_getPreferencesFilePath())[1]
    return joinAndNormalizePath(os.path.dirname(preferences_file_path))


preferencesDir = getPreferencesDir()


def save(restart=False):
    BigWorld.savePreferences()
    if restart:
        import WGC
        WGC.notifyRestart()
    BigWorld.worldDrawEnabled(False)


def restartGame():
    save(restart=True)
    addCallback(1.0, BigWorld.restartGame)


def closeClient():
    save()
    addCallback(1.0, BigWorld.quit)


def disconnect():
    addCallback(1.0, BigWorld.disconnect)


def openWebBrowser(url):
    BigWorld.wg_openWebBrowser(url)


def checkCurrentConfigPath(configs_path):
    for dir_name in os.listdir(configs_path):
        full_path = os.path.join(configs_path, dir_name)
        if os.path.isdir(full_path):
            if dir_name == CONFIG_DIR:
                return full_path
            deeper = checkCurrentConfigPath(full_path)
            if deeper is not None:
                return deeper
    return None


def setCurrentConfigPath(configs_path):
    if not os.path.exists(configs_path):
        os.makedirs(configs_path)

    current_path = checkCurrentConfigPath(configs_path) or os.path.join(configs_path, CONFIG_DIR)
    if not os.path.exists(current_path):
        os.makedirs(current_path)

    return current_path


currentConfigPath = setCurrentConfigPath(os.path.join(MODS_DIR, 'configs'))


def cleanupPath(path, safe=False):
    if os.path.isfile(path) or os.path.islink(path):
        try:
            os.unlink(path)
        except Exception:
            pass
    elif os.path.isdir(path):
        if safe:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                cleanupPath(item_path)
        else:
            from shutil import rmtree
            rmtree(path, ignore_errors=True)


def cleanupUpdates():
    updates_path = './updates'
    if not os.path.exists(updates_path):
        os.makedirs(updates_path)
        return
    listDir = os.listdir(updates_path)
    if listDir:
        ignored = set()
        upcoming_patches = '../game_info.xml/game/upcoming_patches/'
        upcoming = ResMgr.openSection(upcoming_patches)
        if upcoming:
            ignored.update(os.path.dirname(val.asString) for value in upcoming.values() for val in value.values())
        for name in ignored.symmetric_difference(listDir):
            full_path = joinAndNormalizePath(updates_path, name)
            cleanupPath(full_path)
            logger = dependency.instance(IALogger)
            logger.logInfo('CLEARING THE UPDATE FOLDER: {}', full_path)
        ResMgr.purge(upcoming_patches, True)


def clearClientCache():
    for dirName in os.listdir(preferencesDir):
        if '_cache' in dirName or dirName == 'profile':
            cleanupPath(os.path.join(preferencesDir, dirName), safe=True)
            logger = dependency.instance(IALogger)
            logger.logInfo('CLEANING CLIENT CACHE FOLDER: {}', dirName)


def encodeData(data):
    """encode dict strings keys/values to utf-8."""
    if isinstance(data, dict):
        return {key.encode(UTF_8): encodeData(value) for key, value in data.iteritems()}
    elif isinstance(data, list):
        return [encodeData(element) for element in data]
    elif isinstance(data, (str, unicode)):
        return data.encode(UTF_8)
    else:
        return data


def openJsonFile(path):
    logger = dependency.instance(IALogger)
    if not os.path.isfile(path):
        message = "JSON file not found: {}".format(path)
        logger.logWarning(message)
        raise IOError(message)
    from io import open
    with open(path, 'r', encoding='utf-8-sig') as f:
        content = f.read()
    if not content.strip():
        message = "JSON decode error in '{}': file is empty".format(path)
        logger.logWarning(message)
        raise IOError(message)
    try:
        import json
        data = json.loads(content)
    except ValueError as e:
        message = "JSON decode error in '{}': {}".format(path, str(e))
        logger.logWarning(message)
        raise ValueError(message)

    return encodeData(data)


def writeJsonFile(path, data):
    """Creates a new JSON file in a folder or replace old."""
    import json
    file_data = unicode(json.dumps(data, skipkeys=True, ensure_ascii=False, indent=2, sort_keys=True))
    if file_data:
        from io import open
        with open(path, 'w', encoding=UTF_8) as dataFile:
            dataFile.write(file_data)


def getObserverCachePath():
    new_path = os.path.join(preferencesDir, 'mods', MOD_CACHE)
    if not os.path.isdir(new_path):
        os.makedirs(new_path)
    return new_path


def getUpdatePath():
    path = os.path.join(getObserverCachePath(), 'update')
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def cleanupObserverUpdates():
    root = getUpdatePath()
    for filename in os.listdir(root):
        path = os.path.join(root, filename)
        try:
            from shutil import rmtree
            rmtree(path) if os.path.isdir(path) else os.unlink(path)
        except OSError as e:
            logger = dependency.instance(IALogger)
            logger.logError('cleanupObserverUpdates: {} — {}', path, str(e))


base_before_override = {}


def find_similar_attr_name(obj, target_name):
    attrs = dir(obj)
    if target_name in attrs:
        return target_name
    logger = dependency.instance(IALogger)
    for name in attrs:
        if target_name in name:
            logger.logDebug('{} {}', target_name, name)
            return name
    logger.logError("overrideError: method '{}' do not find in '{}'", target_name, str(obj))
    return None


def overrideMethod(wg_class, _method_name='__init__'):
    """
    wg_class: class object
    method_name: Unicode, default __init__
    """
    method_name = find_similar_attr_name(wg_class, _method_name)

    def outer(new_method):
        if method_name is None:
            return new_method
        logger = dependency.instance(IALogger)
        class_name = getattr(wg_class, '__name__', wg_class.__class__.__name__)
        full_name_with_class = "{0}.{1}*{2}".format(class_name, method_name, new_method.__name__)
        if full_name_with_class in base_before_override:
            logger.logDebug('overrideMethod: {} already added to storage', full_name_with_class)
            return new_method
        old_method = getattr(wg_class, method_name)
        if callable(old_method):
            base_before_override[full_name_with_class] = old_method
            setattr(wg_class, method_name, lambda *args, **kwargs: new_method(old_method, *args, **kwargs))
            logger.logDebug('overrideMethod: Set override to {}.{} >> {func}', class_name, method_name, func=new_method)
        else:
            logger.logError('overrideMethod: {}.{} is not callable', class_name, method_name)
        return new_method

    return outer


def cancelOverride(wg_class, _method_name, replaced_name):
    method_name = find_similar_attr_name(wg_class, _method_name)
    if method_name is not None:
        class_name = getattr(wg_class, '__name__', wg_class.__class__.__name__)
        full_name_with_class = '{0}.{1}*{2}'.format(class_name, method_name, replaced_name)
        if full_name_with_class in base_before_override:
            setattr(wg_class, method_name, base_before_override.pop(full_name_with_class))
            logger = dependency.instance(IALogger)
            logger.logDebug('cancelOverride: override {} removed', full_name_with_class)


def toggleOverride(obj, method_name, func, enable):
    if enable:
        overrideMethod(obj, method_name)(func)
    else:
        cancelOverride(obj, method_name, func.__name__)


def percentToColor(percent, saturation=0.5, brightness=1.0, color_blind=False, as_int=False):
    """
    Returns a HEX color code based on percent.
    If color_blind=True, uses a smooth gradient: blue → green (no yellow).
    Args:
        percent (float): Value between 0.0 and 1.0.
        saturation (float): Saturation level (default: 0.5).
        brightness (float): Brightness level (default: 1.0).
        color_blind (bool): Enables color-blind-safe gradient if True.
        as_int (bool): If True, returns int (0xRRGGBB), else HEX string.
    """
    if color_blind:
        # Blue → Green
        hue = 0.666 + (-0.333 * percent)
    else:
        hue = min(0.8333, percent * 0.3333)

    r, g, b = (int(i * 255) for i in hsv_to_rgb(hue, saturation, brightness))
    if as_int:
        return (r << 16) | (g << 8) | b
    else:
        return '#{:02X}{:02X}{:02X}'.format(r, g, b)


def hexToInt(color):
    """
    Converts color string to integer.
    Accepts formats: '#RRGGBB', '0xRRGGBB', 'RRGGBB'.
    Compatible with Python 2.7. Falls back to 16448250 on error.
    """
    hex_part = color.lstrip("#").lstrip("0x").upper()
    if len(hex_part) == 6:
        return int(hex_part, 16)
    logger = dependency.instance(IALogger)
    logger.logError("hexToInt: color code is corrupted >> {} <<, should be #RRGGBB or 0xRRGGBB or RRGGBB".format(color))
    return 16448250


def colorToHex(color):
    """
    Converts color string to hex string.
    Accepts formats: '#RRGGBB', '0xRRGGBB', 'RRGGBB', even longer strings.
    Compatible with Python 2.7. Falls back to 0xFAFAFAon error.
    """
    if color.startswith('0x') and len(color) == 8:
        return color
    hex_part = 16448250
    try:
        hex_part = int(color.replace('#', '').replace('0x', '').upper()[:6], 16)
    except Exception as error:
        logger = dependency.instance(IALogger)
        logger.logError(error)
    return hex(hex_part)


def getPercent(param_a, param_b):
    if param_b <= 0 or param_a <= 0:
        return 0.0
    return float(max(0.0, param_a)) / param_b


def getEncoding():
    # type: () -> str
    custom_locale_encoding_alias = {
        'cp65001': UTF_8,
        'utf8': UTF_8,
        'win1251': 'cp1251',
        'euro': 'ISO8859-15',
        'latin1': 'ISO8859-1',
        'english': 'ISO8859-1'
    }
    import locale
    locale.locale_encoding_alias.update(custom_locale_encoding_alias)
    coding = locale.getpreferredencoding()
    normalized = locale.locale_encoding_alias.get(coding)
    if normalized:
        return normalized
    if '.' in coding:
        suffix = coding.split('.')[-1].lower()
        normalized_suffix = locale.locale_encoding_alias.get(suffix)
        if normalized_suffix:
            return normalized_suffix
    return coding


ENCODING_LOCALE = getEncoding()
ENCODING_ERRORS = 'ignore'


def safe_import(iterPatches, noneResults=False):
    result = []
    logger = dependency.instance(IALogger)
    for path, name in iterPatches:
        try:
            module = importlib.import_module(path)
        except ImportError as e:
            logger.logDebug('Import error: {}', str(e))
        else:
            cls = getattr(module, name, None)
            if cls is not None:
                result.append(cls)
                continue
            else:
                logger.logError('Import error: {} has no attribute {}', str(module), name)
        if noneResults:
            result.append(None)

    return tuple(result)


SIXTH_SENSE_PATH = 'gui/maps/icons/battle_observer/sixth_sense/'
SIXTH_SENSE_LIST = sorted(encodeData(ResMgr.openSection(SIXTH_SENSE_PATH).keys()))


def safe_index(seq, value, default=0):
    return next((i for i, x in enumerate(seq) if x == value), default)


def printDebuginfo():
    logger = dependency.instance(IALogger)
    logger.logDebug("VERSIONED_MODS_DIR: {}", VERSIONED_MODS_DIR)
    logger.logDebug("IS_XVM_INSTALLED: {}", IS_XVM_INSTALLED)
    logger.logDebug("currentConfigPath: {}", currentConfigPath)
    logger.logDebug("SIXTH_SENSE_LIST: {}", SIXTH_SENSE_LIST)
    logger.logDebug("ENCODING_LOCALE: {}", ENCODING_LOCALE)
    logger.logDebug("IS_COMMON_TEST: {}", IS_COMMON_TEST)


def get_parent_window():
    """
    Gets the main window of the application.
    """
    ui_loader = dependency.instance(IGuiLoader)
    if ui_loader and ui_loader.windowsManager:
        return ui_loader.windowsManager.getMainWindow()
    return None


class TimeInterval(_TimeInterval):

    @property
    def interval(self):
        return self.__interval

    @interval.setter
    def interval(self, value):
        self.__interval = value
        self.restart()


flags = ('isOnlyForFunRandomBattles', 'isOnlyForBattleRoyaleBattles', 'isOnlyForMapsTrainingBattles',
         'isOnlyForClanWarsBattles', 'isOnlyForComp7Battles', 'isOnlyForEventBattles', 'isOnlyForEpicBattles')


def isSpecialBattleVehicle(vehicle):
    return any(getattr(vehicle, f, False) for f in flags)

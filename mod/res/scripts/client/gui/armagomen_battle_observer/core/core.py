import os
from shutil import rmtree
from string import printable

import ResMgr

from gui.Scaleform.battle_entry import BattleEntry
from gui.Scaleform.daapi.settings import config
from gui.Scaleform.lobby_entry import LobbyEntry
from .bo_constants import FILE_NAME, MASSAGES, MAIN, CACHE_DIRS, GLOBAL, SWF, MOD_VERSION
from .bw_utils import getPreferencesFilePath, logInfo, logError


class ObserverCore(object):
    __slots__ = ("modsDir", "gameVersion", "workingDir", "fileName")

    def __init__(self):
        self.modsDir, self.gameVersion = self.getCurrentModPath()
        self.workingDir = os.path.join(self.modsDir, self.gameVersion)
        self.fileName = FILE_NAME.format(MOD_VERSION)

    def addLibraries(self):
        get_librariesBattle = BattleEntry._getRequiredLibraries
        get_librariesLobby = LobbyEntry._getRequiredLibraries
        BattleEntry._getRequiredLibraries = lambda b_self: self.add_libs(get_librariesBattle, b_self)
        LobbyEntry._getRequiredLibraries = lambda b_self: self.add_libs(get_librariesLobby, b_self)
        config.BATTLE_PACKAGES += ("gui.armagomen_battle_observer.battle",)
        config.LOBBY_PACKAGES += ("gui.armagomen_battle_observer.lobby",)

    @staticmethod
    def add_libs(baseMethod, entry):
        libs = baseMethod(entry)
        isTuple = isinstance(libs, tuple)
        if isTuple:
            libs = list(libs)
        if isinstance(entry, LobbyEntry) and SWF.LOBBY not in libs:
            libs.append(SWF.LOBBY)
        elif isinstance(entry, BattleEntry) and SWF.BATTLE not in libs:
            libs.append(SWF.BATTLE)
        return libs if not isTuple else tuple(libs)

    @staticmethod
    def checkDecoder(_string):
        for char in _string:
            if char not in printable:
                import locale
                return locale.getpreferredencoding()
        return None

    def mod_version(self):
        return 'v{0} - {1}'.format(MOD_VERSION, self.gameVersion)

    def clearClientCache(self, category=None):
        path = os.path.normpath(unicode(getPreferencesFilePath(), 'utf-8', errors='ignore'))
        path = os.path.split(path)[GLOBAL.FIRST]
        if category is None:
            for dirName in CACHE_DIRS:
                self.removeDirs(os.path.join(path, dirName), dirName)
        else:
            self.removeDirs(os.path.join(path, category), category)

    @staticmethod
    def removeDirs(normpath, dirName):
        if os.path.exists(normpath):
            rmtree(normpath, ignore_errors=True, onerror=None)
            logInfo('CLEANING CACHE: {0}'.format(dirName))

    @staticmethod
    def getCurrentModPath():
        p = os.path
        cwd = os.getcwdu() if p.supports_unicode_filenames else os.getcwd()
        if any(x in cwd for x in ("win32", "win64")):
            cwd = p.split(cwd)[GLOBAL.FIRST]
        for sec in ResMgr.openSection(p.join(cwd, 'paths.xml'))['Paths'].values():
            if './mods/' in sec.asString:
                return p.split(p.realpath(p.join(cwd, p.normpath(sec.asString))))

    def modMessage(self, title):
        logInfo('MOD {}: {}'.format(title, self.mod_version()))

    def fini(self):
        from config import cfg
        from battle_cache import cache
        if cfg.main[MAIN.AUTO_CLEAR_CACHE]:
            self.clearClientCache()
        if cache.errorKeysSet and GLOBAL.DEBUG_MODE:
            for key in sorted(cache.errorKeysSet):
                logError(key)
        self.modMessage(MASSAGES.FINISH)


m_core = ObserverCore()


class SafeDict(dict):
    def __missing__(self, key):
        return '%({macro})s'.format(macro=key)


def overrideMethod(cls, methodName="__init__"):
    """
    :type cls: class object
    :type methodName: unicode
    """
    if methodName != "__init__" and methodName.startswith("__") and not methodName.endswith("__"):
        check_name = methodName[1:]
        if hasattr(cls, check_name):
            methodName = check_name
        else:
            for name in dir(cls):
                if methodName in name:
                    methodName = name
                    break

    def outer(new_method):
        old_method = getattr(cls, methodName, None)
        if old_method is not None and callable(old_method):
            def override(*args, **kwargs):
                return new_method(old_method, *args, **kwargs)

            setattr(cls, methodName, override)
        else:
            logError("{0} in {1} is not callable or undefined".format(methodName, cls.__name__))
        return new_method
    return outer


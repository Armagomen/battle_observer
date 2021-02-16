import os
from shutil import rmtree
from string import printable

import ResMgr

from .bo_constants import FILE_NAME, MASSAGES, MAIN, CACHE_DIRS, GLOBAL, MOD_VERSION
from .bw_utils import getPreferencesFilePath, logInfo, logError


class ObserverCore(object):
    __slots__ = ("modsDir", "gameVersion", "workingDir", "fileName")

    def __init__(self):
        self.modsDir, self.gameVersion = self.getCurrentModPath()
        self.workingDir = os.path.join(self.modsDir, self.gameVersion)
        self.fileName = FILE_NAME.format(MOD_VERSION)

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


def overrideMethod(wg_class, method_name="__init__"):
    """
    :type wg_class: class object
    :type method_name: unicode default __init__
    """
    class_name = wg_class.__name__
    if not hasattr(wg_class, method_name):
        if method_name.startswith("__") and not method_name.endswith("__"):
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

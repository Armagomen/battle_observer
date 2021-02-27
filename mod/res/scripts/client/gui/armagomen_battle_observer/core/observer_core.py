import os
from shutil import rmtree
from string import printable

from constants import AUTH_REALM
from gui.shared.personality import ServicesLocator
from skeletons.gui.app_loader import GuiGlobalSpaceID
from .bo_constants import FILE_NAME, MOD_VERSION, MASSAGES, GLOBAL, CACHE_DIRS, MAIN, MOD_NAME
from .utils.bw_utils import logInfo, logError, getPreferencesFilePath, getCurrentModPath


class ObserverCore(object):
    __slots__ = ("modsDir", "gameVersion", "workingDir", "fileName", "isFileValid", "isLoading", "mod_version")

    def __init__(self):
        self.modsDir, self.gameVersion = getCurrentModPath()
        self.workingDir = os.path.join(self.modsDir, self.gameVersion)
        self.fileName = FILE_NAME.format(MOD_VERSION)
        self.isFileValid = self.isModValidFileName()
        self.isLoading = AUTH_REALM != MASSAGES.NA and self.isFileValid
        self.mod_version = 'v{0} - {1}'.format(MOD_VERSION, self.gameVersion)

    @staticmethod
    def checkDecoder(_string):
        for char in _string:
            if char not in printable:
                import locale
                return locale.getpreferredencoding()
        return None

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

    def onExit(self):
        if self.isLoading:
            from .config import cfg
            from .battle import cache
            if cfg.main[MAIN.AUTO_CLEAR_CACHE]:
                self.clearClientCache()
            if cache.errorKeysSet and GLOBAL.DEBUG_MODE:
                for key in sorted(cache.errorKeysSet):
                    logError(key)
            logInfo('MOD {}: {}'.format(MASSAGES.FINISH, self.mod_version))

    def isModValidFileName(self):
        return self.fileName in os.listdir(self.workingDir)

    def start(self):
        if self.isLoading:
            logInfo('MOD {}: {}'.format(MASSAGES.START, self.mod_version))
            from .config import c_Loader
            c_Loader.start()
            from .utils import m_Loader
            m_Loader.start()
        else:
            from .utils.bw_utils import logWarning
            from gui.Scaleform.daapi.view import dialogs
            from gui import DialogsInterface
            from .update.dialog_button import DialogButtons
            locked = MASSAGES.LOCKED if self.isFileValid else MASSAGES.LOCKED_BY_FILE_NAME.format(self.fileName)
            logWarning(locked)

            def loadBlocked(spaceID):
                if spaceID in (GuiGlobalSpaceID.LOGIN, GuiGlobalSpaceID.LOBBY):
                    title = '{} is locked'.format(MOD_NAME)
                    btn = DialogButtons('Close')
                    DialogsInterface.showDialog(dialogs.SimpleDialogMeta(title, locked, btn), lambda proceed: None)
                    ServicesLocator.appLoader.onGUISpaceEntered -= loadBlocked

            ServicesLocator.appLoader.onGUISpaceEntered += loadBlocked

import os
from shutil import rmtree

from armagomen.battle_observer.components import ComponentsLoader
from armagomen.battle_observer.core.bo_constants import FILE_NAME, MOD_VERSION, MASSAGES, GLOBAL, CACHE_DIRS, MAIN, \
    MOD_NAME
from armagomen.battle_observer.core.update.dialog_button import DialogButtons
from armagomen.battle_observer.core.update.worker import UpdateMain
from armagomen.utils.common import logInfo, getPreferencesFilePath, getCurrentModPath, logWarning, overrideMethod
from gui.Scaleform.daapi.settings import config as packages
from gui.Scaleform.daapi.view.lobby.header.LobbyHeader import LobbyHeader
from gui.shared.personality import ServicesLocator
from skeletons.gui.app_loader import GuiGlobalSpaceID


class ObserverCore(object):
    __slots__ = ("modsDir", "gameVersion", "workingDir", "fileName", "isFileValid", "mod_version",
                 "settings", "configLoader", "moduleLoader", "update")

    def __init__(self, configLoader):
        self.settings = configLoader.settings
        self.configLoader = configLoader
        self.modsDir, self.gameVersion = getCurrentModPath()
        self.workingDir = os.path.join(self.modsDir, self.gameVersion)
        self.fileName = FILE_NAME.format(MOD_VERSION)
        self.isFileValid = self.isModValidFileName()
        self.mod_version = 'v{0} - {1}'.format(MOD_VERSION, self.gameVersion)
        self.update = UpdateMain()
        self.update.subscribe()
        overrideMethod(LobbyHeader, "as_updateOnlineCounterS")(self.as_updateOnlineCounterS)
        overrideMethod(LobbyHeader, "as_setServerS")(self.as_setServerS)

    def as_setServerS(self, base, header, serverShortName, const, type):
        if self.settings.main[MAIN.HIDE_SERVER_IN_HANGAR]:
            return base(header, GLOBAL.EMPTY_LINE, GLOBAL.EMPTY_LINE, type)
        return base(header, serverShortName, const, type)

    def as_updateOnlineCounterS(self, base, header, clusterStats, regionStats, tooltip, isAvailable):
        if self.settings.main[MAIN.HIDE_SERVER_IN_HANGAR]:
            return base(header, "ONLINE", regionStats, GLOBAL.EMPTY_LINE, isAvailable)
        return base(header, clusterStats, regionStats, tooltip, isAvailable)

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
        if self.isFileValid:
            if self.settings.main[MAIN.AUTO_CLEAR_CACHE]:
                self.clearClientCache()
            logInfo('MOD {}: {}'.format(MASSAGES.FINISH, self.mod_version))

    def isModValidFileName(self):
        return self.fileName in os.listdir(self.workingDir)

    def start(self):
        if self.isFileValid:
            ServicesLocator.appLoader.onGUISpaceEntered += self.configLoader.loadHangarSettings
            logInfo('MOD {}: {}'.format(MASSAGES.START, self.mod_version))
            ComponentsLoader().start()
            self.configLoader.start()
            packages.BATTLE_PACKAGES += ("armagomen.battle_observer.battle",)
            packages.LOBBY_PACKAGES += ("armagomen.battle_observer.lobby",)
        else:
            from gui.Scaleform.daapi.view import dialogs
            from gui import DialogsInterface
            locked = MASSAGES.LOCKED_BY_FILE_NAME.format(self.fileName)
            logWarning(locked)

            def loadBlocked(spaceID):
                if spaceID in (GuiGlobalSpaceID.LOGIN, GuiGlobalSpaceID.LOBBY):
                    title = '{} is locked'.format(MOD_NAME)
                    btn = DialogButtons('Close')
                    DialogsInterface.showDialog(dialogs.SimpleDialogMeta(title, locked, btn), lambda proceed: None)
                    ServicesLocator.appLoader.onGUISpaceEntered -= loadBlocked

            ServicesLocator.appLoader.onGUISpaceEntered += loadBlocked

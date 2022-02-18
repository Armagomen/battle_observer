import os
import sys

from armagomen.battle_observer import __version__
from armagomen.battle_observer.core.battle.settings import BATTLES_RANGE
from armagomen.battle_observer.core.update.worker import UpdateMain
from armagomen.constants import FILE_NAME, MESSAGES, MAIN, getRandomLogo
from armagomen.utils.common import logInfo, getCurrentModPath, logWarning, clearClientCache, cleanupUpdates
from async import async, await
from gui.Scaleform.daapi.settings import config as packages
from gui.impl.dialogs import dialogs
from gui.impl.dialogs.builders import WarningDialogBuilder
from gui.impl.pub.dialog_window import DialogButtons
from gui.shared.personality import ServicesLocator
from skeletons.gui.app_loader import GuiGlobalSpaceID


class ObserverCore(object):
    __slots__ = ("modsDir", "gameVersion", "isFileValid", "mod_version", "configLoader", "moduleLoader",
                 "componentsLoader")

    def __init__(self):
        self.modsDir, self.gameVersion = getCurrentModPath()
        self.isFileValid = self.isModValidFileName()
        self.mod_version = 'v{0} - {1}'.format(__version__, self.gameVersion)
        ServicesLocator.appLoader.onGUISpaceEntered += self.onGUISpaceEntered

    def onExit(self, settings):
        if not self.isFileValid:
            return
        if settings.main[MAIN.AUTO_CLEAR_CACHE]:
            clearClientCache()
        cleanupUpdates()
        ServicesLocator.appLoader.onGUISpaceEntered -= self.onGUISpaceEntered
        logInfo('MOD {0}: {1}'.format(MESSAGES.FINISH, self.mod_version))

    def isModValidFileName(self):
        return FILE_NAME.format(__version__) in os.listdir(os.path.join(self.modsDir, self.gameVersion))

    def start(self):
        update = UpdateMain()
        update.subscribe()
        logInfo("Launched at python " + sys.version)
        logInfo('MOD {0}: {1}'.format(MESSAGES.START, self.mod_version))
        BATTLE_PACKAGES = packages.BATTLE_PACKAGES_BY_ARENA_TYPE
        for guiType in BATTLE_PACKAGES:
            if guiType in BATTLES_RANGE:
                BATTLE_PACKAGES[guiType] += ("armagomen.battle_observer.battle",)
        packages.BATTLE_PACKAGES_BY_DEFAULT += ("armagomen.battle_observer.battle",)
        packages.LOBBY_PACKAGES += ("armagomen.battle_observer.lobby",)

    def onGUISpaceEntered(self, spaceID):
        if self.isFileValid or spaceID not in (GuiGlobalSpaceID.LOGIN, GuiGlobalSpaceID.LOBBY):
            return
        self.showLockedDialog()

    @staticmethod
    def getLockedDialog(title, message):
        builder = WarningDialogBuilder()
        builder.setFormattedTitle(title)
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.CANCEL, "Close", True, rawLabel="Close")
        return builder.build()

    @async
    def showLockedDialog(self):
        locked = MESSAGES.LOCKED_BY_FILE_NAME.format(FILE_NAME.format(__version__))
        logWarning(locked)
        yield await(dialogs.showSimple(self.getLockedDialog(getRandomLogo(), locked), DialogButtons.CANCEL))

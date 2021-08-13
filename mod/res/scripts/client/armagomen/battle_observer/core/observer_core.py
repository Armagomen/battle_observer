import os
import sys

from armagomen.battle_observer import __version__
from armagomen.battle_observer.components import ComponentsLoader
from armagomen.battle_observer.core.battle.settings import BATTLES_RANGE
from armagomen.battle_observer.core.update.dialog_button import DialogButtons
from armagomen.battle_observer.core.update.worker import UpdateMain
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import FILE_NAME, MESSAGES, MAIN, MOD_NAME
from armagomen.utils.common import logInfo, getCurrentModPath, logWarning, setMaxFrameRate, clearClientCache
from gui.Scaleform.daapi.settings import config as packages
from gui.shared.personality import ServicesLocator
from skeletons.gui.app_loader import GuiGlobalSpaceID


class ObserverCore(object):
    __slots__ = ("modsDir", "gameVersion", "isFileValid", "mod_version", "configLoader", "moduleLoader",
                 "componentsLoader")

    def __init__(self, configLoader):
        self.configLoader = configLoader
        self.modsDir, self.gameVersion = getCurrentModPath()
        self.isFileValid = self.isModValidFileName()
        self.mod_version = 'v{0} - {1}'.format(__version__, self.gameVersion)
        self.componentsLoader = ComponentsLoader()
        ServicesLocator.appLoader.onGUISpaceEntered += self.onGUISpaceEntered
        settings.onModSettingsChanged += self.onModSettingsChanged

    @staticmethod
    def onModSettingsChanged(config, blockID):
        if blockID == MAIN.NAME and config[MAIN.ENABLE_FPS_LIMITER]:
            setMaxFrameRate(config[MAIN.MAX_FRAME_RATE])

    def onExit(self):
        if not self.isFileValid:
            return
        if settings.main[MAIN.AUTO_CLEAR_CACHE]:
            clearClientCache()
        logInfo('MOD {0}: {1}'.format(MESSAGES.FINISH, self.mod_version))

    def isModValidFileName(self):
        return FILE_NAME.format(__version__) in os.listdir(os.path.join(self.modsDir, self.gameVersion))

    def start(self):
        update = UpdateMain()
        update.subscribe()
        if not self.isFileValid:
            return
        logInfo("Launched at python " + sys.version)
        logInfo('MOD {0}: {1}'.format(MESSAGES.START, self.mod_version))
        self.componentsLoader.start()
        self.configLoader.start()
        BATTLE_PACKAGES = packages.BATTLE_PACKAGES_BY_ARENA_TYPE
        for guiType in BATTLE_PACKAGES:
            if guiType in BATTLES_RANGE:
                BATTLE_PACKAGES[guiType] += ("armagomen.battle_observer.battle",)
        packages.BATTLE_PACKAGES_BY_DEFAULT += ("armagomen.battle_observer.battle",)
        packages.LOBBY_PACKAGES += ("armagomen.battle_observer.lobby",)

    def onGUISpaceEntered(self, spaceID):
        if self.isFileValid or spaceID not in (GuiGlobalSpaceID.LOGIN, GuiGlobalSpaceID.LOBBY):
            return
        from gui.Scaleform.daapi.view import dialogs
        from gui import DialogsInterface
        locked = MESSAGES.LOCKED_BY_FILE_NAME.format(FILE_NAME.format(__version__))
        logWarning(locked)
        title = '{0} is locked'.format(MOD_NAME)
        btn = DialogButtons('Close')
        DialogsInterface.showDialog(dialogs.SimpleDialogMeta(title, locked, btn), lambda proceed: None)

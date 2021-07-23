import os

from armagomen.battle_observer import __version__
from armagomen.battle_observer.components import ComponentsLoader
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
                 "componentsLoader", "limiterEnabled")

    def __init__(self, configLoader):
        self.configLoader = configLoader
        self.modsDir, self.gameVersion = getCurrentModPath()
        self.isFileValid = self.isModValidFileName()
        self.mod_version = 'v{0} - {1}'.format(__version__, self.gameVersion)
        self.componentsLoader = ComponentsLoader()
        self.limiterEnabled = settings.main[MAIN.ENABLE_FPS_LIMITER]
        ServicesLocator.appLoader.onGUISpaceEntered += self.onGUISpaceEntered

    def onExit(self):
        if self.isFileValid:
            if settings.main[MAIN.AUTO_CLEAR_CACHE]:
                clearClientCache()
            logInfo('MOD {0}: {1}'.format(MESSAGES.FINISH, self.mod_version))

    def isModValidFileName(self):
        return FILE_NAME.format(__version__) in os.listdir(os.path.join(self.modsDir, self.gameVersion))

    def start(self):
        update = UpdateMain()
        update.subscribe()
        if self.isFileValid:
            logInfo('MOD {0}: {1}'.format(MESSAGES.START, self.mod_version))
            self.componentsLoader.start()
            self.configLoader.start()
            packages.BATTLE_PACKAGES += ("armagomen.battle_observer.battle",)
            packages.LOBBY_PACKAGES += ("armagomen.battle_observer.lobby",)

    def onGUISpaceEntered(self, spaceID):
        if not self.isFileValid and spaceID in (GuiGlobalSpaceID.LOGIN, GuiGlobalSpaceID.LOBBY):
            from gui.Scaleform.daapi.view import dialogs
            from gui import DialogsInterface
            locked = MESSAGES.LOCKED_BY_FILE_NAME.format(FILE_NAME.format(__version__))
            logWarning(locked)
            title = '{0} is locked'.format(MOD_NAME)
            btn = DialogButtons('Close')
            DialogsInterface.showDialog(dialogs.SimpleDialogMeta(title, locked, btn), lambda proceed: None)

        if spaceID in (GuiGlobalSpaceID.LOBBY, GuiGlobalSpaceID.BATTLE):
            if settings.main[MAIN.ENABLE_FPS_LIMITER] != self.limiterEnabled:
                self.limiterEnabled = settings.main[MAIN.ENABLE_FPS_LIMITER]
                setMaxFrameRate(settings[MAIN.MAX_FRAME_RATE] if self.limiterEnabled else 300)

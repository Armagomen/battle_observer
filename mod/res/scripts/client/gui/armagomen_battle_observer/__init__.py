__author__ = "Armagomen"
__copyright__ = "Copyright 2014-2021, Armagomen"
__credits__ = ["Armagomen"]
__license__ = "CC BY-NC-SA 4.0"
__maintainer__ = "Armagomen"
__email__ = "armagomen@gmail.com"
__status__ = "Production"
__http__ = "localhost"
__all__ = ['init', 'fini']

from os import listdir

from constants import AUTH_REALM
from gui.shared.personality import ServicesLocator
from skeletons.gui.app_loader import GuiGlobalSpaceID
from .core.bo_constants import MASSAGES, MOD_NAME, GLOBAL
from .core.core import m_core, overrideMethod
from .core.events import g_events


class BattleObserver(object):
    __slots__ = ("isFileValid", "isLoading")

    def __init__(self):
        self.isFileValid = self.isModValidFileName()
        self.isLoading = AUTH_REALM != MASSAGES.NA and self.isFileValid
        if self.isLoading:
            self.enableHooks()

    @staticmethod
    def isModValidFileName():
        return m_core.fileName in listdir(m_core.workingDir)

    @staticmethod
    def enableHooks():
        from Avatar import PlayerAvatar

        @overrideMethod(PlayerAvatar, "showTracer")
        def showTracer(base, avatar, shooterID, *args):
            if shooterID == avatar.playerVehicleID:
                g_events.onPlayerShooting(avatar)
            return base(avatar, shooterID, *args)

        @overrideMethod(PlayerAvatar, "getOwnVehicleShotDispersionAngle")
        def getOwnVehicleShotDispersionAngle(base, *args, **kwargs):
            dispersion_angle = base(*args, **kwargs)
            g_events.onDispersionAngleUpdate(dispersion_angle[GLOBAL.FIRST])
            return dispersion_angle

    def start(self):
        if self.isLoading:
            m_core.modMessage(MASSAGES.START)
            from .core.config import c_Loader
            from .core.loader import m_Loader
            m_Loader.start()
            c_Loader.start()
        else:
            from .core.bw_utils import logWarning
            from gui.Scaleform.daapi.view import dialogs
            from gui import DialogsInterface
            from .core.dialog_button import DialogButtons
            locked = MASSAGES.LOCKED if self.isFileValid else MASSAGES.LOCKED_BY_FILE_NAME.format(m_core.fileName)
            logWarning(locked)

            def loadBlocked(spaceID):
                if spaceID in (GuiGlobalSpaceID.LOGIN, GuiGlobalSpaceID.LOBBY):
                    title = '{} is locked'.format(MOD_NAME)
                    btn = DialogButtons('Close')
                    DialogsInterface.showDialog(dialogs.SimpleDialogMeta(title, locked, btn), lambda proceed: None)
                    ServicesLocator.appLoader.onGUISpaceEntered -= loadBlocked

            ServicesLocator.appLoader.onGUISpaceEntered += loadBlocked

    def onExit(self):
        if self.isLoading:
            m_core.fini()


mod_battleObserver = BattleObserver()


def init():
    mod_battleObserver.start()


def fini():
    mod_battleObserver.onExit()

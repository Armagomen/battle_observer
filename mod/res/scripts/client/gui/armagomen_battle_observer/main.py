from os import listdir

from constants import AUTH_REALM
from gui.Scaleform.daapi.view.battle.classic.stats_exchange import ClassicStatisticsDataController
from gui.Scaleform.daapi.view.battle.epic.stats_exchange import EpicStatisticsDataController
from gui.Scaleform.daapi.view.battle.epic_random.stats_exchange import EpicRandomStatisticsDataController
from gui.Scaleform.daapi.view.battle.ranked.stats_exchange import RankedStatisticsDataController
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
        from .core.inject_flash import g_flash
        g_flash.inject()

        from Vehicle import Vehicle
        from Avatar import PlayerAvatar
        from gui.Scaleform.daapi.view.battle.shared.minimap.plugins import ArenaVehiclesPlugin

        @overrideMethod(Vehicle, "onHealthChanged")
        def healthChanged(base, *args, **kwargs):
            g_events.onHealthChanged(*args, **kwargs)
            return base(*args, **kwargs)

        @overrideMethod(EpicRandomStatisticsDataController, "as_updateVehicleStatusS")
        @overrideMethod(EpicStatisticsDataController, "as_updateVehicleStatusS")
        @overrideMethod(RankedStatisticsDataController, "as_updateVehicleStatusS")
        @overrideMethod(ClassicStatisticsDataController, "as_updateVehicleStatusS")
        def updateVehicleStatusS(base, *args, **kwargs):
            g_events.updateStatus(*args, **kwargs)
            return base(*args, **kwargs)

        @overrideMethod(PlayerAvatar, "showTracer")
        def showTracer(base, avatar, shooterID, *args):
            if shooterID == avatar.playerVehicleID:
                g_events.onPlayerShooting(avatar)
            return base(avatar, shooterID, *args)

        @overrideMethod(ArenaVehiclesPlugin, "__setInAoI")
        def setInAoI(base, *args, **kwargs):
            g_events.setInAoI(*args)
            return base(*args, **kwargs)

        def tryLoadHangarSettings(spaceID):
            if spaceID == GuiGlobalSpaceID.LOGIN:
                ServicesLocator.appLoader.onGUISpaceEntered -= tryLoadHangarSettings
                from .hangar import config_interface_loader
                config_interface_loader.check()

        @overrideMethod(PlayerAvatar, "getOwnVehicleShotDispersionAngle")
        def getOwnVehicleShotDispersionAngle(base, *args, **kwargs):
            dispersion_angle = base(*args, **kwargs)
            g_events.onDispersionAngleUpdate(dispersion_angle[GLOBAL.FIRST])
            return dispersion_angle

        ServicesLocator.appLoader.onGUISpaceEntered += tryLoadHangarSettings

    def start(self):
        if self.isLoading:
            m_core.modMessage(MASSAGES.START)
            from .core.update import g_update
            g_update.subscribe()
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

    def fini(self):
        if self.isLoading:
            m_core.fini()


mod_battleObserver = BattleObserver()

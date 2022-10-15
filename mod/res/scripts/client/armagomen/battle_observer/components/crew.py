from CurrentVehicle import g_currentVehicle
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.battle_observer.settings.hangar.i18n import localization
from armagomen.constants import MAIN, CREW_XP, getLogo
from armagomen.utils.common import logInfo, overrideMethod, logError, ignored_vehicles
from armagomen.utils.dialogs import CrewDialog
from armagomen.utils.events import g_events
from frameworks.wulf import WindowLayer
from gui import SystemMessages
from gui.Scaleform.daapi.view.lobby.exchange.ExchangeXPWindow import ExchangeXPWindow
from gui.shared.gui_items.processors.tankman import TankmanReturn
from gui.shared.gui_items.processors.vehicle import VehicleTmenXPAccelerator
from gui.shared.utils import decorators
from gui.veh_post_progression.models.progression import PostProgressionCompletion
from helpers import dependency
from skeletons.gui.app_loader import IAppLoader
from skeletons.gui.shared import IItemsCache
from wg_async import wg_async, wg_await


class CrewProcessor(object):
    itemsCache = dependency.descriptor(IItemsCache)

    def __init__(self):
        self.invID = None
        self.inProcess = False
        g_events.onVehicleChanged += self.updateCrew
        overrideMethod(ExchangeXPWindow, "as_vehiclesDataChangedS")(self.onXPExchangeDataChanged)

    @staticmethod
    def getLocalizedMessage(value, description):
        dialog = localization[CREW_XP.NAME]
        return dialog[description] + "\n\n" + dialog[CREW_XP.ENABLE if value else CREW_XP.DISABLE]

    @wg_async
    def showDialog(self, vehicle, value, description):
        self.inProcess = True
        dialog = CrewDialog()
        app = dependency.instance(IAppLoader).getApp()
        if app is not None and app.containerManager is not None:
            view = app.containerManager.getView(WindowLayer.VIEW)
            dialog.setView(view)
        title = getLogo() + "\n" + vehicle.userName
        message = self.getLocalizedMessage(value, description)
        dialogResult = yield wg_await(dialog.showCrewDialog(title, message, vehicle.userName))
        if dialogResult:
            self.accelerateCrewXp(vehicle, value)
        self.inProcess = False

    @decorators.adisp_process('updateTankmen')
    def accelerateCrewXp(self, vehicle, value):
        result = yield VehicleTmenXPAccelerator(vehicle, value, confirmationEnabled=False).request()
        if result.success:
            logInfo("The accelerated crew training is %s for '%s'" % (value, vehicle.userName))

    @staticmethod
    def isPPFullXP(vehicle):
        iterator = vehicle.postProgression.iterOrderedSteps()
        return vehicle.xp >= sum(x.getPrice().xp for x in iterator if not x.isRestricted() and not x.isReceived())

    def isAccelerateTraining(self, vehicle):
        if not vehicle.postProgressionAvailability(unlockOnly=True).result:
            return True, CREW_XP.NOT_AVAILABLE
        elif vehicle.postProgression.getCompletion() is PostProgressionCompletion.FULL:
            return True, CREW_XP.IS_FULL_COMPLETE
        elif self.isPPFullXP(vehicle):
            return True, CREW_XP.IS_FULL_XP
        else:
            return False, CREW_XP.NED_TURN_OFF

    def accelerateCrewTraining(self):
        if settings.main[MAIN.CREW_TRAINING]:
            vehicle = g_currentVehicle.item
            if vehicle is None or vehicle.userName in ignored_vehicles or not vehicle.isElite or \
                    vehicle.isLocked or vehicle.isInBattle or vehicle.isCrewLocked:
                return
            acceleration, description = self.isAccelerateTraining(vehicle)
            if vehicle.isXPToTman != acceleration and not self.inProcess:
                self.showDialog(vehicle, acceleration, description)

    def updateCrew(self):
        self.returnCrew()
        self.accelerateCrewTraining()

    def returnCrew(self):
        if self.invID != g_currentVehicle.invID and settings.main[MAIN.CREW_RETURN]:
            self.invID = g_currentVehicle.invID
            vehicle = g_currentVehicle.item
            if vehicle is None or vehicle.isLocked or vehicle.isInBattle or vehicle.isCrewLocked or vehicle.isCrewFull:
                return
            self._processReturnCrew(vehicle)

    @decorators.adisp_process('crewReturning')
    def _processReturnCrew(self, vehicle):
        result = yield TankmanReturn(vehicle).request()
        if result.userMsg:
            SystemMessages.pushI18nMessage(result.userMsg, type=result.sysMsgType)
            logInfo("{}: {}".format(vehicle.userName, result.userMsg))

    def onXPExchangeDataChanged(self, base, dialog, data, *args, **kwargs):
        try:
            ID = "id"
            CANDIDATE = "isSelectCandidate"
            vehicleList = data['vehicleList']
            for vehicleData in vehicleList:
                vehicle = self.itemsCache.items.getItemByCD(vehicleData[ID])
                check, _ = self.isAccelerateTraining(vehicle)
                vehicleData[CANDIDATE] &= check
        except Exception as error:
            logError("CrewProcessor onXPExchangeDataChanged: {}", repr(error))
        finally:
            return base(dialog, data, *args, **kwargs)


crew = CrewProcessor()

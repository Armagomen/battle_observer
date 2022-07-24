from CurrentVehicle import g_currentVehicle, _CurrentVehicle
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.battle_observer.settings.hangar.i18n import localization
from armagomen.constants import MAIN, CREW_XP, getRandomLogo
from armagomen.utils.common import logInfo, overrideMethod, logError, ignored_vehicles
from armagomen.utils.dialogs import CrewDialog
from armagomen.utils.events import g_events
from async import async, await
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


class CrewProcessor(object):
    itemsCache = dependency.descriptor(IItemsCache)

    def __init__(self):
        self.inProcess = False
        self.dialog = CrewDialog()
        g_events.onHangarVehicleChanged += self.onVehicleChanged
        overrideMethod(_CurrentVehicle, "_changeDone")(self.onChangeDone)
        overrideMethod(ExchangeXPWindow, "as_vehiclesDataChangedS")(self.onXPExchangeDataChanged)

    @staticmethod
    def getLocalizedMessage(value, description):
        dialog = localization[CREW_XP.NAME]
        return dialog[description] + "\n\n" + dialog[CREW_XP.ENABLE if value else CREW_XP.DISABLE]

    @async
    def showDialog(self, vehicle, value, description):
        app = dependency.instance(IAppLoader).getApp()
        if app is not None and app.containerManager is not None:
            view = app.containerManager.getView(WindowLayer.VIEW)
            self.dialog.setView(view)
        title = getRandomLogo() + "\n" + vehicle.userName
        message = self.getLocalizedMessage(value, description)
        dialogResult = yield await(self.dialog.showCrewDialog(title, message, vehicle.userName))
        if dialogResult:
            self.accelerateCrewXp(vehicle, value)
        self.inProcess = False

    @decorators.process('updateTankmen')
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

    def onVehicleChanged(self):
        if not settings.main[MAIN.CREW_TRAINING] or not g_currentVehicle.isPresent() or self.inProcess:
            return
        vehicle = g_currentVehicle.item
        if not vehicle.isElite or vehicle.isLocked or vehicle.isInBattle or vehicle.userName in ignored_vehicles:
            return
        acceleration, description = self.isAccelerateTraining(vehicle)
        if vehicle.isXPToTman != acceleration:
            self.inProcess = True
            self.showDialog(vehicle, acceleration, description)

    @decorators.process('crewReturning')
    def _processReturnCrew(self, vehicle):
        result = yield TankmanReturn(vehicle).request()
        if result.userMsg:
            SystemMessages.pushI18nMessage(result.userMsg, type=result.sysMsgType)
            logInfo("{}: {}".format(vehicle.userName, result.userMsg))

    def onChangeDone(self, base, *args, **kwargs):
        try:
            if settings.main[MAIN.CREW_RETURN] and g_currentVehicle.isPresent():
                vehicle = g_currentVehicle.item
                if not vehicle.isInBattle and not vehicle.isCrewFull:
                    self._processReturnCrew(vehicle)
        except Exception as error:
            logError("CrewProcessor onChangeDone: " + repr(error))
        finally:
            return base(*args, **kwargs)

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
            logError("CrewProcessor onXPExchangeDataChanged: " + repr(error))
        finally:
            return base(dialog, data, *args, **kwargs)


crew = CrewProcessor()

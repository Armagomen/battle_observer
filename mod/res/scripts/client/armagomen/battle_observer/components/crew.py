from threading import Thread

from armagomen._constants import CREW_XP, GLOBAL, MAIN
from armagomen.battle_observer.settings import user_settings
from armagomen.battle_observer.settings.hangar.i18n import localization
from armagomen.utils.common import openIgnoredVehicles, overrideMethod, updateIgnoredVehicles
from armagomen.utils.dialogs import CrewDialog
from armagomen.utils.events import g_events
from armagomen.utils.logging import DEBUG, logDebug, logError, logInfo
from gui import SystemMessages
from gui.impl.pub.dialog_window import DialogButtons
from gui.Scaleform.daapi.view.lobby.exchange.ExchangeXPWindow import ExchangeXPWindow
from gui.shared.gui_items.processors.tankman import TankmanReturn
from gui.shared.gui_items.processors.vehicle import VehicleTmenXPAccelerator
from gui.shared.utils import decorators
from gui.veh_post_progression.models.progression import PostProgressionCompletion
from helpers import dependency
from skeletons.gui.shared import IItemsCache
from wg_async import wg_async, wg_await

ignored_vehicles = openIgnoredVehicles()


class CrewProcessor(object):
    itemsCache = dependency.descriptor(IItemsCache)

    def __init__(self):
        self.intCD = None
        self.isDialogVisible = False
        g_events.onVehicleChangedDelayed += self.updateCrew
        overrideMethod(ExchangeXPWindow, "as_vehiclesDataChangedS")(self.onXPExchangeDataChanged)

    @staticmethod
    def getLocalizedMessage(value, description):
        dialog = localization[CREW_XP.NAME]
        return GLOBAL.NEW_LINE.join((dialog[description], dialog[CREW_XP.ENABLE if value else CREW_XP.DISABLE]))

    @wg_async
    def showDialog(self, vehicle, value, description):
        self.isDialogVisible = True
        message = self.getLocalizedMessage(value, description)
        dialog_result = yield wg_await(CrewDialog().showCrewDialog(vehicle.userName, message))
        if dialog_result.result == DialogButtons.SUBMIT:
            self.accelerateCrewXp(vehicle, value)
        elif dialog_result.result == DialogButtons.PURCHASE:
            ignored_vehicles.add(vehicle.userName)
            updateIgnoredVehicles(ignored_vehicles)
        self.isDialogVisible = False

    @decorators.adisp_process('updateTankmen')
    def accelerateCrewXp(self, vehicle, value):
        result = yield VehicleTmenXPAccelerator(vehicle, value, confirmationEnabled=False).request()
        if result.success:
            logInfo("The accelerated crew training is {} for '{}'", value, vehicle.userName)

    @staticmethod
    def isPostProgressionFullXP(vehicle):
        iterator = vehicle.postProgression.iterOrderedSteps()
        currentXP = vehicle.xp
        needToProgress = sum(x.getPrice().xp for x in iterator if not x.isRestricted() and not x.isReceived())
        if user_settings.main[DEBUG]:
            logDebug("isPPFullXP - {}: {}/{}", vehicle.userName, currentXP, needToProgress)
        return currentXP >= needToProgress

    def isAccelerateTraining(self, vehicle):
        if not vehicle.postProgressionAvailability(unlockOnly=True).result:
            return True, CREW_XP.NOT_AVAILABLE
        elif vehicle.postProgression.getCompletion() is PostProgressionCompletion.FULL:
            return True, CREW_XP.IS_FULL_COMPLETE
        elif self.isPostProgressionFullXP(vehicle):
            return True, CREW_XP.IS_FULL_XP
        else:
            return False, CREW_XP.NED_TURN_OFF

    def accelerateCrewTraining(self, vehicle):
        if vehicle.userName in ignored_vehicles or not vehicle.isElite:
            return
        acceleration, description = self.isAccelerateTraining(vehicle)
        if vehicle.isXPToTman != acceleration and not self.isDialogVisible:
            self.showDialog(vehicle, acceleration, description)

    def isCrewAvailable(self, vehicle):
        lastCrewIDs = vehicle.lastCrew
        if lastCrewIDs is None:
            return False
        for lastTankmenInvID in lastCrewIDs:
            actualLastTankman = self.itemsCache.items.getTankman(lastTankmenInvID)
            if actualLastTankman is not None and actualLastTankman.isInTank:
                lastTankmanVehicle = self.itemsCache.items.getVehicle(actualLastTankman.vehicleInvID)
                if lastTankmanVehicle and lastTankmanVehicle.isLocked:
                    return False
        return True

    def updateCrew(self, vehicle):
        if vehicle is None or vehicle.isLocked or vehicle.isInBattle or vehicle.isCrewLocked:
            return
        if user_settings.main[MAIN.CREW_RETURN] and self.intCD != vehicle.intCD:
            if not vehicle.isCrewFull and self.isCrewAvailable(vehicle):
                self._processReturnCrew(vehicle)
            self.intCD = vehicle.intCD
        if user_settings.main[MAIN.CREW_TRAINING]:
            self.accelerateCrewTraining(vehicle)

    @decorators.adisp_process('crewReturning')
    def _processReturnCrew(self, vehicle):
        result = yield TankmanReturn(vehicle).request()
        if result.userMsg:
            SystemMessages.pushI18nMessage(result.userMsg, type=result.sysMsgType)
            logInfo("{}: {}", vehicle.userName, result.userMsg)

    def onXPExchangeDataChanged(self, base, dialog, data, *args, **kwargs):
        try:
            ID = "id"
            CANDIDATE = "isSelectCandidate"
            for vehicleData in data['vehicleList']:
                vehicle = self.itemsCache.items.getItemByCD(vehicleData[ID])
                check, _ = self.isAccelerateTraining(vehicle)
                vehicleData[CANDIDATE] &= check
        except Exception as error:
            logError("CrewProcessor onXPExchangeDataChanged: {}", repr(error))
        finally:
            return base(dialog, data, *args, **kwargs)


crew = Thread(target=CrewProcessor)
crew.daemon = True
crew.start()

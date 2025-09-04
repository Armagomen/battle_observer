from AccountCommands import VEHICLE_SETTINGS_FLAG
from armagomen._constants import CREW_XP, IS_WG_CLIENT, MAIN
from armagomen.battle_observer.i18n.crew import CREW_DIALOG_BY_LANG
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import updateIgnoredVehicles
from armagomen.utils.dialogs import CrewDialog
from armagomen.utils.events import g_events
from armagomen.utils.logging import logDebug, logInfo
from gui import SystemMessages
from gui.impl.pub.dialog_window import DialogButtons

if IS_WG_CLIENT:
    from gui.shared.gui_items.processors.tankman import TankmanAutoReturn
    from gui.shared.gui_items.processors.vehicle import VehicleAutoReturnProcessor
else:
    from gui.shared.gui_items.processors.tankman import TankmanReturn

from gui.shared.notifications import NotificationPriorityLevel
from gui.shared.utils import decorators
from gui.veh_post_progression.models.progression import PostProgressionCompletion
from helpers import dependency
from skeletons.gui.shared import IItemsCache
from wg_async import wg_async, wg_await


class CrewProcessor(object):
    itemsCache = dependency.descriptor(IItemsCache)

    def __init__(self):
        self.intCD = None
        self.isDialogVisible = False
        self.ignored_vehicles = set()
        updateIgnoredVehicles(self.ignored_vehicles)
        if any(not isinstance(vehicle, int) for vehicle in self.ignored_vehicles):
            self.ignored_vehicles = {v for v in self.ignored_vehicles if isinstance(v, int)}
            updateIgnoredVehicles(self.ignored_vehicles, True)
        g_events.onVehicleChangedDelayed += self.onVehicleChanged
        logDebug("accelerateCrewXp ignored vehicles: {}", self.ignored_vehicles)

    def fini(self):
        g_events.onVehicleChangedDelayed -= self.onVehicleChanged

    @staticmethod
    def getLocalizedMessage(value, description):
        return "<br><br>".join((CREW_DIALOG_BY_LANG[description], CREW_DIALOG_BY_LANG[CREW_XP.ENABLE if value else CREW_XP.DISABLE]))

    @wg_async
    def showAccelerateDialog(self, vehicle, value, description):
        self.isDialogVisible = True
        message = self.getLocalizedMessage(value, description)
        dialog_result = yield wg_await(CrewDialog().showCrewDialog(vehicle.userName, message))
        if dialog_result.result == DialogButtons.SUBMIT:
            self.accelerateCrewXp(vehicle, value)
        elif dialog_result.result == DialogButtons.PURCHASE:
            self.ignored_vehicles.add(vehicle.intCD)
            updateIgnoredVehicles(self.ignored_vehicles, True)
        self.isDialogVisible = False

    @decorators.adisp_process('updateTankmen')
    def accelerateCrewXp(self, vehicle, value):
        from gui.shared.gui_items.processors.vehicle import VehicleTmenXPAccelerator
        result = yield VehicleTmenXPAccelerator(vehicle, value, confirmationEnabled=False).request()
        if result.success:
            logInfo("The accelerated crew training is {} for '{}'", value, vehicle.userName)

    @staticmethod
    def isPostProgressionFullXP(vehicle):
        iterator = vehicle.postProgression.iterOrderedSteps()
        currentXP = vehicle.xp
        needToProgress = sum(x.getPrice().xp for x in iterator if not x.isRestricted() and not x.isReceived())
        logDebug("isPostProgressionFullXP - {}: {}/{}", vehicle.userName, currentXP, needToProgress)
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

    def isCrewAvailable(self, vehicle):
        isLockedFound = False
        for tankmanID in vehicle.lastCrew:
            tankman = self.itemsCache.items.getTankman(tankmanID)
            if tankman and tankman.isInTank:
                tankmanVehicle = self.itemsCache.items.getVehicle(tankman.vehicleInvID)
                if tankmanVehicle:
                    isLockedFound |= tankmanVehicle.isLocked
        return not isLockedFound

    def onVehicleChanged(self, vehicle):
        logDebug("crew onVehicleChanged")
        if not vehicle or vehicle.isLocked:
            return
        if user_settings.main[MAIN.CREW_RETURN]:
            self.updateAutoReturn(vehicle)
        if IS_WG_CLIENT and user_settings.main[MAIN.CREW_TRAINING]:
            self.updateAcceleration(vehicle)

    def updateAutoReturn(self, vehicle):
        if self.intCD != vehicle.intCD:
            if IS_WG_CLIENT:
                self.__autoReturnToggleSwitch(vehicle)
            else:
                self.__processReturnCrew(vehicle)
            self.intCD = vehicle.intCD

    def updateAcceleration(self, vehicle):
        if not self.isDialogVisible:
            if vehicle.intCD in self.ignored_vehicles or not vehicle.isElite:
                return
            acceleration, description = self.isAccelerateTraining(vehicle)
            if vehicle.isXPToTman != acceleration:
                self.showAccelerateDialog(vehicle, acceleration, description)

    @staticmethod
    def isSpecialVehicle(vehicle):
        flags = ('isOnlyForFunRandomBattles', 'isOnlyForBattleRoyaleBattles', 'isOnlyForMapsTrainingBattles',
                 'isOnlyForClanWarsBattles', 'isOnlyForComp7Battles', 'isOnlyForEventBattles', 'isOnlyForEpicBattles')
        return any(getattr(vehicle, f, False) for f in flags)

    @decorators.adisp_process('updating')
    def __autoReturnToggleSwitch(self, vehicle):
        autoReturn = bool(vehicle.settings & VEHICLE_SETTINGS_FLAG.AUTO_RETURN)
        if autoReturn or self.isSpecialVehicle(vehicle):
            return
        available = bool(vehicle.lastCrew)
        if available != autoReturn:
            result = yield VehicleAutoReturnProcessor(vehicle, available).request()
            if available and result.success and not vehicle.isCrewLocked and not vehicle.isCrewFull:
                result = yield TankmanAutoReturn(vehicle).request()
            if not result.success and result.userMsg:
                SystemMessages.pushI18nMessage(result.userMsg, type=result.sysMsgType, priority=NotificationPriorityLevel.MEDIUM)

    @decorators.adisp_process('crewReturning')
    def __processReturnCrew(self, vehicle):
        if not vehicle.isCrewFull and bool(vehicle.lastCrew) and self.isCrewAvailable(vehicle):
            result = yield TankmanReturn(vehicle).request()
            if result.userMsg:
                SystemMessages.pushI18nMessage(result.userMsg, type=result.sysMsgType, priority=NotificationPriorityLevel.MEDIUM)


crew = CrewProcessor()


def fini():
    crew.fini()

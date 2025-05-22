from armagomen._constants import CREW_XP, GLOBAL, IS_WG_CLIENT, MAIN
from armagomen.battle_observer.settings import user_settings
from armagomen.battle_observer.settings.hangar.i18n import localization
from armagomen.utils.common import openIgnoredVehicles, updateIgnoredVehicles
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
        self.ignored_vehicles = openIgnoredVehicles()
        update_vehicles = False
        for vehicle in tuple(self.ignored_vehicles):
            if not isinstance(vehicle, int):
                self.ignored_vehicles.discard(vehicle)
                update_vehicles = True
        if update_vehicles:
            updateIgnoredVehicles(self.ignored_vehicles)
        g_events.onVehicleChangedDelayed += self.onVehicleChanged
        logDebug("accelerateCrewXp ignored vehicles: {}", self.ignored_vehicles)

    @staticmethod
    def getLocalizedMessage(value, description):
        dialog = localization[CREW_XP.NAME]
        return GLOBAL.NEW_LINE.join((dialog[description], dialog[CREW_XP.ENABLE if value else CREW_XP.DISABLE]))

    @wg_async
    def showAccelerateDialog(self, vehicle, value, description):
        self.isDialogVisible = True
        message = self.getLocalizedMessage(value, description)
        dialog_result = yield wg_await(CrewDialog().showCrewDialog(vehicle.userName, message))
        if dialog_result.result == DialogButtons.SUBMIT:
            self.accelerateCrewXp(vehicle, value)
        elif dialog_result.result == DialogButtons.PURCHASE:
            self.ignored_vehicles.add(vehicle.intCD)
            updateIgnoredVehicles(self.ignored_vehicles)
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

    def onVehicleChanged(self, vehicle):
        if not vehicle or vehicle.isLocked or vehicle.isInBattle or vehicle.isCrewLocked or vehicle.isAwaitingBattle or vehicle.isInPrebattle:
            return
        if user_settings.main[MAIN.CREW_RETURN] and vehicle.lastCrew:
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

    @decorators.adisp_process('updating')
    def __autoReturnToggleSwitch(self, vehicle):
        if not vehicle.isAutoReturn:
            result = yield VehicleAutoReturnProcessor(vehicle, True).request()
            if result.success:
                result = yield TankmanAutoReturn(vehicle).request()
            if not result.success and result.userMsg:
                SystemMessages.pushI18nMessage(result.userMsg, type=result.sysMsgType, priority=NotificationPriorityLevel.MEDIUM)

    @decorators.adisp_process('crewReturning')
    def __processReturnCrew(self, vehicle):
        if not vehicle.isCrewFull and self.isCrewAvailable(vehicle):
            result = yield TankmanReturn(vehicle).request()
            if result.userMsg:
                SystemMessages.pushI18nMessage(result.userMsg, type=result.sysMsgType, priority=NotificationPriorityLevel.MEDIUM)


crew = CrewProcessor()


def fini():
    g_events.onVehicleChangedDelayed -= crew.onVehicleChanged

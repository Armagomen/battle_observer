from AccountCommands import VEHICLE_SETTINGS_FLAG
from armagomen._constants import CREW
from armagomen.battle_observer.i18n.crew import CREW_DIALOG_BY_LANG, CREW_XP
from armagomen.battle_observer.settings import IBOSettingsLoader
from armagomen.utils.common import isSpecialBattleVehicle, updateIgnoredVehicles
from armagomen.utils.dialogs import CrewDialog
from armagomen.utils.events import g_events
from armagomen.utils.logging import logDebug, logInfo
from dossiers2.custom.cache import getCache
from gui import SystemMessages
from gui.impl.pub.dialog_window import DialogButtons
from gui.shared.gui_items.processors.tankman import TankmanAutoReturn
from gui.shared.gui_items.processors.vehicle import VehicleAutoReturnProcessor, VehicleTmenXPAccelerator
from gui.shared.notifications import NotificationPriorityLevel
from gui.shared.utils import decorators
from gui.veh_post_progression.models.progression import PostProgressionCompletion
from helpers import dependency
from skeletons.gui.shared import IItemsCache
from wg_async import wg_async, wg_await


class CrewProcessor(object):
    itemsCache = dependency.descriptor(IItemsCache)
    settingsLoader = dependency.descriptor(IBOSettingsLoader)

    def __init__(self):
        self.xp_to_11_lvl = 325000
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
    def getLocalizedMessage(value, description, xp):
        return "{}\n\n<b>{}</b>".format(CREW_DIALOG_BY_LANG[description].format(xp),
                                        CREW_DIALOG_BY_LANG[CREW_XP.ENABLE if value else CREW_XP.DISABLE])

    @wg_async
    def showAccelerateDialog(self, vehicle, value, message):
        self.isDialogVisible = True
        dialog_result = yield wg_await(CrewDialog().show(vehicle.userName, message))
        if dialog_result.result == DialogButtons.SUBMIT:
            self.accelerateCrewXp(vehicle, value)
        elif dialog_result.result == DialogButtons.PURCHASE:
            self.ignored_vehicles.add(vehicle.intCD)
            updateIgnoredVehicles(self.ignored_vehicles, True)
        self.isDialogVisible = False

    @decorators.adisp_process('updateTankmen')
    def accelerateCrewXp(self, vehicle, value):
        result = yield VehicleTmenXPAccelerator(vehicle, value, confirmationEnabled=False).request()
        if result.success:
            logInfo("The accelerated crew training is {} for '{}'", value, vehicle.userName)

    @staticmethod
    def getRemainPostProgressionXP(vehicle):
        postProgressionAvailability = vehicle.postProgressionAvailability(unlockOnly=True).result
        if postProgressionAvailability:
            iterator = vehicle.postProgression.iterOrderedSteps()
            remain_PP_XP = sum(x.getPrice().xp for x in iterator if not x.isRestricted() and not x.isReceived())
            logDebug("postProgressionXP - {}: {}", vehicle.userName, remain_PP_XP)
            return postProgressionAvailability, remain_PP_XP - vehicle.xp
        return postProgressionAvailability, 0

    def isXPto11(self, vehicle):
        enabled = self.settingsLoader.getSetting(CREW.NAME, CREW.THRESHOLD)
        return enabled and vehicle.level == 10 and not vehicle.isSpecial and not vehicle.isCollectible and \
            getCache()['vehiclesByLevel'][11].isdisjoint(vehicle.getEliteStatusProgress().unlocked)

    def isAccelerateTraining(self, vehicle):
        postProgressionAvailability, xp = self.getRemainPostProgressionXP(vehicle)
        acceleration, description = False, CREW_XP.NED_TURN_OFF

        isXPto11 = self.isXPto11(vehicle)
        if isXPto11:
            xp += self.xp_to_11_lvl

        if isXPto11 and xp > 0:
            description = CREW_XP.THRESHOLD
        elif not vehicle.isFullyElite:
            description = CREW_XP.NOT_ELITE
        elif not postProgressionAvailability:
            acceleration, description = True, CREW_XP.NOT_AVAILABLE
        elif vehicle.postProgression.getCompletion() is PostProgressionCompletion.FULL or xp <= 0:
            acceleration, description = True, CREW_XP.IS_FULL_COMPLETE

        return acceleration, description, max(0, xp)

    def onVehicleChanged(self, vehicle):
        logDebug("crew onVehicleChanged")
        if not vehicle or vehicle.isLocked or isSpecialBattleVehicle(vehicle):
            return
        if self.settingsLoader.getSetting(CREW.NAME, CREW.CREW_RETURN):
            self.updateAutoReturn(vehicle)
        if self.settingsLoader.getSetting(CREW.NAME, CREW.CREW_TRAINING):
            self.updateAcceleration(vehicle)

    def updateAutoReturn(self, vehicle):
        if self.intCD != vehicle.intCD:
            self.__autoReturnToggleSwitch(vehicle)
            self.intCD = vehicle.intCD

    def updateAcceleration(self, vehicle):
        if not self.isDialogVisible:
            if vehicle.intCD in self.ignored_vehicles or not vehicle.isElite:
                return
            acceleration, description, xp = self.isAccelerateTraining(vehicle)
            if vehicle.isXPToTman != acceleration:
                message = self.getLocalizedMessage(acceleration, description, xp)
                self.showAccelerateDialog(vehicle, acceleration, message)

    @decorators.adisp_process('updating')
    def __autoReturnToggleSwitch(self, vehicle):
        autoReturn = bool(vehicle.settings & VEHICLE_SETTINGS_FLAG.AUTO_RETURN)
        if autoReturn:
            return
        available = bool(vehicle.lastCrew)
        if available != autoReturn:
            result = yield VehicleAutoReturnProcessor(vehicle, available).request()
            if available and result.success and not vehicle.isCrewLocked and not vehicle.isCrewFull:
                result = yield TankmanAutoReturn(vehicle).request()
            if not result.success and result.userMsg:
                SystemMessages.pushI18nMessage(result.userMsg, type=result.sysMsgType, priority=NotificationPriorityLevel.MEDIUM)


crew = CrewProcessor()


def fini():
    crew.fini()

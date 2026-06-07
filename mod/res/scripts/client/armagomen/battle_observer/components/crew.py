import os
from collections import defaultdict

from AccountCommands import VEHICLE_SETTINGS_FLAG
from armagomen._constants import CREW
from armagomen import IALogger
from armagomen.battle_observer.i18n.crew import CREW_DIALOG_BY_LANG, CREW_XP
from armagomen.battle_observer.settings import IBOSettingsLoader
from armagomen.utils.common import getObserverCachePath, IS_COMMON_TEST, isSpecialBattleVehicle, openJsonFile, writeJsonFile
from armagomen.utils.dialogs import CrewDialog
from armagomen.utils.events import g_events
from dossiers2.custom.cache import getCache
from gui import SystemMessages
from gui.impl.pub.dialog_window import DialogButtons
from gui.shared.gui_items.processors.tankman import TankmanAutoReturn
from gui.shared.gui_items.processors.vehicle import VehicleAutoReturnProcessor, VehicleTmenXPAccelerator
from gui.shared.notifications import NotificationPriorityLevel
from gui.shared.utils import decorators
from gui.veh_post_progression.models.progression import PostProgressionCompletion
from helpers import dependency
from skeletons.connection_mgr import IConnectionManager
from skeletons.gui.shared import IItemsCache
from wg_async import wg_async, wg_await


class TrackingList(list):
    def __init__(self, parent):
        super(TrackingList, self).__init__()
        self.parent = parent

    def append(self, item):
        self.parent._updated = True
        super(TrackingList, self).append(item)


class CrewIgnoredCache(defaultdict):
    logger = dependency.descriptor(IALogger)

    def __init__(self):
        super(CrewIgnoredCache, self).__init__(lambda: TrackingList(self))
        self.file_path = os.path.join(getObserverCachePath(), 'crew_ignored.json')
        self._loaded = False
        self._updated = False

    def __setitem__(self, key, value):
        self._updated = True
        return super(CrewIgnoredCache, self).__setitem__(key, value)

    def saveCache(self):
        if self._updated:
            serialized = {k: sorted(v) for k, v in self.iteritems()}
            writeJsonFile(self.file_path, serialized)
            self.logger.logDebug('CrewIgnoredCache saved: {}', serialized)

    def getUserCache(self, userName):
        if not self._loaded and os.path.isfile(self.file_path):
            self._loaded = True
            loaded = openJsonFile(self.file_path)
            if isinstance(loaded, dict):
                for k, v in loaded.iteritems():
                    self[k] = TrackingList(self)
                    self[k].extend(v)
                self._updated = False

        result = self[userName]
        self.logger.logDebug("CrewIgnoredCache loaded for {}: {}", userName, result)
        return result


class CrewProcessor(object):
    itemsCache = dependency.descriptor(IItemsCache)
    settingsLoader = dependency.descriptor(IBOSettingsLoader)
    connectionMgr = dependency.descriptor(IConnectionManager)
    logger = dependency.descriptor(IALogger)

    def __init__(self):
        self.xp_to_11_lvl = 325000
        self.isDialogVisible = False
        self.hidden_update = False
        self.ignored_vehicles_cache = CrewIgnoredCache()
        self.user_cache = None
        g_events.onVehicleChangedDelayed += self.onVehicleChanged
        self.connectionMgr.onLoggedOn += self._onLoggedOn

    def fini(self):
        g_events.onVehicleChangedDelayed -= self.onVehicleChanged
        self.connectionMgr.onLoggedOn -= self._onLoggedOn
        self.ignored_vehicles_cache.saveCache()

    def _onLoggedOn(self, responseData):
        if IS_COMMON_TEST:
            return
        if responseData.get("isDemoAccount", False):
            return
        self.user_cache = self.ignored_vehicles_cache.getUserCache(responseData.get('name'))

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
        elif dialog_result.result == DialogButtons.PURCHASE and vehicle.intCD not in self.user_cache:
            self.user_cache.append(vehicle.intCD)
        self.isDialogVisible = False

    @decorators.adisp_process('updateTankmen')
    def accelerateCrewXp(self, vehicle, value):
        result = yield VehicleTmenXPAccelerator(vehicle, value, confirmationEnabled=False).request()
        if result.success:
            self.logger.logInfo("The accelerated crew training is {} for '{}'", value, vehicle.userName)

    def getRemainPostProgressionXP(self, vehicle):
        postProgressionAvailability = vehicle.postProgressionAvailability(unlockOnly=True).result
        if postProgressionAvailability:
            iterator = vehicle.postProgression.iterOrderedSteps()
            remain_PP_XP = sum(x.getPrice().xp for x in iterator if not x.isRestricted() and not x.isReceived())
            self.logger.logDebug("postProgressionXP - {}: {}", vehicle.userName, remain_PP_XP)
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
        self.logger.logDebug("crew onVehicleChanged")
        if not vehicle or vehicle.isLocked or isSpecialBattleVehicle(vehicle):
            return
        if self.settingsLoader.getSetting(CREW.NAME, CREW.RETURN):
            self.__autoReturnToggleSwitch(vehicle)
        if self.settingsLoader.getSetting(CREW.NAME, CREW.TRAINING):
            self.updateAcceleration(vehicle)

    def updateAcceleration(self, vehicle):
        if self.isDialogVisible or not vehicle.isElite or self.user_cache is not None and vehicle.intCD in self.user_cache:
            return
        acceleration, description, xp = self.isAccelerateTraining(vehicle)
        if vehicle.isXPToTman != acceleration:
            if self.settingsLoader.getSetting(CREW.NAME, CREW.HIDDEN_ACCELERATE):
                self.accelerateCrewXp(vehicle, acceleration)
            else:
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

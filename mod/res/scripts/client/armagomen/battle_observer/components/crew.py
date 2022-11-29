from armagomen.battle_observer.settings.default_settings import settings
from armagomen.battle_observer.settings.hangar.i18n import localization
from armagomen.constants import MAIN, CREW_XP, getLogo, GLOBAL
from armagomen.utils.common import logInfo, overrideMethod, logError, ignored_vehicles, logDebug
from armagomen.utils.dialogs import CrewDialog
from armagomen.utils.events import g_events
from gui import SystemMessages
from gui.Scaleform.daapi.view.lobby.exchange.ExchangeXPWindow import ExchangeXPWindow
from gui.shared.gui_items.processors.tankman import TankmanReturn
from gui.shared.gui_items.processors.vehicle import VehicleTmenXPAccelerator
from gui.shared.utils import decorators
from gui.veh_post_progression.models.progression import PostProgressionCompletion
from helpers import dependency
from skeletons.gui.shared import IItemsCache
from wg_async import wg_async, wg_await


class CrewProcessor(object):
    itemsCache = dependency.descriptor(IItemsCache)

    def __init__(self):
        self.invID = None
        self.inProcess = False
        g_events.onVehicleChangedDelayed += self.updateCrew
        overrideMethod(ExchangeXPWindow, "as_vehiclesDataChangedS")(self.onXPExchangeDataChanged)

    @staticmethod
    def getLocalizedMessage(value, description):
        dialog = localization[CREW_XP.NAME]
        return GLOBAL.NEW_LINE.join((dialog[description], dialog[CREW_XP.ENABLE if value else CREW_XP.DISABLE]))

    @wg_async
    def showDialog(self, vehicle, value, description):
        self.inProcess = True
        dialog = CrewDialog()
        title = GLOBAL.NEW_LINE.join((getLogo(), vehicle.userName))
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

    def accelerateCrewTraining(self, vehicle):
        if vehicle is None or vehicle.userName in ignored_vehicles or not vehicle.isElite or \
                vehicle.isLocked or vehicle.isInBattle or vehicle.isCrewLocked:
            return
        acceleration, description = self.isAccelerateTraining(vehicle)
        if vehicle.isXPToTman != acceleration and not self.inProcess:
            self.showDialog(vehicle, acceleration, description)

    def updateCrew(self, vehicle):
        if settings.main[MAIN.CREW_RETURN]:
            self.returnCrew(vehicle)
        if settings.main[MAIN.CREW_TRAINING]:
            self.accelerateCrewTraining(vehicle)

    def returnCrew(self, vehicle):
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
            for vehicleData in data['vehicleList']:
                vehicle = self.itemsCache.items.getItemByCD(vehicleData[ID])
                check, _ = self.isAccelerateTraining(vehicle)
                vehicleData[CANDIDATE] &= check
        except Exception as error:
            logError("CrewProcessor onXPExchangeDataChanged: {}", repr(error))
        finally:
            return base(dialog, data, *args, **kwargs)


crew = CrewProcessor()

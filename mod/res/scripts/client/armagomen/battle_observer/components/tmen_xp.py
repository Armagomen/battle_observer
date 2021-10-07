from CurrentVehicle import g_currentVehicle
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import MAIN
from armagomen.utils.common import logInfo, overrideMethod
from gui.Scaleform.daapi.view.lobby.hangar.Hangar import Hangar
from gui.shared.gui_items.Vehicle import Vehicle
from gui.shared.gui_items.processors.vehicle import VehicleTmenXPAccelerator
from gui.shared.utils import decorators
from gui.veh_post_progression.models.progression import PostProgressionCompletion


class AccelerateCrewXp(object):

    def __init__(self):
        self.inProcess = False
        overrideMethod(Hangar, "__onCurrentVehicleChanged")(self.onVehicleChanged)

    @decorators.process('updateTankmen')
    def accelerateTmenXp(self, vehicle, value):
        """
        :type value: bool
        :type vehicle: Vehicle
        """
        result = yield VehicleTmenXPAccelerator(vehicle, value).request()
        if result.success:
            logInfo("The accelerated crew training is %s for '%s'" % (value, vehicle.userName))
        self.inProcess = False

    @staticmethod
    def checkXP(vehicle):
        """
        :type vehicle: Vehicle
        """
        iterator = vehicle.postProgression.iterOrderedSteps()
        return vehicle.xp >= sum(x.getPrice().xp for x in iterator if not x.isRestricted() and not x.isReceived())

    def onVehicleChanged(self, base, *args, **kwargs):
        base(*args, **kwargs)
        if not settings.main[MAIN.CREW_TRAINING] or not g_currentVehicle.isPresent() or self.inProcess:
            return
        vehicle = g_currentVehicle.item  # type: Vehicle
        if not vehicle.isElite or g_currentVehicle.isLocked() or g_currentVehicle.isInBattle():
            return
        value = False
        if vehicle.isFullyElite:
            availability = vehicle.postProgressionAvailability().result
            complete = vehicle.postProgression.getCompletion() is PostProgressionCompletion.FULL
            value = not availability or complete or self.checkXP(vehicle)
        if vehicle.isXPToTman != value:
            self.inProcess = True
            self.accelerateTmenXp(vehicle, value)


crewXP = AccelerateCrewXp()

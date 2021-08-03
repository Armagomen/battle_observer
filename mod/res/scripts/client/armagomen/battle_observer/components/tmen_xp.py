from CurrentVehicle import g_currentVehicle
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import MAIN
from armagomen.utils.common import logInfo
from gui.Scaleform.Waiting import Waiting
from gui.shared.gui_items.processors.vehicle import VehicleTmenXPAccelerator
from gui.shared.utils import decorators
from gui.veh_post_progression.models.progression import PostProgressionCompletion


class AccelerateTmenXp(object):
    def __init__(self):
        self.__vehicle = None
        self.__value = None
        g_currentVehicle.onChanged += self.onVehicleChanged

    @decorators.process('updateTankmen')
    def accelerateTmenXp(self, vehicle, value):
        result = yield VehicleTmenXPAccelerator(vehicle, value).request()
        if result.success:
            logInfo("The accelerated crew training is %s for %s" % (value, vehicle.name))

    def onVehicleChanged(self):
        vehicle = g_currentVehicle.item
        if not settings.main[MAIN.UNLOCK_CREW] or Waiting.isOpened('updateTankmen') or not vehicle:
            return
        if vehicle.postProgressionAvailability() and vehicle.isPostProgressionExists:
            value = vehicle.postProgression.getCompletion() == PostProgressionCompletion.FULL
            if self.__vehicle == vehicle.intCD and self.__value == value:
                return
            if vehicle.isXPToTman and not value or not vehicle.isXPToTman and value:
                self.__vehicle = vehicle.intCD
                self.__value = value
                self.accelerateTmenXp(vehicle, value)


tmenXP = AccelerateTmenXp()

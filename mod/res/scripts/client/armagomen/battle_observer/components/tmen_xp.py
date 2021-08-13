from CurrentVehicle import g_currentVehicle
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import MAIN
from armagomen.utils.common import logInfo, overrideMethod
from gui.Scaleform.daapi.view.lobby.hangar.Hangar import Hangar
from gui.shared.gui_items.processors.vehicle import VehicleTmenXPAccelerator
from gui.shared.utils import decorators
from gui.veh_post_progression.models.progression import PostProgressionCompletion


class AccelerateTmenXp(object):
    def __init__(self):
        self.inProcess = False

    @decorators.process('updateTankmen')
    def accelerateTmenXp(self, vehicle, value):
        result = yield VehicleTmenXPAccelerator(vehicle, value).request()
        if result.success:
            logInfo("The accelerated crew training is %s for %s" % (value, vehicle.name))
        self.inProcess = False

    def onVehicleChanged(self):
        vehicle = g_currentVehicle.item
        if not settings.main[MAIN.UNLOCK_CREW] or vehicle is None or self.inProcess:
            return
        if vehicle.postProgressionAvailability():
            value = vehicle.postProgression.getCompletion() == PostProgressionCompletion.FULL
            if vehicle.isXPToTman and not value or not vehicle.isXPToTman and value:
                self.inProcess = True
                self.accelerateTmenXp(vehicle, value)


tmenXP = AccelerateTmenXp()


@overrideMethod(Hangar, "_populate")
def hangarPopulate(base, *args):
    g_currentVehicle.onChanged += tmenXP.onVehicleChanged
    return base(*args)


@overrideMethod(Hangar, "_dispose")
def hangarDispose(base, *args):
    g_currentVehicle.onChanged -= tmenXP.onVehicleChanged
    return base(*args)

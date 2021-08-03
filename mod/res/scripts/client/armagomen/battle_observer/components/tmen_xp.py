from CurrentVehicle import g_currentVehicle
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import MAIN
from armagomen.utils.common import logInfo
from gui.shared.gui_items.processors.vehicle import VehicleTmenXPAccelerator
from gui.shared.utils import decorators
from gui.veh_post_progression.models.progression import PostProgressionCompletion


@decorators.process('updateTankmen')
def accelerateTmenXp(vehicle, value):
    result = yield VehicleTmenXPAccelerator(vehicle, value).request()
    if result.success:
        logInfo("The accelerated crew training is %s for %s" % (value, vehicle.name))


def onVehicleChanged():
    if not settings.main[MAIN.UNLOCK_CREW]:
        return
    vehicle = g_currentVehicle.item
    if vehicle.postProgressionAvailability() and vehicle.isPostProgressionExists:
        value = vehicle.postProgression.getCompletion() == PostProgressionCompletion.FULL
        if vehicle.isXPToTman and not value or not vehicle.isXPToTman and value:
            accelerateTmenXp(vehicle, value)


g_currentVehicle.onChanged += onVehicleChanged

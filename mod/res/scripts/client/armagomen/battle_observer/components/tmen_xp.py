from CurrentVehicle import g_currentVehicle
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import MAIN
from armagomen.utils.common import logInfo
from armagomen.utils.events import g_events
from gui.shared.gui_items.processors.vehicle import VehicleTmenXPAccelerator
from gui.shared.utils import decorators
from gui.veh_post_progression.models.progression import PostProgressionCompletion

FULL = PostProgressionCompletion.FULL


class AccelerateCrewXp(object):

    def __init__(self):
        self.inProcess = False
        g_events.onConnected += self.onConnected
        g_events.onDisconnected += self.onDisconnected

    @decorators.process('updateTankmen')
    def accelerateTmenXp(self, vehicle, value):
        result = yield VehicleTmenXPAccelerator(vehicle, value).request()
        if result.success:
            logInfo("The accelerated crew training is %s for %s" % (value, vehicle.name))
        self.inProcess = False

    @staticmethod
    def checkXP(vehicle):
        xp = 0
        for step in vehicle.postProgression.iterUnorderedSteps():
            xp += step.getPrice().xp
        return vehicle.xp >= xp

    def onVehicleChanged(self):
        if not settings.main[MAIN.CREW_TRAINING]:
            return
        vehicle = g_currentVehicle.item
        if vehicle is None or self.inProcess or not vehicle.isElite or vehicle.isAwaitingBattle:
            return
        value = False
        if vehicle.isFullyElite:
            availability = vehicle.postProgressionAvailability().result
            value = not availability or vehicle.postProgression.getCompletion() is FULL or self.checkXP(vehicle)
        if vehicle.isXPToTman != value:
            self.inProcess = True
            self.accelerateTmenXp(vehicle, value)

    def onConnected(self):
        g_currentVehicle.onChanged += self.onVehicleChanged

    def onDisconnected(self):
        g_currentVehicle.onChanged -= self.onVehicleChanged


crewXP = AccelerateCrewXp()

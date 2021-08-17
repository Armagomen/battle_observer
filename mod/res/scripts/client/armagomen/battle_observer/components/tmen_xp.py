from CurrentVehicle import g_currentVehicle
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import MAIN
from armagomen.utils.common import logInfo
from gui.shared.gui_items.processors.vehicle import VehicleTmenXPAccelerator
from gui.shared.utils import decorators
from gui.veh_post_progression.models.progression import PostProgressionCompletion
from helpers import dependency
from skeletons.gui.shared.utils import IHangarSpace

FULL = PostProgressionCompletion.FULL


class AccelerateCrewXp(object):
    hangarSpace = dependency.descriptor(IHangarSpace)

    def __init__(self):
        self.inProcess = False
        self.hangarSpace.onSpaceCreating += self.onSpaceCreating
        self.hangarSpace.onSpaceDestroy += self.onSpaceDestroy

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
        if vehicle is None or self.inProcess or not vehicle.isElite or vehicle.isLocked:
            return
        value = False
        if vehicle.isFullyElite:
            availability = vehicle.postProgressionAvailability().result
            value = not availability or vehicle.postProgression.getCompletion() is FULL or self.checkXP(vehicle)
        if vehicle.isXPToTman != value:
            self.inProcess = True
            self.accelerateTmenXp(vehicle, value)

    def onSpaceCreating(self):
        g_currentVehicle.onChanged += self.onVehicleChanged

    def onSpaceDestroy(self, inited):
        g_currentVehicle.onChanged -= self.onVehicleChanged


crewXP = AccelerateCrewXp()

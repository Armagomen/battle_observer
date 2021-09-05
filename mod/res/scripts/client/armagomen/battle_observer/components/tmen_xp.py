from CurrentVehicle import g_currentVehicle
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import MAIN
from armagomen.utils.common import logInfo, callback
from gui.shared.gui_items.processors.vehicle import VehicleTmenXPAccelerator
from gui.shared.utils import decorators
from gui.veh_post_progression.models.progression import PostProgressionCompletion
from helpers import dependency
from skeletons.gui.shared.utils import IHangarSpace


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
        iterator = vehicle.postProgression.iterOrderedSteps()
        return vehicle.xp >= sum(x.getPrice().xp for x in iterator if not x.isRestricted() and not x.isReceived())

    def onChanged(self):
        callback(1.0, self.onVehicleChanged)

    def onVehicleChanged(self):
        if not settings.main[MAIN.CREW_TRAINING]:
            return
        vehicle = g_currentVehicle.item
        if vehicle is None or vehicle.isLocked or self.inProcess or not vehicle.isElite:
            return
        value = False
        if vehicle.isFullyElite:
            availability = vehicle.postProgressionAvailability().result
            complete = vehicle.postProgression.getCompletion() is PostProgressionCompletion.FULL
            value = not availability or complete or self.checkXP(vehicle)
        if vehicle.isXPToTman != value:
            self.inProcess = True
            self.accelerateTmenXp(vehicle, value)

    def onSpaceCreating(self):
        g_currentVehicle.onChanged += self.onChanged

    def onSpaceDestroy(self, inited):
        g_currentVehicle.onChanged -= self.onChanged


crewXP = AccelerateCrewXp()

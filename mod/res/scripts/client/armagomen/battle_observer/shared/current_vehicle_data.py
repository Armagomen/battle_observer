import math
from collections import namedtuple

from armagomen._logger import IALogger
from armagomen.battle_observer.shared.interface import IBOCurrentVehicleCachedData
from armagomen.battle_observer.shared.on_vehicle_change import OnVehicleChangeSubscribed
from dossiers2.ui.achievements import MARK_ON_GUN_RECORD
from Event import SafeEvent
from helpers import dependency
from skeletons.gui.shared import IItemsCache

PARAMS = ("tankAvgDamage", "tankAvgAssist", "tankAvgStun", "tankAvgBlocked", "marksRating", "marksValue", "name", "marksAvailable",
          "winRate", "battles")
EfficiencyAVGData = namedtuple("EfficiencyAVGData", PARAMS)


class CurrentVehicleCachedData(OnVehicleChangeSubscribed, IBOCurrentVehicleCachedData):
    __slots__ = ("__EfficiencyAVGData", "__default", "onChanged")
    itemsCache = dependency.descriptor(IItemsCache)
    logger = dependency.descriptor(IALogger)

    def __init__(self):
        self.logger.logInfo("Initializing CurrentVehicleCachedData")
        self.onChanged = SafeEvent()
        default = 2000
        self.__default = EfficiencyAVGData(default, default, default, 0, 0.0, 0, "Undefined", False, 0.0, 0)
        self.__EfficiencyAVGData = None
        super(CurrentVehicleCachedData, self).__init__()

    def fini(self):
        super(CurrentVehicleCachedData, self).fini()
        self.logger.logInfo("Finished CurrentVehicleCachedData")

    def onVehicleChanged(self, vehicle):
        self.__EfficiencyAVGData = self.setAvgData(vehicle) if vehicle is not None else None
        self.onChanged(self.__EfficiencyAVGData)

    def setAvgData(self, vehicle):
        dossier = self.itemsCache.items.getVehicleDossier(vehicle.intCD)
        random = dossier.getRandomStats()
        marks = random.getAchievement(MARK_ON_GUN_RECORD)
        return EfficiencyAVGData(
            int(random.getAvgDamage() or 0),
            int(random.getDamageAssistedEfficiency() or 0),
            int(random.getAvgDamageAssistedStun() or 0),
            int(math.ceil(random.getAvgDamageBlocked() or 0.0)),
            marks.getDamageRating(),
            marks.getValue(),
            vehicle.userName,
            vehicle.level > 4,
            (random.getWinsEfficiency() or 0.0),
            int(random.getBattlesCount())
        )

    @property
    def efficiencyAvgData(self):
        return self.__EfficiencyAVGData or self.__default

    @property
    def default(self):
        return self.__default

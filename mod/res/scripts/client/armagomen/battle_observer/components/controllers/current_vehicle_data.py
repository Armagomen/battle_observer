from collections import namedtuple

from CurrentVehicle import g_currentVehicle
from dossiers2.ui.achievements import MARK_ON_GUN_RECORD
from helpers import dependency
from skeletons.gui.shared import IItemsCache

PARAMS = ("tankAvgDamage", "tankAvgAssist", "tankAvgStun", "tankAvgBlocked", "marksOnGunValue", "marksOnGunIcon", "name", "marksAvailable",
          "winRate", "battles")
EfficiencyAVGData = namedtuple("EfficiencyAVGData", PARAMS)


class CurrentVehicleCachedData(object):
    __slots__ = ("__EfficiencyAVGData", "__default")
    itemsCache = dependency.descriptor(IItemsCache)

    def __init__(self):
        default = 3000
        self.__default = EfficiencyAVGData(default, default, default, 0, 0.0, "", "Undefined", False, 0.0, 0)
        self.__EfficiencyAVGData = None

    def onVehicleChanged(self):
        if g_currentVehicle.isPresent():
            self.setAvgData(g_currentVehicle.intCD, g_currentVehicle.item.userName, g_currentVehicle.item.level)
        else:
            self.__EfficiencyAVGData = None

    def setAvgData(self, intCD, name, level):
        dossier = self.itemsCache.items.getVehicleDossier(intCD)
        random = dossier.getRandomStats()
        marks = random.getAchievement(MARK_ON_GUN_RECORD)
        blocked = random.getAvgDamageBlocked() or 0
        self.__EfficiencyAVGData = EfficiencyAVGData(
            int(random.getAvgDamage() or 0),
            int(random.getDamageAssistedEfficiency() or 0),
            int(random.getAvgDamageAssistedStun() or 0),
            int(blocked) if blocked > 99 else round(blocked, 2),
            marks.getDamageRating(),
            "<img src='img://gui/{}' width='20' height='18' vspace='-8'>".format(marks.getIcons()[marks.IT_95X85][3:]),
            name,
            level > 4,
            (random.getWinsEfficiency() or 0.0) * 100,
            int(random.getBattlesCount())
        )

    @property
    def efficiencyAvgData(self):
        return self.__EfficiencyAVGData or self.__default

    @property
    def default(self):
        return self.__default

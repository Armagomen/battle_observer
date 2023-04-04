from collections import namedtuple

from CurrentVehicle import g_currentVehicle
from armagomen.utils.common import logDebug
from armagomen.utils.events import g_events
from dossiers2.ui.achievements import MARK_ON_GUN_RECORD
from helpers import dependency
from skeletons.gui.shared import IItemsCache

EfficiencyAVGData = namedtuple("EfficiencyAVGData", (
    "damage", "assist", "stun", "blocked", "marksOnGunValue", "marksOnGunIcon", "name", "marksAvailable"))


class CurrentVehicleCachedData(object):
    itemsCache = dependency.descriptor(IItemsCache)

    def __init__(self):
        self.__default = EfficiencyAVGData(0, 0, 0, 0, 0, "", "Undefined", False)
        self.__EfficiencyAVGData = None

    def onVehicleChanged(self):
        if g_currentVehicle.isPresent():
            self.setAvgData(g_currentVehicle.intCD, g_currentVehicle.item.userName, g_currentVehicle.item.level)
        else:
            self.__EfficiencyAVGData = None

    def setAvgData(self, intCD, name, level):
        dossier = self.itemsCache.items.getVehicleDossier(intCD)
        random = dossier.getRandomStats()
        marksOnGun = random.getAchievement(MARK_ON_GUN_RECORD)
        icon = marksOnGun.getIcons()['95x85'][3:]
        marksOnGunIcon = "<img src='img://gui/{}' width='22' height='20' vspace='-10'>".format(icon)
        self.__EfficiencyAVGData = EfficiencyAVGData(
            int(random.getAvgDamage() or 0),
            int(random.getDamageAssistedEfficiency() or 0),
            int(random.getAvgDamageAssistedStun() or 0),
            int(random.getAvgDamageBlocked() or 0),
            round(marksOnGun.getDamageRating(), 2), marksOnGunIcon, name, level > 4)
        logDebug(self.__EfficiencyAVGData)
        g_events.onAVGDataUpdated(self.__EfficiencyAVGData)

    @property
    def efficiencyAvgData(self):
        return self.__EfficiencyAVGData or self.__default

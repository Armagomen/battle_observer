from collections import namedtuple

from armagomen.battle_observer.settings import user_settings
from armagomen.utils.logging import DEBUG, logDebug
from CurrentVehicle import g_currentVehicle
from dossiers2.ui.achievements import MARK_ON_GUN_RECORD
from helpers import dependency
from skeletons.gui.shared import IItemsCache

EfficiencyAVGData = namedtuple("EfficiencyAVGData", (
    "damage", "assist", "stun", "blocked", "marksOnGunValue", "marksOnGunIcon", "name", "marksAvailable", "winRate"))


class CurrentVehicleCachedData(object):
    itemsCache = dependency.descriptor(IItemsCache)

    def __init__(self):
        default = 2500
        self.__default = EfficiencyAVGData(default, default, default, 0, 0.0, "", "Undefined", False, 0.0)
        self.__EfficiencyAVGData = None

    def onVehicleChanged(self):
        if g_currentVehicle.isPresent():
            self.setAvgData(g_currentVehicle.intCD, g_currentVehicle.item.userName, g_currentVehicle.item.level)
        else:
            self.__EfficiencyAVGData = None

    @staticmethod
    def getWinsEfficiency(random):
        win_rate = random.getWinsEfficiency()
        return round(win_rate * 100, 2) if win_rate is not None else 0.0

    def setAvgData(self, intCD, name, level):
        dossier = self.itemsCache.items.getVehicleDossier(intCD)
        random = dossier.getRandomStats()
        marksOnGun = random.getAchievement(MARK_ON_GUN_RECORD)
        icon = marksOnGun.getIcons()['95x85'][3:]
        marksOnGunIcon = "<img src='img://gui/{}' width='20' height='18' vspace='-8'>".format(icon)
        blocked = random.getAvgDamageBlocked() or 0
        self.__EfficiencyAVGData = EfficiencyAVGData(
            int(random.getAvgDamage() or 0),
            int(random.getDamageAssistedEfficiency() or 0),
            int(random.getAvgDamageAssistedStun() or 0),
            int(blocked) if blocked > 99 else round(blocked, 2),
            round(marksOnGun.getDamageRating(), 2), marksOnGunIcon, name, level > 4, self.getWinsEfficiency(random)
        )
        if user_settings.main[DEBUG]:
            logDebug(self.__EfficiencyAVGData)

    @property
    def efficiencyAvgData(self):
        return self.__EfficiencyAVGData or self.__default

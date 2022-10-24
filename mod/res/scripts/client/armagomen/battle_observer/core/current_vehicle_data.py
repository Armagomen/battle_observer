import math
from collections import namedtuple

from CurrentVehicle import g_currentVehicle
from armagomen.utils.common import logError, logDebug
from constants import ROLE_TYPE

EfficiencyAVGData = namedtuple("EfficiencyAVGData", ("damage", "assist"))


class CurrentVehicleCachedData(object):

    def __init__(self):
        self.__isSPG = False
        self.__EfficiencyAVGData = EfficiencyAVGData(0, 0)

    def init(self):
        g_currentVehicle.onChanged += self.onVehicleChanged

    def fini(self):
        g_currentVehicle.onChanged -= self.onVehicleChanged

    def onVehicleChanged(self):
        self.__isSPG = g_currentVehicle.item.role == ROLE_TYPE.SPG
        damage = 0
        assist = 0
        try:
            dossier = g_currentVehicle.getDossier()
            if dossier:
                random = dossier.getRandomStats()
                d_damage = random.getAvgDamage()
                d_assist = random.getDamageAssistedEfficiency()
                if d_damage is not None:
                    damage = int(math.floor(d_damage))
                if d_assist is not None:
                    assist = int(math.floor(d_assist))
        except Exception as error:
            logError(repr(error))
        finally:
            self.__EfficiencyAVGData = EfficiencyAVGData(damage, assist)
        logDebug("set vehicle efficiency {} avgDamage={}, avgAssist={}", g_currentVehicle.item.userName, damage, assist)

    @property
    def efficiencyAvgData(self):
        return self.__EfficiencyAVGData

    @property
    def isSPG(self):
        return self.__isSPG

import math
from collections import namedtuple

from CurrentVehicle import g_currentVehicle
from PlayerEvents import g_playerEvents
from armagomen.utils.common import logError, logDebug

EfficiencyAVGData = namedtuple("EfficiencyAVGData", ("damage", "assist", "stun", "blocked"))
DEBUG_STRING = "set vehicle cache: name={} avgDamage={}, avgAssist={}, stun={}, blocked={}"


class CurrentVehicleCachedData(object):

    def __init__(self):
        self.__EfficiencyAVGData = EfficiencyAVGData(0, 0, 0, 0)

    def init(self):
        g_playerEvents.onArenaCreated += self.onArenaCreated

    def fini(self):
        g_playerEvents.onArenaCreated -= self.onArenaCreated

    def onArenaCreated(self):
        damage = 0
        assist = 0
        stun = 0
        blocked = 0
        try:
            dossier = g_currentVehicle.getDossier()
            if dossier:
                random = dossier.getRandomStats()
                d_damage = random.getAvgDamage()
                d_assist = random.getDamageAssistedEfficiency()
                d_stun = random.getAvgDamageAssistedStun()
                d_blocked = random.getAvgDamageBlocked()
                if d_damage is not None:
                    damage = int(math.floor(d_damage))
                if d_assist is not None:
                    assist = int(math.floor(d_assist))
                if d_stun is not None:
                    stun = int(math.floor(d_stun))
                if d_blocked is not None:
                    blocked = int(math.floor(d_blocked))
        except Exception as error:
            logError(repr(error))
        finally:
            self.__EfficiencyAVGData = EfficiencyAVGData(damage, assist, stun, blocked)
        logDebug(DEBUG_STRING, g_currentVehicle.item.userName, *self.__EfficiencyAVGData)

    @property
    def efficiencyAvgData(self):
        return self.__EfficiencyAVGData

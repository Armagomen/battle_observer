from __future__ import absolute_import, division

from armagomen._constants import ARMOR_CALC, GLOBAL
from armagomen._logger import IALogger
from armagomen.battle_observer.settings.interface import IBOSettingsLoader
from armagomen.battle_observer.shared.interface import IShotResultHelper
from armagomen.battle_observer.shared.on_vehicle_change import isSpecialBattleVehicle
from constants import QUEUE_TYPE
from Event import Event
from gui.shared.gui_items.Tankman import crewMemberRealSkillLevel, tankmen
from helpers import dependency
from PlayerEvents import g_playerEvents


class BOEvent(Event):

    def __call__(self, *args, **kwargs):
        for delegate in self:
            delegate(*args, **kwargs)


class ShotResultHelper(IShotResultHelper):
    logger = dependency.descriptor(IALogger)
    settingsLoader = dependency.instance(IBOSettingsLoader)

    QUEUE_TYPES = (QUEUE_TYPE.RANDOMS, QUEUE_TYPE.FUN_RANDOM, QUEUE_TYPE.UNKNOWN, QUEUE_TYPE.COMP7_LIGHT, QUEUE_TYPE.COMP7,
                   QUEUE_TYPE.MAPS_TRAINING, QUEUE_TYPE.WINBACK)

    RND_MIN_MAX_INFO = 'ShotResultHelper: final randomization: {}/{}, vehicle: {}'
    RND_ERROR = 'ShotResultHelper: ERROR: {}'

    def __init__(self):
        self.onArmorChanged = BOEvent()
        self.onMarkerColorChanged = BOEvent()
        g_playerEvents.onEnqueued += self.onEnqueued
        self.skills = ('gunner_armorer', 'loader_ammunitionImprove')
        self.__defaults = (0.75, 1.25)
        self.__pp_min_multiplier, self.__pp_max_multiplier = self.__defaults
        self.logger.logInfo("Initializing ShotResultHelper")

    def fini(self):
        g_playerEvents.onEnqueued += self.onEnqueued
        self.logger.logInfo("Finished ShotResultHelper")

    def onEnqueued(self, queueType, *args):
        if queueType in self.QUEUE_TYPES:
            from CurrentVehicle import g_currentVehicle
            self.updateRandomization(g_currentVehicle.item)
        else:
            self.resetToDefault()

    def resetToDefault(self):
        self.__pp_min_multiplier, self.__pp_max_multiplier = self.__defaults

    def updateRandomization(self, vehicle):
        self.resetToDefault()
        if isSpecialBattleVehicle(vehicle) or not self.settingsLoader.getSetting(ARMOR_CALC.NAME, GLOBAL.ENABLED):
            return
        try:
            for skill_name in self.skills:
                real_skill_level = crewMemberRealSkillLevel(vehicle, skill_name)
                if real_skill_level == tankmen.NO_SKILL:
                    continue
                skill_kpi = tankmen.getSkillsConfig().getSkill(skill_name).kpi
                for kpi in skill_kpi:
                    delta = real_skill_level * round((kpi.value - 1.0) * 0.01, 4)
                    if kpi.isPositive:
                        self.__pp_min_multiplier += delta
                    else:
                        self.__pp_max_multiplier += delta
            self.logger.logInfo(self.RND_MIN_MAX_INFO, self.__pp_min_multiplier, self.__pp_max_multiplier, vehicle.userName)
        except Exception as e:
            self.logger.logError(self.RND_ERROR, e)

    def getMinMaxPiercingPower(self, power):
        return power * self.__pp_min_multiplier, power * self.__pp_max_multiplier

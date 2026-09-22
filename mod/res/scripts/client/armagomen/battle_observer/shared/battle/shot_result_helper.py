from collections import defaultdict

from armagomen._constants import ARMOR_CALC, GLOBAL
from armagomen._logger import IALogger
from armagomen.battle_observer.shared.interface import IShotResultHelper
from armagomen.utils.common import MinMax
from constants import QUEUE_TYPE
from Event import Event
from helpers import dependency
from PlayerEvents import g_playerEvents


class BOEvent(Event):

    def __call__(self, *args, **kwargs):
        for delegate in self:
            delegate(*args, **kwargs)


class ShotResultHelper(IShotResultHelper):
    logger = dependency.descriptor(IALogger)

    QUEUE_TYPES = (QUEUE_TYPE.RANDOMS, QUEUE_TYPE.FUN_RANDOM, QUEUE_TYPE.UNKNOWN, QUEUE_TYPE.COMP7_LIGHT, QUEUE_TYPE.COMP7,
                   QUEUE_TYPE.MAPS_TRAINING, QUEUE_TYPE.WINBACK)
    GUNNER_ARMORER = 'gunner_armorer'
    LOADER_AMMUNITION_IMPROVE = 'loader_ammunitionImprove'
    RND_MIN_MAX_INFO = 'ShotResultHelper: final randomization: {}/{}, vehicle: {}, skills: {}'
    RND_SKILL_DIFF_DEBUG = 'ShotResultHelper: skill_name: {} skill_lvl: {} level_increase: {} percent: {}'
    RND_SKILL_NOT_FOUND = 'ShotResultHelper: SKILL_NOT_FOUND skill_name: {}'
    RND_SET_PIERCING_DISTRIBUTION_BOUND_DEBUG = 'ShotResultHelper setSkillsBound: {}'
    RND_ERROR = 'ShotResultHelper: ERROR: {}'

    __slots__ = ('__bound', 'min', 'max', '__defaults')

    def __init__(self):
        self.logger.logInfo("Initializing ShotResultHelper")
        g_playerEvents.onEnqueued += self.onEnqueued
        self.__defaults = MinMax(0.75, 1.25)
        self.pp_min = self.__defaults.min
        self.pp_max = self.__defaults.max
        self.__bound = {self.GUNNER_ARMORER: 0.0005, self.LOADER_AMMUNITION_IMPROVE: 0.0002}
        self.onArmorChanged = BOEvent()
        self.onMarkerColorChanged = BOEvent()

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
        if self.pp_min != self.__defaults.min:
            self.pp_min = self.__defaults.min
        if self.pp_max != self.__defaults.max:
            self.pp_max = self.__defaults.max

    def getCurrentSkillEfficiency(self, tman, skill_name):
        skill = tman.skillsMap.get(skill_name)
        if skill is not None and skill.level > 0:
            level_increase, bonuses = tman.crewLevelIncrease
            result = ((skill.level + level_increase) * tman.skillsEfficiency) * self.__bound[skill_name]
            self.logger.logDebug(self.RND_SKILL_DIFF_DEBUG, skill_name, skill.level, level_increase, result)
            return result
        return 0.0

    def updateRandomization(self, vehicle):
        from armagomen.battle_observer.settings.interface import IBOSettingsLoader
        settingsLoader = dependency.instance(IBOSettingsLoader)
        self.resetToDefault()
        if vehicle is None or not settingsLoader.getSetting(ARMOR_CALC.NAME, GLOBAL.ENABLED):
            return
        try:
            data = defaultdict(list)
            for _, tman in vehicle.crew:
                if not tman or not tman.canUseSkillsInCurrentVehicle:
                    continue
                for skill_name in tman.getPossibleSkills().intersection(self.__bound):
                    data[skill_name].append(self.getCurrentSkillEfficiency(tman, skill_name))
            for skill_name, value in data.items():
                if not value:
                    continue
                percent = sum(value) / len(value)
                self.min += percent
                if skill_name == self.GUNNER_ARMORER:
                    self.max -= percent
            self.logger.logInfo(self.RND_MIN_MAX_INFO, self.min, self.max, vehicle.userName, data)
        except Exception as e:
            self.logger.logError(self.RND_ERROR, e)

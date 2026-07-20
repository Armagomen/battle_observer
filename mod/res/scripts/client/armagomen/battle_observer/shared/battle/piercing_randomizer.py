from armagomen import IALogger
from armagomen._constants import ARMOR_CALC, GLOBAL
from collections import defaultdict
from constants import QUEUE_TYPE
from gui.shared.gui_items import KPI
from helpers import dependency
from items.tankmen import getSkillsConfig
from PlayerEvents import g_playerEvents


class IBOPiercingRandomizer(object):

    def fini(self):
        raise NotImplementedError

    def updateRandomization(self, vehicle):
        raise NotImplementedError


class PiercingRandomizer(IBOPiercingRandomizer):
    logger = dependency.descriptor(IALogger)

    DEFAULT_RANDOMIZATION = (0.75, 1.25)
    QUEUE_TYPES = (QUEUE_TYPE.RANDOMS, QUEUE_TYPE.FUN_RANDOM, QUEUE_TYPE.UNKNOWN, QUEUE_TYPE.COMP7_LIGHT, QUEUE_TYPE.COMP7,
                   QUEUE_TYPE.MAPS_TRAINING, QUEUE_TYPE.WINBACK)
    GUNNER_ARMORER = 'gunner_armorer'
    LOADER_AMMUNITION_IMPROVE = 'loader_ammunitionImprove'
    RND_MIN_MAX_INFO = 'PiercingRandomizer: final randomization: {}/{}, vehicle: {}, skills: {}'
    RND_SKILL_DIFF_DEBUG = 'PiercingRandomizer: skill_name: {} skill_lvl: {} level_increase: {} percent: {}'
    RND_SKILL_NOT_FOUND = 'PiercingRandomizer: SKILL_NOT_FOUND skill_name: {}'
    RND_SET_PIERCING_DISTRIBUTION_BOUND_DEBUG = 'PiercingRandomizer setSkillsBound: {}'
    RND_ERROR = 'PiercingRandomizer: ERROR: {}'

    __slots__ = ['__bound', 'min', 'max']

    def __init__(self):
        self.logger.logInfo("Initializing PiercingRandomizer")
        g_playerEvents.onEnqueued += self.onEnqueued
        self.min, self.max = self.DEFAULT_RANDOMIZATION
        self.__bound = defaultdict(float)

        for skill_name in (self.GUNNER_ARMORER, self.LOADER_AMMUNITION_IMPROVE):
            descrArgs = getSkillsConfig().getSkill(skill_name).uiSettings.descrArgs
            for name, descr in descrArgs:
                if name == KPI.Name.DAMAGE_AND_PIERCING_DISTRIBUTION_LOWER_BOUND:
                    self.__bound[skill_name] = round(descr.value, 4)
                    break

        self.logger.logDebug(self.RND_SET_PIERCING_DISTRIBUTION_BOUND_DEBUG, self.__bound)

    def fini(self):
        g_playerEvents.onEnqueued += self.onEnqueued
        self.logger.logInfo("Finished PiercingRandomizer")

    def onEnqueued(self, queueType, *args):
        if queueType in self.QUEUE_TYPES:
            from CurrentVehicle import g_currentVehicle
            self.updateRandomization(g_currentVehicle.item)
        else:
            self.min, self.max = self.DEFAULT_RANDOMIZATION

    def getCurrentSkillEfficiency(self, tman, skill_name):
        skill = tman.skillsMap.get(skill_name)
        if skill is not None and skill.level > 0:
            level_increase, bonuses = tman.crewLevelIncrease
            result = ((skill.level + level_increase) * tman.skillsEfficiency) * self.__bound[skill_name]
            self.logger.logDebug(self.RND_SKILL_DIFF_DEBUG, skill_name, skill.level, level_increase, result)
            return result
        return 0.0

    def updateRandomization(self, vehicle):
        from armagomen.battle_observer.settings import IBOSettingsLoader
        settingsLoader = dependency.instance(IBOSettingsLoader)
        self.min, self.max = self.DEFAULT_RANDOMIZATION
        if vehicle is None or not settingsLoader.getSetting(ARMOR_CALC.NAME, GLOBAL.ENABLED):
            return
        try:
            data = {self.GUNNER_ARMORER: [], self.LOADER_AMMUNITION_IMPROVE: []}
            for _, tman in vehicle.crew:
                if not tman or not tman.canUseSkillsInCurrentVehicle:
                    continue
                for skill_name in tman.getPossibleSkills().intersection(data.keys()):
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

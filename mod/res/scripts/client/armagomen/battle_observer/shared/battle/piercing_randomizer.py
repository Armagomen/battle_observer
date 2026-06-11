from collections import defaultdict

from armagomen import IALogger
from armagomen._constants import ARMOR_CALC, GLOBAL
from armagomen.utils.common import MinMax
from armagomen.utils.events import g_events
from gui.shared.gui_items import KPI
from helpers import dependency
from items.tankmen import getSkillsConfig


class IBOPiercingRandomizer(object):

    def fini(self):
        raise NotImplementedError

    def updateRandomization(self, vehicle):
        raise NotImplementedError

    @property
    def confines(self):
        raise NotImplementedError


class PiercingRandomizer(IBOPiercingRandomizer):
    logger = dependency.descriptor(IALogger)

    DEFAULT_RANDOMIZATION = MinMax(0.75, 1.25)
    GUNNER_ARMORER = 'gunner_armorer'
    LOADER_AMMUNITION_IMPROVE = 'loader_ammunitionImprove'
    RND_MIN_MAX_INFO = 'PiercingRandomizer: final randomization: {}, vehicle: {}, skills: {}'
    RND_SKILL_DIFF_DEBUG = 'PiercingRandomizer: skill_name: {} skill_lvl: {} level_increase: {} percent: {}'
    RND_SKILL_NOT_FOUND = 'PiercingRandomizer: SKILL_NOT_FOUND skill_name: {}'
    RND_SET_PIERCING_DISTRIBUTION_BOUND_DEBUG = 'PiercingRandomizer getMaxSkillPercent: skill_name {}, percent {}'

    __slots__ = ['__confines', '__bound']

    def __init__(self):
        self.logger.logInfo("Initializing PiercingRandomizer")
        g_events.onVehicleChangedDelayed += self.updateRandomization
        self.__confines = None
        self.__bound = defaultdict(float)

    def fini(self):
        g_events.onVehicleChangedDelayed -= self.updateRandomization
        self.logger.logInfo("Finished PiercingRandomizer")

    def getMaxSkillBound(self, skill_name):
        if not self.__bound[skill_name]:
            descrArgs = getSkillsConfig().getSkill(skill_name).uiSettings.descrArgs
            for name, descr in descrArgs:
                if name == KPI.Name.DAMAGE_AND_PIERCING_DISTRIBUTION_LOWER_BOUND:
                    value = round(descr.value, 4)
                    self.__bound[skill_name] = value
                    self.logger.logDebug(self.RND_SET_PIERCING_DISTRIBUTION_BOUND_DEBUG, skill_name, value)
                    break
        return self.__bound[skill_name]

    @property
    def confines(self):
        return self.__confines or self.DEFAULT_RANDOMIZATION

    def getCurrentSkillEfficiency(self, tman, skill_name):
        skill = tman.skillsMap.get(skill_name)
        if skill is None:
            self.logger.logDebug(self.RND_SKILL_NOT_FOUND, skill_name)
            return 0
        level_increase, bonuses = tman.crewLevelIncrease
        result = (skill.level + level_increase) * tman.skillsEfficiency * self.getMaxSkillBound(skill_name)
        self.logger.logDebug(self.RND_SKILL_DIFF_DEBUG, skill_name, skill.level, level_increase, result)
        return result

    def updateRandomization(self, vehicle):
        from armagomen.battle_observer.settings import IBOSettingsLoader
        settingsLoader = dependency.instance(IBOSettingsLoader)
        if vehicle is None or not settingsLoader.getSetting(ARMOR_CALC.NAME, GLOBAL.ENABLED):
            self.__confines = None
            return
        data = {self.GUNNER_ARMORER: [], self.LOADER_AMMUNITION_IMPROVE: []}
        for _, tman in vehicle.crew:
            if not tman or not tman.canUseSkillsInCurrentVehicle:
                continue
            for skill_name in tman.getPossibleSkills().intersection(data.keys()):
                data[skill_name].append(self.getCurrentSkillEfficiency(tman, skill_name))
        randomization_min, randomization_max = self.DEFAULT_RANDOMIZATION
        skills = data.items()
        for skill_name, value in skills:
            if value:
                percent = sum(value) / len(value)
                randomization_min += percent
                if skill_name == self.GUNNER_ARMORER:
                    randomization_max -= percent
        self.__confines = MinMax(round(randomization_min, 4), round(randomization_max, 4))
        self.logger.logInfo(self.RND_MIN_MAX_INFO, self.__confines, vehicle.userName, skills)

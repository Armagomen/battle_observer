from armagomen._constants import ARMOR_CALC, GLOBAL
from armagomen.battle_observer.settings import IBOSettingsLoader
from armagomen.utils.common import MinMax
from armagomen.utils.events import g_events
from armagomen.utils.logging import logDebug
from gui.shared.gui_items import KPI
from helpers import dependency
from items.tankmen import getSkillsConfig


class PiercingRandomizer(object):
    settingsLoader = dependency.descriptor(IBOSettingsLoader)

    DEFAULT_RANDOMIZATION = MinMax(0.75, 1.25)
    GUNNER_ARMORER = 'gunner_armorer'
    LOADER_AMMUNITION_IMPROVE = 'loader_ammunitionImprove'
    RND_MIN_MAX_DEBUG = 'PIERCING_POWER_RANDOMIZATION: {}, vehicle: {}'
    RND_SKILL_DIFF_DEBUG = 'PIERCING_POWER_RANDOMIZATION: skill_name: {} skill_lvl: {} level_increase: {} percent: {}'
    RND_SKILL_NOT_FOUND = 'PIERCING_POWER_RANDOMIZATION: SKILL_NOT_FOUND skill_name: {}'
    RND_SET_PIERCING_DISTRIBUTION_BOUND_DEBUG = 'PIERCING_POWER_RANDOMIZATION: skill_name {}, percent {}'

    PIERCING_DISTRIBUTION_BOUND = {}

    def __init__(self):
        self.__confines = None

    def init(self):
        g_events.onVehicleChangedDelayed += self.updateRandomization

    def fini(self):
        g_events.onVehicleChangedDelayed -= self.updateRandomization

    def getBaseSkillPercent(self, skill_name):
        percent = self.PIERCING_DISTRIBUTION_BOUND.get(skill_name, 0)
        if not percent:
            descrArgs = getSkillsConfig().getSkill(skill_name).uiSettings.descrArgs
            for name, descr in descrArgs:
                if name == KPI.Name.DAMAGE_AND_PIERCING_DISTRIBUTION_LOWER_BOUND:
                    percent = self.PIERCING_DISTRIBUTION_BOUND[skill_name] = round(descr.value, 4)
                    logDebug(self.RND_SET_PIERCING_DISTRIBUTION_BOUND_DEBUG, skill_name, percent)
                break
        return percent

    @property
    def confines(self):
        return self.__confines or self.DEFAULT_RANDOMIZATION

    def getCurrentSkillEfficiency(self, tman, skill_name):
        skill = tman.skillsMap.get(skill_name)
        if skill is None:
            logDebug(self.RND_SKILL_NOT_FOUND, skill_name)
            return 0
        level_increase, bonuses = tman.crewLevelIncrease
        result = (skill.level + level_increase) * tman.skillsEfficiency * self.getBaseSkillPercent(skill_name)
        logDebug(self.RND_SKILL_DIFF_DEBUG, skill_name, skill.level, level_increase, result)
        return result

    def updateRandomization(self, vehicle):
        if vehicle is None or not self.settingsLoader.getSetting(ARMOR_CALC.NAME, GLOBAL.ENABLED):
            self.__confines = None
            return
        data = {self.GUNNER_ARMORER: [], self.LOADER_AMMUNITION_IMPROVE: []}
        for _, tman in vehicle.crew:
            if not tman or not tman.canUseSkillsInCurrentVehicle:
                continue
            for skill_name in tman.getPossibleSkills().intersection(data.keys()):
                data[skill_name].append(self.getCurrentSkillEfficiency(tman, skill_name))
        randomization_min, randomization_max = self.DEFAULT_RANDOMIZATION
        for skill_name, value in data.items():
            if value:
                percent = sum(value) / len(value)
                randomization_min += percent
                if skill_name == self.GUNNER_ARMORER:
                    randomization_max -= percent
        self.__confines = MinMax(round(randomization_min, 4), round(randomization_max, 4))
        logDebug(self.RND_MIN_MAX_DEBUG, self.__confines, vehicle.userName)

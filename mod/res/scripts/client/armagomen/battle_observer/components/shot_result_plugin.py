from collections import namedtuple

from aih_constants import SHOT_RESULT
from armagomen._constants import ARMOR_CALC, GLOBAL, IS_LESTA
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import getPlayer, overrideMethod
from armagomen.utils.events import g_events
from armagomen.utils.logging import logDebug
from AvatarInputHandler.gun_marker_ctrl import _CrosshairShotResults
from constants import SHELL_MECHANICS_TYPE, SHELL_TYPES
from CurrentVehicle import g_currentVehicle
from DestructibleEntity import DestructibleEntity
from gui.battle_control import avatar_getter
from gui.Scaleform.daapi.view.battle.epic.battle_carousel import BattleCarouselDataProvider
from gui.Scaleform.daapi.view.battle.shared.crosshair import plugins
from gui.Scaleform.genConsts.CROSSHAIR_VIEW_ID import CROSSHAIR_VIEW_ID
from items.components.component_constants import DEFAULT_PIERCING_POWER_RANDOMIZATION, \
    MODERN_HE_PIERCING_POWER_REDUCTION_FACTOR_FOR_SHIELDS
from Vehicle import Vehicle

MinMax = namedtuple("MinMax", ("min", "max"))
DEFAULT_RANDOMIZATION = MinMax(1.0 - DEFAULT_PIERCING_POWER_RANDOMIZATION, 1.0 + DEFAULT_PIERCING_POWER_RANDOMIZATION)


class _ShotResult(_CrosshairShotResults):
    RANDOMIZATION = DEFAULT_RANDOMIZATION
    UNDEFINED_RESULT = (SHOT_RESULT.UNDEFINED, None)
    _JET_FACTOR = 0.001
    ENTITY_TYPES = (Vehicle, DestructibleEntity)

    @staticmethod
    def _isAlly(entity, player, onAlly):
        return False if onAlly else entity.publicInfo['team'] == player.team

    @classmethod
    def _getShotResult(cls, hitPoint, collision, direction, multiplier, onAlly, player):
        if player is None or collision is None:
            return cls.UNDEFINED_RESULT
        entity = collision.entity
        if not isinstance(entity, cls.ENTITY_TYPES) or not entity.isAlive() or cls._isAlly(entity, player, onAlly):
            return cls.UNDEFINED_RESULT
        c_details = cls._getAllCollisionDetails(hitPoint, direction, entity)
        if c_details is None:
            return cls.UNDEFINED_RESULT
        shot = player.getVehicleDescriptor().shot
        distance = player.position.flatDistTo(hitPoint)
        piercing_power = cls._computePiercingPowerAtDist(shot.piercingPower, distance, shot.maxDistance, multiplier)
        if cls._isModernMechanics(shot.shell):
            return cls._computeArmorModern(c_details, shot.shell, piercing_power)
        else:
            return cls._computeArmorDefault(c_details, shot.shell, piercing_power)

    @classmethod
    def _checkShotResult(cls, data):
        armor, piercing_power, _, ricochet, no_damage = data
        if no_damage or ricochet:
            return SHOT_RESULT.NOT_PIERCED
        elif armor < piercing_power * cls.RANDOMIZATION.min:
            return SHOT_RESULT.GREAT_PIERCED
        elif armor > piercing_power * cls.RANDOMIZATION.max:
            return SHOT_RESULT.NOT_PIERCED
        else:
            return SHOT_RESULT.LITTLE_PIERCED

    @staticmethod
    def _isModernMechanics(shell):
        return shell.kind == SHELL_TYPES.HIGH_EXPLOSIVE and shell.type.mechanics == SHELL_MECHANICS_TYPE.MODERN

    @classmethod
    def _computeArmorDefault(cls, c_details, shell, piercing_power):
        computed_armor = GLOBAL.ZERO
        ricochet = False
        no_damage = True
        is_jet = False
        jet_start_dist = GLOBAL.ZERO
        jet_loss = cls._SHELL_EXTRA_DATA[shell.kind].jetLossPPByDist
        ignoredMaterials = set()
        for detail in c_details:
            mat_info = detail.matInfo
            if mat_info is None or (detail.compName, mat_info.kind) in ignoredMaterials:
                continue
            hitAngleCos = detail.hitAngleCos if mat_info.useHitAngle else 1.0
            if is_jet:
                jetDist = detail.dist - jet_start_dist
                if jetDist > GLOBAL.ZERO:
                    piercing_power *= 1.0 - jetDist * jet_loss
            else:
                ricochet = cls._shouldRicochet(shell, hitAngleCos, mat_info)
            computed_armor += cls._computePenetrationArmor(shell, hitAngleCos, mat_info)
            if mat_info.vehicleDamageFactor:
                no_damage = False
                break
            if jet_loss > GLOBAL.ZERO:
                is_jet = True
                jet_start_dist += detail.dist + mat_info.armor * cls._JET_FACTOR
            if mat_info.collideOnceOnly:
                ignoredMaterials.add((detail.compName, mat_info.kind))
        data = (computed_armor, piercing_power, shell.caliber, ricochet, no_damage)
        return cls._checkShotResult(data), data

    @classmethod
    def _computeArmorModern(cls, c_details, shell, piercing_power):
        computed_armor = GLOBAL.ZERO
        ignoredMaterials = set()
        no_damage = True
        for detail in c_details:
            mat_info = detail.matInfo
            if mat_info is None or (detail.compName, mat_info.kind) in ignoredMaterials:
                continue
            hitAngleCos = detail.hitAngleCos if mat_info.useHitAngle else 1.0
            computed_armor += cls._computePenetrationArmor(shell, hitAngleCos, mat_info)
            if mat_info.vehicleDamageFactor:
                no_damage = False
                break
            if shell.type.shieldPenetration:
                piercing_power -= computed_armor * MODERN_HE_PIERCING_POWER_REDUCTION_FACTOR_FOR_SHIELDS
            if mat_info.collideOnceOnly:
                ignoredMaterials.add((detail.compName, mat_info.kind))
        data = (computed_armor, max(piercing_power, 0), shell.caliber, False, no_damage)
        return cls._checkShotResult(data), data


class ShotResultIndicatorPlugin(plugins.ShotResultIndicatorPlugin):

    def __init__(self, parentObj):
        super(ShotResultIndicatorPlugin, self).__init__(parentObj)
        self.__onAlly = bool(user_settings.armor_calculator[ARMOR_CALC.ON_ALLY])
        self.__player = getPlayer()

    def __updateColor(self, markerType, hitPoint, collision, direction):
        shot_result, data = _ShotResult._getShotResult(hitPoint, collision, direction, self.__piercingMultiplier,
                                                       self.__onAlly, self.__player)
        if shot_result in self.__colors:
            color = self.__colors[shot_result]
            if self.__cache[markerType] != shot_result and self._parentObj.setGunMarkerColor(markerType, color):
                self.__cache[markerType] = shot_result
                g_events.onMarkerColorChanged(color)
            g_events.onArmorChanged(data)

    def __setMapping(self, keys):
        super(ShotResultIndicatorPlugin, self).__setMapping(keys)
        self.__mapping[CROSSHAIR_VIEW_ID.STRATEGIC] = True

    def start(self):
        super(ShotResultIndicatorPlugin, self).start()
        if not IS_LESTA:
            prebattleCtrl = self.sessionProvider.dynamic.prebattleSetup
            if prebattleCtrl is not None:
                prebattleCtrl.onVehicleChanged += self.__updateCurrVehicleInfo

    def stop(self):
        super(ShotResultIndicatorPlugin, self).stop()
        if not IS_LESTA:
            prebattleCtrl = self.sessionProvider.dynamic.prebattleSetup
            if prebattleCtrl is not None:
                prebattleCtrl.onVehicleChanged -= self.__updateCurrVehicleInfo

    def __updateCurrVehicleInfo(self, vehicle):
        if avatar_getter.isObserver(self.__player) or vehicle is None:
            return
        _updateRandomization(vehicle)


@overrideMethod(BattleCarouselDataProvider, 'selectVehicle')
def _selectVehicle(base, *args):
    invID = base(*args)
    if invID:
        _updateRandomization(g_currentVehicle.itemsCache.items.getVehicle(invID))
    return invID


@overrideMethod(plugins, 'createPlugins')
def createPlugins(base, *args):
    _plugins = base(*args)
    if user_settings.armor_calculator[GLOBAL.ENABLED]:
        _plugins['shotResultIndicator'] = ShotResultIndicatorPlugin
    return _plugins


GUNNER_ARMORER = 'gunner_armorer'
LOADER_AMMUNITION_IMPROVE = 'loader_ammunitionImprove'
RND_DEBUG = 'PIERCING_POWER_RANDOMIZATION: {}, vehicle: {}'
RND_DIFF_DEBUG = "PIERCING_POWER_RANDOMIZATION getRandomDiff: skill_name: {} skill_lvl: {} skill_level_bonus: {} percent: {}"


def getCurrentSkillEfficiency(percent, tman, skill_name):
    skill_level = tman.skillsMap[skill_name].level
    skill_level_bonus = tman.crewLevelIncrease[0]
    result = (skill_level + skill_level_bonus) * percent * tman.skillsEfficiency
    logDebug(RND_DIFF_DEBUG, skill_name, skill_level, skill_level_bonus, result)
    return result * 0.01


def _updateRandomization(vehicle):
    if IS_LESTA:
        return
    randomization_min, randomization_max = DEFAULT_RANDOMIZATION
    if user_settings.armor_calculator[GLOBAL.ENABLED] and vehicle is not None and vehicle.isCrewFull:
        gunners = []
        loaders = []
        for _, tman in vehicle.crew:
            if not tman or not tman.canUseSkillsInCurrentVehicle:
                continue
            if GUNNER_ARMORER in tman.skillsMap:
                gunners.append(getCurrentSkillEfficiency(0.05, tman, GUNNER_ARMORER))
            if LOADER_AMMUNITION_IMPROVE in tman.skillsMap:
                loaders.append(getCurrentSkillEfficiency(0.02, tman, LOADER_AMMUNITION_IMPROVE))
        if gunners:
            efficiency = sum(gunners) / len(gunners)
            randomization_min += efficiency
            randomization_max -= efficiency
        if loaders:
            randomization_min += sum(loaders) / len(loaders)
    _ShotResult.RANDOMIZATION = MinMax(round(randomization_min, 4), round(randomization_max, 4))
    logDebug(RND_DEBUG, _ShotResult.RANDOMIZATION, vehicle.userName)


# from skeletons.gui.shared.gui_items import IGuiItemsFactory
# from helpers import dependency
#
# @dependency.replace_none_kwargs(itemsFactory=IGuiItemsFactory)
# def hasSkill(skillName, itemsFactory=None):
#     if not skillName:
#         return False
#     player = getPlayer()
#     if player is None:
#         return False
#     vehicle = player.vehicle
#     if vehicle is None:
#         vehicle = player.getVehicleAttached()
#     if vehicle is None:
#         return False
#     isRoleSkill= '_' in skillName
#     crewCompactDescrs = list(vehicle.crewCompactDescrs)
#     crew = tuple(map(lambda tankmanStrCD: itemsFactory.createTankman(tankmanStrCD, -1), crewCompactDescrs))
#     skillAvailability = tuple(skillName in tankman.skillsMap for tankman in crew)
#     return any(skillAvailability) if isRoleSkill else all(skillAvailability)


g_events.onVehicleChangedDelayed += _updateRandomization


def fini():
    g_events.onVehicleChangedDelayed -= _updateRandomization

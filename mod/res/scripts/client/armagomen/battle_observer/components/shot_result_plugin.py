from aih_constants import SHOT_RESULT
from armagomen._constants import ARMOR_CALC, GLOBAL
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import getPlayer, isReplay, MinMax, overrideMethod
from armagomen.utils.events import g_events
from armagomen.utils.logging import logDebug
from AvatarInputHandler.gun_marker_ctrl import _CrosshairShotResults, computePiercingPowerAtDist
from constants import SHELL_MECHANICS_TYPE, SHELL_TYPES
from DestructibleEntity import DestructibleEntity
from gui.battle_control import avatar_getter
from gui.Scaleform.daapi.view.battle.shared.crosshair import plugins
from gui.Scaleform.genConsts.CROSSHAIR_VIEW_ID import CROSSHAIR_VIEW_ID
from gui.shared.gui_items import KPI
from items.tankmen import getSkillsConfig
from Vehicle import Vehicle

DEFAULT_RANDOMIZATION = MinMax(0.75, 1.25)


class _ShotResult(_CrosshairShotResults):
    RANDOMIZATION = DEFAULT_RANDOMIZATION
    UNDEFINED_RESULT = (SHOT_RESULT.UNDEFINED, None)
    ENTITY_TYPES = (Vehicle, DestructibleEntity)
    JET_FACTOR = 0.001
    PP_REDUCTION_FACTOR = 3.0

    @classmethod
    def _isDestructibleComponent(cls, entity, componentID):
        return entity.isDestructibleComponent(componentID) if isinstance(entity, DestructibleEntity) else True

    @classmethod
    def _getShotResult(cls, gunMarker, multiplier, player):
        if player is None or gunMarker.collData is None:
            return cls.UNDEFINED_RESULT
        entity = gunMarker.collData.entity
        if not isinstance(entity, cls.ENTITY_TYPES) or not entity.isAlive() or entity.publicInfo['team'] == player.team:
            return cls.UNDEFINED_RESULT
        return cls._result(gunMarker, multiplier, player)

    @classmethod
    def _result(cls, gunMarker, multiplier, player):
        collision_details = cls._getAllCollisionDetails(gunMarker.position, gunMarker.direction, gunMarker.collData.entity)
        if collision_details is None:
            return cls.UNDEFINED_RESULT
        vDesc = player.getVehicleDescriptor()
        gunInstallationSlot = vDesc.gunInstallations[gunMarker.gunInstallationIndex]
        shot = vDesc.shot if gunInstallationSlot.isMainInstallation() else gunInstallationSlot.gun.shots[0]
        shell = shot.shell
        distance = player.position.flatDistTo(gunMarker.position)
        piercing_power = computePiercingPowerAtDist(shot.piercingPower, distance, shot.maxDistance, multiplier)
        if cls._isModernMechanics(shell):
            return cls._computeArmorModernHE(collision_details, shell, piercing_power, gunMarker.collData.entity)
        else:
            return cls._computeArmorDefault(collision_details, shell, piercing_power, gunMarker.collData.entity)

    @classmethod
    def _checkShotResult(cls, data):
        armor, piercing_power, _, ricochet, no_damage = data
        if no_damage or ricochet:
            return SHOT_RESULT.UNDEFINED
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
    def _computeArmorDefault(cls, collision_details, shell, piercing_power, entity):
        armor = 0
        ignored_materials = set()
        jet_loss = cls._SHELL_EXTRA_DATA[shell.kind].jetLossPPByDist
        jet_start_dist = 0
        no_damage = True
        ricochet = False

        for detail in collision_details:
            if not cls._isDestructibleComponent(entity, detail.compName):
                continue
            mat_info = detail.matInfo
            if not mat_info or (detail.compName, mat_info.kind) in ignored_materials:
                continue
            hitAngleCos = detail.hitAngleCos if mat_info.useHitAngle else 1.0
            if jet_start_dist > 0:
                jetDist = detail.dist - jet_start_dist
                if jetDist > 0:
                    piercing_power = max(0, piercing_power * (1.0 - jetDist * jet_loss))
            else:
                ricochet = cls._shouldRicochet(shell, hitAngleCos, mat_info)
                if ricochet:
                    break
            armor += cls._computePenetrationArmor(shell, hitAngleCos, mat_info)
            if mat_info.vehicleDamageFactor:
                no_damage = False
                break
            if jet_loss > 0:
                jet_start_dist = detail.dist + mat_info.armor * cls.JET_FACTOR
            if mat_info.collideOnceOnly:
                ignored_materials.add((detail.compName, mat_info.kind))
        data = (int(armor), int(piercing_power), int(shell.caliber), ricochet, no_damage)
        return cls._checkShotResult(data), data

    @classmethod
    def _computeArmorModernHE(cls, collision_details, shell, piercing_power, entity):
        armor = 0
        ignored_materials = set()
        no_damage = True

        for detail in collision_details:
            if not cls._isDestructibleComponent(entity, detail.compName):
                continue
            mat_info = detail.matInfo
            if not mat_info or (detail.compName, mat_info.kind) in ignored_materials:
                continue
            hitAngleCos = detail.hitAngleCos if mat_info.useHitAngle else 1.0
            armor += cls._computePenetrationArmor(shell, hitAngleCos, mat_info)
            if mat_info.vehicleDamageFactor:
                no_damage = False
                break
            if shell.type.shieldPenetration:
                piercing_power = max(0, piercing_power - armor * cls.PP_REDUCTION_FACTOR)
            if mat_info.collideOnceOnly:
                ignored_materials.add((detail.compName, mat_info.kind))
        data = (int(armor), int(piercing_power), int(shell.caliber), False, no_damage)
        return cls._checkShotResult(data), data


class _ShotResultAll(_ShotResult):

    @classmethod
    def _getShotResult(cls, gunMarker, multiplier, player):
        collision = gunMarker.collData
        if player is None or collision is None or not isinstance(collision.entity, cls.ENTITY_TYPES) or not collision.entity.isAlive():
            return cls.UNDEFINED_RESULT
        return cls._result(gunMarker, multiplier, player)


class ShotResultIndicatorPlugin(plugins.ShotResultIndicatorPlugin):

    def __init__(self, parentObj):
        super(ShotResultIndicatorPlugin, self).__init__(parentObj)
        self.__player = getPlayer()
        self.__data = None
        self.__resolver = _ShotResultAll if user_settings.armor_calculator[ARMOR_CALC.ON_ALLY] else _ShotResult

    def __onGunMarkerStateChanged(self, markerType, gunMarkerState, supportMarkersInfo):
        if not self.__isEnabled:
            return
        shot_result, data = self.__resolver._getShotResult(gunMarkerState, self.__piercingMultiplier, self.__player)
        if shot_result in self.__colors:
            color = self.__colors[shot_result]
            if self.__cache[markerType] != shot_result and self._parentObj.setGunMarkerColor(markerType, color):
                self.__cache[markerType] = shot_result
                g_events.onMarkerColorChanged(color)
            if self.__data != data:
                self.__data = data
                g_events.onArmorChanged(data)

    def __setMapping(self, keys):
        super(ShotResultIndicatorPlugin, self).__setMapping(keys)
        self.__mapping[CROSSHAIR_VIEW_ID.STRATEGIC] = True

    def start(self):
        super(ShotResultIndicatorPlugin, self).start()
        self.__player = getPlayer()
        prebattleCtrl = self.sessionProvider.dynamic.prebattleSetup
        if prebattleCtrl is not None:
            prebattleCtrl.onVehicleChanged += self.__updateCurrVehicleInfo

    def stop(self):
        super(ShotResultIndicatorPlugin, self).stop()
        prebattleCtrl = self.sessionProvider.dynamic.prebattleSetup
        if prebattleCtrl is not None:
            prebattleCtrl.onVehicleChanged -= self.__updateCurrVehicleInfo

    def __updateCurrVehicleInfo(self, vehicle):
        if not avatar_getter.isObserver(self.__player) and vehicle is not None:
            Randomizer._updateRandomization(vehicle)


@overrideMethod(plugins, 'createPlugins')
def createPlugins(base, *args):
    _plugins = base(*args)
    if user_settings.armor_calculator[GLOBAL.ENABLED]:
        _plugins['shotResultIndicator'] = ShotResultIndicatorPlugin
    return _plugins


class Randomizer(object):
    GUNNER_ARMORER = 'gunner_armorer'
    LOADER_AMMUNITION_IMPROVE = 'loader_ammunitionImprove'
    RND_MIN_MAX_DEBUG = 'PIERCING_POWER_RANDOMIZATION: {}, vehicle: {}'
    RND_SKILL_DIFF_DEBUG = 'PIERCING_POWER_RANDOMIZATION: skill_name: {} skill_lvl: {} level_increase: {} percent: {}'
    RND_SET_PIERCING_DISTRIBUTION_BOUND_DEBUG = 'PIERCING_POWER_RANDOMIZATION: skill_name {}, percent {}'

    PIERCING_DISTRIBUTION_BOUND = {}

    @classmethod
    def getBaseSkillPercent(cls, skill_name):
        percent = cls.PIERCING_DISTRIBUTION_BOUND.get(skill_name, 0)
        if not percent:
            descrArgs = getSkillsConfig().getSkill(skill_name).uiSettings.descrArgs
            for name, descr in descrArgs:
                if name == KPI.Name.DAMAGE_AND_PIERCING_DISTRIBUTION_LOWER_BOUND:
                    percent = cls.PIERCING_DISTRIBUTION_BOUND[skill_name] = round(descr.value, 4)
                    logDebug(cls.RND_SET_PIERCING_DISTRIBUTION_BOUND_DEBUG, skill_name, percent)
                break
        return percent

    @classmethod
    def getCurrentSkillEfficiency(cls, tman, skill_name):
        skill = tman.skillsMap.get(skill_name)
        if skill is None:
            return 0
        level_increase, bonuses = tman.crewLevelIncrease
        result = (skill.level + level_increase) * tman.skillsEfficiency * cls.getBaseSkillPercent(skill_name)
        logDebug(cls.RND_SKILL_DIFF_DEBUG, skill_name, skill.level, level_increase, result)
        return result

    @classmethod
    def _updateRandomization(cls, vehicle):
        randomization_min, randomization_max = DEFAULT_RANDOMIZATION
        if user_settings.armor_calculator[GLOBAL.ENABLED] and vehicle is not None:
            data = {cls.GUNNER_ARMORER: [], cls.LOADER_AMMUNITION_IMPROVE: []}
            for _, tman in vehicle.crew:
                if not tman or not tman.canUseSkillsInCurrentVehicle:
                    continue
                for skill_name in tman.getPossibleSkills().intersection(data):
                    data[skill_name].append(cls.getCurrentSkillEfficiency(tman, skill_name))

            for skill_name, value in data.items():
                if value:
                    percent = sum(value) / len(value)
                    randomization_min += percent
                    if skill_name == cls.GUNNER_ARMORER:
                        randomization_max -= percent
        _ShotResult.RANDOMIZATION = MinMax(round(randomization_min, 4), round(randomization_max, 4))
        logDebug(cls.RND_MIN_MAX_DEBUG, _ShotResult.RANDOMIZATION, vehicle.userName)


if not isReplay():
    g_events.onVehicleChangedDelayed += Randomizer._updateRandomization


    def fini():
        g_events.onVehicleChangedDelayed -= Randomizer._updateRandomization

from aih_constants import SHOT_RESULT
from armagomen._constants import ARMOR_CALC, GLOBAL
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import getPlayer, overrideMethod
from armagomen.utils.events import g_events
from armagomen.utils.logging import logDebug
from AvatarInputHandler.gun_marker_ctrl import _CrosshairShotResults
from constants import SHELL_MECHANICS_TYPE, SHELL_TYPES, SHELL_TYPES as SHELLS
from DestructibleEntity import DestructibleEntity
from gui.Scaleform.daapi.view.battle.shared.crosshair import plugins
from gui.Scaleform.genConsts.CROSSHAIR_VIEW_ID import CROSSHAIR_VIEW_ID
from items.components import component_constants
from items.components.component_constants import MODERN_HE_PIERCING_POWER_REDUCTION_FACTOR_FOR_SHIELDS
from Vehicle import Vehicle


class _ShotResult(object):
    RANDOMIZATION = component_constants.DEFAULT_PIERCING_POWER_RANDOMIZATION
    UNDEFINED_RESULT = (SHOT_RESULT.UNDEFINED, None, None, None, False, False)
    _JET_FACTOR = 0.001
    FULL_PP_RANGE = (SHELLS.HIGH_EXPLOSIVE, SHELLS.HOLLOW_CHARGE)

    @staticmethod
    def isAlly(entity, player, onAlly):
        return False if onAlly else entity.publicInfo['team'] == player.team

    @classmethod
    def getShotResult(cls, hitPoint, collision, direction, piercingMultiplier, onAlly, player):
        if player is None or collision is None:
            return cls.UNDEFINED_RESULT
        entity = collision.entity
        if not isinstance(entity, (Vehicle, DestructibleEntity)) or not entity.isAlive() or cls.isAlly(entity, player,
                                                                                                       onAlly):
            return cls.UNDEFINED_RESULT
        c_details = _CrosshairShotResults._getAllCollisionDetails(hitPoint, direction, entity)
        if c_details is None:
            return cls.UNDEFINED_RESULT
        shot = player.getVehicleDescriptor().shot
        shell = shot.shell
        distance = player.position.flatDistTo(hitPoint)
        is_modern = cls.isModernMechanics(shell)
        if is_modern or shot.shell.kind in cls.FULL_PP_RANGE:
            piercing_power = shot.piercingPower[0] * piercingMultiplier
        else:
            piercing_power = _CrosshairShotResults._computePiercingPowerAtDist(shot.piercingPower, distance,
                                                                               shot.maxDistance,
                                                                               piercingMultiplier)
        return cls.computeArmorHE(c_details, shell, piercing_power) if is_modern else cls.computeArmor(c_details, shell,
                                                                                                       piercing_power)

    @classmethod
    def _checkShotResult(cls, armor, piercing_power, ricochet, no_damage):
        if no_damage or ricochet:
            return SHOT_RESULT.NOT_PIERCED
        else:
            offset = piercing_power * cls.RANDOMIZATION
            if armor < piercing_power - offset:
                return SHOT_RESULT.GREAT_PIERCED
            elif armor > piercing_power + offset:
                return SHOT_RESULT.NOT_PIERCED
            else:
                return SHOT_RESULT.LITTLE_PIERCED

    @staticmethod
    def isModernMechanics(shell):
        return shell.kind == SHELL_TYPES.HIGH_EXPLOSIVE and shell.type.mechanics == SHELL_MECHANICS_TYPE.MODERN

    @classmethod
    def computeArmor(cls, c_details, shell, piercing_power):
        computed_armor = GLOBAL.ZERO
        ricochet = False
        no_damage = True
        is_jet = False
        jet_start_dist = GLOBAL.ZERO
        jet_loss = _CrosshairShotResults._SHELL_EXTRA_DATA[shell.kind].jetLossPPByDist
        ignoredMaterials = set()
        for detail in c_details:
            mat_info = detail.matInfo
            if mat_info is None or (detail.compName, mat_info.kind) in ignoredMaterials:
                continue
            hitAngleCos = detail.hitAngleCos if mat_info.useHitAngle else 1.0
            computed_armor += _CrosshairShotResults._computePenetrationArmor(shell, hitAngleCos, mat_info)
            if is_jet:
                jetDist = detail.dist - jet_start_dist
                if jetDist > GLOBAL.ZERO:
                    piercing_power *= 1.0 - jetDist * jet_loss
            else:
                ricochet = _CrosshairShotResults._shouldRicochet(shell, hitAngleCos, mat_info)
            if mat_info.vehicleDamageFactor:
                no_damage = False
                break
            if jet_loss > GLOBAL.ZERO:
                is_jet = True
                jet_start_dist += detail.dist + mat_info.armor * cls._JET_FACTOR
            if mat_info.collideOnceOnly:
                ignoredMaterials.add((detail.compName, mat_info.kind))

        shot_result = cls._checkShotResult(computed_armor, piercing_power, ricochet, no_damage)
        return shot_result, computed_armor, piercing_power, shell.caliber, ricochet, no_damage

    @classmethod
    def computeArmorHE(cls, c_details, shell, piercing_power):
        computed_armor = GLOBAL.ZERO
        ignoredMaterials = set()
        no_damage = True
        for detail in c_details:
            mat_info = detail.matInfo
            if mat_info is None or (detail.compName, mat_info.kind) in ignoredMaterials:
                continue
            hitAngleCos = detail.hitAngleCos if mat_info.useHitAngle else 1.0
            armor = _CrosshairShotResults._computePenetrationArmor(shell, hitAngleCos, mat_info)
            computed_armor += armor
            if mat_info.vehicleDamageFactor:
                no_damage = False
                break
            if shell.type.shieldPenetration:
                piercing_power -= armor * MODERN_HE_PIERCING_POWER_REDUCTION_FACTOR_FOR_SHIELDS
            if mat_info.collideOnceOnly:
                ignoredMaterials.add((detail.compName, mat_info.kind))

        shot_result = cls._checkShotResult(computed_armor, max(piercing_power, 0), False, no_damage)
        return shot_result, computed_armor, max(piercing_power, 0), shell.caliber, False, no_damage


class ShotResultIndicatorPlugin(plugins.ShotResultIndicatorPlugin):

    def __init__(self, parentObj):
        super(ShotResultIndicatorPlugin, self).__init__(parentObj)
        self.__onAlly = bool(user_settings.armor_calculator[ARMOR_CALC.ON_ALLY])
        self.__player = getPlayer()

    def __updateColor(self, markerType, hitPoint, collision, direction):
        shot_result, armor, piercing_power, caliber, ricochet, no_damage = \
            _ShotResult.getShotResult(hitPoint, collision, direction, self.__piercingMultiplier, self.__onAlly,
                                      self.__player)
        if shot_result in self.__colors:
            color = self.__colors[shot_result]
            if self.__cache[markerType] != shot_result and self._parentObj.setGunMarkerColor(markerType, color):
                self.__cache[markerType] = shot_result
                g_events.onMarkerColorChanged(color)
            g_events.onArmorChanged(armor, piercing_power, caliber, ricochet, no_damage)

    def __setMapping(self, keys):
        super(ShotResultIndicatorPlugin, self).__setMapping(keys)
        self.__mapping[CROSSHAIR_VIEW_ID.STRATEGIC] = True


@overrideMethod(plugins, 'createPlugins')
def createPlugins(base, *args):
    _plugins = base(*args)
    if user_settings.armor_calculator[GLOBAL.ENABLED]:
        _plugins['shotResultIndicator'] = ShotResultIndicatorPlugin
    return _plugins


GUNNER_ARMORER = 'gunner_armorer'


def _updateRandomization(vehicle):
    randomization = component_constants.DEFAULT_PIERCING_POWER_RANDOMIZATION
    if user_settings.armor_calculator[GLOBAL.ENABLED] and vehicle is not None and vehicle.isCrewFull:
        for _, tman in vehicle.crew:
            if tman and GUNNER_ARMORER in tman.skillsMap and tman.canUseSkillsInCurrentVehicle:
                level = tman.skillsMap[GUNNER_ARMORER].level * tman.skillsEfficiency * (tman.nativeTankRealRoleLevel / 100.0)
                randomization += (0.2 - randomization) * (level - randomization) / 100
                logDebug("PIERCING_POWER_RANDOMIZATION level: {}, randomization: {}", level, randomization)
                break
    _ShotResult.RANDOMIZATION = randomization


g_events.onVehicleChangedDelayed += _updateRandomization


def fini():
    g_events.onVehicleChangedDelayed -= _updateRandomization

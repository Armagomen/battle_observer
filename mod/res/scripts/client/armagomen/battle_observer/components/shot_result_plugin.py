from AvatarInputHandler.gun_marker_ctrl import _CrosshairShotResults
from DestructibleEntity import DestructibleEntity
from Vehicle import Vehicle
from aih_constants import SHOT_RESULT
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import GLOBAL, ARMOR_CALC
from armagomen.utils.common import getPlayer, overrideMethod
from armagomen.utils.events import g_events
from constants import SHELL_MECHANICS_TYPE, SHELL_TYPES as SHELLS, SHELL_TYPES
from gui.Scaleform.daapi.view.battle.shared.crosshair import plugins
from gui.Scaleform.genConsts.CROSSHAIR_VIEW_ID import CROSSHAIR_VIEW_ID
from items.components.component_constants import MODERN_HE_PIERCING_POWER_REDUCTION_FACTOR_FOR_SHIELDS

UNDEFINED_RESULT = (SHOT_RESULT.UNDEFINED, None, None, None, False, False)
_MIN_PIERCING_DIST = 100.0
_MAX_PIERCING_DIST = 500.0
_JET_FACTOR = 0.001
_LERP_RANGE_PIERCING_DIST = _MAX_PIERCING_DIST - _MIN_PIERCING_DIST


class ShotResultResolver(object):

    def __init__(self):
        self.__player = None
        self.__onAlly = bool(settings.armor_calculator[ARMOR_CALC.ON_ALLY])

    def setPlayer(self):
        self.__player = getPlayer()

    def isAlly(self, entity):
        return False if self.__onAlly else entity.publicInfo.team == self.__player.team

    def getShotResult(self, collision, hitPoint, direction, piercingMultiplier):
        if collision is None or self.__player is None:
            return UNDEFINED_RESULT
        entity = collision.entity
        if not isinstance(entity, (Vehicle, DestructibleEntity)) or not entity.isAlive() or self.isAlly(entity):
            return UNDEFINED_RESULT
        c_details = _CrosshairShotResults._getAllCollisionDetails(hitPoint, direction, entity)
        if c_details is None:
            return UNDEFINED_RESULT
        shot = self.__player.getVehicleDescriptor().shot
        shell = shot.shell
        full_piercing_power = self.getFullPiercingPower(hitPoint, piercingMultiplier, shell, shot)
        armor, piercing_power, ricochet, no_damage = self.computeArmor(c_details, shell, full_piercing_power,
                                                                       self.isModernMechanics(shell))
        if no_damage or ricochet:
            shot_result = SHOT_RESULT.NOT_PIERCED
        else:
            piercing_power_offset = piercing_power * shell.piercingPowerRandomization
            if armor < piercing_power - piercing_power_offset:
                shot_result = SHOT_RESULT.GREAT_PIERCED
            elif armor > piercing_power + piercing_power_offset:
                shot_result = SHOT_RESULT.NOT_PIERCED
            else:
                shot_result = SHOT_RESULT.LITTLE_PIERCED
        return shot_result, armor, piercing_power, shell.caliber, ricochet, no_damage

    def getFullPiercingPower(self, hitPoint, piercingMultiplier, shell, shot):
        p100, p500 = (pp * piercingMultiplier for pp in shot.piercingPower)
        if shell.kind == SHELLS.HIGH_EXPLOSIVE or shell.kind == SHELLS.HOLLOW_CHARGE:
            return p100
        else:
            distance = hitPoint.distTo(self.__player.position)
            if distance <= _MIN_PIERCING_DIST:
                return p100
            elif distance < _MAX_PIERCING_DIST:
                return p100 + (p500 - p100) * (distance - _MIN_PIERCING_DIST) / _LERP_RANGE_PIERCING_DIST
            return p500

    @staticmethod
    def isModernMechanics(shell):
        return shell.kind == SHELL_TYPES.HIGH_EXPLOSIVE and shell.type.mechanics == SHELL_MECHANICS_TYPE.MODERN and \
            shell.type.shieldPenetration

    def computeArmor(self, c_details, shell, full_piercing_power, is_modern_he):
        computed_armor = GLOBAL.ZERO
        piercing_power = full_piercing_power
        ricochet = False
        no_damage = True
        is_jet = False
        jet_start_dist = GLOBAL.ZERO
        jetLossPPByDist = _CrosshairShotResults._SHELL_EXTRA_DATA[shell.kind].jetLossPPByDist
        for detail in c_details:
            mat_info = detail.matInfo
            if mat_info is None:
                continue
            hit_angle_cos = detail.hitAngleCos
            computed_armor += _CrosshairShotResults._computePenetrationArmor(shell, hit_angle_cos, mat_info)
            if is_jet:
                jetDist = detail.dist - jet_start_dist
                if jetDist > GLOBAL.ZERO:
                    piercing_power *= 1.0 - jetDist * jetLossPPByDist
            else:
                ricochet = _CrosshairShotResults._shouldRicochet(shell, hit_angle_cos, mat_info)
            if mat_info.vehicleDamageFactor:
                no_damage = False
                break
            elif is_modern_he:
                piercing_power -= computed_armor * MODERN_HE_PIERCING_POWER_REDUCTION_FACTOR_FOR_SHIELDS
                piercing_power = max(piercing_power, GLOBAL.ZERO)
            elif jetLossPPByDist > GLOBAL.ZERO:
                is_jet = True
                jet_start_dist += detail.dist + mat_info.armor * _JET_FACTOR
        return computed_armor, piercing_power, ricochet, no_damage


class ShotResultIndicatorPlugin(plugins.ShotResultIndicatorPlugin):

    def __init__(self, parentObj):
        super(ShotResultIndicatorPlugin, self).__init__(parentObj)
        self.__resolver = ShotResultResolver()

    def __updateColor(self, markerType, hitPoint, collide, _dir):
        shot_result, armor, piercing_power, caliber, ricochet, no_damage = \
            self.__resolver.getShotResult(collide, hitPoint, _dir, self.__piercingMultiplier)
        if shot_result in self.__colors:
            color = self.__colors[shot_result]
            if self.__cache[markerType] != shot_result and self._parentObj.setGunMarkerColor(markerType, color):
                self.__cache[markerType] = shot_result
                g_events.onMarkerColorChanged(color)
            g_events.onArmorChanged(armor, piercing_power, caliber, ricochet, no_damage)

    def __setMapping(self, keys):
        super(ShotResultIndicatorPlugin, self).__setMapping(keys)
        self.__mapping[CROSSHAIR_VIEW_ID.STRATEGIC] = True

    def start(self):
        super(ShotResultIndicatorPlugin, self).start()
        self.__resolver.setPlayer()


@overrideMethod(plugins, 'createPlugins')
def createPlugins(base, *args):
    _plugins = base(*args)
    if settings.armor_calculator[GLOBAL.ENABLED]:
        _plugins['shotResultIndicator'] = ShotResultIndicatorPlugin
    return _plugins

from collections import namedtuple

from AvatarInputHandler.gun_marker_ctrl import _CrosshairShotResults, _MIN_PIERCING_DIST, _LERP_RANGE_PIERCING_DIST
from aih_constants import SHOT_RESULT
from armagomen.battle_observer.core import view_settings
from armagomen.constants import ARMOR_CALC, VEHICLE, GLOBAL, ALIASES
from armagomen.utils.common import getPlayer, overrideMethod, events
from constants import SHELL_MECHANICS_TYPE, SHELL_TYPES
from gui.Scaleform.daapi.view.battle.shared.crosshair import plugins
from gui.Scaleform.genConsts.CROSSHAIR_VIEW_ID import CROSSHAIR_VIEW_ID
from items.components.component_constants import MODERN_HE_PIERCING_POWER_REDUCTION_FACTOR_FOR_SHIELDS

MinMaxCurrent = namedtuple("piercingPower", ("min", "max", "current"))


class ShotResultResolver(object):
    __slots__ = ("resolver", "_player")

    def __init__(self):
        self.resolver = _CrosshairShotResults
        self._player = getPlayer()

    def getShotResult(self, collision, hitPoint, direction, multiplier):
        if collision is None:
            return ARMOR_CALC.NONE_DATA
        entity = collision.entity
        if not entity.isAlive():
            return ARMOR_CALC.NONE_DATA
        if entity.publicInfo[VEHICLE.TEAM] == self._player.team:
            return ARMOR_CALC.NONE_DATA
        cDetails = self.resolver._getAllCollisionDetails(hitPoint, direction, entity)
        if cDetails is None:
            return ARMOR_CALC.NONE_DATA
        vehicleDescriptor = self._player.getVehicleDescriptor()
        shot = vehicleDescriptor.shot
        shell = shot.shell
        dist = hitPoint.flatDistTo(self._player.getOwnVehiclePosition())
        isHE = shell.kind == SHELL_TYPES.HIGH_EXPLOSIVE and shell.type.mechanics == SHELL_MECHANICS_TYPE.MODERN
        piercingPower = self.computePiercingPower(dist, shot, multiplier)
        armor, ricochet, penetration, noDamage = self.computeArmor(cDetails, shell, piercingPower, isHE)
        shotResult = SHOT_RESULT.NOT_PIERCED if noDamage or ricochet else self.shotResult(armor, piercingPower)
        return shotResult, armor, penetration, shell.caliber, ricochet, noDamage

    def computeArmor(self, cDetails, shell, piercingPower, isHE):
        computed_armor = GLOBAL.ZERO
        penetration = piercingPower.current
        ricochet = False
        noDamage = True
        isFirst = True
        for detail in cDetails:
            matInfo = detail.matInfo
            if matInfo is None:
                continue
            hitAngleCos = detail.hitAngleCos if matInfo.useHitAngle else 1.0
            armor = self.resolver._computePenetrationArmor(shell.kind, hitAngleCos, matInfo, shell.caliber)
            if isFirst:
                ricochet = self.resolver._shouldRicochet(shell.kind, hitAngleCos, matInfo, shell.caliber)
                isFirst = False
            if isHE and not matInfo.vehicleDamageFactor and shell.type.shieldPenetration:
                penetration -= armor * MODERN_HE_PIERCING_POWER_REDUCTION_FACTOR_FOR_SHIELDS
                if penetration < GLOBAL.F_ZERO:
                    penetration = GLOBAL.F_ZERO
            computed_armor += armor
            if matInfo.vehicleDamageFactor:
                noDamage = False
                break
        return computed_armor, ricochet, penetration, noDamage

    @staticmethod
    def shotResult(armor, piercingPower):
        if armor < piercingPower.min:
            return SHOT_RESULT.GREAT_PIERCED
        elif armor > piercingPower.max:
            return SHOT_RESULT.NOT_PIERCED
        else:
            return SHOT_RESULT.LITTLE_PIERCED

    @staticmethod
    def computePiercingPower(distance, shot, multiplier):
        """
        compute Piercing Power at distance.
        :param distance: distance to target
        :param shot: shell shot params piercingPower, maxDistance in shot object
        :param multiplier: x
        :return Piercing Power: namedtuple("piercingPower", ("min", "max", "current"))
        """

        p100, p500 = (pp * multiplier for pp in shot.piercingPower)
        if p100 == p500 or distance <= _MIN_PIERCING_DIST:
            return MinMaxCurrent(p100 * ARMOR_CALC.GREAT_PIERCED, p100 * ARMOR_CALC.NOT_PIERCED, p100)
        elif distance < shot.maxDistance:
            power = p100 + (p500 - p100) * (distance - _MIN_PIERCING_DIST) / _LERP_RANGE_PIERCING_DIST
            if power < p500:
                return MinMaxCurrent(p500 * ARMOR_CALC.GREAT_PIERCED, p500 * ARMOR_CALC.NOT_PIERCED, p500)
            return MinMaxCurrent(power * ARMOR_CALC.GREAT_PIERCED, power * ARMOR_CALC.NOT_PIERCED, power)


class ShotResultPlugin(plugins.ShotResultIndicatorPlugin):

    def __init__(self, parentObj):
        super(ShotResultPlugin, self).__init__(parentObj)
        self.resolver = ShotResultResolver()

    def _ShotResultIndicatorPlugin__updateColor(self, markerType, hitPoint, collide, _dir):
        multiple = self._ShotResultIndicatorPlugin__piercingMultiplier
        result, counted, penetration, caliber, ricochet, noDamage = \
            self.resolver.getShotResult(collide, hitPoint, _dir, multiple)
        if result in self._ShotResultIndicatorPlugin__colors:
            color = self._ShotResultIndicatorPlugin__colors[result]
            cache = self._ShotResultIndicatorPlugin__cache
            if cache[markerType] != result and self._parentObj.setGunMarkerColor(markerType, color):
                cache[markerType] = result
                events.onMarkerColorChanged(color)
            events.onArmorChanged(counted, penetration, caliber, ricochet, noDamage)

    def _ShotResultIndicatorPlugin__setEnabled(self, viewID):
        self._ShotResultIndicatorPlugin__isEnabled = self._ShotResultIndicatorPlugin__mapping[viewID] or \
                                                     viewID == CROSSHAIR_VIEW_ID.STRATEGIC
        if self._ShotResultIndicatorPlugin__isEnabled:
            for markerType, shotResult in self._ShotResultIndicatorPlugin__cache.iteritems():
                self._parentObj.setGunMarkerColor(markerType, self._ShotResultIndicatorPlugin__colors[shotResult])
        else:
            self._ShotResultIndicatorPlugin__cache.clear()

    def _ShotResultIndicatorPlugin__onGunMarkerStateChanged(self, markerType, position, direction, collision):
        if self._ShotResultIndicatorPlugin__isEnabled:
            self._ShotResultIndicatorPlugin__updateColor(markerType, position, collision, direction)


@overrideMethod(plugins, 'createPlugins')
def createPlugins(base, *args):
    _plugins = base(*args)
    if view_settings.getSetting(ALIASES.ARMOR_CALC):
        _plugins['shotResultIndicator'] = ShotResultPlugin
    return _plugins

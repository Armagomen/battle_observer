from AvatarInputHandler.gun_marker_ctrl import _CrosshairShotResults, _MIN_PIERCING_DIST, _LERP_RANGE_PIERCING_DIST
from aih_constants import SHOT_RESULT
from armagomen.battle_observer.core import view_settings
from armagomen.constants import ARMOR_CALC, VEHICLE, GLOBAL, ALIASES
from armagomen.utils.common import getPlayer, overrideMethod, events
from constants import SHELL_TYPES
from gui.Scaleform.daapi.view.battle.shared.crosshair import plugins
from gui.Scaleform.genConsts.CROSSHAIR_VIEW_ID import CROSSHAIR_VIEW_ID
from vehicle_systems.tankStructure import TankPartIndexes

try:
    from constants import SHELL_MECHANICS_TYPE
    from items.components.component_constants import MODERN_HE_PIERCING_POWER_REDUCTION_FACTOR_FOR_SHIELDS

    COMPATIBILITY_MODE = False
except ImportError:
    COMPATIBILITY_MODE = True


class ShotResultResolver(object):
    __slots__ = ("resolver", "_player")

    def __init__(self):
        self.resolver = _CrosshairShotResults
        self.resolver._VEHICLE_TRACE_FORWARD_LENGTH = 10.0
        self._player = getPlayer()

    def getShotResult(self, collision, targetPos, direction, multiplier):
        if collision is None:
            return ARMOR_CALC.NONE_DATA
        entity = collision.entity
        if not entity.isAlive():
            return ARMOR_CALC.NONE_DATA
        if entity.publicInfo[VEHICLE.TEAM] == self._player.team:
            return ARMOR_CALC.NONE_DATA
        cDetails = self.resolver._getAllCollisionDetails(targetPos, direction, entity)
        if cDetails is None:
            return ARMOR_CALC.NONE_DATA
        vehicleDescriptor = self._player.getVehicleDescriptor()
        shot = vehicleDescriptor.shot
        shell = shot.shell
        dist = targetPos.flatDistTo(self._player.gunRotator.getCurShotPosition()[GLOBAL.FIRST])
        if COMPATIBILITY_MODE:
            isHE = False
        else:
            isHE = shell.kind == SHELL_TYPES.HIGH_EXPLOSIVE and shell.type.mechanics == SHELL_MECHANICS_TYPE.MODERN
        armor, ricochet, penetration = self.computeArmor(cDetails, shell, self.computePP(dist, shot, multiplier), isHE)
        return self.shotResult(armor, penetration), armor, penetration, shell.caliber, ricochet

    def computeArmor(self, cDetails, shell, penetration, isHE):
        counted_armor = GLOBAL.ZERO
        ignoredMaterials = set()
        ricochet = False
        isFirst = True
        for detail in cDetails:
            matInfo = detail.matInfo
            if matInfo is None:
                continue
            if (detail.compName, matInfo.kind) in ignoredMaterials:
                continue
            hitAngleCos = detail.hitAngleCos if matInfo.useHitAngle else 1.0
            armor = self.resolver._computePenetrationArmor(shell.kind, hitAngleCos, matInfo, shell.caliber)
            if isFirst:
                if TankPartIndexes.CHASSIS != detail.compName:
                    ricochet = self.resolver._shouldRicochet(shell.kind, hitAngleCos, matInfo, shell.caliber)
                isFirst = False
            if isHE and not matInfo.vehicleDamageFactor and shell.type.shieldPenetration:
                penetration -= armor * MODERN_HE_PIERCING_POWER_REDUCTION_FACTOR_FOR_SHIELDS
                if penetration < GLOBAL.F_ZERO:
                    penetration = GLOBAL.F_ZERO
            counted_armor += armor
            if matInfo.collideOnceOnly:
                ignoredMaterials.add((detail.compName, matInfo.kind))
            if matInfo.vehicleDamageFactor:
                break
        return counted_armor, ricochet, penetration

    @staticmethod
    def shotResult(counted_armor, penetration):
        if counted_armor < penetration * ARMOR_CALC.GREAT_PIERCED:
            return SHOT_RESULT.GREAT_PIERCED
        elif counted_armor > penetration * ARMOR_CALC.NOT_PIERCED:
            return SHOT_RESULT.NOT_PIERCED
        else:
            return SHOT_RESULT.LITTLE_PIERCED

    @staticmethod
    def computePP(distance, shot, multiplier):
        """
        compute Piercing Power at distance.
        :param distance: distance to target
        :param shot: shell shot params piercingPower, maxDistance in shot object
        :param multiplier: x
        :return Piercing Power: float number
        """

        p100, p500 = (pp * multiplier for pp in shot.piercingPower)
        if p100 == p500:
            return p100
        if distance <= _MIN_PIERCING_DIST:
            return p100
        elif distance < shot.maxDistance:
            power = p100 + (p500 - p100) * (distance - _MIN_PIERCING_DIST) / _LERP_RANGE_PIERCING_DIST
            if power < p500:
                return p500
            return power


class ShotResultPlugin(plugins.ShotResultIndicatorPlugin):

    def __init__(self, parentObj):
        super(ShotResultPlugin, self).__init__(parentObj)
        self.resolver = ShotResultResolver()

    def _ShotResultIndicatorPlugin__updateColor(self, markerType, position, collision, direction):
        multiplier = self._ShotResultIndicatorPlugin__piercingMultiplier
        result, counted, penetration, caliber, ricochet = self.resolver.getShotResult(collision, position, direction,
                                                                                      multiplier)
        if result in self._ShotResultIndicatorPlugin__colors:
            color = self._ShotResultIndicatorPlugin__colors[result]
            cache = self._ShotResultIndicatorPlugin__cache
            if cache[markerType] != result and self._parentObj.setGunMarkerColor(markerType, color):
                cache[markerType] = result
                events.onMarkerColorChanged(color)
            events.onArmorChanged(counted, penetration, caliber, ricochet)

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

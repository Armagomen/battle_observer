from collections import namedtuple

from AvatarInputHandler.gun_marker_ctrl import _CrosshairShotResults, _MIN_PIERCING_DIST, _LERP_RANGE_PIERCING_DIST
from DestructibleEntity import DestructibleEntity
from Vehicle import Vehicle
from aih_constants import SHOT_RESULT
from armagomen.battle_observer.core import view_settings
from armagomen.constants import ARMOR_CALC, VEHICLE, GLOBAL, ALIASES
from armagomen.utils.common import getPlayer, overrideMethod, events
from constants import SHELL_MECHANICS_TYPE, SHELL_TYPES as SHELLS
from gui.Scaleform.daapi.view.battle.shared.crosshair import plugins
from gui.Scaleform.genConsts.CROSSHAIR_VIEW_ID import CROSSHAIR_VIEW_ID
from items.components.component_constants import MODERN_HE_PIERCING_POWER_REDUCTION_FACTOR_FOR_SHIELDS

PiercingPower = namedtuple("PiercingPower", ("min", "max", "current"))
ShotResult = namedtuple("ShotResult", ("result", "armor", "piercingPower", "caliber", "ricochet", "noDamage"))
UndefinedShotResult = ShotResult(SHOT_RESULT.UNDEFINED, None, None, None, False, False)


class ShotResultResolver(object):
    __slots__ = ("resolver", "_player")

    def __init__(self):
        self.resolver = _CrosshairShotResults
        self._player = getPlayer()

    def isAlly(self, entity):
        return entity.publicInfo[VEHICLE.TEAM] == self._player.team

    def getShotResult(self, collision, hitPoint, direction, piercingMultiplier):
        if collision is None:
            return UndefinedShotResult
        entity = collision.entity
        if not isinstance(entity, (Vehicle, DestructibleEntity)) or not entity.isAlive() or self.isAlly(entity):
            return UndefinedShotResult
        cDetails = self.resolver._getAllCollisionDetails(hitPoint, direction, entity)
        if cDetails is None:
            return UndefinedShotResult
        vehicleDescriptor = self._player.getVehicleDescriptor()
        shot = vehicleDescriptor.shot
        isHE = shot.shell.kind == SHELLS.HIGH_EXPLOSIVE and shot.shell.type.mechanics == SHELL_MECHANICS_TYPE.MODERN
        fullPiercingPower = self.computePiercingPower(hitPoint, shot, piercingMultiplier)
        armor, piercingPower, ricochet, noDamage = self.computeArmor(cDetails, shot, fullPiercingPower, isHE)
        shotResult = SHOT_RESULT.NOT_PIERCED if noDamage or ricochet else self.shotResult(armor, piercingPower)
        return ShotResult(shotResult, armor, piercingPower.current, shot.shell.caliber, ricochet, noDamage)

    def computeArmor(self, cDetails, shot, fullPiercingPower, isHE):
        computed_armor = GLOBAL.ZERO
        pPower = fullPiercingPower
        ricochet = False
        noDamage = True
        isFirst = True
        for detail in cDetails:
            matInfo = detail.matInfo
            if matInfo is None:
                continue
            hitAngleCos = detail.hitAngleCos if matInfo.useHitAngle else 1.0
            armor = self.resolver._computePenetrationArmor(shot.shell.kind, hitAngleCos, matInfo, shot.shell.caliber)
            if isFirst:
                ricochet = self.resolver._shouldRicochet(shot.shell.kind, hitAngleCos, matInfo, shot.shell.caliber)
                isFirst = False
            if isHE and not matInfo.vehicleDamageFactor and shot.shell.type.shieldPenetration:
                pPower -= armor * MODERN_HE_PIERCING_POWER_REDUCTION_FACTOR_FOR_SHIELDS
                if pPower < GLOBAL.F_ZERO:
                    pPower = GLOBAL.F_ZERO
            computed_armor += armor
            if matInfo.vehicleDamageFactor:
                noDamage = False
                break
        piercingPower = PiercingPower(pPower * ARMOR_CALC.GREAT_PIERCED, pPower * ARMOR_CALC.NOT_PIERCED, pPower)
        return computed_armor, piercingPower, ricochet, noDamage

    @staticmethod
    def shotResult(armor, piercingPower):
        if armor < piercingPower.min:
            return SHOT_RESULT.GREAT_PIERCED
        elif armor > piercingPower.max:
            return SHOT_RESULT.NOT_PIERCED
        else:
            return SHOT_RESULT.LITTLE_PIERCED

    def computePiercingPower(self, hitPoint, shot, multiplier):
        """
        compute Piercing Power at distance.
        :param hitPoint: target position
        :param shot: shell shot params piercingPower, maxDistance in shot object
        :param multiplier: x
        :return Piercing Power: at distance
        """
        distance = hitPoint.flatDistTo(self._player.getOwnVehiclePosition())
        p100, p500 = (pp * multiplier for pp in shot.piercingPower)
        if p100 == p500 or distance <= _MIN_PIERCING_DIST:
            return p100
        elif distance < shot.maxDistance:
            return max(p500, p100 + (p500 - p100) * (distance - _MIN_PIERCING_DIST) / _LERP_RANGE_PIERCING_DIST)
        return p500


class ShotResultIndicatorPlugin(plugins.ShotResultIndicatorPlugin):

    def __init__(self, parentObj):
        super(ShotResultIndicatorPlugin, self).__init__(parentObj)
        self.__resolver = ShotResultResolver()

    def __updateColor(self, markerType, hitPoint, collide, _dir):
        shotResult = self.__resolver.getShotResult(collide, hitPoint, _dir, self.__piercingMultiplier)
        if shotResult.result in self.__colors:
            color = self.__colors[shotResult.result]
            if self.__cache[markerType] != shotResult.result and self._parentObj.setGunMarkerColor(markerType, color):
                self.__cache[markerType] = shotResult.result
                events.onMarkerColorChanged(color)
            events.onArmorChanged(shotResult)

    def __setEnabled(self, viewID):
        self.__isEnabled = self.__mapping[viewID] or viewID == CROSSHAIR_VIEW_ID.STRATEGIC
        if self.__isEnabled:
            for markerType, shotResult in self.__cache.iteritems():
                self._parentObj.setGunMarkerColor(markerType, self.__colors[shotResult])
        else:
            self.__cache.clear()

    def __onGunMarkerStateChanged(self, markerType, position, direction, collision):
        if self.__isEnabled:
            self.__updateColor(markerType, position, collision, direction)


@overrideMethod(plugins, 'createPlugins')
def createPlugins(base, *args):
    _plugins = base(*args)
    if view_settings.getSetting(ALIASES.ARMOR_CALC):
        _plugins['shotResultIndicator'] = ShotResultIndicatorPlugin
    return _plugins

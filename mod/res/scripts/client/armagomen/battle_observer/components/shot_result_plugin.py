from AvatarInputHandler.gun_marker_ctrl import _CrosshairShotResults
from DestructibleEntity import DestructibleEntity
from Vehicle import Vehicle
from aih_constants import SHOT_RESULT
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import VEHICLE, GLOBAL, ARMOR_CALC
from armagomen.utils.common import getPlayer, overrideMethod
from armagomen.utils.events import g_events
from constants import SHELL_MECHANICS_TYPE, SHELL_TYPES as SHELLS
from gui.Scaleform.daapi.view.battle.shared.crosshair import plugins
from gui.Scaleform.genConsts.CROSSHAIR_VIEW_ID import CROSSHAIR_VIEW_ID
from items.components.component_constants import MODERN_HE_PIERCING_POWER_REDUCTION_FACTOR_FOR_SHIELDS

UNDEFINED_RESULT = (SHOT_RESULT.UNDEFINED, None, None, None, False, False)
_MIN_PIERCING_DIST = 100.0
_MAX_PIERCING_DIST = 500.0
_LERP_RANGE_PIERCING_DIST = _MAX_PIERCING_DIST - _MIN_PIERCING_DIST


class ShotResultResolver(object):
    __slots__ = ("resolver", "__player")

    def __init__(self):
        self.resolver = _CrosshairShotResults
        self.__player = None

    def setPlayer(self):
        self.__player = getPlayer()

    def isAlly(self, entity):
        if not settings.armor_calculator[ARMOR_CALC.ON_ALLY]:
            return entity.publicInfo[VEHICLE.TEAM] == self.__player.team
        return False

    def getShotResult(self, collision, hitPoint, direction, piercingMultiplier):
        if collision is None or self.__player is None:
            return UNDEFINED_RESULT
        entity = collision.entity
        if not isinstance(entity, (Vehicle, DestructibleEntity)) or not entity.isAlive() or self.isAlly(entity):
            return UNDEFINED_RESULT
        cDetails = self.resolver._getAllCollisionDetails(hitPoint, direction, entity)
        if cDetails is None:
            return UNDEFINED_RESULT
        shot = self.__player.getVehicleDescriptor().shot
        shell = shot.shell
        isHE = shell.kind == SHELLS.HIGH_EXPLOSIVE
        if isHE or shell.kind == SHELLS.HOLLOW_CHARGE:
            fullPiercingPower = shot.piercingPower[GLOBAL.FIRST] * piercingMultiplier
        else:
            fullPiercingPower = self.computePiercingPower(hitPoint, shot, piercingMultiplier)
        armor, piercingPower, ricochet, noDamage = self.computeArmor(cDetails, shell, fullPiercingPower, isHE)
        shotResult = SHOT_RESULT.NOT_PIERCED if noDamage or ricochet else self.shotResult(armor, piercingPower, shell)
        return shotResult, armor, piercingPower, shell.caliber, ricochet, noDamage

    @staticmethod
    def isModernMechanics(shell):
        return shell.type.mechanics == SHELL_MECHANICS_TYPE.MODERN and shell.type.shieldPenetration

    def computeArmor(self, cDetails, shell, fullPiercingPower, isHE):
        computedArmor = GLOBAL.ZERO
        piercingPower = fullPiercingPower
        ricochet = False
        noDamage = True
        isJet = False
        jetStartDist = GLOBAL.ZERO
        shellExtraData = self.resolver._SHELL_EXTRA_DATA[shell.kind]
        for detail in cDetails:
            matInfo = detail.matInfo
            if matInfo is None:
                continue
            hitAngleCos = detail.hitAngleCos
            computedArmor += self.resolver._computePenetrationArmor(shell.kind, hitAngleCos, matInfo, shell.caliber)
            if isJet:
                jetDist = detail.dist - jetStartDist
                if jetDist > GLOBAL.ZERO:
                    piercingPower = fullPiercingPower - jetDist * shellExtraData.jetLossPPByDist
            else:
                ricochet = self.resolver._shouldRicochet(shell.kind, hitAngleCos, matInfo, shell.caliber)
            if matInfo.vehicleDamageFactor:
                noDamage = False
                break
            elif isHE and self.isModernMechanics(shell):
                piercingPower -= computedArmor * MODERN_HE_PIERCING_POWER_REDUCTION_FACTOR_FOR_SHIELDS
                piercingPower = max(piercingPower, GLOBAL.ZERO)
            elif shellExtraData.jetLossPPByDist > GLOBAL.ZERO:
                isJet = True
                jetStartDist += detail.dist + matInfo.armor * 0.001
        return computedArmor, piercingPower, ricochet, noDamage

    @staticmethod
    def shotResult(armor, piercingPower, shell):
        piercingPowerOffset = piercingPower * shell.piercingPowerRandomization
        if armor < piercingPower - piercingPowerOffset:
            return SHOT_RESULT.GREAT_PIERCED
        elif armor > piercingPower + piercingPowerOffset:
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
        distance = hitPoint.distTo(self.__player.position)
        p100, p500 = (pp * multiplier for pp in shot.piercingPower)
        if distance <= _MIN_PIERCING_DIST:
            return p100
        elif distance < _MAX_PIERCING_DIST:
            return p100 + (p500 - p100) * (distance - _MIN_PIERCING_DIST) / _LERP_RANGE_PIERCING_DIST
        return p500


class ShotResultIndicatorPlugin(plugins.ShotResultIndicatorPlugin):

    def __init__(self, parentObj):
        super(ShotResultIndicatorPlugin, self).__init__(parentObj)
        self.__resolver = ShotResultResolver()

    def __updateColor(self, markerType, hitPoint, collide, _dir):
        shotResult, armor, piercingPower, caliber, ricochet, noDamage = \
            self.__resolver.getShotResult(collide, hitPoint, _dir, self.__piercingMultiplier)
        if shotResult in self.__colors:
            color = self.__colors[shotResult]
            if self.__cache[markerType] != shotResult and self._parentObj.setGunMarkerColor(markerType, color):
                self.__cache[markerType] = shotResult
                g_events.onMarkerColorChanged(color)
            g_events.onArmorChanged(armor, piercingPower, caliber, ricochet, noDamage)

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

    def start(self):
        super(ShotResultIndicatorPlugin, self).start()
        self.__resolver.setPlayer()


@overrideMethod(plugins, 'createPlugins')
def createPlugins(base, *args):
    _plugins = base(*args)
    if settings.armor_calculator[GLOBAL.ENABLED]:
        _plugins['shotResultIndicator'] = ShotResultIndicatorPlugin
    return _plugins

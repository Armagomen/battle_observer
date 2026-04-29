from aih_constants import SHOT_RESULT
from armagomen._constants import ARMOR_CALC, GLOBAL
from armagomen.battle_observer.controllers import IPiercingRandomizer
from armagomen.battle_observer.settings import IBOSettingsLoader
from armagomen.utils.common import getPlayer, overrideMethod
from armagomen.utils.events import g_events
from AvatarInputHandler.gun_marker_ctrl import _CrosshairShotResults, computePiercingPowerAtDist
from constants import SHELL_MECHANICS_TYPE, SHELL_TYPES
from DestructibleEntity import DestructibleEntity
from gui.battle_control import avatar_getter
from gui.Scaleform.daapi.view.battle.shared.crosshair import plugins
from gui.Scaleform.genConsts.CROSSHAIR_VIEW_ID import CROSSHAIR_VIEW_ID
from helpers import dependency
from Vehicle import Vehicle


class _ShotResult(_CrosshairShotResults):
    randomizer = dependency.descriptor(IPiercingRandomizer)
    UNDEFINED_RESULT = (SHOT_RESULT.UNDEFINED, None)
    ENTITY_TYPES = (Vehicle, DestructibleEntity)
    PP_REDUCTION_FACTOR = 3.0
    DEFAULT_HIT_ANGLE_COS = 1.0

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
        entity = gunMarker.collData.entity
        collision_details = cls._getAllCollisionDetails(gunMarker.position, gunMarker.direction, entity)
        if collision_details is None:
            return cls.UNDEFINED_RESULT
        vDesc = player.getVehicleDescriptor()
        gunInstallationSlot = vDesc.gunInstallations[gunMarker.gunInstallationIndex]
        shot = vDesc.shot if gunInstallationSlot.isMainInstallation() else gunInstallationSlot.gun.shots[0]
        shell = shot.shell
        distance = player.position.flatDistTo(gunMarker.position)
        piercing_power = computePiercingPowerAtDist(shot.piercingPower, distance, shot.maxDistance, multiplier)
        if shell.kind == SHELL_TYPES.HIGH_EXPLOSIVE and shell.type.mechanics == SHELL_MECHANICS_TYPE.MODERN:
            return cls.__computeArmorModernHE(collision_details, shell, piercing_power, entity)
        elif shell.kind == SHELL_TYPES.HOLLOW_CHARGE:
            return cls.__computeArmorHC(collision_details, shell, piercing_power, entity)
        else:
            return cls.__computeArmorDefault(collision_details, shell, piercing_power, entity)

    @classmethod
    def _checkShotResult(cls, armor, piercing_power, no_damage):
        if no_damage:
            return SHOT_RESULT.UNDEFINED
        elif armor < piercing_power * cls.randomizer.confines.min:
            return SHOT_RESULT.GREAT_PIERCED
        elif armor > piercing_power * cls.randomizer.confines.max:
            return SHOT_RESULT.NOT_PIERCED
        else:
            return SHOT_RESULT.LITTLE_PIERCED

    @classmethod
    def __computeArmorDefault(cls, collision_details, shell, piercing_power, entity):
        full_armor = 0
        ignored_materials = set()
        no_damage = True
        ricochet = False

        for detail in collision_details:
            if not cls._isDestructibleComponent(entity, detail.compName):
                continue
            mat_info = detail.matInfo
            if not mat_info or (detail.compName, mat_info.kind) in ignored_materials:
                continue
            hitAngleCos = detail.hitAngleCos if mat_info.useHitAngle else cls.DEFAULT_HIT_ANGLE_COS
            ricochet = cls._shouldRicochet(shell, hitAngleCos, mat_info)
            if ricochet:
                break
            full_armor += cls._computePenetrationArmor(shell, hitAngleCos, mat_info)
            if mat_info.vehicleDamageFactor:
                no_damage = False
                break
            if mat_info.collideOnceOnly:
                ignored_materials.add((detail.compName, mat_info.kind))

        result = cls._checkShotResult(full_armor, piercing_power, ricochet or no_damage)
        data = (int(round(full_armor)), int(round(piercing_power)), int(shell.caliber), ricochet, no_damage)
        return result, data

    @classmethod
    def __computeArmorHC(cls, collision_details, shell, piercing_power, entity):
        full_armor = 0
        jet_start_dist = 0
        ignored_materials = set()
        is_jet = False
        jet_loss = cls._SHELL_EXTRA_DATA[shell.kind].jetLossPPByDist
        no_damage = True
        ricochet = False

        for detail in collision_details:
            if not cls._isDestructibleComponent(entity, detail.compName):
                continue
            mat_info = detail.matInfo
            if not mat_info or (detail.compName, mat_info.kind) in ignored_materials:
                continue
            hitAngleCos = detail.hitAngleCos if mat_info.useHitAngle else cls.DEFAULT_HIT_ANGLE_COS
            if is_jet:
                jetDist = detail.dist - jet_start_dist
                if jetDist > 0.0:
                    loss = 1.0 - jetDist * jet_loss
                    if loss <= 0.0:
                        break
                    piercing_power *= loss
            else:
                ricochet = cls._shouldRicochet(shell, hitAngleCos, mat_info)
                if ricochet:
                    break
            armor = cls._computePenetrationArmor(shell, hitAngleCos, mat_info)
            full_armor += armor
            if mat_info.vehicleDamageFactor:
                no_damage = False
                break
            is_jet = True
            jet_start_dist = detail.dist + armor * 0.001
            if mat_info.collideOnceOnly:
                ignored_materials.add((detail.compName, mat_info.kind))

        result = cls._checkShotResult(full_armor, piercing_power, ricochet or no_damage)
        data = (int(round(full_armor)), int(round(piercing_power)), int(shell.caliber), ricochet, no_damage)
        return result, data

    @classmethod
    def __computeArmorModernHE(cls, collision_details, shell, piercing_power, entity):
        full_armor = 0
        ignored_materials = set()
        no_damage = True

        for detail in collision_details:
            if not cls._isDestructibleComponent(entity, detail.compName):
                continue
            mat_info = detail.matInfo
            if not mat_info or (detail.compName, mat_info.kind) in ignored_materials:
                continue
            hitAngleCos = detail.hitAngleCos if mat_info.useHitAngle else cls.DEFAULT_HIT_ANGLE_COS
            armor = cls._computePenetrationArmor(shell, hitAngleCos, mat_info)
            full_armor += armor
            if mat_info.vehicleDamageFactor:
                no_damage = False
                break
            if shell.type.shieldPenetration:
                piercing_power -= armor * cls.PP_REDUCTION_FACTOR
                if piercing_power <= 0:
                    break
            if mat_info.collideOnceOnly:
                ignored_materials.add((detail.compName, mat_info.kind))
        result = cls._checkShotResult(full_armor, piercing_power, no_damage)
        data = (int(round(full_armor)), int(round(piercing_power)), int(shell.caliber), False, no_damage)
        return result, data


class _ShotResultAll(_ShotResult):

    @classmethod
    def _getShotResult(cls, gunMarker, multiplier, player):
        collision = gunMarker.collData
        if player is None or collision is None or not isinstance(collision.entity, cls.ENTITY_TYPES) or not collision.entity.isAlive():
            return cls.UNDEFINED_RESULT
        return cls._result(gunMarker, multiplier, player)


class ShotResultIndicatorPlugin(plugins.ShotResultIndicatorPlugin):
    settingsLoader = dependency.descriptor(IBOSettingsLoader)
    randomizer = dependency.descriptor(IPiercingRandomizer)

    def __init__(self, parentObj):
        super(ShotResultIndicatorPlugin, self).__init__(parentObj)
        self.__player = getPlayer()
        self.__data = None
        self.__resolver = _ShotResultAll if self.settingsLoader.getSetting(ARMOR_CALC.NAME, ARMOR_CALC.ON_ALLY) else _ShotResult

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
            self.randomizer.updateRandomization(vehicle)


@overrideMethod(plugins, 'createPlugins')
def createPlugins(base, *args):
    _plugins = base(*args)
    settingsLoader = dependency.instance(IBOSettingsLoader)
    if settingsLoader.getSetting(ARMOR_CALC.NAME, GLOBAL.ENABLED):
        _plugins['shotResultIndicator'] = ShotResultIndicatorPlugin
    return _plugins

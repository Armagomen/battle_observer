from collections import defaultdict

from AvatarInputHandler.gun_marker_ctrl import _CrosshairShotResults, _MIN_PIERCING_DIST, _LERP_RANGE_PIERCING_DIST
from PlayerEvents import g_playerEvents
from account_helpers.settings_core.settings_constants import GRAPHICS
from aih_constants import SHOT_RESULT
from armagomen.battle_observer.core import view_settings
from armagomen.constants import ARMOR_CALC, VEHICLE, GLOBAL, ALIASES
from armagomen.utils.common import getPlayer, overrideMethod, events
from constants import SHELL_TYPES
from gui.Scaleform.daapi.view.battle.shared.crosshair import plugins
from gui.Scaleform.daapi.view.battle.shared.crosshair.settings import SHOT_RESULT_TO_ALT_COLOR, \
    SHOT_RESULT_TO_DEFAULT_COLOR
from gui.Scaleform.genConsts.CROSSHAIR_VIEW_ID import CROSSHAIR_VIEW_ID
from gui.Scaleform.genConsts.GUN_MARKER_VIEW_CONSTANTS import GUN_MARKER_VIEW_CONSTANTS as _VIEW_CONSTANTS
from gui.battle_control.battle_constants import FEEDBACK_EVENT_ID
from soft_exception import SoftException
from vehicle_systems.tankStructure import TankPartIndexes

try:
    from constants import SHELL_MECHANICS_TYPE
    from items.components.component_constants import MODERN_HE_PIERCING_POWER_REDUCTION_FACTOR_FOR_SHIELDS

    COMPATIBILITY_MODE = False
except ImportError:
    COMPATIBILITY_MODE = True


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


class ShotResultPlugin(plugins.CrosshairPlugin):
    __slots__ = ('__isEnabled', '__playerTeam', '__cache', '__colors', '__mapping', '_player', 'isStrategic',
                 'resolver', 'multiplier')

    def __init__(self, parentObj):
        super(ShotResultPlugin, self).__init__(parentObj)
        self.__isEnabled = False
        self.__mapping = defaultdict(lambda: False)
        self.__playerTeam = 0
        self.__cache = defaultdict(str)
        self.__colors = None
        self._player = None
        self.isStrategic = False
        self.multiplier = 1
        self.resolver = _CrosshairShotResults
        self.resolver._VEHICLE_TRACE_FORWARD_LENGTH = 10.0

    def start(self):
        ctrl = self.sessionProvider.shared.crosshair
        if ctrl is None:
            raise SoftException('Crosshair controller is not found')
        ctrl.onCrosshairViewChanged += self.__onCrosshairViewChanged
        ctrl.onGunMarkerStateChanged += self.__onGunMarkerStateChanged
        ctrl = self.sessionProvider.shared.feedback
        if ctrl is None:
            raise SoftException('Crosshair controller is not found')
        ctrl.onVehicleFeedbackReceived += self.__onVehicleFeedbackReceived
        g_playerEvents.onTeamChanged += self.__onTeamChanged
        self.__playerTeam = self.sessionProvider.getArenaDP().getNumberOfTeam()
        self.__setColors(self.settingsCore.getSetting(GRAPHICS.COLOR_BLIND))
        self.__setMapping(plugins._SETTINGS_KEYS)
        self.__setEnabled(self._parentObj.getViewID())
        self.settingsCore.onSettingsChanged += self.__onSettingsChanged
        self._player = getPlayer()

    def stop(self):
        ctrl = self.sessionProvider.shared.crosshair
        if ctrl is not None:
            ctrl.onCrosshairViewChanged -= self.__onCrosshairViewChanged
            ctrl.onGunMarkerStateChanged -= self.__onGunMarkerStateChanged
        ctrl = self.sessionProvider.shared.feedback
        if ctrl is not None:
            ctrl.onVehicleFeedbackReceived -= self.__onVehicleFeedbackReceived
        g_playerEvents.onTeamChanged -= self.__onTeamChanged
        self.settingsCore.onSettingsChanged -= self.__onSettingsChanged
        self.__colors = None
        self._player = None
        self.isStrategic = False

    def __setColors(self, isColorBlind):
        if isColorBlind:
            self.__colors = SHOT_RESULT_TO_ALT_COLOR
        else:
            self.__colors = SHOT_RESULT_TO_DEFAULT_COLOR

    def __setMapping(self, keys):
        getter = self.settingsCore.getSetting
        for key in keys:
            settings = getter(key)
            if 'gunTagType' in settings:
                value = settings['gunTagType'] in _VIEW_CONSTANTS.GUN_TAG_SHOT_RESULT_TYPES
                self.__mapping[plugins._SETTINGS_KEY_TO_VIEW_ID[key]] = value

    def __updateColor(self, markerType, position, collision, direction):
        result, counted, penetration, caliber, ricochet = self.__getCountedArmor(collision, position, direction)
        if result in self.__colors:
            color = self.__colors[result]
            if self.__cache[markerType] != result and self._parentObj.setGunMarkerColor(markerType, color):
                self.__cache[markerType] = result
                events.onMarkerColorChanged(color)
            events.onArmorChanged(counted, penetration, caliber, color, ricochet)

    def __setEnabled(self, viewID):
        self.__isEnabled = self.__mapping[viewID]
        self.isStrategic = viewID == CROSSHAIR_VIEW_ID.STRATEGIC
        if self.__isEnabled or self.isStrategic:
            for markerType, shotResult in self.__cache.iteritems():
                self._parentObj.setGunMarkerColor(markerType, self.__colors[shotResult])
        else:
            self.__cache.clear()

    def __onGunMarkerStateChanged(self, markerType, position, direction, collision):
        if self.__isEnabled or self.isStrategic:
            self.__updateColor(markerType, position, collision, direction)

    def __onCrosshairViewChanged(self, viewID):
        self.__setEnabled(viewID)

    def __onSettingsChanged(self, diff):
        update = False
        if GRAPHICS.COLOR_BLIND in diff:
            self.__setColors(diff[GRAPHICS.COLOR_BLIND])
            update = True
        changed = set(diff.keys()) & plugins._SETTINGS_KEYS
        if changed:
            self.__setMapping(changed)
            update = True
        if update:
            self.__setEnabled(self._parentObj.getViewID())

    def __onTeamChanged(self, teamID):
        self.__playerTeam = teamID

    def __getCountedArmor(self, collision, targetPos, direction):
        if collision is None:
            return ARMOR_CALC.NONE_DATA
        entity = collision.entity
        if not entity.isAlive():
            return ARMOR_CALC.NONE_DATA
        if entity.publicInfo[VEHICLE.TEAM] == self.__playerTeam:
            return ARMOR_CALC.NONE_DATA
        cDetails = self.resolver._getAllCollisionDetails(targetPos, direction, entity)
        if cDetails is None:
            return ARMOR_CALC.NONE_DATA
        vehicleDescriptor = self._player.getVehicleDescriptor()
        shot = vehicleDescriptor.shot
        shell = shot.shell
        dist = (targetPos - self._player.getOwnVehiclePosition()).length
        if COMPATIBILITY_MODE:
            isHE = False
        else:
            isHE = shell.kind == SHELL_TYPES.HIGH_EXPLOSIVE and shell.type.mechanics == SHELL_MECHANICS_TYPE.MODERN
        armor, ricochet, penetration = self.computeArmor(cDetails, shell, computePP(dist, shot, self.multiplier), isHE)
        return self.shotResult(armor, penetration), armor, penetration, shell.caliber, ricochet

    def computeArmor(self, cDetails, shell, penetration, isHE):
        counted_armor = GLOBAL.ZERO
        mid_dist = (cDetails[GLOBAL.FIRST].dist + cDetails[GLOBAL.LAST].dist) * ARMOR_CALC.HALF
        ricochet = False
        isFirst = True
        chassis_calculated = False
        for detail in cDetails:
            if detail.dist > mid_dist:
                break
            matInfo = detail.matInfo
            if matInfo is None:
                continue
            hitAngleCos = detail.hitAngleCos if matInfo.useHitAngle else 1.0
            armor = self.resolver._computePenetrationArmor(shell.kind, hitAngleCos, matInfo, shell.caliber)
            if isFirst:
                if TankPartIndexes.CHASSIS != detail.compName:
                    ricochet = self.resolver._shouldRicochet(shell.kind, hitAngleCos, matInfo, shell.caliber)
                isFirst = False
            if isHE and shell.type.shieldPenetration and TankPartIndexes.CHASSIS == detail.compName:
                if not chassis_calculated:
                    penetration -= armor * MODERN_HE_PIERCING_POWER_REDUCTION_FACTOR_FOR_SHIELDS
                    chassis_calculated = True
                if penetration < GLOBAL.F_ZERO:
                    penetration = GLOBAL.F_ZERO
            counted_armor += armor
        return counted_armor, ricochet, penetration

    @staticmethod
    def shotResult(counted_armor, penetration):
        if counted_armor < penetration * ARMOR_CALC.GREAT_PIERCED:
            return SHOT_RESULT.GREAT_PIERCED
        elif counted_armor > penetration * ARMOR_CALC.NOT_PIERCED:
            return SHOT_RESULT.NOT_PIERCED
        else:
            return SHOT_RESULT.LITTLE_PIERCED

    def __onVehicleFeedbackReceived(self, eventID, _, value):
        if eventID == FEEDBACK_EVENT_ID.VEHICLE_ATTRS_CHANGED:
            self.multiplier = value.get('gunPiercing', 1)


@overrideMethod(plugins, 'createPlugins')
def createPlugins(base, *args):
    _plugins = base(*args)
    if view_settings.getSetting(ALIASES.ARMOR_CALC):
        _plugins['shotResultIndicator'] = ShotResultPlugin
    return _plugins

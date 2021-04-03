from collections import defaultdict

from AvatarInputHandler.gun_marker_ctrl import _computePiercingPowerAtDistImpl, _CrosshairShotResults
from PlayerEvents import g_playerEvents
from account_helpers.settings_core.settings_constants import GRAPHICS
from aih_constants import SHOT_RESULT
from armagomen.battle_observer.core import view_settings
from armagomen.battle_observer.core.bo_constants import ARMOR_CALC, VEHICLE, GLOBAL, ALIASES
from armagomen.utils.common import getPlayer, overrideMethod, events
from gui.Scaleform.daapi.view.battle.shared.crosshair import plugins
from gui.Scaleform.daapi.view.battle.shared.crosshair.settings import SHOT_RESULT_TO_ALT_COLOR, \
    SHOT_RESULT_TO_DEFAULT_COLOR
from gui.Scaleform.genConsts.CROSSHAIR_VIEW_ID import CROSSHAIR_VIEW_ID
from gui.Scaleform.genConsts.GUN_MARKER_VIEW_CONSTANTS import GUN_MARKER_VIEW_CONSTANTS as _VIEW_CONSTANTS
from gui.battle_control.battle_constants import FEEDBACK_EVENT_ID
from soft_exception import SoftException


class ShotResultPlugin(plugins.CrosshairPlugin):
    __slots__ = ('__isEnabled', '__playerTeam', '__cache', '__colors', '__mapping', '_player', '_isSPG',
                 '_resolver', '__piercingMultiplier')

    def __init__(self, parentObj):
        super(ShotResultPlugin, self).__init__(parentObj)
        self.__isEnabled = False
        self.__mapping = defaultdict(lambda: False)
        self.__playerTeam = 0
        self.__cache = defaultdict(str)
        self.__colors = None
        self._player = None
        self._isSPG = False
        self.__piercingMultiplier = 1
        self._resolver = _CrosshairShotResults
        self._resolver._VEHICLE_TRACE_FORWARD_LENGTH = 10.0

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
        self._isSPG = False

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
        self._isSPG = viewID == CROSSHAIR_VIEW_ID.STRATEGIC
        if self.__isEnabled or self._isSPG:
            for markerType, shotResult in self.__cache.iteritems():
                self._parentObj.setGunMarkerColor(markerType, self.__colors[shotResult])
        else:
            self.__cache.clear()

    def __onGunMarkerStateChanged(self, markerType, position, direction, collision):
        if self.__isEnabled or self._isSPG:
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
        cDetails = self._resolver._getAllCollisionDetails(targetPos, direction, entity)
        if cDetails is None:
            return ARMOR_CALC.NONE_DATA
        vehicleDescriptor = self._player.getVehicleDescriptor()
        shell = vehicleDescriptor.shot.shell
        caliber = shell.caliber
        shellKind = shell.kind
        counted_armor = GLOBAL.ZERO
        computeArmor = self._resolver._computePenetrationArmor
        mid_dist = (cDetails[GLOBAL.FIRST][GLOBAL.FIRST] + cDetails[GLOBAL.LAST][GLOBAL.FIRST]) * ARMOR_CALC.HALF
        ricochet = False
        isFirst = True
        for detail in cDetails:
            if detail.dist > mid_dist:
                break
            matInfo = detail.matInfo
            if matInfo is None:
                continue
            counted_armor += computeArmor(shellKind, detail.hitAngleCos, matInfo, caliber)
            if isFirst:
                ricochet = self._resolver._shouldRicochet(shellKind, detail.hitAngleCos, matInfo, caliber)
                isFirst = False
        result, penetration = self.__getShotResult(counted_armor, targetPos, vehicleDescriptor)
        return result, counted_armor, penetration, caliber, ricochet

    def __getShotResult(self, countedArmor, targetPos, vehicleDescriptor):
        p100, p500 = vehicleDescriptor.shot.piercingPower
        penetration = p100
        if p100 != p500:
            dist = (targetPos - self._player.getOwnVehiclePosition()).length
            penetration = _computePiercingPowerAtDistImpl(dist, vehicleDescriptor.shot.maxDistance,
                                                          p100 * self.__piercingMultiplier,
                                                          p500 * self.__piercingMultiplier)
        if countedArmor < penetration * ARMOR_CALC.GREAT_PIERCED:
            result = SHOT_RESULT.GREAT_PIERCED
        elif countedArmor > penetration * ARMOR_CALC.NOT_PIERCED:
            result = SHOT_RESULT.NOT_PIERCED
        else:
            result = SHOT_RESULT.LITTLE_PIERCED
        return result, penetration

    def __onVehicleFeedbackReceived(self, eventID, _, value):
        if eventID == FEEDBACK_EVENT_ID.VEHICLE_ATTRS_CHANGED:
            self.__piercingMultiplier = value.get('gunPiercing', 1)


@overrideMethod(plugins, 'createPlugins')
def createPlugins(base, *args):
    _plugins = base(*args)
    if view_settings.getSetting(ALIASES.ARMOR_CALC):
        _plugins['shotResultIndicator'] = ShotResultPlugin
    return _plugins

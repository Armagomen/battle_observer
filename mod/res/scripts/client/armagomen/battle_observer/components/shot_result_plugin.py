from collections import defaultdict

from PlayerEvents import g_playerEvents
from account_helpers.settings_core.settings_constants import GRAPHICS
from aih_constants import SHOT_RESULT
from armagomen.battle_observer.core import b_core
from armagomen.battle_observer.core.bo_constants import ARMOR_CALC, VEHICLE, GLOBAL
from armagomen.utils.common import getPlayer, overrideMethod
from gui.Scaleform.daapi.view.battle.shared.crosshair import plugins
from gui.Scaleform.daapi.view.battle.shared.crosshair.settings import SHOT_RESULT_TO_ALT_COLOR, \
    SHOT_RESULT_TO_DEFAULT_COLOR
from gui.Scaleform.genConsts.CROSSHAIR_VIEW_ID import CROSSHAIR_VIEW_ID
from gui.Scaleform.genConsts.GUN_MARKER_VIEW_CONSTANTS import GUN_MARKER_VIEW_CONSTANTS as _VIEW_CONSTANTS
from soft_exception import SoftException


def getAllCollisionDetails(targetPos, direction, entity):
    startPoint = targetPos - direction * ARMOR_CALC.BACKWARD_LENGTH
    endPoint = targetPos + direction * ARMOR_CALC.FORWARD_LENGTH
    return entity.collideSegmentExt(startPoint, endPoint)


class ObserverShotResultIndicatorPlugin(plugins.CrosshairPlugin):
    __slots__ = ('__isEnabled', '__playerTeam', '__cache', '__colors', '__mapping',
                 '__piercingMultiplier', '_player', '_isSPG')

    def __init__(self, parentObj):
        super(ObserverShotResultIndicatorPlugin, self).__init__(parentObj)
        self.__isEnabled = False
        self.__mapping = defaultdict(lambda: False)
        self.__playerTeam = 0
        self.__cache = defaultdict(str)
        self.__colors = None
        self.__piercingMultiplier = 1
        self._player = None
        self._isSPG = False

    def start(self):
        ctrl = self.sessionProvider.shared.crosshair
        if ctrl is None:
            raise SoftException('Crosshair controller is not found')
        ctrl.onCrosshairViewChanged += self.__onCrosshairViewChanged
        ctrl.onGunMarkerStateChanged += self.__onGunMarkerStateChanged
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
        armor_sum, counted_armor, result = self.__getCountedArmor(collision, position, direction)
        if result in self.__colors:
            color = self.__colors[result]
            if self.__cache[markerType] != result and self._parentObj.setGunMarkerColor(markerType, color):
                self.__cache[markerType] = result
                b_core.onMarkerColorChanged(color)
            if result != SHOT_RESULT.UNDEFINED:
                b_core.onArmorChanged(armor_sum, color, counted_armor)

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
        if collision is not None and getattr(collision, 'isVehicle', False):
            entity = collision.entity
            if entity.publicInfo[VEHICLE.TEAM] != self.__playerTeam and entity.isAlive():
                details = getAllCollisionDetails(targetPos, direction, entity)
                if details is not None:
                    notUseCos = GLOBAL.ZERO
                    useCos = GLOBAL.ZERO
                    armorSum = GLOBAL.ZERO
                    fDist = details[GLOBAL.FIRST][GLOBAL.FIRST] + details[GLOBAL.LAST][GLOBAL.FIRST]
                    midDist = fDist * ARMOR_CALC.HALF
                    for dist, hitAngleCos, matInfo, compIdx in details:
                        if midDist > dist and matInfo:
                            if compIdx not in ARMOR_CALC.SKIP_DETAILS and hitAngleCos > GLOBAL.ZERO:
                                useCos += matInfo.armor / hitAngleCos
                            else:
                                notUseCos += matInfo.armor
                            armorSum += matInfo.armor
                    counted_armor = useCos + notUseCos
                    return armorSum, counted_armor, self.__getShotResult(counted_armor, targetPos)
        return ARMOR_CALC.NONE_DATA

    def __getShotResult(self, countedArmor, targetPos):
        p100, p500 = self._player.getVehicleDescriptor().shot.piercingPower
        power = p100
        if p100 != p500:
            dist = (targetPos - self._player.getOwnVehiclePosition()).length
            if dist > ARMOR_CALC.MIN_DIST:
                result = power + (p500 - power) * (dist - ARMOR_CALC.MIN_DIST) / ARMOR_CALC.EFFECTIVE_DISTANCE
                power = max(p500, result)
        if countedArmor < power * ARMOR_CALC.GREAT_PIERCED:
            return SHOT_RESULT.GREAT_PIERCED
        elif countedArmor > power * ARMOR_CALC.NOT_PIERCED:
            return SHOT_RESULT.NOT_PIERCED
        else:
            return SHOT_RESULT.LITTLE_PIERCED


@overrideMethod(plugins, 'createPlugins')
def createPlugins(base, *args):
    _plugins = base(*args)
    if b_core.armorCalcEnabled:
        _plugins['shotResultIndicator'] = ObserverShotResultIndicatorPlugin
    return _plugins

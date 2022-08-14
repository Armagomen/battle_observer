from account_helpers.settings_core.settings_constants import GAME, GRAPHICS
from armagomen.battle_observer.meta.battle.team_health_meta import TeamHealthMeta
from armagomen.constants import MARKERS, GLOBAL, HP_BARS, VEHICLE_TYPES, COLORS
from armagomen.utils.keys_listener import g_keysListener
from gui.battle_control.arena_info.vos_collections import FragCorrelationSortKey
from gui.battle_control.controllers.battle_field_ctrl import IBattleFieldListener


class CorrelationMarkers(object):

    def __init__(self, arenaDP, settingsCore, settings, vehicleTypes, colors, as_markersS):
        self._arenaDP = arenaDP
        self.as_markersS = as_markersS
        self.settings = settings
        self.settingsCore = settingsCore
        self.vehicleTypes = vehicleTypes
        self.colors = colors
        self.__allyTeam = self._arenaDP.getNumberOfTeam()
        self.__enemyTeam = self._arenaDP.getNumberOfTeam(enemy=True)
        self.vehicleTypeColor = settings[MARKERS.CLASS_COLOR]
        self.color = self.updateMarkersColorDict()
        self.enabled = self.settingsCore.getSetting(GAME.SHOW_VEHICLES_COUNTER)
        g_keysListener.registerComponent(self.keyEvent, keyList=self.settings[MARKERS.HOT_KEY])

    def updateMarkersColorDict(self, isBlind=None):
        if isBlind is None:
            isBlind = self.settingsCore.getSetting(GRAPHICS.COLOR_BLIND)
        dead_color = self.colors[COLORS.GLOBAL][COLORS.DEAD_COLOR]
        blind = COLORS.ENEMY_BLIND_MAME if isBlind else COLORS.ENEMY_MAME
        return {
            self.__allyTeam: {False: dead_color, True: self.colors[COLORS.GLOBAL][COLORS.ALLY_MAME]},
            self.__enemyTeam: {False: dead_color, True: self.colors[COLORS.GLOBAL][blind]}
        }

    def getIcon(self, vInfoVO):
        isAlive = vInfoVO.isAlive()
        if self.vehicleTypeColor and isAlive:
            color = self.vehicleTypes[VEHICLE_TYPES.CLASS_COLORS][vInfoVO.vehicleType.classTag]
        else:
            color = self.color[vInfoVO.team][isAlive]
        return MARKERS.ICON.format(color, MARKERS.TYPE_ICON[vInfoVO.vehicleType.classTag])

    def update(self):
        if self.enabled:
            left, right = [], []
            for vInfo in sorted(self._arenaDP.getVehiclesInfoIterator(), key=FragCorrelationSortKey):
                if not vInfo.vehicleType.isObserver:
                    if vInfo.team == self.__allyTeam:
                        left.append(self.getIcon(vInfo))
                    else:
                        right.append(self.getIcon(vInfo))
            result = GLOBAL.EMPTY_LINE.join(reversed(left)), GLOBAL.EMPTY_LINE.join(right)
        else:
            result = GLOBAL.EMPTY_LINE, GLOBAL.EMPTY_LINE
        self.as_markersS(*result)

    def keyEvent(self, isKeyDown):
        if isKeyDown:
            self.settingsCore.applySettings({GAME.SHOW_VEHICLES_COUNTER: not self.enabled})

    def onSettingsApplied(self, diff):
        if GRAPHICS.COLOR_BLIND in diff:
            self.color = self.updateMarkersColorDict(bool(diff[GRAPHICS.COLOR_BLIND]))
            self.update()
        if GAME.SHOW_VEHICLES_COUNTER in diff:
            self.enabled = bool(diff[GAME.SHOW_VEHICLES_COUNTER])
            self.update()


class TeamsHP(TeamHealthMeta, IBattleFieldListener):

    def __init__(self):
        super(TeamsHP, self).__init__()
        self.showAliveCount = False
        self.markers = None
        self.observers = set(vInfo.vehicleID for vInfo in self._arenaDP.getVehiclesInfoIterator() if vInfo.isObserver())

    def _populate(self):
        super(TeamsHP, self)._populate()
        gui = self._arenaVisitor.gui
        isNormalMode = gui.isRandomBattle() or gui.isRankedBattle() or gui.isTrainingBattle()
        self.showAliveCount = self.settings[HP_BARS.ALIVE] and isNormalMode
        if self.settings[MARKERS.NAME][GLOBAL.ENABLED] and isNormalMode:
            self.markers = CorrelationMarkers(self._arenaDP, self.settingsCore, self.settings[MARKERS.NAME],
                                              self.vehicle_types, self.colors, self.as_markersS)
        self.settingsCore.onSettingsApplied += self.onSettingsApplied

    def _dispose(self):
        self.settingsCore.onSettingsApplied -= self.onSettingsApplied
        self.markers = None
        super(TeamsHP, self)._dispose()

    def updateTeamHealth(self, alliesHP, enemiesHP, totalAlliesHP, totalEnemiesHP):
        self.as_updateHealthS(alliesHP, enemiesHP, totalAlliesHP, totalEnemiesHP)
        if self.settings[HP_BARS.DIFF]:
            self.as_differenceS(alliesHP - enemiesHP)

    def updateDeadVehicles(self, aliveAllies, deadAllies, aliveEnemies, deadEnemies):
        if self.showAliveCount:
            self.as_updateScoreS(len(aliveAllies.difference(deadAllies)), len(aliveEnemies.difference(deadEnemies)))
        else:
            if self.observers:
                deadEnemies = deadEnemies.difference(self.observers)
                deadAllies = deadAllies.difference(self.observers)
            self.as_updateScoreS(len(deadEnemies), len(deadAllies))
        if self.markers is not None:
            self.markers.update()

    def onSettingsApplied(self, diff):
        if self.markers is not None:
            self.markers.onSettingsApplied(diff)
        if GRAPHICS.COLOR_BLIND in diff:
            self.as_colorBlindS(bool(diff[GRAPHICS.COLOR_BLIND]))

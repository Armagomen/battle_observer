from account_helpers.settings_core.settings_constants import GAME, GRAPHICS
from armagomen.battle_observer.core import keysParser
from armagomen.battle_observer.core.bo_constants import MARKERS, GLOBAL, HP_BARS, VEHICLE_TYPES, COLORS
from armagomen.battle_observer.meta.battle.team_health_meta import TeamHealthMeta
from gui.battle_control.arena_info.vos_collections import FragCorrelationSortKey
from gui.battle_control.controllers.battle_field_ctrl import IBattleFieldListener


class CorrelationMarkers(object):

    def __init__(self, arenaDP, settingsCore, settings, vehicleTypes, colors):
        self._arenaDP = arenaDP
        self.settingsCore = settingsCore
        self.vehicleTypes = vehicleTypes
        self.colors = colors
        self.__allyTeam = self._arenaDP.getNumberOfTeam()
        self.__enemyTeam = self._arenaDP.getNumberOfTeam(enemy=True)
        self.mcColor = settings[MARKERS.CLASS_COLOR]
        self.color = self.updateMarkersColorDict()
        self.enabled = self.settingsCore.getSetting(GAME.SHOW_VEHICLES_COUNTER)

    def updateMarkersColorDict(self):
        dead_color = self.colors[COLORS.GLOBAL][COLORS.DEAD_COLOR]
        blind = COLORS.ENEMY_BLIND_MAME if self.settingsCore.getSetting(GRAPHICS.COLOR_BLIND) else COLORS.ENEMY_MAME
        return {
            self.__allyTeam: {False: dead_color, True: self.colors[COLORS.GLOBAL][COLORS.ALLY_MAME]},
            self.__enemyTeam: {False: dead_color, True: self.colors[COLORS.GLOBAL][blind]}
        }

    def getIcon(self, vInfoVO):
        isAlive = vInfoVO.isAlive()
        if self.mcColor and isAlive:
            color = self.vehicleTypes[VEHICLE_TYPES.CLASS_COLORS][vInfoVO.vehicleType.classTag]
        else:
            color = self.color[vInfoVO.team][isAlive]
        return MARKERS.ICON.format(color, MARKERS.TYPE_ICON[vInfoVO.vehicleType.classTag])

    @property
    def update(self):
        if not self.enabled:
            return GLOBAL.EMPTY_LINE, GLOBAL.EMPTY_LINE
        left, right = [], []
        for vInfoVO in sorted(self._arenaDP.getVehiclesInfoIterator(), key=FragCorrelationSortKey):
            if not vInfoVO.isObserver():
                if vInfoVO.team == self.__allyTeam:
                    left.append(self.getIcon(vInfoVO))
                else:
                    right.append(self.getIcon(vInfoVO))
        return GLOBAL.EMPTY_LINE.join(reversed(left)), GLOBAL.EMPTY_LINE.join(right)


class TeamsHP(TeamHealthMeta, IBattleFieldListener):

    def __init__(self):
        super(TeamsHP, self).__init__()
        self.showAliveCount = False
        self.markers = None
        self.observers = set()
        for vinfoVo in self._arenaDP.getVehiclesInfoIterator():
            if vinfoVo.isObserver():
                self.observers.add(vinfoVo.vehicleID)

    def _populate(self):
        super(TeamsHP, self)._populate()
        self.showAliveCount = self.settings[HP_BARS.ALIVE] and self.isNormalMode
        if self.settings[MARKERS.NAME][GLOBAL.ENABLED] and self.isNormalMode:
            self.markers = CorrelationMarkers(self._arenaDP, self.settingsCore, self.settings[MARKERS.NAME],
                                              self.vehicle_types, self.colors)
            self.as_moveTeamBasesPanel()
        self.as_startUpdateS(self.settings, self.colors[COLORS.GLOBAL],
                             self.settingsCore.getSetting(GRAPHICS.COLOR_BLIND))
        self.settingsCore.onSettingsApplied += self.onSettingsApplied
        if self.markers is not None:
            keysParser.registerComponent(MARKERS.HOT_KEY, self.settings[MARKERS.NAME][MARKERS.HOT_KEY])
            keysParser.onKeyPressed += self.keyEvent

    def _dispose(self):
        self.settingsCore.onSettingsApplied -= self.onSettingsApplied
        if self.markers is not None:
            keysParser.onKeyPressed -= self.keyEvent
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
            self.as_markersS(*self.markers.update)

    @property
    def isNormalMode(self):
        random = self._arenaVisitor.gui.isRandomBattle()
        ranked = self._arenaVisitor.gui.isRankedBattle()
        training = self._arenaVisitor.gui.isTrainingBattle()
        return random or ranked or training

    def getAlpha(self):
        return round(min(1.0, self.colors[COLORS.GLOBAL][GLOBAL.ALPHA] * 1.4), 2)

    def keyEvent(self, key, isKeyDown):
        if key == MARKERS.HOT_KEY and isKeyDown:
            self.settingsCore.applySettings({GAME.SHOW_VEHICLES_COUNTER: not self.markers.enabled})

    def onSettingsApplied(self, diff):
        for name, setting in diff.iteritems():
            if name == GRAPHICS.COLOR_BLIND:
                if self.markers is not None:
                    self.markers.color = self.markers.updateMarkersColorDict()
                    self.as_markersS(*self.markers.update)
                self.as_colorBlindS(bool(setting))
            elif name == GAME.SHOW_VEHICLES_COUNTER:
                if self.markers is not None:
                    self.markers.enabled = bool(setting)
                    self.as_markersS(*self.markers.update)

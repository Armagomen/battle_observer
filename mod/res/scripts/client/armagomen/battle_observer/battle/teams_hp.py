from account_helpers.settings_core.settings_constants import GAME, GRAPHICS
from armagomen.battle_observer.core import config, keysParser
from armagomen.battle_observer.core.constants import MARKERS, GLOBAL, HP_BARS, VEHICLE_TYPES, COLORS
from armagomen.battle_observer.meta.battle.team_health_meta import TeamHealthMeta
from gui.battle_control.arena_info.vos_collections import FragCorrelationSortKey
from gui.battle_control.controllers.battle_field_ctrl import IBattleFieldListener
from gui.shared.personality import ServicesLocator

settingsCore = ServicesLocator.settingsCore


class CorrelationMarkers(object):

    def __init__(self, arenaDP):
        self._arenaDP = arenaDP
        self.__allyTeam = self._arenaDP.getNumberOfTeam()
        self.__enemyTeam = self._arenaDP.getNumberOfTeam(enemy=True)
        self.mcColor = config.hp_bars[MARKERS.NAME][MARKERS.CLASS_COLOR]
        self.vcColor = config.vehicle_types[VEHICLE_TYPES.CLASS_COLORS]
        self.color = self.updateMarkersColorDict()
        self.enabled = settingsCore.getSetting(GAME.SHOW_VEHICLES_COUNTER)

    def updateMarkersColorDict(self):
        dead_color = config.colors[COLORS.GLOBAL][COLORS.DEAD_COLOR]
        blind = COLORS.ENEMY_BLIND_MAME if settingsCore.getSetting(GRAPHICS.COLOR_BLIND) else COLORS.ENEMY_MAME
        return {
            self.__allyTeam: {False: dead_color, True: config.colors[COLORS.GLOBAL][COLORS.ALLY_MAME]},
            self.__enemyTeam: {False: dead_color, True: config.colors[COLORS.GLOBAL][blind]}
        }

    def getIcon(self, vInfoVO):
        isAlive = vInfoVO.isAlive()
        if self.mcColor and isAlive:
            color = self.vcColor[vInfoVO.vehicleType.classTag]
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
        self.showAliveCount = config.hp_bars[HP_BARS.ALIVE] and self.isNormalMode
        if config.hp_bars[MARKERS.NAME][GLOBAL.ENABLED] and self.isNormalMode:
            self.markers = CorrelationMarkers(self._arenaDP)
        else:
            self.markers = None
        self.observers = set()
        for vinfoVo in self._arenaDP.getVehiclesInfoIterator():
            if vinfoVo.isObserver():
                self.observers.add(vinfoVo.vehicleID)

    def _populate(self):
        super(TeamsHP, self)._populate()
        is_color_blind_enabled = settingsCore.getSetting(GRAPHICS.COLOR_BLIND)
        self.as_startUpdateS(config.hp_bars, config.colors[COLORS.GLOBAL], is_color_blind_enabled)
        settingsCore.onSettingsApplied += self.onSettingsApplied
        if self.markers is not None:
            keysParser.registerComponent(MARKERS.HOT_KEY, config.hp_bars[MARKERS.NAME][MARKERS.HOT_KEY])
            keysParser.onKeyPressed += self.keyEvent

    def _dispose(self):
        settingsCore.onSettingsApplied -= self.onSettingsApplied
        if self.markers is not None:
            keysParser.onKeyPressed -= self.keyEvent
        super(TeamsHP, self)._dispose()

    def updateTeamHealth(self, alliesHP, enemiesHP, totalAlliesHP, totalEnemiesHP):
        self.as_updateHealthS(alliesHP, enemiesHP, totalAlliesHP, totalEnemiesHP)
        if config.hp_bars[HP_BARS.DIFF]:
            self.as_differenceS(alliesHP - enemiesHP)

    def updateDeadVehicles(self, aliveAllies, deadAllies, aliveEnemies, deadEnemies):
        if self.showAliveCount:
            self.as_updateScoreS(len(aliveAllies.difference(self.observers)),
                                 len(aliveEnemies.difference(self.observers)))
        else:
            self.as_updateScoreS(len(deadEnemies.difference(self.observers)),
                                 len(deadAllies.difference(self.observers)))
        if self.markers is not None:
            self.as_markersS(*self.markers.update)

    @property
    def isNormalMode(self):
        random = self._arenaVisitor.gui.isRandomBattle()
        ranked = self._arenaVisitor.gui.isRankedBattle()
        training = self._arenaVisitor.gui.isTrainingBattle()
        return random or ranked or training

    @staticmethod
    def getAlpha():
        return round(min(1.0, config.colors[COLORS.GLOBAL][GLOBAL.ALPHA] * 1.4), 2)

    def keyEvent(self, key, isKeyDown):
        if key == MARKERS.HOT_KEY and isKeyDown:
            settingsCore.applySettings({GAME.SHOW_VEHICLES_COUNTER: not self.markers.enabled})

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

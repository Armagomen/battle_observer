from account_helpers.settings_core.settings_constants import GAME, GRAPHICS
from gui.battle_control.arena_info.vos_collections import FragCorrelationSortKey
from gui.battle_control.controllers.battle_field_ctrl import IBattleFieldListener
from gui.shared.personality import ServicesLocator
from ..core.battle_cache import cache
from ..core.bo_constants import MARKERS, GLOBAL, HP_BARS, VEHICLE_TYPES, COLORS
from ..core.config import cfg
from ..core.events import g_events
from ..core.keys_parser import g_keysParser
from ..meta.battle.team_health_meta import TeamHealthMeta

settingsCore = ServicesLocator.settingsCore


class CorrelationMarkers(object):

    def __init__(self):
        self.mcColor = cfg.markers[MARKERS.CLASS_COLOR]
        self.vcColor = cfg.vehicle_types[VEHICLE_TYPES.CLASS_COLORS]
        self.color = self.updateMarkersColorDict()
        self.enabled = settingsCore.getSetting(GAME.SHOW_VEHICLES_COUNTER)

    @staticmethod
    def updateMarkersColorDict():
        dead_color = cfg.colors[MARKERS.NAME][MARKERS.DEAD_COLOR]
        blind = MARKERS.ENEMY_COLOR_BLIND if settingsCore.getSetting(GRAPHICS.COLOR_BLIND) else MARKERS.ENEMY
        return {
            cache.allyTeam: {MARKERS.NOT_ALIVE: dead_color, MARKERS.ALIVE: cfg.colors[MARKERS.NAME][MARKERS.ALLY]},
            cache.enemyTeam: {MARKERS.NOT_ALIVE: dead_color, MARKERS.ALIVE: cfg.colors[MARKERS.NAME][blind]}
        }

    def getIcon(self, vInfoVO):
        isAlive = vInfoVO.isAlive()
        if self.mcColor and isAlive:
            color = self.vcColor[vInfoVO.vehicleType.classTag]
        else:
            color = self.color[vInfoVO.team][isAlive]
        return MARKERS.ICON.format(color, MARKERS.TYPE_ICON[vInfoVO.vehicleType.classTag])

    def getMarkers(self):
        left, right = [], []
        allyTeam = cache.allyTeam
        for vInfoVO in sorted(cache.arenaDP.getVehiclesInfoIterator(), key=FragCorrelationSortKey):
            if vInfoVO.team == allyTeam:
                left.append(self.getIcon(vInfoVO))
            else:
                right.append(self.getIcon(vInfoVO))
        return GLOBAL.EMPTY_LINE.join(reversed(left)), GLOBAL.EMPTY_LINE.join(right)


class TeamsHP(TeamHealthMeta, IBattleFieldListener):

    def __init__(self):
        super(TeamsHP, self).__init__()
        self.gui = self.sessionProvider.arenaVisitor.gui
        self.showAliveCount = cfg.hp_bars[HP_BARS.ALIVE] and self.isRandomOrRanked()
        self.markers = CorrelationMarkers() if cfg.markers[GLOBAL.ENABLED] and self.isRandomOrRanked() else None

    def _populate(self):
        super(TeamsHP, self)._populate()
        isColorBlindEnabled = settingsCore.getSetting(GRAPHICS.COLOR_BLIND)
        self.as_startUpdateS(cfg.hp_bars, isColorBlindEnabled, cfg.markers)
        if self.markers is not None:
            g_keysParser.registerComponent(MARKERS.HOT_KEY, cfg.markers[MARKERS.HOT_KEY])
            g_events.onKeyPressed += self.keyEvent
            settingsCore.onSettingsApplied += self.onSettingsApplied

    def _dispose(self):
        if self.markers is not None:
            g_events.onKeyPressed -= self.keyEvent
            settingsCore.onSettingsApplied -= self.onSettingsApplied
        super(TeamsHP, self)._dispose()

    def updateTeamHealth(self, alliesHP, enemiesHP, totalAlliesHP, totalEnemiesHP):
        self.as_updateHealthS(alliesHP, enemiesHP, totalAlliesHP, totalEnemiesHP)
        if cfg.hp_bars[HP_BARS.DIFF]:
            self.as_differenceS(alliesHP - enemiesHP)

    def updateDeadVehicles(self, aliveAllies, deadAllies, aliveEnemies, deadEnemies):
        if self.showAliveCount:
            self.as_updateScoreS(len(aliveAllies), len(aliveEnemies))
        else:
            self.as_updateScoreS(len(deadEnemies), len(deadAllies))
        if self.markers is not None and self.markers.enabled:
            self.as_markersS(*self.markers.getMarkers())

    def isRandomOrRanked(self):
        return self.gui.isRandomBattle() or self.gui.isRankedBattle() or self.gui.isTrainingBattle()

    @staticmethod
    def getAlpha():
        return round(min(1.0, cfg.hp_bars[COLORS.NAME][GLOBAL.ALPHA] * 1.4), 2)

    def keyEvent(self, key, isKeyDown):
        if key == MARKERS.HOT_KEY and isKeyDown:
            settingsCore.applySettings({GAME.SHOW_VEHICLES_COUNTER: not self.markers.enabled})

    def onSettingsApplied(self, diff):
        for name, setting in diff.iteritems():
            if name == GRAPHICS.COLOR_BLIND:
                self.markers.color = self.markers.updateMarkersColorDict()
                if self.markers.enabled:
                    self.as_markersS(*self.markers.getMarkers())
            elif name == GAME.SHOW_VEHICLES_COUNTER:
                self.markers.enabled = bool(setting)
                if self.markers.enabled:
                    self.as_markersS(*self.markers.getMarkers())
                else:
                    self.as_clearMarkersS()

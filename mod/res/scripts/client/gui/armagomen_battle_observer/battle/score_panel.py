from collections import defaultdict

from account_helpers.settings_core.settings_constants import GAME, GRAPHICS
from gui.battle_control.arena_info.vos_collections import FragCorrelationSortKey
from gui.shared.personality import ServicesLocator
from ..core.battle_cache import cache
from ..core.bo_constants import MARKERS, GLOBAL, HP_BARS, VEHICLE_TYPES, SCORE_PANEL, COLORS
from ..core.config import cfg
from ..core.events import g_events
from ..core.keys_parser import g_keysParser
from ..meta.battle.score_panel_meta import ScorePanelMeta


class ScorePanel(ScorePanelMeta):
    settingsCore = ServicesLocator.settingsCore

    def __init__(self):
        super(ScorePanel, self).__init__()
        self.mcColor = cfg.markers[MARKERS.CLASS_COLOR]
        self.vcColor = cfg.vehicle_types[VEHICLE_TYPES.CLASS_COLORS]
        self.showAliveCount = cfg.hp_bars[HP_BARS.ALIVE] and self.isRandomOrRanked()
        self.markersEnable = self.isMarkersEnabled(self.settingsCore.getSetting(GAME.SHOW_VEHICLES_COUNTER))
        self.color = defaultdict(dict)

    def isRandomOrRanked(self):
        guiVisitor = self.sessionProvider.arenaVisitor.gui
        return guiVisitor.isRandomBattle() or guiVisitor.isRankedBattle() or guiVisitor.isTrainingBattle()

    @property
    def colorblindString(self):
        return MARKERS.ENEMY_COLOR_BLIND if self.settingsCore.getSetting(GRAPHICS.COLOR_BLIND) else MARKERS.ENEMY

    def isMarkersEnabled(self, setting):
        return bool(self.isRandomOrRanked() and cfg.markers[GLOBAL.ENABLED] and
                    not self.sessionProvider.arenaVisitor.gui.isEpicRandomBattle() and bool(setting))

    @staticmethod
    def getAlpha():
        return round(min(1.0, cfg.hp_bars[COLORS.NAME][GLOBAL.ALPHA] * 1.4), 2)

    def onEnterBattlePage(self):
        super(ScorePanel, self).onEnterBattlePage()
        guiVisitor = self.sessionProvider.arenaVisitor.gui
        if not guiVisitor.isEpicBattle():
            g_events.updateStatus += self.updateStatus
            self.as_startUpdateS(cfg.markers)
            dead_color = cfg.colors[MARKERS.NAME][MARKERS.DEAD_COLOR]
            self.color[cache.allyTeam] = {
                MARKERS.NOT_ALIVE: dead_color, MARKERS.ALIVE: cfg.colors[MARKERS.NAME][MARKERS.ALLY]
            }
            self.color[cache.enemyTeam] = {
                MARKERS.NOT_ALIVE: dead_color, MARKERS.ALIVE: cfg.colors[MARKERS.NAME][self.colorblindString]
            }
            if not guiVisitor.isEventBattle():
                if self.showAliveCount:
                    score = [cache.arenaDP.getAlliesVehiclesNumber(), cache.arenaDP.getEnemiesVehiclesNumber()]
                else:
                    score = [GLOBAL.ZERO, GLOBAL.ZERO]
                self.as_updateScoreS(*score)
            if self.markersEnable:
                g_keysParser.registerComponent(MARKERS.HOT_KEY, cfg.markers[MARKERS.HOT_KEY])
                g_events.onKeyPressed += self.keyEvent
                self.settingsCore.onSettingsApplied += self.onSettingsApplied
                self.onLoadUpdate()

    def onExitBattlePage(self):
        guiVisitor = self.sessionProvider.arenaVisitor.gui
        if not guiVisitor.isEpicBattle():
            if self.markersEnable:
                g_events.onKeyPressed -= self.keyEvent
                self.settingsCore.onSettingsApplied -= self.onSettingsApplied
            g_events.updateStatus -= self.updateStatus
        super(ScorePanel, self).onExitBattlePage()

    def updateStatus(self, controller, info):
        if SCORE_PANEL.TOTAL_STATS in info:
            total_stats = info[SCORE_PANEL.TOTAL_STATS]
            if self.showAliveCount:
                ally = cache.arenaDP.getAlliesVehiclesNumber() - total_stats[SCORE_PANEL.RIGHT_SCOPE]
                enemy = cache.arenaDP.getEnemiesVehiclesNumber() - total_stats[SCORE_PANEL.LEFT_SCOPE]
            else:
                ally = total_stats[SCORE_PANEL.LEFT_SCOPE]
                enemy = total_stats[SCORE_PANEL.RIGHT_SCOPE]
            self.as_updateScoreS(ally, enemy)
        if self.markersEnable:
            a_list = info.get(SCORE_PANEL.LEFT_CORRELATION_IDS, SCORE_PANEL.EMPTY_LIST)
            e_list = info.get(SCORE_PANEL.RIGHT_CORRELATION_IDS, SCORE_PANEL.EMPTY_LIST)
            if a_list or e_list:
                self.updateMarkers(a_list, e_list)

    def keyEvent(self, key, isKeyDown):
        if key == MARKERS.HOT_KEY and isKeyDown:
            self.settingsCore.applySettings({GAME.SHOW_VEHICLES_COUNTER: not self.markersEnable})

    def onSettingsApplied(self, diff):
        for name, setting in diff.iteritems():
            if name == GRAPHICS.COLOR_BLIND:
                self.color[cache.enemyTeam][MARKERS.ALIVE] = cfg.colors[MARKERS.NAME][self.colorblindString]
                if self.markersEnable:
                    self.onLoadUpdate()
            elif name == GAME.SHOW_VEHICLES_COUNTER:
                self.markersEnable = self.isMarkersEnabled(setting)
                if self.markersEnable:
                    self.onLoadUpdate()
                else:
                    self.as_clearMarkersS()

    def getIcon(self, vehicleID):
        vInfoVO = cache.arenaDP.getVehicleInfo(vehicleID)
        isAlive = vInfoVO.isAlive()
        if self.mcColor and isAlive:
            color = self.vcColor[vInfoVO.vehicleType.classTag]
        else:
            color = self.color[vInfoVO.team][isAlive]
        return MARKERS.ICON.format(color, MARKERS.TYPE_ICON[vInfoVO.vehicleType.classTag])

    def updateMarkers(self, leftCorrelationIDs, rightCorrelationIDs):
        self.as_markersS(GLOBAL.EMPTY_LINE.join(self.getIcon(vehicleID) for vehicleID in reversed(leftCorrelationIDs)),
                         GLOBAL.EMPTY_LINE.join(self.getIcon(vehicleID) for vehicleID in rightCorrelationIDs))

    def onLoadUpdate(self):
        correlationIDs = {cache.allyTeam: [], cache.enemyTeam: []}
        for vInfoVO in sorted(cache.arenaDP.getVehiclesInfoIterator(), key=FragCorrelationSortKey):
            correlationIDs[vInfoVO.team].append(vInfoVO.vehicleID)
        self.updateMarkers(correlationIDs[cache.allyTeam], correlationIDs[cache.enemyTeam])

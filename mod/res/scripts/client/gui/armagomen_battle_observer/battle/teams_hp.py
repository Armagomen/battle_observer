from account_helpers.settings_core.settings_constants import GRAPHICS
from gui.shared.personality import ServicesLocator

from ..core.battle_cache import cache, g_health
from ..core.bo_constants import HP_BARS
from ..core.config import cfg
from ..core.events import g_events
from ..meta.battle.team_health_meta import TeamHealthMeta


class TeamsHP(TeamHealthMeta):

    def __init__(self):
        super(TeamsHP, self).__init__()
        self.gui = self.sessionProvider.arenaVisitor.gui

    def onEnterBattlePage(self):
        super(TeamsHP, self).onEnterBattlePage()
        if not self.gui.isEpicBattle():
            self.as_startUpdateS(cfg.hp_bars, ServicesLocator.settingsCore.getSetting(GRAPHICS.COLOR_BLIND))
            self.onModuleStarted()
            g_events.updateHealthPoints += self.updateHealthPoints

    def onExitBattlePage(self):
        if not self.gui.isEpicBattle():
            g_events.updateHealthPoints -= self.updateHealthPoints
        super(TeamsHP, self).onExitBattlePage()

    def onModuleStarted(self):
        for team, team_name in cache.teams.iteritems():
            self.as_updateHealthS(team_name, g_health.getTeamCurrent(team), g_health.getTeamMaximum(team))
        self.updateDiff()

    def updateHealthPoints(self, team, team_current, team_maximum, *args):
        self.as_updateHealthS(cache.teams[team], team_current, team_maximum)
        self.updateDiff()

    def updateDiff(self):
        if cfg.hp_bars[HP_BARS.DIFF]:
            diff = g_health.getTeamCurrent(cache.allyTeam) - g_health.getTeamCurrent(cache.enemyTeam)
            self.as_differenceS(diff)

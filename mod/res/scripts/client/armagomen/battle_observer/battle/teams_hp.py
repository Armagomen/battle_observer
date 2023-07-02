from account_helpers.settings_core.settings_constants import GAME, GRAPHICS, ScorePanelStorageKeys as C_BAR
from armagomen._constants import HP_BARS
from armagomen.battle_observer.meta.battle.team_health_meta import TeamHealthMeta
from gui.battle_control.controllers.battle_field_ctrl import IBattleFieldListener
from PlayerEvents import g_playerEvents


class TeamsHP(TeamHealthMeta, IBattleFieldListener):

    def __init__(self):
        super(TeamsHP, self).__init__()
        self.showAliveCount = False
        self.observers = set(vInfo.vehicleID for vInfo in self._arenaDP.getVehiclesInfoIterator() if vInfo.isObserver())

    def _populate(self):
        super(TeamsHP, self)._populate()
        is_normal_mode = self.gui.isRandomBattle() or self.gui.isRankedBattle() or self.gui.isTrainingBattle()
        self.showAliveCount = self.settings[HP_BARS.ALIVE] and is_normal_mode
        self.settingsCore.onSettingsApplied += self.onSettingsApplied
        g_playerEvents.onAvatarReady += self.updateCounters

    def updateCounters(self):
        self.settingsCore.applySetting(C_BAR.SHOW_HP_BAR, False)
        self.settingsCore.applySetting(C_BAR.ENABLE_TIER_GROUPING, False)
        self.as_updateCountersPositionS()

    def _dispose(self):
        self.settingsCore.onSettingsApplied -= self.onSettingsApplied
        g_playerEvents.onAvatarReady -= self.updateCounters
        super(TeamsHP, self)._dispose()

    def updateTeamHealth(self, alliesHP, enemiesHP, totalAlliesHP, totalEnemiesHP):
        self.as_updateHealthS(alliesHP, enemiesHP, totalAlliesHP, totalEnemiesHP)

    def updateDeadVehicles(self, aliveAllies, deadAllies, aliveEnemies, deadEnemies):
        if self.showAliveCount:
            self.as_updateScoreS(len(aliveAllies.difference(deadAllies)), len(aliveEnemies.difference(deadEnemies)))
        else:
            if self.observers:
                deadEnemies = deadEnemies.difference(self.observers)
                deadAllies = deadAllies.difference(self.observers)
            self.as_updateScoreS(len(deadEnemies), len(deadAllies))

    def onSettingsApplied(self, diff):
        if GRAPHICS.COLOR_BLIND in diff:
            self.as_colorBlindS(bool(diff[GRAPHICS.COLOR_BLIND]))
        if GAME.SHOW_VEHICLES_COUNTER in diff or C_BAR.SHOW_HP_BAR in diff or C_BAR.ENABLE_TIER_GROUPING in diff:
            self.updateCounters()

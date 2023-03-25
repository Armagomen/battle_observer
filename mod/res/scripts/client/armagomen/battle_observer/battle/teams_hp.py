from account_helpers.settings_core.settings_constants import GAME, GRAPHICS, ScorePanelStorageKeys
from armagomen.battle_observer.meta.battle.team_health_meta import TeamHealthMeta
from armagomen.constants import HP_BARS
from gui.battle_control.controllers.battle_field_ctrl import IBattleFieldListener


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

    def _dispose(self):
        self.settingsCore.onSettingsApplied -= self.onSettingsApplied
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
        showTiers = diff.get(ScorePanelStorageKeys.ENABLE_TIER_GROUPING)
        if showTiers is None:
            showTiers = bool(self.settingsCore.getSetting(ScorePanelStorageKeys.ENABLE_TIER_GROUPING))
        if GAME.SHOW_VEHICLES_COUNTER in diff or showTiers:
            if showTiers:
                self.settingsCore.applySetting(ScorePanelStorageKeys.ENABLE_TIER_GROUPING, False)
            self.as_updateCorrelationBarS()

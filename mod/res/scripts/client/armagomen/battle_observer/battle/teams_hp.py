from account_helpers.settings_core.settings_constants import ScorePanelStorageKeys
from armagomen._constants import HP_BARS
from armagomen.battle_observer.meta.battle.team_health_meta import TeamHealthMeta
from armagomen.utils.logging import logDebug
from gui.battle_control.controllers.battle_field_ctrl import IBattleFieldListener


class TeamsHP(TeamHealthMeta, IBattleFieldListener):
    settingParams = set(ScorePanelStorageKeys.ALL())

    def __init__(self):
        super(TeamsHP, self).__init__()
        self.showAliveCount = False

    def _populate(self):
        super(TeamsHP, self)._populate()
        is_normal_mode = self.gui.isRandomBattle() or self.gui.isRankedBattle() or self.gui.isTrainingBattle()
        self.showAliveCount = self.settings[HP_BARS.ALIVE] and is_normal_mode
        self.updateDefaultTopPanel(self.settingParams)

    def updateDefaultTopPanel(self, settingKeys):
        if self.settings[HP_BARS.STYLE] == HP_BARS.STYLES.league_big:
            settingKeys = settingKeys.copy()
            settingKeys.discard(ScorePanelStorageKeys.ENABLE_TIER_GROUPING)
        if settingKeys and any(self.settingsCore.applySetting(key, False) is not None for key in settingKeys):
            self.settingsCore.applyStorages(False)
            self.settingsCore.clearStorages()

    def updateTeamHealth(self, alliesHP, enemiesHP, totalAlliesHP, totalEnemiesHP):
        self.as_updateHealthS(alliesHP, enemiesHP, max(alliesHP, totalAlliesHP), max(enemiesHP, totalEnemiesHP))

    def updateDeadVehicles(self, aliveAllies, deadAllies, aliveEnemies, deadEnemies):
        if self.showAliveCount:
            self.as_updateScoreS(len(aliveAllies), len(aliveEnemies))
            logDebug("aliveAllies: {}, aliveEnemies: {}", aliveAllies, aliveEnemies)
        else:
            self.as_updateScoreS(len(deadEnemies), len(deadAllies))
            logDebug("deadEnemies: {} deadAllies: {}", deadEnemies, deadAllies)

    def onColorblindUpdated(self, blind):
        self.as_colorBlindS(blind)

    def onSettingsApplied(self, diff):
        super(TeamsHP, self).onSettingsApplied(diff)
        keys = {key for key, value in diff.items() if key in self.settingParams and value}
        if keys:
            self.updateDefaultTopPanel(keys)

from account_helpers.settings_core.settings_constants import GRAPHICS, ScorePanelStorageKeys as C_BAR
from armagomen._constants import HP_BARS
from armagomen.battle_observer.meta.battle.team_health_meta import TeamHealthMeta
from gui.battle_control.controllers.battle_field_ctrl import IBattleFieldListener
from PlayerEvents import g_playerEvents


class TeamsHP(TeamHealthMeta, IBattleFieldListener):

    def __init__(self):
        super(TeamsHP, self).__init__()
        self.showAliveCount = False
        self.__observers = None

    def _populate(self):
        super(TeamsHP, self)._populate()
        is_normal_mode = self.gui.isRandomBattle() or self.gui.isRankedBattle() or self.gui.isTrainingBattle()
        self.showAliveCount = self.settings[HP_BARS.ALIVE] and is_normal_mode
        self.settingsCore.onSettingsApplied += self.onSettingsApplied
        g_playerEvents.onAvatarReady += self.updateDefaultTopPanel

    @property
    def observers(self):
        if self.__observers is None:
            self.__observers = set(
                vInfo.vehicleID for vInfo in self._arenaDP.getVehiclesInfoIterator() if vInfo.isObserver())
        return self.__observers

    def updateDefaultTopPanel(self, settingName=None):
        result = None
        items = (C_BAR.ENABLE_TIER_GROUPING, C_BAR.SHOW_HP_BAR)
        if settingName is not None:
            items = (settingName,)
        for key in items:
            if self.settingsCore.getSetting(key):
                result = self.settingsCore.applySetting(key, False)
        if result is not None:
            self.settingsCore.applyStorages(False)
            self.settingsCore.clearStorages()

    def _dispose(self):
        self.settingsCore.onSettingsApplied -= self.onSettingsApplied
        g_playerEvents.onAvatarReady -= self.updateDefaultTopPanel
        super(TeamsHP, self)._dispose()

    def updateTeamHealth(self, alliesHP, enemiesHP, totalAlliesHP, totalEnemiesHP):
        self.as_updateHealthS(alliesHP, enemiesHP, max(alliesHP, totalAlliesHP), max(enemiesHP, totalEnemiesHP))

    def updateDeadVehicles(self, aliveAllies, deadAllies, aliveEnemies, deadEnemies):
        if self.showAliveCount:
            self.as_updateScoreS(len(aliveAllies.difference(deadAllies)), len(aliveEnemies.difference(deadEnemies)))
        else:
            if self.observers:
                deadEnemies = deadEnemies.difference(self.observers)
                deadAllies = deadAllies.difference(self.observers)
            self.as_updateScoreS(len(deadEnemies), len(deadAllies))

    def onSettingsApplied(self, diff):
        for key, value in diff.iteritems():
            if key == GRAPHICS.COLOR_BLIND:
                self.as_colorBlindS(bool(value))
            elif key in (C_BAR.SHOW_HP_BAR, C_BAR.ENABLE_TIER_GROUPING) and value:
                self.updateDefaultTopPanel(key)

from account_helpers.settings_core.settings_constants import GRAPHICS, ScorePanelStorageKeys
from gui.battle_control.controllers.battle_field_ctrl import IBattleFieldListener
from gui.shared.personality import ServicesLocator
from ..core.bo_constants import HP_BARS
from ..core.config import cfg
from ..meta.battle.team_health_meta import TeamHealthMeta


class TeamsHP(TeamHealthMeta, IBattleFieldListener):

    def __init__(self):
        super(TeamsHP, self).__init__()
        self.gui = self.sessionProvider.arenaVisitor.gui

    def _populate(self):
        super(TeamsHP, self)._populate()
        if not self.gui.isEpicBattle():
            self.as_startUpdateS(cfg.hp_bars, ServicesLocator.settingsCore.getSetting(GRAPHICS.COLOR_BLIND))
            # if not ServicesLocator.settingsCore.getSetting(ScorePanelStorageKeys.SHOW_HP_BAR):
            #     ServicesLocator.settingsCore.applySetting(ScorePanelStorageKeys.SHOW_HP_BAR, True)

    def updateTeamHealth(self, alliesHP, enemiesHP, totalAlliesHP, totalEnemiesHP):
        self.as_updateHealthS(alliesHP, enemiesHP, totalAlliesHP, totalEnemiesHP)
        if cfg.hp_bars[HP_BARS.DIFF]:
            self.as_differenceS(alliesHP - enemiesHP)

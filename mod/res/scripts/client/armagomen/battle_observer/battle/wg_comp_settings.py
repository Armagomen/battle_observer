from armagomen.battle_observer.core import cfg
from armagomen.battle_observer.core.constants import GLOBAL, MAIN
from armagomen.battle_observer.meta.battle.wg_comp_meta import WgCompMeta


class WGCompSettings(WgCompMeta):

    def moveWGItems(self):
        return cfg.markers[GLOBAL.ENABLED] and cfg.hp_bars[GLOBAL.ENABLED] and \
               not self.sessionProvider.arenaVisitor.gui.isEpicRandomBattle()

    def onEnterBattlePage(self):
        super(WGCompSettings, self).onEnterBattlePage()
        move = self.moveWGItems()
        self.as_enableAnimationS(cfg.main[MAIN.ENABLE_BARS_ANIMATION])
        self.as_moveQuestsS(move)
        if cfg.main[MAIN.REMOVE_SHADOW_IN_PREBATTLE]:
            self.as_hideShadowInPreBattleS()
        if cfg.main[MAIN.HIDE_CHAT] and self.sessionProvider.arenaVisitor.gui.isRandomBattle():
            self.as_hideMessengerS()
        if not cfg.team_bases_panel[GLOBAL.ENABLED] and move:
            self.as_moveTeamBasesPanelS()

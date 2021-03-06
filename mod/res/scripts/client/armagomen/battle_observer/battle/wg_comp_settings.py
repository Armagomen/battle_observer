from armagomen.battle_observer.core import config
from armagomen.battle_observer.core.constants import GLOBAL, MAIN
from armagomen.battle_observer.meta.battle.wg_comp_meta import WgCompMeta


class WGCompSettings(WgCompMeta):

    def moveWGItems(self):
        return config.markers[GLOBAL.ENABLED] and config.hp_bars[GLOBAL.ENABLED] and \
               not self.sessionProvider.arenaVisitor.gui.isEpicRandomBattle()

    def onEnterBattlePage(self):
        super(WGCompSettings, self).onEnterBattlePage()
        move = self.moveWGItems()
        self.as_enableAnimationS(config.main[MAIN.ENABLE_BARS_ANIMATION])
        self.as_moveQuestsS(move)
        if config.main[MAIN.REMOVE_SHADOW_IN_PREBATTLE]:
            self.as_hideShadowInPreBattleS()
        if config.main[MAIN.HIDE_CHAT] and self.sessionProvider.arenaVisitor.gui.isRandomBattle():
            self.as_hideMessengerS()
        if not config.team_bases_panel[GLOBAL.ENABLED] and move:
            self.as_moveTeamBasesPanelS()

from armagomen.constants import MAIN
from armagomen.battle_observer.meta.battle.wg_comp_meta import WgCompMeta


class WGCompSettings(WgCompMeta):

    def onEnterBattlePage(self):
        super(WGCompSettings, self).onEnterBattlePage()
        if self.settings[MAIN.REMOVE_SHADOW_IN_PREBATTLE]:
            self.as_hideShadowInPreBattleS()
        if self.settings[MAIN.HIDE_CHAT] and self.sessionProvider.arenaVisitor.gui.isRandomBattle():
            self.as_hideMessengerS()

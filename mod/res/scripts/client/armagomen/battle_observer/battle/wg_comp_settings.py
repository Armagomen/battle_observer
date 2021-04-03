from armagomen.battle_observer.core.bo_constants import MAIN
from armagomen.battle_observer.meta.battle.wg_comp_meta import WgCompMeta


class WGCompSettings(WgCompMeta):

    def onEnterBattlePage(self):
        super(WGCompSettings, self).onEnterBattlePage()
        self.as_enableAnimationS(self.settings.main[MAIN.ENABLE_BARS_ANIMATION])
        if self.settings.main[MAIN.REMOVE_SHADOW_IN_PREBATTLE]:
            self.as_hideShadowInPreBattleS()
        if self.settings.main[MAIN.HIDE_CHAT] and self.sessionProvider.arenaVisitor.gui.isRandomBattle():
            self.as_hideMessengerS()

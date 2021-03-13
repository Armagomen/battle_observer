from armagomen.battle_observer.core import config
from armagomen.battle_observer.core.bo_constants import GLOBAL, MAIN, MARKERS
from armagomen.battle_observer.meta.battle.wg_comp_meta import WgCompMeta


class WGCompSettings(WgCompMeta):

    def onEnterBattlePage(self):
        super(WGCompSettings, self).onEnterBattlePage()
        self.as_enableAnimationS(config.main[MAIN.ENABLE_BARS_ANIMATION])
        if config.hp_bars[GLOBAL.ENABLED] and config.hp_bars[MARKERS.NAME][GLOBAL.ENABLED]:
            self.as_moveTeamBasesPanelS()
        if config.main[MAIN.REMOVE_SHADOW_IN_PREBATTLE]:
            self.as_hideShadowInPreBattleS()
        if config.main[MAIN.HIDE_CHAT] and self.sessionProvider.arenaVisitor.gui.isRandomBattle():
            self.as_hideMessengerS()

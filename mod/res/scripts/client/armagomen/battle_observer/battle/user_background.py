from armagomen.battle_observer.core import config
from armagomen.battle_observer.core.constants import MAIN, HP_BARS
from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class UserBackGround(BaseModMeta):

    def onEnterBattlePage(self):
        super(UserBackGround, self).onEnterBattlePage()
        data = {
            "bg_vis": config.hp_bars[HP_BARS.STYLE] == HP_BARS.NORMAL_STYLE and config.main[MAIN.BG],
            "isLeague": config.hp_bars[HP_BARS.STYLE] == HP_BARS.LEAGUE_STYLE,
            "bg_alpha": config.main[MAIN.BG_TRANSPARENCY],
            "uBG": config.user_background
        }
        self.as_startUpdateS(data)

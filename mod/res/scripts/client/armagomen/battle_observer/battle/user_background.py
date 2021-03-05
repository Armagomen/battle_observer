from armagomen.battle_observer.core import cfg
from armagomen.battle_observer.core.bo_constants import MAIN, HP_BARS
from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class UserBackGround(BaseModMeta):

    @property
    def checkStyle(self):
        return cfg.hp_bars[HP_BARS.STYLE] == HP_BARS.NORMAL_STYLE and cfg.main[MAIN.BG]

    def onEnterBattlePage(self):
        super(UserBackGround, self).onEnterBattlePage()
        data = {
            "bg_vis": self.checkStyle,
            "bg_alpha": cfg.main[MAIN.BG_TRANSPARENCY],
            "uBG": cfg.user_background
        }
        self.as_startUpdateS(data)

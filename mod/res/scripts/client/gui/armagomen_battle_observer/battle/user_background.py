from ..core.bo_constants import MAIN, HP_BARS
from ..core import cfg
from ..meta.battle.base_mod_meta import BaseModMeta


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

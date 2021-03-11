from armagomen.battle_observer.core import config
from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class UserBackGround(BaseModMeta):

    def onEnterBattlePage(self):
        super(UserBackGround, self).onEnterBattlePage()
        self.as_startUpdateS(config.user_background)

from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class UserBackGround(BaseModMeta):

    def onEnterBattlePage(self):
        self.as_startUpdateS(self.settings)
        super(UserBackGround, self).onEnterBattlePage()
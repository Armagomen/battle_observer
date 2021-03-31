from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class UserBackGround(BaseModMeta):

    def onEnterBattlePage(self):
        super(UserBackGround, self).onEnterBattlePage()
        self.as_startUpdateS(self.settings.user_background)

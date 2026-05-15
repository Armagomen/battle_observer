from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class OwnHealthMeta(BaseModMeta):

    def as_setOwnHealthS(self, scale, text, color):
        if self._isDAAPIInited():
            self.flashObject.as_setOwnHealth(scale, text, color)

    def as_BarVisibleS(self, visible):
        if self._isDAAPIInited():
            self.flashObject.as_BarVisible(visible)

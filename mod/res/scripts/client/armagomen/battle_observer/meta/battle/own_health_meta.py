from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class OwnHealthMeta(BaseModMeta):


    def as_setOwnHealthS(self, scale, text, color):
        return self.flashObject.as_setOwnHealth(scale, text, color) if self._isDAAPIInited() else None

    def as_BarVisibleS(self, visible):
        return self.flashObject.as_BarVisible(visible) if self._isDAAPIInited() else None

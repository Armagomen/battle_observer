from armagomen.battle_observer.meta.lobby.base_mod_meta import BaseModMeta


class AvgDataMeta(BaseModMeta):
    def as_setDataS(self, text):
        return self.flashObject.as_setData(text) if self._isDAAPIInited() else None

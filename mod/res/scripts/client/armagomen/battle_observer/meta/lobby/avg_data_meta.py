from armagomen.battle_observer.meta.lobby.base_mod_meta import BaseModMeta


class AvgDataMeta(BaseModMeta):
    def as_setDataS(self, text):
        return self.flashObject.as_setData(text) if self._isDAAPIInited() else None

    def as_updatePositionsS(self, enabled):
        return self.flashObject.as_updatePositions(enabled) if self._isDAAPIInited() else None

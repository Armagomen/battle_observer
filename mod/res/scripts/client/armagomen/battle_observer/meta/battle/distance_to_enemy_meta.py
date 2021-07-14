from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class DistanceMeta(BaseModMeta):

    def __init__(self):
        super(DistanceMeta, self).__init__()

    def as_setDistanceS(self, text):
        return self.flashObject.as_setDistance(text) if self._isDAAPIInited() else None

from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class OwnHealthMeta(BaseModMeta):

    def __init__(self):
        super(OwnHealthMeta, self).__init__()

    def as_setOwnHealthS(self, scale, text, color):
        return self.flashObject.as_setOwnHealth(scale, text, color) if self._isDAAPIInited() else None

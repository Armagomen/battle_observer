from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class MinimapMeta(BaseModMeta):

    def __init__(self):
        super(MinimapMeta, self).__init__()

    def as_MinimapCenteredS(self, enable):
        return self.flashObject.as_MinimapCentered(enable) if self._isDAAPIInited() else None

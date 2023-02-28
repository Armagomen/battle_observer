from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class DebugPanelMeta(BaseModMeta):

    def __init__(self):
        super(DebugPanelMeta, self).__init__()

    def as_updateS(self, ping, fps, isLaggingNow):
        return self.flashObject.as_update(ping, fps, isLaggingNow) if self._isDAAPIInited() else None

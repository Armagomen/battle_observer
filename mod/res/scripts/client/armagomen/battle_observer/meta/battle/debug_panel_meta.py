from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class DebugPanelMeta(BaseModMeta):

    def __init__(self):
        super(DebugPanelMeta, self).__init__()

    def as_fpsPingS(self, debug, fps, ping):
        return self.flashObject.as_fpsPing(debug, fps, ping) if self._isDAAPIInited() else None

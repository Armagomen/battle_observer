from armagomen.battle_observer.meta.lobby.base_mod_meta import BaseModMeta


class HangarEfficiencyMeta(BaseModMeta):

    def __init__(self):
        super(HangarEfficiencyMeta, self).__init__()

    def as_updateValueS(self, value):
        return self.flashObject.as_updateValue(value) if self._isDAAPIInited() else None

    def as_addToStageS(self):
        self.flashObject.as_addToStage() if self._isDAAPIInited() else None

    def as_clearSceneS(self):
        self.flashObject.as_clearScene() if self._isDAAPIInited() else None

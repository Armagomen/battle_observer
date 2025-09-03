from armagomen.battle_observer.meta.lobby.base_mod_meta import BaseModMeta


class DateTimesMeta(BaseModMeta):

    def __init__(self):
        super(DateTimesMeta, self).__init__()

    def as_updateTimeS(self, text):
        self.flashObject.as_updateTime(text) if self._isDAAPIInited() else None

    def as_addToStageS(self):
        self.flashObject.as_addToStage() if self._isDAAPIInited() else None

    def as_clearSceneS(self):
        self.flashObject.as_clearScene() if self._isDAAPIInited() else None

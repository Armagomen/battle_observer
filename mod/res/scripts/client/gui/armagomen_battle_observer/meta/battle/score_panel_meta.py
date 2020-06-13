from .base_mod_meta import BaseModMeta


class ScorePanelMeta(BaseModMeta):

    def __init__(self):
        super(ScorePanelMeta, self).__init__()

    def as_updateScoreS(self, ally, enemy):
        return self.flashObject.as_updateScore(ally, enemy) if self._isDAAPIInited() else None

    def as_markersS(self, left, right):
        return self.flashObject.as_markers(left, right) if self._isDAAPIInited() else None

    def as_clearMarkersS(self):
        return self.flashObject.as_clearMarkers() if self._isDAAPIInited() else None

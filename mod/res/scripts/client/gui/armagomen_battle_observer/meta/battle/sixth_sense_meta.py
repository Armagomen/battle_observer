from .base_mod_meta import BaseModMeta


class SixthSenseMeta(BaseModMeta):

    def __init__(self):
        super(SixthSenseMeta, self).__init__()

    def as_showS(self):
        return self.flashObject.as_show() if self._isDAAPIInited() else None

    def as_hideS(self):
        return self.flashObject.as_hide() if self._isDAAPIInited() else None

    def as_updateTimerS(self, text):
        return self.flashObject.as_updateTimer(text) if self._isDAAPIInited() else None

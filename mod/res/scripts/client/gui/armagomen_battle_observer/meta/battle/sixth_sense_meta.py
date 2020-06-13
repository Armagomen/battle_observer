from .base_mod_meta import BaseModMeta

class SixthSenseMeta(BaseModMeta):

    def __init__(self):
        super(SixthSenseMeta, self).__init__()
        
    def as_sixthSenseS(self, show, text):
        return self.flashObject.as_sixthSense(show, text) if self._isDAAPIInited() else None
from .base_mod_meta import BaseModMeta

class FlyghtTimeMeta(BaseModMeta):

    def __init__(self):
        super(FlyghtTimeMeta, self).__init__()
        
    def as_flyghtTimeS(self, text):
        return self.flashObject.as_flyghtTime(text) if self._isDAAPIInited() else None  

from .base_mod_meta import BaseModMeta

class DateTimesMeta(BaseModMeta):

    def __init__(self):
        super(DateTimesMeta, self).__init__()
        
    def as_setDateTimeS(self, text):
        return self.flashObject.as_setDateTime(text) if self._isDAAPIInited() else None    
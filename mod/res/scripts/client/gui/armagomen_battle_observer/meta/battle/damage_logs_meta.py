from .base_mod_meta import BaseModMeta


class DamageLogsMeta(BaseModMeta):

    def __init__(self):
        super(DamageLogsMeta, self).__init__()

    def as_updateLogS(self, inLog, text):
        return self.flashObject.as_updateLog(inLog, text) if self._isDAAPIInited() else None

    def as_updateDamageS(self, text):
        return self.flashObject.as_updateDamage(text) if self._isDAAPIInited() else None

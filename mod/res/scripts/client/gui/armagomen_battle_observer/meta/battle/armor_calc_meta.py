from .base_mod_meta import BaseModMeta


class ArmorCalcMeta(BaseModMeta):

    def __init__(self):
        super(ArmorCalcMeta, self).__init__()

    def as_armorCalcS(self, text):
        return self.flashObject.as_armorCalc(text) if self._isDAAPIInited() else None

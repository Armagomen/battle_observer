from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class ArmorCalcMeta(BaseModMeta):

    def __init__(self):
        super(ArmorCalcMeta, self).__init__()

    def as_armorCalcS(self, text):
        return self.flashObject.as_armorCalc(text) if self._isDAAPIInited() else None

    def as_clearMessage(self):
        return self.flashObject.as_armorCalc("") if self._isDAAPIInited() else None

    def as_updateColor(self, color):
        return self.flashObject.as_updateColor(color) if self._isDAAPIInited() else None

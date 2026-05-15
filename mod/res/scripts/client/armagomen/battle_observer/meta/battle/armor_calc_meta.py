from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class ArmorCalcMeta(BaseModMeta):

    def __init__(self):
        super(ArmorCalcMeta, self).__init__()

    def as_armorCalcS(self, text):
        if self._isDAAPIInited():
            self.flashObject.as_armorCalc(text)

    def as_clearMessage(self):
        if self._isDAAPIInited():
            self.flashObject.as_armorCalc("")

    def as_updateColor(self, color):
        if self._isDAAPIInited():
            self.flashObject.as_updateColor(color)

from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class SixthSenseMeta(BaseModMeta):

    def __init__(self):
        super(SixthSenseMeta, self).__init__()

    def as_showS(self, seconds):
        if self._isDAAPIInited():
            self.flashObject.as_show(seconds)

    def as_hideS(self):
        if self._isDAAPIInited():
            self.flashObject.as_hide()

    def playSound(self):
        pass

    def getIconName(self):
        return "lamp_2.png"

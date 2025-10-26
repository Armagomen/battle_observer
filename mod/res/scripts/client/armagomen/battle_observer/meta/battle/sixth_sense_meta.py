from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class SixthSenseMeta(BaseModMeta):

    def __init__(self):
        super(SixthSenseMeta, self).__init__()

    def as_showS(self, seconds):
        return self.flashObject.as_show(seconds) if self._isDAAPIInited() else None

    def as_hideS(self):
        return self.flashObject.as_hide() if self._isDAAPIInited() else None

    def playSound(self):
        pass

    def getIconName(self):
        return "lamp_2.png"

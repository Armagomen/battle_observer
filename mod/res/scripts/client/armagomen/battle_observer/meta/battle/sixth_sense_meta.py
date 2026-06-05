from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class SixthSenseMeta(BaseModMeta):

    def __init__(self):
        super(SixthSenseMeta, self).__init__()

    def as_invoke(self, seconds, percentage):
        if self._isDAAPIInited():
            self.flashObject.as_invoke(seconds, percentage)

    def as_show(self):
        if self._isDAAPIInited():
            self.flashObject.as_show()

    def getIconName(self):
        return "lamp_2.png"

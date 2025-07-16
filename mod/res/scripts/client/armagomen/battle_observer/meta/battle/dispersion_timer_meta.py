from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class DispersionTimerMeta(BaseModMeta):

    def __init__(self):
        super(DispersionTimerMeta, self).__init__()
        self._isColorBlind = self.isColorBlind()

    def as_updateTimerTextS(self, text):
        return self.flashObject.as_upateTimerText(text) if self._isDAAPIInited() else None

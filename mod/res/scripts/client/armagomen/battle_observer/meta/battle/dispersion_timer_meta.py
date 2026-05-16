from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class DispersionTimerMeta(BaseModMeta):

    def as_updateTimerTextS(self, text, color):
        if self._isDAAPIInited():
            self.flashObject.as_upateTimerText(text, color)

from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class DispersionTimerMeta(BaseModMeta):

    def as_updateTimerTextS(self, text, color):
        return self.flashObject.as_upateTimerText(text, color) if self._isDAAPIInited() else None

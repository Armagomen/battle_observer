from .base_mod_meta import BaseModMeta

class BattleTimerMeta(BaseModMeta):

    def __init__(self):
        super(BattleTimerMeta, self).__init__()
        
    def as_timerS(self, timer):
        return self.flashObject.as_timer(timer) if self._isDAAPIInited() else None
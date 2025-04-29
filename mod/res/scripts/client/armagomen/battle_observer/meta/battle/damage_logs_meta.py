from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class DamageLogsMeta(BaseModMeta):

    def __init__(self):
        super(DamageLogsMeta, self).__init__()

    def as_updateTopLogS(self, text):
        return self.flashObject.as_updateTopLog(text) if self._isDAAPIInited() else None

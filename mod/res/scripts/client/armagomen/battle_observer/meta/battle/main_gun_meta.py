from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class MainGunMeta(BaseModMeta):

    def __init__(self):
        super(MainGunMeta, self).__init__()

    def as_gunDataS(self, value, max_value, warning):
        return self.flashObject.as_gunData(value, max_value, warning) if self._isDAAPIInited() else None

from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class DistanceMeta(BaseModMeta):

    def __init__(self):
        super(DistanceMeta, self).__init__()

    def as_setUpdateEnabled(self, param):
        if self._isDAAPIInited():
            self.flashObject.as_setUpdateEnabled(param)

    def getUpdatedDistance(self):
        return ''

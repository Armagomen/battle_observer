from .base_mod_meta import BaseModMeta


class TeamHealthMeta(BaseModMeta):

    def __init__(self):
        super(TeamHealthMeta, self).__init__()

    def as_updateHealthS(self, alliesHP, enemiesHP, totalAlliesHP, totalEnemiesHP):
        return self.flashObject.as_updateHealth(alliesHP, enemiesHP, totalAlliesHP,
                                                totalEnemiesHP) if self._isDAAPIInited() else None

    def as_differenceS(self, diff):
        return self.flashObject.as_difference(diff) if self._isDAAPIInited() else None

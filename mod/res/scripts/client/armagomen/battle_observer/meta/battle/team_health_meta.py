from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class TeamHealthMeta(BaseModMeta):

    def __init__(self):
        super(TeamHealthMeta, self).__init__()

    def as_updateHealthS(self, alliesHP, enemiesHP, totalAlliesHP, totalEnemiesHP):
        if self._isDAAPIInited():
            self.flashObject.as_updateHealth(alliesHP, enemiesHP, totalAlliesHP, totalEnemiesHP)

    def as_updateScoreS(self, ally, enemy):
        if self._isDAAPIInited():
            self.flashObject.as_updateScore(ally, enemy)

    def as_updateCorrelationBarS(self):
        if self._isDAAPIInited():
            self.flashObject.as_updateCorrelationBar()

from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class TeamHealthMeta(BaseModMeta):

    def __init__(self):
        super(TeamHealthMeta, self).__init__()

    def as_updateHealthS(self, alliesHP, enemiesHP, totalAlliesHP, totalEnemiesHP):
        return self.flashObject.as_updateHealth(alliesHP, enemiesHP, totalAlliesHP,
                                                totalEnemiesHP) if self._isDAAPIInited() else None

    def as_updateCountersPositionS(self):
        return self.flashObject.as_updateCountersPosition() if self._isDAAPIInited() else None

    def as_updateScoreS(self, ally, enemy):
        return self.flashObject.as_updateScore(ally, enemy) if self._isDAAPIInited() else None

    def as_updateCorrelationBarS(self):
        return self.flashObject.as_updateCorrelationBar() if self._isDAAPIInited() else None

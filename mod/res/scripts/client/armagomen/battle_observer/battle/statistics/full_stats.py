from armagomen.battle_observer.meta.battle.stats_meta import StatsMeta, STATISTICS


class FullStats(StatsMeta):

    def getPattern(self, isEnemy):
        return self.settings[STATISTICS.TAB_RIGHT] if isEnemy else self.settings[STATISTICS.TAB_LEFT], None

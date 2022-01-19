from armagomen.battle_observer.meta.battle.stats_meta import StatsMeta, STATISTICS


class PlayersPanelsStatistic(StatsMeta):

    def getPattern(self, isEnemy):
        return self.settings[STATISTICS.PANELS_RIGHT] if isEnemy else self.settings[STATISTICS.PANELS_LEFT], \
               self.settings[STATISTICS.PANELS_RIGHT_CUT] if isEnemy else self.settings[STATISTICS.PANELS_LEFT_CUT]

    def py_getCutWidth(self):
        return self.settings[STATISTICS.PANELS_CUT_WIDTH]

    def py_getFullWidth(self):
        return self.settings[STATISTICS.PANELS_FULL_WIDTH]

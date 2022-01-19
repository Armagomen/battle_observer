from armagomen.battle_observer.meta.battle.stats_meta import StatsMeta, STATISTICS, g_events


class BattleLoading(StatsMeta):

    def getPattern(self, isEnemy):
        return self.settings[STATISTICS.LOADING_RIGHT] if isEnemy else self.settings[STATISTICS.LOADING_LEFT], None

    def onEnterBattlePage(self):
        g_events.updateVehicleData -= self._updateVehicleData

from armagomen.battle_observer.meta.battle.stats_meta import StatsMeta, STATISTICS


class BattleLoading(StatsMeta):

    def __init__(self):
        super(BattleLoading, self).__init__()
        self.__update = True

    def getPattern(self, isEnemy):
        return self.settings[STATISTICS.LOADING_RIGHT] if isEnemy else self.settings[STATISTICS.LOADING_LEFT], None

    def _updateVehicleData(self, isEnemy, vehicleID):
        if self.__update:
            super(BattleLoading, self)._updateVehicleData(isEnemy, vehicleID)

    def onEnterBattlePage(self):
        self.__update = False

    def onExitBattlePage(self):
        self.__update = True

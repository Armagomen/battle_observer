from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta
from armagomen.battle_observer.statistics.statistic_data_loader import getCachedStatisticData


class StatsMeta(BaseModMeta):
    def __init__(self):
        super(StatsMeta, self).__init__()
        self.statisticsData = getCachedStatisticData(
            vInfo.player.accountDBID for vInfo in self._arenaDP.getVehiclesInfoIterator())

    @staticmethod
    def py_statisticEnabled():
        return False

    @staticmethod
    def py_iconEnabled():
        return True

    def py_getStatisticString(self, accountDBID, isEnemy):
        pass

    def py_getIconColor(self, vehicleID):
        pass

    @staticmethod
    def py_getIconMultiplier():
        pass

from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta
from armagomen.battle_observer.statistics.statistic_data_loader import getCachedStatisticData


class StatsMeta(BaseModMeta):
    def __init__(self):
        super(StatsMeta, self).__init__()
        self.statisticsData = getCachedStatisticData(
            vInfo.player.accountDBID for vInfo in self._arenaDP.getVehiclesInfoIterator())

    def as_updateVehicleStatusS(self, data):
        return self.flashObject.as_updateVehicleStatus(data) if self._isDAAPIInited() else None

    def as_showStats(self, statisticEnabled, iconEnabled):
        return self.flashObject.as_showStats(statisticEnabled, iconEnabled) if self._isDAAPIInited() else None

    def py_getStatisticString(self, accountDBID, isEnemy):
        pass

    def py_getIconColor(self, vehicleID):
        pass

    @staticmethod
    def py_getIconMultiplier():
        pass

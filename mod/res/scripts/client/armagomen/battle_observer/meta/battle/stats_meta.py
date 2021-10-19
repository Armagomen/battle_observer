from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta
from armagomen.battle_observer.statistics.statistic_data_loader import getCachedStatisticData, statisticEnabled
from armagomen.constants import STATISTICS


class StatsMeta(BaseModMeta):
    def __init__(self):
        super(StatsMeta, self).__init__()
        self.statisticsData = getCachedStatisticData(
            vInfo.player.accountDBID for vInfo in self._arenaDP.getVehiclesInfoIterator())

    def py_statisticEnabled(self):
        return statisticEnabled and self.settings[STATISTICS.STATISTIC_ENABLED]

    def py_iconEnabled(self):
        return self.settings[STATISTICS.ICON_ENABLED]

    def py_getIconMultiplier(self):
        return self.settings[STATISTICS.ICON_BLACKOUT]

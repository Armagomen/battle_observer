from armagomen.battle_observer.core import settings
from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta
from armagomen.battle_observer.statistics.statistic_data_loader import getCachedStatisticData
from armagomen.constants import STATISTICS


class StatsMeta(BaseModMeta):
    def __init__(self):
        super(StatsMeta, self).__init__()
        self.statisticsData = getCachedStatisticData(
            vInfo.player.accountDBID for vInfo in self._arenaDP.getVehiclesInfoIterator())

    @staticmethod
    def py_statisticEnabled():
        return settings.statistics[STATISTICS.STATISTIC_ENABLED]

    @staticmethod
    def py_iconEnabled():
        return settings.statistics[STATISTICS.ICON_ENABLED]

    @staticmethod
    def py_getIconMultiplier():
        return settings.statistics[STATISTICS.ICON_BLACKOUT]

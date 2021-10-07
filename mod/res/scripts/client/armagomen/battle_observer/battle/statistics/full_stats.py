from armagomen.battle_observer.meta.battle.stats_meta import StatsMeta
from armagomen.battle_observer.statistics.statistic_wtr import getStatisticString
from armagomen.constants import VEHICLE_TYPES, STATISTICS


class FullStats(StatsMeta):

    def py_getStatisticString(self, accountDBID, isEnemy, vehicleID):
        pattern = self.settings[STATISTICS.TAB_RIGHT] if isEnemy else self.settings[STATISTICS.TAB_LEFT]
        vInfoVO = self._arenaDP.getVehicleInfo(vehicleID)
        result = getStatisticString(accountDBID, self.statisticsData, vInfoVO.player.clanAbbrev)
        if result is not None:
            return pattern % result
        return None

    def py_getIconColor(self, vehicleID):
        vInfoVO = self._arenaDP.getVehicleInfo(vehicleID)
        return self.vehicle_types[VEHICLE_TYPES.CLASS_COLORS].get(vInfoVO.vehicleType.classTag)

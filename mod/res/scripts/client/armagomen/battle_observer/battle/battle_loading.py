# coding=utf-8
from armagomen.battle_observer.core import settings
from armagomen.battle_observer.meta.battle.stats_meta import StatsMeta
from armagomen.battle_observer.statistics.statistic_data_loader import statisticEnabled
from armagomen.battle_observer.statistics.statistic_wtr import getStatisticString
from armagomen.constants import VEHICLE_TYPES, PANELS
from armagomen.utils.common import callback

ALLY_PATTERN = "<font color='%(colorWTR)s'>[%(WTR)d]</font><font color='%(colorWTR)s'>%(nickname).10s</font>"
ENEMY_PATTERN = "<font color='%(colorWTR)s'>%(nickname).10s</font><font color='%(colorWTR)s'>[%(WTR)d]</font>"


class BattleLoading(StatsMeta):

    def _populate(self):
        super(BattleLoading, self)._populate()
        if statisticEnabled and self.statisticsData:
            callback(0.01, self.afterPopulate)

    def afterPopulate(self):
        self.as_showStats(settings.players_panels[PANELS.STATISTIC_ENABLED],
                          settings.players_panels[PANELS.ICONS_ENABLED])

    def py_getStatisticString(self, accountDBID, isEnemy):
        pattern = ENEMY_PATTERN if isEnemy else ALLY_PATTERN
        return pattern % getStatisticString(accountDBID, self.statisticsData)

    def py_getIconColor(self, vehicleID):
        vInfoVO = self._arenaDP.getVehicleInfo(vehicleID)
        return self.vehicle_types[VEHICLE_TYPES.CLASS_COLORS].get(vInfoVO.vehicleType.classTag)

    @staticmethod
    def py_getIconMultiplier():
        return settings.players_panels[PANELS.ICONS_BLACKOUT]

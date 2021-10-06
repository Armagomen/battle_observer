# coding=utf-8
from armagomen.battle_observer.core import settings
from armagomen.battle_observer.meta.battle.stats_meta import StatsMeta
from armagomen.battle_observer.statistics.statistic_wtr import getStatisticString
from armagomen.constants import VEHICLE_TYPES, PANELS

ALLY_PATTERN = "<font color='%(colorWTR)s'>[%(WTR)d]</font><font color='%(colorWTR)s'>%(nickname)s</font>"
ENEMY_PATTERN = "<font color='%(colorWTR)s'>%(nickname)s</font><font color='%(colorWTR)s'>[%(WTR)d]</font>"


class FullStats(StatsMeta):

    @staticmethod
    def py_statisticEnabled():
        return settings.players_panels[PANELS.STATISTIC_ENABLED]

    @staticmethod
    def py_iconEnabled():
        return settings.players_panels[PANELS.ICONS_ENABLED]

    def py_getStatisticString(self, accountDBID, isEnemy):
        pattern = ENEMY_PATTERN if isEnemy else ALLY_PATTERN
        return pattern % getStatisticString(accountDBID, self.statisticsData)

    def py_getIconColor(self, vehicleID):
        vInfoVO = self._arenaDP.getVehicleInfo(vehicleID)
        return self.vehicle_types[VEHICLE_TYPES.CLASS_COLORS].get(vInfoVO.vehicleType.classTag)

    @staticmethod
    def py_getIconMultiplier():
        return settings.players_panels[PANELS.ICONS_BLACKOUT]

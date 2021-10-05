# coding=utf-8
from armagomen.battle_observer.core import settings
from armagomen.battle_observer.meta.battle.stats_meta import StatsMeta
from armagomen.battle_observer.statistics.statistic_data_loader import statisticEnabled
from armagomen.battle_observer.statistics.statistic_wtr import getStatisticString
from armagomen.constants import VEHICLE_TYPES, PANELS
from armagomen.utils.common import callback, overrideMethod
from gui.Scaleform.daapi.view.battle.classic import ClassicPage
from gui.Scaleform.daapi.view.battle.classic.stats_exchange import ClassicStatisticsDataController
from gui.Scaleform.daapi.view.battle.ranked.stats_exchange import RankedStatisticsDataController

ALLY_PATTERN = "<font color='%(colorWTR)s'>[%(WTR)d]</font><font color='%(colorWTR)s'>%(nickname)s</font>"
ENEMY_PATTERN = "<font color='%(colorWTR)s'>%(nickname)s</font><font color='%(colorWTR)s'>[%(WTR)d]</font>"


class FullStats(StatsMeta):

    def __init__(self):
        super(FullStats, self).__init__()
        self.isToggled = False
        overrideMethod(ClassicPage, "_toggleFullStats")(self._handleToggleFullStats)
        overrideMethod(ClassicStatisticsDataController, "as_updateVehicleStatusS")(self.updateVInfoVO)
        overrideMethod(RankedStatisticsDataController, "as_updateVehicleStatusS")(self.updateVInfoVO)

    def updateVInfoVO(self, base, stats, data):
        base(stats, data)
        if self.isToggled:
            callback(0.02, lambda: self.as_updateVehicleStatusS(data))

    def _handleToggleFullStats(self, base, page, isShown, permanent=None, tabIndex=None):
        base(page, isShown, permanent=permanent, tabIndex=tabIndex)
        self.isToggled = isShown
        if isShown and tabIndex == 0:
            if statisticEnabled and self.statisticsData:
                callback(0.04, self.afterTabPressed)

    def afterTabPressed(self):
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

    def onNameChanged(self, holder):
        print dir(holder)

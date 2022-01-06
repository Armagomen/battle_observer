from armagomen.battle_observer.meta.battle.stats_meta import StatsMeta
from armagomen.battle_observer.statistics.statistic_wtr import wtr_rating
from armagomen.constants import STATISTICS
from armagomen.utils.events import g_events


class PlayersPanelsStatistic(StatsMeta):
    COLOR_WTR = "colorWTR"

    def __init__(self):
        super(PlayersPanelsStatistic, self).__init__()
        self.cache = {0: ("", None, None, None)}

    def _populate(self):
        super(PlayersPanelsStatistic, self)._populate()
        g_events.updateVehicleData += self.updateVehicleData

    def _dispose(self):
        g_events.updateVehicleData -= self.updateVehicleData
        self.cache.clear()
        super(PlayersPanelsStatistic, self)._dispose()

    def updateVehicleData(self, isEnemy, vehicleID):
        if vehicleID not in self.cache:
            vInfo = self._arenaDP.getVehicleInfo(vehicleID)
            accountDBID = vInfo.player.accountDBID
            iconColor = self.py_getIconColor(vInfo.vehicleType.classTag)
            result = wtr_rating.getStatisticsData(accountDBID, vInfo.player.clanAbbrev) if accountDBID else None
            if result is not None:
                patternFUL = self.settings[STATISTICS.PANELS_RIGHT] if isEnemy else \
                    self.settings[STATISTICS.PANELS_LEFT]
                patternCUT = self.settings[STATISTICS.PANELS_RIGHT_CUT] if isEnemy else \
                    self.settings[STATISTICS.PANELS_LEFT_CUT]
                self.cache[vehicleID] = (iconColor, patternFUL % result, patternCUT % result, result[self.COLOR_WTR])
            else:
                self.cache[vehicleID] = (iconColor, None, None, None)
        self.as_updateVehicleS(isEnemy, vehicleID, *self.cache[vehicleID])

    def py_getCutWidth(self):
        return self.settings[STATISTICS.PANELS_CUT_WIDTH]

    def py_getFullWidth(self):
        return self.settings[STATISTICS.PANELS_FULL_WIDTH]

    def py_vehicleStatisticColorEnabled(self):
        return self.settings[STATISTICS.CHANGE_VEHICLE_COLOR]

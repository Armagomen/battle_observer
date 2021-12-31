from armagomen.battle_observer.meta.battle.stats_meta import StatsMeta
from armagomen.battle_observer.statistics.statistic_wtr import getStatisticString
from armagomen.constants import STATISTICS
from armagomen.utils.common import parseColorToHex
from armagomen.utils.events import g_events


class PlayersPanelsStatistic(StatsMeta):
    COLOR_WTR = "colorWTR"

    def py_getStatisticString(self, accountDBID, isEnemy, clanAbbrev):
        patternCUT = self.settings[STATISTICS.PANELS_RIGHT_CUT] if isEnemy else \
            self.settings[STATISTICS.PANELS_LEFT_CUT]
        patternFUL = self.settings[STATISTICS.PANELS_RIGHT] if isEnemy else \
            self.settings[STATISTICS.PANELS_LEFT]
        result = getStatisticString(accountDBID, clanAbbrev)
        if result is not None:
            return patternFUL % result, patternCUT % result, parseColorToHex(result[self.COLOR_WTR])
        return None, None, None

    def _populate(self):
        super(PlayersPanelsStatistic, self)._populate()
        g_events.updateVehicleStatus += self.updateVehicleStatus

    def _dispose(self):
        g_events.updateVehicleStatus -= self.updateVehicleStatus

    def updateVehicleStatus(self, isEnemy, vehicleID):
        self.as_updateVehicleS(isEnemy, vehicleID)

    def py_getCutWidth(self):
        return self.settings[STATISTICS.PANELS_CUT_WIDTH]

    def py_getFullWidth(self):
        return self.settings[STATISTICS.PANELS_FULL_WIDTH]

    def py_vehicleStatisticColorEnabled(self):
        return self.settings[STATISTICS.CHANGE_VEHICLE_COLOR]

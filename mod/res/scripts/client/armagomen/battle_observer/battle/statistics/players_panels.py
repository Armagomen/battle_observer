from armagomen.battle_observer.meta.battle.stats_meta import StatsMeta
from armagomen.battle_observer.statistics.statistic_wtr import getStatisticString
from armagomen.constants import STATISTICS
from armagomen.utils.common import parseColorToHex


class PlayersPanelsStatistic(StatsMeta):

    def py_getStatisticString(self, accountDBID, isEnemy, clanAbbrev):
        patternCUT = self.settings[STATISTICS.PANELS_RIGHT_CUT] if isEnemy else \
            self.settings[STATISTICS.PANELS_LEFT_CUT]
        patternFUL = self.settings[STATISTICS.PANELS_RIGHT] if isEnemy else \
            self.settings[STATISTICS.PANELS_LEFT]
        result = getStatisticString(accountDBID, clanAbbrev)
        if result is not None:
            return patternFUL % result, patternCUT % result, parseColorToHex(result["colorWTR"])
        return None, None, None

    def py_getCutWidth(self):
        return self.settings[STATISTICS.PANELS_CUT_WIDTH]

    def py_getFullWidth(self):
        return self.settings[STATISTICS.PANELS_FULL_WIDTH]

    def py_vehicleStatisticColorEnabled(self):
        return self.settings[STATISTICS.CHANGE_VEHICLE_COLOR]

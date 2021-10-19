from armagomen.battle_observer.meta.battle.stats_meta import StatsMeta
from armagomen.battle_observer.statistics.statistic_wtr import getStatisticString, getStatisticColor
from armagomen.constants import VEHICLE_TYPES, STATISTICS, GLOBAL


class PlayersPanelsStatistic(StatsMeta):

    def py_getStatisticString(self, accountDBID, isEnemy, clanAbbrev, cut):
        if cut:
            pattern = self.settings[STATISTICS.PANELS_RIGHT_CUT] if isEnemy else \
                self.settings[STATISTICS.PANELS_LEFT_CUT]
        else:
            pattern = self.settings[STATISTICS.PANELS_RIGHT] if isEnemy else \
                self.settings[STATISTICS.PANELS_LEFT]
        if not pattern:
            return GLOBAL.EMPTY_LINE
        result = getStatisticString(accountDBID, self.statisticsData, clanAbbrev)
        if result is not None:
            return pattern % result
        return GLOBAL.EMPTY_LINE

    def py_getIconColor(self, classTag):
        return self.vehicle_types[VEHICLE_TYPES.CLASS_COLORS].get(classTag, GLOBAL.EMPTY_LINE)

    def py_getCutWidth(self):
        return self.settings[STATISTICS.PANELS_CUT_WIDTH]

    def py_getFullWidth(self):
        return self.settings[STATISTICS.PANELS_FULL_WIDTH]

    def py_getStatColor(self, accountDBID):
        if self.settings[STATISTICS.CHANGE_VEHICLE_COLOR]:
            return getStatisticColor(accountDBID)
        return GLOBAL.EMPTY_LINE

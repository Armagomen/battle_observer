from armagomen.battle_observer.meta.battle.stats_meta import StatsMeta
from armagomen.battle_observer.statistics.statistic_wtr import getStatisticString
from armagomen.constants import VEHICLE_TYPES, STATISTICS


class BattleLoading(StatsMeta):

    def py_getStatisticString(self, accountDBID, isEnemy, clanAbbrev):
        pattern = self.settings[STATISTICS.LOADING_RIGHT] if isEnemy else self.settings[STATISTICS.LOADING_LEFT]
        result = getStatisticString(accountDBID, self.statisticsData, clanAbbrev)
        if result is not None:
            return pattern % result
        return None

    def py_getIconColor(self, classTag):
        return self.vehicle_types[VEHICLE_TYPES.CLASS_COLORS].get(classTag)

    def onEnterBattlePage(self):
        super(BattleLoading, self).onEnterBattlePage()
        self.flashObject.as_clear()

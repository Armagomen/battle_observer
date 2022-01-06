from armagomen.battle_observer.meta.battle.stats_meta import StatsMeta
from armagomen.battle_observer.statistics.statistic_wtr import wtr_rating
from armagomen.constants import STATISTICS


class BattleLoading(StatsMeta):

    def py_getStatisticString(self, accountDBID, isEnemy, clanAbbrev):
        pattern = self.settings[STATISTICS.LOADING_RIGHT] if isEnemy else self.settings[STATISTICS.LOADING_LEFT]
        if pattern:
            result = wtr_rating.getStatisticsData(accountDBID, clanAbbrev)
            if result is not None:
                return pattern % result
        return None

    def onEnterBattlePage(self):
        if self._isDAAPIInited():
            self._dispose()

from armagomen.battle_observer.meta.battle.stats_meta import StatsMeta
from armagomen.battle_observer.statistics.statistic_wtr import getStatisticString
from armagomen.constants import STATISTICS, GLOBAL


class BattleLoading(StatsMeta):

    def py_getStatisticString(self, accountDBID, isEnemy, clanAbbrev):
        pattern = self.settings[STATISTICS.LOADING_RIGHT] if isEnemy else self.settings[STATISTICS.LOADING_LEFT]
        if not pattern:
            return GLOBAL.EMPTY_LINE
        result = getStatisticString(accountDBID, clanAbbrev)
        if result is not None:
            return pattern % result
        return GLOBAL.EMPTY_LINE

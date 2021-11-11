from armagomen.battle_observer.meta.battle.stats_meta import StatsMeta
from armagomen.battle_observer.statistics.statistic_wtr import getStatisticString
from armagomen.constants import STATISTICS


class FullStats(StatsMeta):

    def py_getStatisticString(self, accountDBID, isEnemy, clanAbbrev):
        pattern = self.settings[STATISTICS.TAB_RIGHT] if isEnemy else self.settings[STATISTICS.TAB_LEFT]
        if pattern:
            result = getStatisticString(accountDBID, clanAbbrev)
            if result is not None:
                return pattern % result
        return None

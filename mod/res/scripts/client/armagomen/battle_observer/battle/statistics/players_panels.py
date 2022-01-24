from armagomen.battle_observer.meta.battle.stats_meta import StatsMeta, STATISTICS
from gui.Scaleform.genConsts.BATTLE_VIEW_ALIASES import BATTLE_VIEW_ALIASES


class PlayersPanelsStatistic(StatsMeta):

    def getPattern(self, isEnemy):
        return self.settings[STATISTICS.PANELS_RIGHT] if isEnemy else self.settings[STATISTICS.PANELS_LEFT], \
               self.settings[STATISTICS.PANELS_RIGHT_CUT] if isEnemy else self.settings[STATISTICS.PANELS_LEFT_CUT]

    def py_getCutWidth(self):
        return self.settings[STATISTICS.PANELS_CUT_WIDTH]

    def py_getFullWidth(self):
        return self.settings[STATISTICS.PANELS_FULL_WIDTH]

    def _updateVehicleData(self, isEnemy, vehicleID):
        if self.as_isComponentVisibleS(BATTLE_VIEW_ALIASES.PLAYERS_PANEL):
            super(PlayersPanelsStatistic, self)._updateVehicleData(isEnemy, vehicleID)

from armagomen.battle_observer.meta.battle.stats_meta import StatsMeta, STATISTICS
from gui.Scaleform.genConsts.BATTLE_VIEW_ALIASES import BATTLE_VIEW_ALIASES


class BattleLoading(StatsMeta):

    def getPattern(self, isEnemy):
        return self.settings[STATISTICS.LOADING_RIGHT] if isEnemy else self.settings[STATISTICS.LOADING_LEFT], None

    def _updateVehicleData(self, isEnemy, vehicleID):
        if self.as_isComponentVisibleS(BATTLE_VIEW_ALIASES.BATTLE_LOADING):
            super(BattleLoading, self)._updateVehicleData(isEnemy, vehicleID)

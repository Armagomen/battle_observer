from armagomen.battle_observer.meta.battle.stats_meta import StatsMeta
from armagomen.battle_observer.statistics.statistic_wtr import wtr_rating
from armagomen.constants import STATISTICS
from armagomen.utils.events import g_events


class BattleLoading(StatsMeta):

    def __init__(self):
        super(BattleLoading, self).__init__()
        self.cache = {0: ("", None)}

    def _populate(self):
        super(BattleLoading, self)._populate()
        g_events.updateVehicleData += self.updateVehicleData

    def _dispose(self):
        g_events.updateVehicleData -= self.updateVehicleData
        self.cache.clear()
        super(BattleLoading, self)._dispose()

    def updateVehicleData(self, isEnemy, vehicleID):
        if vehicleID not in self.cache:
            vInfo = self._arenaDP.getVehicleInfo(vehicleID)
            accountDBID = vInfo.player.accountDBID
            iconColor = self.py_getIconColor(vInfo.vehicleType.classTag)
            result = wtr_rating.getStatisticsData(accountDBID, vInfo.player.clanAbbrev) if accountDBID else None
            if result is not None:
                pattern = self.settings[STATISTICS.LOADING_RIGHT] if isEnemy else self.settings[STATISTICS.LOADING_LEFT]
                self.cache[vehicleID] = (iconColor, pattern % result)
            else:
                self.cache[vehicleID] = (iconColor, None)
        self.as_updateVehicleS(isEnemy, vehicleID, *self.cache[vehicleID])

    def onEnterBattlePage(self):
        g_events.updateVehicleData -= self.updateVehicleData

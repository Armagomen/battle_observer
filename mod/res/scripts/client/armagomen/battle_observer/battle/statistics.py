from math import floor, log

import BigWorld

from armagomen._constants import STATISTICS
from armagomen.battle_observer.meta.battle.statistics_meta import StatisticsMeta
from armagomen.battle_observer.shared import IBOKeysListener, IStatisticsDataLoader
from armagomen.utils.common import getPercent, hexToInt
from helpers import dependency
from skeletons.gui.app_loader import IAppLoader

WTR_RANGES = ((10000, "unique"), (8000, "very_good"), (5400, "good"), (3200, "normal"), (1400, "bad"), (0, "very_bad"))


class Statistics(StatisticsMeta):
    statisticsLoader = dependency.descriptor(IStatisticsDataLoader)
    keysListener = dependency.descriptor(IBOKeysListener)
    appLoader = dependency.descriptor(IAppLoader)

    DEFAULT_COLOR = "#fafafa"
    DEFAULT_WIN_RATE = 0.0
    K = 1000.0
    UNITS = ['', 'k', 'm', 'g', 't', 'p']

    def __init__(self):
        super(Statistics, self).__init__()
        self.__addedVehicles = set()
        self.__sentVehicles = set()
        self.__callback = None

    def _populate(self):
        super(Statistics, self)._populate()
        self.statisticsLoader.onDataResponse += self.onDataResponse
        self.statisticsLoader.requestStatisticsFromApi(
            {str(vInfo.player.accountDBID) for vInfo in self._arenaDP.getVehiclesInfoIterator()
             if vInfo.player.accountDBID and not vInfo.isObserver()}
        )
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            if arena.isFogOfWarEnabled:
                arena.onVehicleAdded += self.onFogOfWarAddedUpdated
                arena.onVehicleUpdated += self.onFogOfWarAddedUpdated
            arena.onVehicleKilled += self.onVehicleKilled
        self.keysListener.registerComponent(self.on_altModeS)

    def _dispose(self):
        self.statisticsLoader.onDataResponse -= self.onDataResponse
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            if arena.isFogOfWarEnabled:
                arena.onVehicleAdded -= self.onFogOfWarAddedUpdated
                arena.onVehicleUpdated -= self.onFogOfWarAddedUpdated
            arena.onVehicleKilled -= self.onVehicleKilled
        super(Statistics, self)._dispose()

    def onVehicleKilled(self, vehicleID, *args):
        self.as_updateDeadS(vehicleID)

    def onAddedUpdatedDelay(self):
        self.__callback = None
        to_request = self.__addedVehicles - self.__sentVehicles
        self.statisticsLoader.requestStatisticsFromApi({str(k) for k in to_request})
        self.__sentVehicles.update(to_request)

    def onFogOfWarAddedUpdated(self, vehicleID):
        vInfo = self.getVehicleInfo(vehicleID)
        if vInfo.isObserver():
            return
        accountDBID = vInfo.player.accountDBID
        if accountDBID and accountDBID not in self.__addedVehicles:
            if self.__callback is not None:
                BigWorld.cancelCallback(self.__callback)
            self.__addedVehicles.add(accountDBID)
            self.__callback = BigWorld.callback(2.0, self.onAddedUpdatedDelay)

    def onDataResponse(self, loadedData):
        for vehicle_id, value in loadedData.iteritems():
            vInfo = self.getVehicleInfo(vehicle_id)
            self.logger.logDebug("Statistics: player={}, value={}", vInfo.player.name, value)
            if len(value) < 3:
                continue
            item_data = self.buildItemData(value)
            self.as_createItem(vehicle_id, vInfo.isEnemy(), item_data)

    def __battlesFormat(self, battles):
        magnitude = int(floor(log(battles, self.K)))
        decimals = 1 if magnitude >= 1 else 0
        value = battles / (self.K ** magnitude)
        return "{0:.{decimals}f}{1}".format(value, self.UNITS[magnitude], decimals=decimals)

    def __getColor(self, rating):
        for value, colorName in WTR_RANGES:
            if rating >= value:
                return hexToInt(self.settings[STATISTICS.COLORS].get(colorName, self.DEFAULT_COLOR))
        return hexToInt(self.DEFAULT_COLOR)

    def buildItemData(self, data):
        return {
            "color": self.__getColor(data["rating"]),
            "winRate": "{:.1%}".format(getPercent(data["wins"], data["battles"])),
            "battles": self.__battlesFormat(data["battles"])
        }

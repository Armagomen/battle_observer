from math import floor, log

import BigWorld
from armagomen._constants import STATISTICS
from armagomen.battle_observer.meta.battle.statistics_and_icons_meta import StatisticsAndIconsMeta
from armagomen.battle_observer.shared import IBOKeysListener, IStatisticsDataLoader
from armagomen.utils.common import getGreatPercent, hexToInt
from gui.shared import EVENT_BUS_SCOPE, events
from helpers import dependency

WGR_RANGES = ((0, "very_bad"), (3500, "bad"), (5300, "normal"), (7400, "good"), (9700, "very_good"), (11000, "unique"))
WTR_RANGES = ((0, "very_bad"), (3100, "bad"), (4700, "normal"), (6700, "good"), (9200, "very_good"), (10900, "unique"))


class StatisticsAndIcons(StatisticsAndIconsMeta):
    statisticsLoader = dependency.descriptor(IStatisticsDataLoader)
    keysListener = dependency.descriptor(IBOKeysListener)

    DEFAULT_COLOR = "#fafafa"
    DEFAULT_WIN_RATE = 0.0
    K = 1000.0
    UNITS = ['', 'k', 'm', 'g', 't', 'p']

    def __init__(self):
        super(StatisticsAndIcons, self).__init__()
        self.useWTR = self.settingsLoader.getSetting(STATISTICS.NAME, STATISTICS.USE_WTR)
        self._format = {True: "{:.1f}{}", False: "{:.0f}{}"}
        self.__addedVehicles = set()
        self.__sentVehicles = set()
        self.__callback = None

    @property
    def statisticsEnabled(self):
        return self.statisticsLoader.enabled and self.settings[STATISTICS.STATISTIC_ENABLED]

    def _populate(self):
        super(StatisticsAndIcons, self)._populate()
        self.keysListener.registerComponent(self.updateAll)
        if self.statisticsEnabled:
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
            arena.onVehicleStatisticsUpdate += self.onVehicleUpdate
            arena.onVehicleKilled += self.onVehicleUpdate
            arena.onAvatarReady += self.onVehicleUpdate
            arena.onPeriodChange += self.updateAll
            arena.onNewVehicleListReceived += self.updateAll
        self.addListener(events.GameEvent.NEXT_PLAYERS_PANEL_MODE, self.updateAll, scope=EVENT_BUS_SCOPE.BATTLE)
        self.addListener(events.GameEvent.SHOW_EXTENDED_INFO, self.updateAll, scope=EVENT_BUS_SCOPE.BATTLE)
        self.updateAll()

    def updateAll(self, *args):
        for vInfo in self._arenaDP.getVehiclesInfoIterator():
            if not vInfo.isObserver():
                self.onVehicleUpdate(vInfo.vehicleID)

    def _dispose(self):
        if self.statisticsEnabled:
            self.statisticsLoader.onDataResponse -= self.onDataResponse
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            if arena.isFogOfWarEnabled:
                arena.onVehicleAdded -= self.onFogOfWarAddedUpdated
                arena.onVehicleUpdated -= self.onFogOfWarAddedUpdated
            arena.onVehicleStatisticsUpdate -= self.onVehicleUpdate
            arena.onVehicleKilled -= self.onVehicleUpdate
            arena.onAvatarReady -= self.onVehicleUpdate
            arena.onPeriodChange -= self.updateAll
            arena.onNewVehicleListReceived -= self.updateAll
        self.removeListener(events.GameEvent.NEXT_PLAYERS_PANEL_MODE, self.updateAll, scope=EVENT_BUS_SCOPE.BATTLE)
        self.removeListener(events.GameEvent.SHOW_EXTENDED_INFO, self.updateAll, scope=EVENT_BUS_SCOPE.BATTLE)
        super(StatisticsAndIcons, self)._dispose()

    def onVehicleUpdate(self, vehicleID, *args):
        isEnemy = self.getVehicleInfo(vehicleID).team != BigWorld.player().team
        BigWorld.callback(0.1, lambda: self.as_updateByVehicleID(vehicleID, isEnemy))

    def onAddedUpdatedDelay(self):
        self.__callback = None
        to_request = self.__addedVehicles - self.__sentVehicles
        self.statisticsLoader.requestStatisticsFromApi({str(k) for k in to_request})
        self.__sentVehicles.update(to_request)

    def onFogOfWarAddedUpdated(self, vehicleID):
        vInfo = self.getVehicleInfo(vehicleID)
        if self.statisticsEnabled:
            accountDBID = vInfo.player.accountDBID
            if accountDBID and accountDBID not in self.__addedVehicles and not vInfo.isObserver():
                if self.__callback is not None:
                    BigWorld.cancelCallback(self.__callback)
                self.__addedVehicles.add(accountDBID)
                self.__callback = BigWorld.callback(2.0, self.onAddedUpdatedDelay)
        if vInfo.vehicleType:
            self.onVehicleUpdate(vehicleID)

    def getPattern(self, isEnemy, itemData):
        if isEnemy:
            return self.settings[STATISTICS.FULL_RIGHT] % itemData, self.settings[STATISTICS.CUT_RIGHT] % itemData
        else:
            return self.settings[STATISTICS.FULL_LEFT] % itemData, self.settings[STATISTICS.CUT_LEFT] % itemData

    def onDataResponse(self, loadedData):
        itemsData = dict()
        for vehicle_id, value in loadedData.iteritems():
            vInfo = self.getVehicleInfo(vehicle_id)
            self.logger.logDebug("Statistics: player={}, value={}", vInfo.player.name, value)
            if len(value) < 4:
                continue
            item_data = self.buildItemData(vInfo.player, value)
            full, cut = self.getPattern(vInfo.isEnemy(), item_data)
            text_color = hexToInt(item_data["color"]) if self.settings[STATISTICS.CHANGE_VEHICLE_COLOR] else 0
            itemsData[vehicle_id] = {"fullName": full, "cutName": cut, "vehicleTextColor": text_color}
        if itemsData:
            self.as_update_wgr_dataS(itemsData)
            self.updateAll()

    def __battlesFormat(self, battles):
        magnitude = int(floor(log(battles, self.K)))
        return self._format[magnitude >= 1].format(battles / self.K ** magnitude, self.UNITS[magnitude])

    def __getColor(self, rating):
        for value, colorName in reversed(WTR_RANGES if self.useWTR else WGR_RANGES):
            if rating >= value:
                return self.settings[STATISTICS.COLORS].get(colorName, self.DEFAULT_COLOR)
        return self.DEFAULT_COLOR

    def buildItemData(self, player, data):
        rating = data["rating" if self.useWTR else "global_rating"]
        return {
            "rating": rating,
            "color": self.__getColor(rating),
            "winRate": getGreatPercent(data["wins"], data["battles"]),
            "battles": self.__battlesFormat(data["battles"]),
            "nickname": player.name,
            "clanTag": "[{}]".format(player.clanAbbrev) if player.clanAbbrev else ""
        }

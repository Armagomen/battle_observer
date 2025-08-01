import json
from httplib import responses
from math import floor, log

from armagomen._constants import STATISTICS, STATISTICS_REGION
from armagomen.battle_observer.meta.battle.wgr_and_icons_meta import WGRAndIconsMeta
from armagomen.utils.async_request import async_url_request
from armagomen.utils.common import addCallback, cancelCallback
from armagomen.utils.logging import logDebug, logError
from uilogging.core.core_constants import HTTP_OK_STATUS
from wg_async import wg_async


class WGRAndIcons(WGRAndIconsMeta):
    COLOR_WGR = 'colorWGR'
    DEFAULT_COLOR = "#fafafa"
    DEFAULT_WIN_RATE = 0.0
    K = 1000.0
    UNITS = ['', 'k', 'm', 'g', 't', 'p']

    def __init__(self):
        super(WGRAndIcons, self).__init__()
        self.ranges = ((3287, "bad"), (5150, "normal"), (7258, "good"), (9586, "very_good"), (11025, "unique"))
        self.itemsData = {}
        self.data_loader = None

    def statisticsEnabled(self):
        return STATISTICS_REGION is not None and self.settings[STATISTICS.STATISTIC_ENABLED]

    def _populate(self):
        super(WGRAndIcons, self)._populate()
        if self.statisticsEnabled():
            self.data_loader = StatisticsDataLoader(self._arenaDP, self.updateAllItems)
            self.data_loader.getStatisticsDataFromServer()
            arena = self._arenaVisitor.getArenaSubscription()
            if arena is not None and not self.isComp7Battle():
                if arena.isFogOfWarEnabled:
                    arena.onVehicleAdded += self.data_loader.updateList
                    arena.onVehicleUpdated += self.data_loader.updateList

    def _dispose(self):
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None and not self.isComp7Battle():
            if arena.isFogOfWarEnabled and self.data_loader is not None:
                arena.onVehicleAdded -= self.data_loader.updateList
                arena.onVehicleUpdated -= self.data_loader.updateList
        self.data_loader = None
        super(WGRAndIcons, self)._dispose()

    def getPattern(self, isEnemy, itemData):
        logDebug("WGRStatistics: isEnemy={}, data={}", isEnemy, itemData)
        if isEnemy:
            return self.settings[STATISTICS.FULL_RIGHT] % itemData, self.settings[STATISTICS.CUT_RIGHT] % itemData
        else:
            return self.settings[STATISTICS.FULL_LEFT] % itemData, self.settings[STATISTICS.CUT_LEFT] % itemData

    def updateAllItems(self, loadedData):
        player_team = self._arenaDP.getNumberOfTeam()
        for accountDBID, value in loadedData.iteritems():
            if not value:
                continue
            vehicle_id = self._arenaDP.getVehIDByAccDBID(accountDBID)
            if vehicle_id in self.itemsData:
                continue
            veh_info = self.getVehicleInfo(vehicle_id)
            item_data = self.buildItemData(veh_info.player.clanAbbrev, value)
            full, cut = self.getPattern(veh_info.team != player_team, item_data)
            text_color = int(item_data[self.COLOR_WGR][1:], 16) if self.settings[STATISTICS.CHANGE_VEHICLE_COLOR] else 0
            self.itemsData[vehicle_id] = {"fullName": full, "cutName": cut, "vehicleTextColor": text_color}
        if self.itemsData:
            self.as_update_wgr_dataS(self.itemsData)

    def __getWinRateAndBattlesCount(self, data):
        random = data["statistics"]["random"]
        battles = int(random["battles"])
        if battles:
            return round(float(random["wins"]) / battles * 100, 2), self.__battlesFormat(battles)
        return self.DEFAULT_WIN_RATE, str(battles)

    def __battlesFormat(self, battles):
        if battles >= self.K:
            magnitude = int(floor(log(battles, self.K)))
            return '%.1f%s' % (battles / self.K ** magnitude, self.UNITS[magnitude])
        return str(battles)

    def __getColor(self, wgr):
        result = "very_bad"
        for value, colorName in self.ranges:
            if wgr >= value:
                result = colorName
            else:
                break
        return self.settings[STATISTICS.COLORS].get(result, self.DEFAULT_COLOR)

    def buildItemData(self, clanTag, data):
        wgr = int(data.get("global_rating", 0))
        win_rate, battles = self.__getWinRateAndBattlesCount(data)
        return {"WGR": wgr, self.COLOR_WGR: self.__getColor(wgr), "winRate": win_rate, "battles": battles,
                "nickname": data.get("nickname"), "clanTag": "[{}]".format(clanTag) if clanTag else ""}


class StatisticsDataLoader(object):
    SEPARATOR = "%2C"
    FIELDS = SEPARATOR.join(("statistics.random.wins", "statistics.random.battles", "global_rating", "nickname"))
    STAT_URL = STATISTICS_REGION + "&account_id={}&extra=statistics.random&language=en&fields=" + FIELDS

    def __init__(self, arenaDP, callback):
        self.arenaDP = arenaDP
        self.__callback = callback
        self._load_try = 0
        self.__getDataCallback = None
        self.__vehicles = set()
        self.__loaded = set()

    def onDataResponse(self, response):
        if response.responseCode == 304:
            return
        if response.responseCode == HTTP_OK_STATUS:
            response_data = json.loads(response.body)
            data = {int(k): v for k, v in response_data.get("data", {}).iteritems()}
            logDebug("StatisticsDataLoader/onDataResponse: FINISH request users data={}", data)
            self.__callback(data)
            self.__loaded.update(data.iterkeys())
        else:
            self.delayedLoad(response.responseCode)

    def delayedLoad(self, code):
        if self._load_try < 5:
            self._load_try += 1
            code = responses.get(code) if isinstance(code, int) else code
            logError("StatisticsDataLoader: error loading statistic data - {}/{}", self._load_try, code)
            addCallback(10.0, self.getStatisticsDataFromServer)

    def updateList(self, vehicleID):
        vInfo = self.arenaDP.getVehicleInfo(vehicleID)
        accountDBID = vInfo.player.accountDBID
        if not accountDBID or accountDBID in self.__loaded or vInfo.isObserver():
            return
        self.__vehicles.add(accountDBID)
        logDebug(self.__vehicles)
        if self.__getDataCallback is None:
            self.__getDataCallback = addCallback(5.0, self.requestData)

    @property
    def vehicles(self):
        while self.__vehicles:
            yield str(self.__vehicles.pop())

    @wg_async
    def requestData(self):
        if self.__getDataCallback is not None:
            cancelCallback(self.__getDataCallback)
            self.__getDataCallback = None
        url = self.STAT_URL.format(self.SEPARATOR.join(self.vehicles))
        response = yield async_url_request(url)
        self.onDataResponse(response)

    def getStatisticsDataFromServer(self):
        for vInfo in self.arenaDP.getVehiclesInfoIterator():
            accountDBID = vInfo.player.accountDBID
            if not accountDBID or accountDBID in self.__loaded or vInfo.isObserver():
                continue
            self.__vehicles.add(accountDBID)
        if self.__vehicles:
            logDebug("getStatisticsDataFromServer: START request data: ids={}", self.__vehicles)
            self.requestData()

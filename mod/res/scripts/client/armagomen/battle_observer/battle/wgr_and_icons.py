import json
from httplib import responses
from math import floor, log

from armagomen._constants import API_KEY, REGIONS, STATISTICS
from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta
from armagomen.utils.common import addCallback, fetchURL
from armagomen.utils.logging import logDebug, logError
from constants import AUTH_REALM
from Event import SafeEvent
from PlayerEvents import g_playerEvents
from uilogging.core.core_constants import HTTP_OK_STATUS

region = REGIONS.get(AUTH_REALM)


class WGRAndIcons(BaseModMeta):
    COLOR_WGR = 'colorWGR'
    DEFAULT_COLOR = "#fafafa"
    DEFAULT_WIN_RATE = 0.0
    K = 1000.0
    UNITS = ['', 'k', 'm', 'g', 't', 'p']

    def __init__(self):
        super(WGRAndIcons, self).__init__()
        self.ranges = ((3280, "bad"), (5165, "normal"), (7274, "good"), (9589, "very_good"), (11015, "unique"))
        self.itemsData = {}
        self.data_loader = None

    def _populate(self):
        super(WGRAndIcons, self)._populate()
        if region is not None and self.settings[STATISTICS.STATISTIC_ENABLED]:
            self.data_loader = StatisticsDataLoader(self._arenaVisitor, self._arenaDP)
            self.data_loader.onDataReceived += self.updateAllItems
            self.data_loader.getStatisticsDataFromServer()
            g_playerEvents.onAvatarReady += self.updateFlash

    def updateFlash(self):
        return self.flashObject.update_wgr_data(self.itemsData) if self._isDAAPIInited() and self.itemsData else None

    def _dispose(self):
        if self.data_loader is not None:
            self.data_loader.onDataReceived -= self.updateAllItems
            self.data_loader = None
            g_playerEvents.onAvatarReady -= self.updateFlash
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
            vehicle_id = self._arenaDP.getVehIDByAccDBID(int(accountDBID))
            if vehicle_id in self.itemsData:
                continue
            veh_info = self._arenaDP.getVehicleInfo(vehicle_id)
            item_data = self.buildItemData(veh_info.player.clanAbbrev, value)
            full, cut = self.getPattern(veh_info.team != player_team, item_data)
            text_color = item_data[self.COLOR_WGR] if self.settings[STATISTICS.CHANGE_VEHICLE_COLOR] else None
            self.itemsData[vehicle_id] = {"fullName": full, "cutName": cut, "vehicleTextColor": text_color}
        self.updateFlash()

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
        return {"WGR": wgr, self.COLOR_WGR: self.__getColor(wgr), "winRate": win_rate,
                "battles": battles, "nickname": data.get("nickname"),
                "clanTag": "[{}]".format(clanTag) if clanTag else ""}


class StatisticsDataLoader(object):
    URL = "https://api.worldoftanks.{}/wot/account/info/?".format(region)
    SEPARATOR = "%2C"
    FIELDS = SEPARATOR.join(("statistics.random.wins", "statistics.random.battles", "global_rating", "nickname"))
    STAT_URL = "{url}application_id={key}&account_id={ids}&extra=statistics.random&fields={fields}&language=en"

    def __init__(self, arenaVisitor, arenaDP):
        self.arena = arenaVisitor.getArenaSubscription()
        self.arenaDP = arenaDP
        self._load_try = 0
        self.__getDataCallback = None
        self.__vehicles = set()
        self.onDataReceived = SafeEvent()
        self.__loaded = set()

    def onDataResponse(self, response):
        if response.responseCode == 304:
            return
        if response.responseCode == HTTP_OK_STATUS:
            response_data = json.loads(response.body)
            data = response_data.get("data", {})
            logDebug("StatisticsDataLoader/onDataResponse: FINISH request users data={}", data)
            self.onDataReceived(data)
            self.__loaded.update(int(k) for k in data.keys())
        else:
            self.delayedLoad(response.responseCode)

    def delayedLoad(self, code):
        if self._load_try < 5:
            self._load_try += 1
            code = responses.get(code) if isinstance(code, int) else code
            logError("StatisticsDataLoader: error loading statistic data - {}/{}", self._load_try, code)
            addCallback(2.0, self.getStatisticsDataFromServer)

    def updateList(self, vehicleID):
        vInfo = self.arenaDP.getVehicleInfo(vehicleID)
        accountDBID = vInfo.player.accountDBID
        if not accountDBID or accountDBID in self.__loaded:
            return
        self.__vehicles.add(accountDBID)
        logDebug(self.__vehicles)
        if self.__getDataCallback is None:
            self.__getDataCallback = addCallback(5.0, self.requestData)

    @property
    def vehicles(self):
        while self.__vehicles:
            yield str(self.__vehicles.pop())

    def requestData(self):
        self.__getDataCallback = None
        url = self.STAT_URL.format(ids=self.SEPARATOR.join(self.vehicles), key=API_KEY, url=self.URL,
                                   fields=self.FIELDS)
        fetchURL(url, self.onDataResponse)

    def getStatisticsDataFromServer(self):
        self.__vehicles.update(vInfo.player.accountDBID for vInfo in self.arenaDP.getVehiclesInfoIterator() if
                               vInfo.player.accountDBID and vInfo.player.accountDBID not in self.__loaded)
        if self.arena is not None and self.arena.isFogOfWarEnabled:
            self.arena.onVehicleAdded += self.updateList
            self.arena.onVehicleUpdated += self.updateList
        logDebug("getStatisticsDataFromServer: START request data: ids={}", self.__vehicles)
        if self.__vehicles:
            self.requestData()

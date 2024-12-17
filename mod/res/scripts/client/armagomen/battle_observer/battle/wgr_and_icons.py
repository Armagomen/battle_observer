import json
from httplib import responses
from math import floor, log

from armagomen._constants import API_KEY, REGIONS, STATISTICS
from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta
from armagomen.utils.common import addCallback, fetchURL
from armagomen.utils.logging import logDebug, logError
from constants import AUTH_REALM
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider
from uilogging.core.core_constants import HTTP_OK_STATUS


class WGRAndIcons(BaseModMeta):
    COLOR_WGR = 'colorWGR'
    DEFAULT_COLOR = "#fafafa"
    DEFAULT_WIN_RATE = 0.0
    K = 1000.0
    UNITS = ['', 'k', 'm', 'g', 't', 'p']

    def __init__(self):
        self.data_loader = None
        super(WGRAndIcons, self).__init__()
        self.ranges = ((3280, "bad"), (5165, "normal"), (7274, "good"), (9589, "very_good"), (11015, "unique"))
        self.itemsData = {}

    def _populate(self):
        super(WGRAndIcons, self)._populate()
        if self.settings[STATISTICS.STATISTIC_ENABLED]:
            self.data_loader = StatisticsDataLoader()
            if not self.data_loader.enabled:
                self.data_loader.regionError()
            else:
                self.data_loader.setFeedback(self.update_wgr_data)
                self.data_loader.getStatisticsDataFromServer()

    def update_wgr_data(self, data):
        self.updateAllItems(self._arenaDP, data)
        if self._isDAAPIInited():
            self.flashObject.update_wgr_data(self.itemsData)
        else:
            logError("WGRAndIcons - DAAPI ERROR")

    def getPattern(self, isEnemy, itemData):
        logDebug("WGRStatistics: isEnemy={}, data={}", isEnemy, itemData)
        if isEnemy:
            return self.settings[STATISTICS.FULL_RIGHT] % itemData, self.settings[STATISTICS.CUT_RIGHT] % itemData
        else:
            return self.settings[STATISTICS.FULL_LEFT] % itemData, self.settings[STATISTICS.CUT_LEFT] % itemData

    def updateAllItems(self, arenaDP, loadedData):
        player_team = arenaDP.getNumberOfTeam()
        for accountDBID, value in loadedData.iteritems():
            if not value:
                continue
            vehicle_id = arenaDP.getVehIDByAccDBID(int(accountDBID))
            if vehicle_id in self.itemsData:
                continue
            veh_info = arenaDP.getVehicleInfo(vehicle_id)
            item_data = self.buildItemData(veh_info.player.clanAbbrev, value)
            full, cut = self.getPattern(veh_info.team != player_team, item_data)
            text_color = item_data[self.COLOR_WGR] if self.settings[STATISTICS.CHANGE_VEHICLE_COLOR] else None
            self.itemsData[vehicle_id] = {"fullName": full, "cutName": cut, "vehicleTextColor": text_color}
        return self.itemsData

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

    def _dispose(self):
        self.data_loader = None
        super(WGRAndIcons, self)._dispose()


region = REGIONS.get(AUTH_REALM)


class StatisticsDataLoader(object):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)
    URL = "https://api.worldoftanks.{}/wot/account/info/?".format(region)
    SEPARATOR = "%2C"
    FIELDS = SEPARATOR.join(("statistics.random.wins", "statistics.random.battles", "global_rating", "nickname"))
    STAT_URL = "{url}application_id={key}&account_id={ids}&extra=statistics.random&fields={fields}&language=en"

    def __init__(self):
        self.enabled = region is not None
        self._load_try = 0
        self.__feedback = None
        self.__getDataCallback = None
        self.__vehicles = set()

    def onDataResponse(self, response):
        if response.responseCode == 304:
            return
        if response.responseCode == HTTP_OK_STATUS:
            response_data = json.loads(response.body)
            data = response_data.get("data", {})
            logDebug("StatisticsDataLoader/onDataResponse: FINISH request users data={}", data)
            if self.__feedback is not None:
                self.__feedback(data)
        else:
            self.delayedLoad(response.responseCode)

    def setFeedback(self, callback_method):
        self.__feedback = callback_method

    def delayedLoad(self, code):
        if self._load_try < 5:
            self._load_try += 1
            code = responses.get(code) if isinstance(code, int) else code
            logError("StatisticsDataLoader: error loading statistic data - {}/{}", self._load_try, code)
            addCallback(2.0, self.getStatisticsDataFromServer)

    @staticmethod
    def regionError():
        logError("Statistics are not available in your region={}. Only in {}", AUTH_REALM, REGIONS.keys())

    def updateList(self, vehicleID):
        vInfo = self.sessionProvider.getArenaDP().getVehicleInfo(vehicleID)
        accountDBID = vInfo.player.accountDBID
        if not accountDBID:
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
        if self.__feedback is None:
            raise ReferenceError("feedback method is not set")
        arenaDP = self.sessionProvider.getArenaDP()
        if arenaDP is None:
            return self.delayedLoad("arenaDP is None")
        self.__vehicles = set(vInfo.player.accountDBID for vInfo in arenaDP.getVehiclesInfoIterator() if
                              vInfo.player.accountDBID)
        if not self.__vehicles:
            return self.delayedLoad("users list is empty")
        arena = self.sessionProvider.arenaVisitor.getArenaSubscription()
        if arena is not None and arena.isFogOfWarEnabled:
            arena.onVehicleAdded += self.updateList
            arena.onVehicleUpdated += self.updateList
        logDebug("StatisticsDataLoader/getStatisticsDataFromServer: START request data: ids={}, len={} ",
                 self.__vehicles, len(self.__vehicles))
        self.requestData()

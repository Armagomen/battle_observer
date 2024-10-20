import json
from httplib import responses

from armagomen._constants import REGIONS
from armagomen.battle_observer.components.statistics.wtr_data import WTRStatistics
from armagomen.utils.common import callback, fetchURL
from armagomen.utils.logging import logDebug, logError
from constants import AUTH_REALM
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider
from uilogging.core.core_constants import HTTP_OK_STATUS

region = REGIONS.get(AUTH_REALM)


class StatisticsDataLoader(object):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)
    URL = "https://api.worldoftanks.{}/wot/account/info/?".format(region)
    SEPARATOR = "%2C"
    FIELDS = SEPARATOR.join(("statistics.random.wins", "statistics.random.battles", "global_rating", "nickname"))
    API_KEY = "5500d1b937426e47e2b039e4a11990be"
    STAT_URL = "{url}application_id={key}&account_id={ids}&extra=statistics.random&fields={fields}&language=en"

    def __init__(self):
        self.enabled = region is not None
        self._load_try = 0
        self.__wtrData = WTRStatistics()
        self.__feedback = None
        self.__isComp7 = False
        self.__getDataCallback = None
        self.__vehicles = set()
        self.__vehicles_to_update = set()

    def onDataResponse(self, response):
        if response.responseCode == HTTP_OK_STATUS:
            response_data = json.loads(response.body)
            data = response_data.get("data", {})
            logDebug("StatisticsDataLoader/onDataResponse: FINISH request users data={}", data)
            items_data = self.__wtrData.updateAllItems(self.sessionProvider.getArenaDP(), data)
            if self.__feedback is not None:
                self.__feedback(items_data)
        else:
            self.delayedLoad(response.responseCode)

    def setFeedback(self, callback_method):
        self.__feedback = callback_method

    def delayedLoad(self, code):
        if self._load_try < 10:
            self._load_try += 1
            code = responses.get(code) if isinstance(code, int) else code
            logError("StatisticsDataLoader: error loading statistic data - {}/{}", self._load_try, code)
            callback(2.0, self.getStatisticsDataFromServer, self.__isComp7)

    @staticmethod
    def regionError():
        logError("Statistics are not available in your region={}. Only in {}", AUTH_REALM, REGIONS.keys())

    def updateList(self, vehicleID):
        vInfo = self.sessionProvider.getArenaDP().getVehicleInfo(vehicleID)
        accountDBID = vInfo.player.accountDBID
        if not accountDBID or accountDBID in self.__vehicles:
            return
        self.__vehicles.add(accountDBID)
        self.__vehicles_to_update.add(accountDBID)
        logDebug(self.__vehicles_to_update)
        if self.__getDataCallback is None:
            self.__getDataCallback = callback(4.0, self.requestData, self.__vehicles_to_update)

    def requestData(self, data):
        self.__getDataCallback = None
        url = self.STAT_URL.format(ids=self.SEPARATOR.join(str(x) for x in data), key=self.API_KEY, url=self.URL,
                                   fields=self.FIELDS)
        fetchURL(url, self.onDataResponse)
        self.__vehicles_to_update.clear()

    def getStatisticsDataFromServer(self, isComp7):
        if not self.enabled:
            return
        if self.__feedback is None:
            raise ReferenceError("feedback method is not set")
        arenaDP = self.sessionProvider.getArenaDP()
        if arenaDP is None:
            return self.delayedLoad("arenaDP is None")
        self.__vehicles = set(vInfo.player.accountDBID for vInfo in arenaDP.getVehiclesInfoIterator() if
                              vInfo.player.accountDBID)
        if not self.__vehicles:
            return self.delayedLoad("users list is empty")
        if self.__isComp7 != isComp7:
            self.__isComp7 = isComp7
            arena = self.sessionProvider.arenaVisitor.getArenaSubscription()
            if arena is not None:
                arena.onVehicleAdded += self.updateList
                arena.onVehicleUpdated += self.updateList
        logDebug("StatisticsDataLoader/getStatisticsDataFromServer: START request data: ids={}, len={} ",
                 self.__vehicles, len(self.__vehicles))
        self.requestData(self.__vehicles)

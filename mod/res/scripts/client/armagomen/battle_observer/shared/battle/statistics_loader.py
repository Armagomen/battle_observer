import json
from collections import defaultdict

from armagomen import IALogger
from armagomen._constants import API_KEY
from armagomen.utils.async_request import async_url_request
from armagomen.utils.common import addCallback
from Event import SafeEvent
from helpers import dependency
from realm import CURRENT_REALM
from skeletons.gui.battle_session import IBattleSessionProvider
from uilogging.core.core_constants import HTTP_OK_STATUS
from wg_async import wg_async

INFO_REGIONS = {"EU": "https://api.worldoftanks.eu/wot/account/info/?application_id={}".format(API_KEY),
                "ASIA": "https://api.worldoftanks.asia/wot/account/info/?application_id={}".format(API_KEY),
                "NA": "https://api.worldoftanks.com/wot/account/info/?application_id={}".format(API_KEY)}

WTR_REGIONS = {"EU": "https://api.worldoftanks.eu/wot/account/wtr/?application_id={}".format(API_KEY),
               "ASIA": "https://api.worldoftanks.asia/wot/account/wtr/?application_id={}".format(API_KEY),
               "NA": "https://api.worldoftanks.com/wot/account/wtr/?application_id={}".format(API_KEY)}

INFO_REGION = INFO_REGIONS.get(CURRENT_REALM)
WTR_REGION = WTR_REGIONS.get(CURRENT_REALM)


class IStatisticsDataLoader(object):

    def requestStatisticsFromApi(self, DBIDs):
        raise NotImplementedError

    def init(self):
        pass

    def fini(self):
        pass

    def updateList(self, vehicleID):
        raise NotImplementedError


class StatisticsDataLoader(IStatisticsDataLoader):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)
    logger = dependency.descriptor(IALogger)

    SEPARATOR = ","

    INFO_URL = str(INFO_REGION) + "&account_id={}&extra=statistics.random&fields=statistics.random.wins,statistics.random.battles,global_rating"
    WTR_URL = str(WTR_REGION) + "&account_id={}&fields=rating"

    def __init__(self):
        super(StatisticsDataLoader, self).__init__()
        self.logger.logInfo("Initializing StatisticsDataLoader")
        self.onDataResponse = SafeEvent()
        self._load_try = 0
        self.enabled = WTR_REGION is not None
        self.__cached_vehicles = defaultdict(dict)

    def fini(self):
        self.__cached_vehicles.clear()
        self.onDataResponse.clear()
        self.logger.logInfo("Finished StatisticsDataLoader")

    def __onInfoResponse(self, response, DBIDs):
        if response.responseCode == 304:
            return
        if response.responseCode == HTTP_OK_STATUS:
            response_data = json.loads(response.body).get("data", {})
            if not response_data:
                return
            for k, v in response_data.iteritems():
                self.__cached_vehicles[k].update(v["statistics"]["random"])
                self.__cached_vehicles[k]["global_rating"] = v["global_rating"]
            self.logger.logDebug("StatisticsDataLoader/__onInfoResponse: FINISH request INFO data={}", response_data)
            self.requestWTR(DBIDs)
        else:
            self.delayedLoad(response.responseCode, DBIDs, self.requestInfo)

    def __onWTRResponse(self, response, DBIDs):
        if response.responseCode == 304:
            return
        if response.responseCode == HTTP_OK_STATUS:
            response_data = json.loads(response.body).get("data", {})
            if not response_data:
                return
            for k, v in response_data.iteritems():
                self.__cached_vehicles[k].update(v)
            self.logger.logDebug("StatisticsDataLoader/__onWTRResponse: FINISH request WTR data={}", response_data)
            self.onResponse(DBIDs)
        else:
            self.delayedLoad(response.responseCode, DBIDs, self.requestWTR)

    def onResponse(self, DBIDs):
        arenaDP = self.sessionProvider.getArenaDP()
        self.onDataResponse({arenaDP.getVehIDByAccDBID(int(accountDBID)): self.__cached_vehicles[accountDBID] for accountDBID in DBIDs})
        self._load_try = 0

    def delayedLoad(self, code, DBIDs, method):
        if self._load_try < 6:
            self._load_try += 1
            self.logger.logError("StatisticsDataLoader: error loading statistic data - {}/{}", self._load_try, code)
            addCallback(5.0, lambda: method(DBIDs))

    def requestStatisticsFromApi(self, DBIDs):
        loaded = set()
        to_request = set()
        for accountDBID in DBIDs:
            if len(self.__cached_vehicles[accountDBID]) != 4:
                to_request.add(accountDBID)
            else:
                loaded.add(accountDBID)
        if loaded:
            self.onResponse(loaded)
        if to_request:
            self.logger.logDebug("requestStatisticsFromApi: START request data: ids={}", to_request)
            self.requestInfo(to_request)

    @wg_async
    def requestWTR(self, DBIDs):
        response = yield async_url_request(self.WTR_URL.format(self.SEPARATOR.join(DBIDs)))
        self.__onWTRResponse(response, DBIDs)

    @wg_async
    def requestInfo(self, DBIDs):
        response = yield async_url_request(self.INFO_URL.format(self.SEPARATOR.join(DBIDs)))
        self.__onInfoResponse(response, DBIDs)

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

    def onDataResponse(self, response):
        if response.responseCode == HTTP_OK_STATUS:
            response_data = json.loads(response.body)
            data = response_data.get("data", {})
            self.__wtrData.updateAllItems(self.sessionProvider.getArenaDP(), data)
            logDebug("StatisticsDataLoader/onDataResponse: FINISH request users data={}", data)
            if self.__feedback is not None:
                self.__feedback(self.__wtrData.itemsData)
        else:
            self.delayedLoad(response.responseCode)

    def setFeedback(self, callback_method):
        self.__feedback = callback_method

    def delayedLoad(self, code):
        if self._load_try < 10:
            self._load_try += 1
            code = responses.get(code) if isinstance(code, int) else code
            logError("StatisticsDataLoader: error loading statistic data - {}/{}", self._load_try, code)
            callback(2.0, self.getStatisticsDataFromServer)

    @staticmethod
    def regionError():
        logError("Statistics are not available in your region={}. Only in {}", AUTH_REALM, REGIONS.keys())

    def getStatisticsDataFromServer(self):
        if not self.enabled:
            return
        if self.__feedback is None:
            raise ReferenceError("feedback method is not set")
        arenaDP = self.sessionProvider.getArenaDP()
        if arenaDP is None:
            return self.delayedLoad("arenaDP is None")
        users = [str(vInfo.player.accountDBID) for vInfo in arenaDP.getVehiclesInfoIterator() if
                 vInfo.player.accountDBID]
        if not users:
            return self.delayedLoad("users list is empty")
        logDebug("StatisticsDataLoader/getStatisticsDataFromServer: START request data: ids={}, len={} ", users,
                 len(users))
        url = self.STAT_URL.format(ids=self.SEPARATOR.join(users), key=self.API_KEY, url=self.URL, fields=self.FIELDS)
        fetchURL(url, self.onDataResponse)

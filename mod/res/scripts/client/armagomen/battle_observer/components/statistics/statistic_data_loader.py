import random

import constants
from armagomen.battle_observer.components.statistics.wtr_data import WTRStatistics
from armagomen.utils.common import urlResponse, logDebug, logInfo, logError, callback
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider

region = constants.AUTH_REALM.lower()
if region == "na":
    region = "com"


class StatisticsDataLoader(object):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)
    URL = "https://api.worldoftanks.{}/wot/account/info/?".format(region)
    SEPARATOR = "%2C"
    FIELDS = SEPARATOR.join(("statistics.random.wins", "statistics.random.battles", "global_rating", "nickname"))
    API_KEY = ("ffa0979342d69fe92970571918cc59b6", "76b3c385f1485e1fee1642c1e287c0ce")
    STAT_URL = "{url}application_id={key}&account_id={ids}&extra=statistics.random&fields={fields}&language=en"

    def __init__(self):
        self.loadedData = {}
        self.enabled = region in ["ru", "eu", "com", "asia"]
        self.loaded = False
        self._load_try = 0
        self.__wtrData = WTRStatistics()
        callback(0.0, self.setCachedStatisticData)

    def request(self, databaseIDS):
        result = urlResponse(self.STAT_URL.format(ids=self.SEPARATOR.join(str(_id) for _id in databaseIDS),
                                                  key=random.choice(self.API_KEY), url=self.URL, fields=self.FIELDS))
        if result is not None:
            data = result.get("data", {})
            result = {int(key): value for key, value in data.iteritems() if value}
        logDebug("StatisticsDataLoader: request result: data={}", result)
        return result

    def delayedLoad(self):
        if self._load_try < 20:
            self._load_try += 1
            callback(0.5, self.setCachedStatisticData)

    def setCachedStatisticData(self):
        if not self.enabled:
            return logInfo("Statistics are not available in your region. Only ru, eu, com, asia")
        arenaDP = self.sessionProvider.getArenaDP()
        if arenaDP is None:
            logError("StatisticsDataLoader/setCachedStatisticData: arenaDP is None")
            return self.delayedLoad()
        users = [vInfo.player.accountDBID for vInfo in arenaDP.getVehiclesInfoIterator() if vInfo.player.accountDBID]
        if not users:
            return self.delayedLoad()
        logDebug("StatisticsDataLoader/setCachedStatisticData: START request data: ids={}, len={} ", users, len(users))
        data = self.request(users)
        if data is not None:
            self.loadedData = data
            logDebug("StatisticsDataLoader/setCachedStatisticData: FINISH request users data")
        else:
            return self.delayedLoad()
        self.loaded = True
        self.__wtrData.updateAllItems(arenaDP, self.loadedData)

    @property
    def itemsWTRData(self):
        return self.__wtrData.itemsData

    def clear(self):
        self.loadedData.clear()
        self.loaded = False

import copy
import random

import constants
from armagomen.battle_observer.core import settings
from armagomen.constants import MAIN
from armagomen.utils.common import urlResponse, logDebug, logInfo, logError
from helpers.func_utils import callback

region = constants.AUTH_REALM.lower()
if region == "na":
    region = "com"


class StatisticsDataLoader(object):
    URL = "https://api.worldoftanks.{}/wot/account/info/?".format(region)
    SEPARATOR = "%2C"
    FIELDS = SEPARATOR.join(("statistics.random.wins", "statistics.random.battles", "global_rating", "nickname"))
    API_KEY = ("ffa0979342d69fe92970571918cc59b6", "76b3c385f1485e1fee1642c1e287c0ce")
    STAT_URL = "{url}application_id={key}&account_id={ids}&extra=statistics.random&fields={fields}&language=en".format(
        url=URL, key=random.choice(API_KEY), ids="{ids}", fields=FIELDS)

    def __init__(self):
        self.cache = {}
        self.enabled = region in ["ru", "eu", "com", "asia"]
        self.loaded = False
        if settings.xvmInstalled:
            logInfo("StatisticsDataLoader: statistics/icons/minimap module is disabled, XVM is installed")

    def request(self, databaseIDS):
        result = urlResponse(self.STAT_URL.format(ids=self.SEPARATOR.join(str(_id) for _id in databaseIDS)))
        if result is not None:
            result = result.get("data")
        logDebug("StatisticsDataLoader: request result: data={}", result)
        return result

    def delayedLoad(self, arenaDP):
        callback(0.1, self, "setCachedStatisticData", arenaDP)

    def setCachedStatisticData(self, arenaDP):
        if not self.enabled:
            return logInfo("Statistics are not available in your region. Only ru, eu, com, asia")
        if arenaDP is None:
            return logError("StatisticsDataLoader: arenaDP is None")
        users = [vInfo.player.accountDBID for vInfo in arenaDP.getVehiclesInfoIterator() if vInfo.player.accountDBID]
        if not users:
            logError("StatisticsDataLoader: users list is empty, deferred loading")
            return self.delayedLoad(arenaDP)
        logDebug("StatisticsDataLoader: START request data: ids={}, len={} ", users, len(users))
        data = self.request(users)
        if data is not None:
            for _id, value in data.iteritems():
                self.cache[int(_id)] = copy.deepcopy(value)
            logDebug("StatisticsDataLoader: FINISH request data")
        else:
            return self.delayedLoad(arenaDP)
        self.loaded = True

    def getUserData(self, databaseID):
        return self.cache.get(databaseID)

    def clear(self):
        self.cache.clear()
        self.loaded = False

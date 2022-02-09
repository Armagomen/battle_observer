import copy

import constants
from armagomen.battle_observer.core import settings
from armagomen.constants import MAIN
from armagomen.utils.common import urlResponse, logDebug, logInfo
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
    API_KEY = "application_id=2a7b45c57d9197bfa7fcb0e342673292&account_id="
    STAT_URL = "{url}{key}{ids}&extra=statistics.random&fields={fields}&language=en".format(
        url=URL, key=API_KEY, ids="{ids}", fields=FIELDS)

    def __init__(self):
        self.cache = {}
        self.enabled = region in ["ru", "eu", "com", "asia"] and not settings.xvmInstalled
        if settings.xvmInstalled:
            logInfo("statistics/icons/minimap module is disabled, XVM is installed")

    def request(self, databaseIDS):
        result = urlResponse(self.STAT_URL.format(ids=self.SEPARATOR.join(str(_id) for _id in databaseIDS)))
        if result is not None:
            result = result.get("data")
        if settings.main[MAIN.DEBUG]:
            logDebug("request statistics result: data={}".format(result))
        return result

    def setCachedStatisticData(self):
        arenaDP = self.sessionProvider.getArenaDP()
        if arenaDP is None or not self.enabled:
            return
        toRequest = []
        for vInfo in arenaDP.getVehiclesInfoIterator():
            if vInfo.player.accountDBID and vInfo.player.accountDBID not in self.cache:
                toRequest.append(vInfo.player.accountDBID)
        if toRequest:
            if settings.main[MAIN.DEBUG]:
                logDebug("START request statistics data: ids={}, len={} ".format(toRequest, len(toRequest)))
            data = self.request(toRequest)
            if data is not None:
                for _id, value in data.iteritems():
                    self.cache[int(_id)] = copy.deepcopy(value)
            if settings.main[MAIN.DEBUG]:
                logDebug("FINISH request statistics data")

    def getStatisticForUser(self, databaseID):
        return self.cache.get(databaseID)

    def clear(self):
        self.cache.clear()


statisticLoader = StatisticsDataLoader()

import copy

import constants
from armagomen.battle_observer.core import settings
from armagomen.battle_observer.statistics.plugin import StatisticPlugin
from armagomen.constants import MAIN, GLOBAL
from armagomen.utils.common import urlResponse, logDebug, logInfo
from gui.shared.personality import ServicesLocator
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
        self.enabled = region in ["ru", "eu", "com", "asia"]
        self.plugin = StatisticPlugin(settings.statistics)

    def request(self, databaseIDS):
        result = urlResponse(self.STAT_URL.format(ids=self.SEPARATOR.join(str(_id) for _id in databaseIDS)))
        if result is not None:
            result = result.get("data")
        if settings.main[MAIN.DEBUG]:
            logDebug("request statistics result: data={}".format(result))
        return result

    def setCachedStatisticData(self):
        arenaDP = self.sessionProvider.getArenaDP()
        result = False
        if arenaDP is None or not self.enabled:
            return result
        toRequest = []
        inCache = GLOBAL.ZERO
        for vInfo in arenaDP.getVehiclesInfoIterator():
            if vInfo.player.accountDBID and vInfo.player.accountDBID not in self.cache:
                toRequest.append(vInfo.player.accountDBID)
            elif vInfo.player.accountDBID in self.cache:
                inCache += GLOBAL.ONE
        if toRequest:
            if settings.main[MAIN.DEBUG]:
                logDebug("START request statistics data: ids={}, len={} ".format(toRequest, len(toRequest)))
            data = self.request(toRequest)
            result = data is not None
            if result:
                for _id, value in data.iteritems():
                    self.cache[int(_id)] = copy.deepcopy(value)
            if settings.main[MAIN.DEBUG]:
                logDebug("FINISH request statistics data")
        else:
            result = inCache > GLOBAL.ZERO
        return result

    def getStatisticForUser(self, databaseID):
        return self.cache.get(databaseID)

    def clear(self):
        self.cache.clear()


statisticLoader = StatisticsDataLoader()


def checkXVM(spaceID):
    ServicesLocator.appLoader.onGUISpaceEntered -= checkXVM
    if not statisticLoader.enabled:
        return
    from sys import modules
    XVM = "xvm"
    for key in modules:
        if statisticLoader.enabled and XVM in key:
            statisticLoader.enabled = False
            break
    if not statisticLoader.enabled:
        settings.statistics[GLOBAL.ENABLED] = statisticLoader.enabled
        settings.minimap[GLOBAL.ENABLED] = statisticLoader.enabled
        logInfo("statistics/icons/minimap module is disabled, XVM is installed")
    else:
        statisticLoader.plugin.start()


ServicesLocator.appLoader.onGUISpaceEntered += checkXVM

import copy

import constants
from armagomen.battle_observer.core import settings
from armagomen.constants import MAIN, GLOBAL
from armagomen.utils.common import urlResponse, logDebug, logInfo
from gui.shared.personality import ServicesLocator
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider

region = constants.AUTH_REALM.lower()
statisticEnabled = region in ["ru", "eu", "na", "asia"]
if region == "na":
    region = "com"

xvmInstalled = False


def checkXVM(*args, **kwargs):
    from sys import modules
    global xvmInstalled
    XVM = "xvm"
    for key in modules:
        if not xvmInstalled and XVM in key:
            xvmInstalled = True
            break
    ServicesLocator.appLoader.onGUISpaceEntered -= checkXVM
    if xvmInstalled:
        logInfo("statistics/icons module is disabled, XVM is installed")


ServicesLocator.appLoader.onGUISpaceEntered += checkXVM

if statisticEnabled:
    URL = "https://api.worldoftanks.{}/wot/account/info/?".format(region)
    SEPARATOR = "%2C"
    FIELDS = SEPARATOR.join(("statistics.random.wins", "statistics.random.battles", "global_rating", "nickname"))
    API_KEY = "application_id=2a7b45c57d9197bfa7fcb0e342673292&account_id="
    STAT_URL = "{url}{key}{ids}&extra=statistics.random&fields={fields}&language=en".format(
        url=URL, key=API_KEY, ids="{ids}", fields=FIELDS)
CACHE = {}


def request(databaseIDS):
    result = urlResponse(STAT_URL.format(ids=SEPARATOR.join(str(_id) for _id in databaseIDS)))
    if result is not None:
        result = result.get("data")
    if settings.main[MAIN.DEBUG]:
        logDebug("request statistics result: data={}".format(result))
    return result


def setCachedStatisticData():
    result = False
    if not statisticEnabled or xvmInstalled:
        return result
    sessionProvider = dependency.instance(IBattleSessionProvider)
    arenaDP = sessionProvider.getArenaDP()
    if arenaDP is None:
        return result
    toRequest = []
    inCache = GLOBAL.ZERO
    for vInfo in arenaDP.getVehiclesInfoIterator():
        if vInfo.player.accountDBID and vInfo.player.accountDBID not in CACHE:
            toRequest.append(vInfo.player.accountDBID)
        elif vInfo.player.accountDBID in CACHE:
            inCache += GLOBAL.ONE
    if toRequest:
        if settings.main[MAIN.DEBUG]:
            logDebug("START request statistics data: ids={}, len={} ".format(toRequest, len(toRequest)))
        data = request(toRequest)
        result = data is not None
        if result:
            for _id, value in data.iteritems():
                CACHE[int(_id)] = copy.deepcopy(value)
        if settings.main[MAIN.DEBUG]:
            logDebug("FINISH request statistics data")
    else:
        result = inCache > GLOBAL.ZERO
    return result


def getStatisticForUser(databaseID):
    return CACHE.get(databaseID)

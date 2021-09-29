import copy

import constants
from armagomen.utils.common import urlResponse

region = constants.AUTH_REALM.lower()
statisticEnabled = region in ["ru", "eu", "na", "asia"]
if region == "na":
    region = "com"

if statisticEnabled:
    URL = "https://api.worldoftanks.{}/wot/account/info/?".format(region)
    API_KEY = "application_id=2a7b45c57d9197bfa7fcb0e342673292&account_id="
    STAT_URL = "{url}{key}{ids}&extra=statistics.random&fields=statistics.random&" \
               "language=en".format(url=URL, key=API_KEY, ids="{ids}")
    WTR = "{url}{key}{ids}&fields=global_rating&language=en".format(url=URL, key=API_KEY, ids="{ids}")
    SEPARATOR = "%2C"
    CACHE = {}
    WTR_CACHE = {}


def normalizeIDS(databaseIDS, wtr=False):
    if wtr:
        return (str(_id) for _id in databaseIDS if _id and _id not in WTR_CACHE)
    return (str(_id) for _id in databaseIDS if _id and _id not in CACHE)


def getCachedStatisticData(databaseIDS):
    if not statisticEnabled:
        return
    databaseIDS = tuple(databaseIDS)
    result = urlResponse(STAT_URL.format(ids=SEPARATOR.join(normalizeIDS(databaseIDS))))
    data = result.get("data")
    if data:
        for _id, value in data.iteritems():
            CACHE[int(_id)] = copy.deepcopy(value["statistics"]["random"])
    return {_id: CACHE[_id] for _id in databaseIDS if _id and _id in CACHE}


def getStatisticData(databaseIDS):
    if not statisticEnabled:
        return
    result = urlResponse(STAT_URL.format(ids=SEPARATOR.join(normalizeIDS(databaseIDS))))
    data = result.get("data")
    if data:
        return {int(_id): value["statistics"]["random"] for _id, value in data.iteritems()}


def getCachedWTR(databaseIDS):
    if not statisticEnabled:
        return
    databaseIDS = tuple(databaseIDS)
    result = urlResponse(WTR.format(ids=SEPARATOR.join(normalizeIDS(databaseIDS, True))))
    data = result.get("data")
    if data:
        for databaseID, value in data.iteritems():
            WTR_CACHE[int(databaseID)] = int(value["global_rating"])
    return {_id: WTR_CACHE[_id] for _id in databaseIDS if _id and _id in WTR_CACHE}


def getWTRRating(databaseIDS):
    if not statisticEnabled:
        return
    result = urlResponse(WTR.format(ids=SEPARATOR.join(normalizeIDS(databaseIDS, True))))
    data = result.get("data")
    if data:
        return {int(_id): int(value[u"global_rating"]) for _id, value in data.iteritems()}

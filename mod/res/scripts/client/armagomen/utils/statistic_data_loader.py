import copy
import json
import urllib2

from armagomen.constants import HEADERS
from armagomen.utils.common import logWarning

API_KEY = "2a7b45c57d9197bfa7fcb0e342673292"
API_URL = "https://api.worldoftanks.ru/wot/account/info/?application_id={key}&account_id=" \
          "{ids}&extra=statistics.random&fields=statistics.random&language=en".format(key=API_KEY, ids="{ids}")
SEPARATOR = "%2C+"
CACHE = {}


def urlResponse(databaseIDS):
    try:
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(), urllib2.HTTPRedirectHandler())
        opener.addheaders = HEADERS
        response = opener.open(API_URL.format(ids=SEPARATOR.join(databaseIDS)))
    except urllib2.URLError:
        logWarning("Technical problems with the server, please inform the developer.")
    else:
        return json.load(response)


def getCachedStatisticData(databaseIDS, update=True):
    databaseIDS = [databaseID for databaseID in databaseIDS if databaseID not in CACHE]
    if not update or not databaseIDS:
        return CACHE
    result = urlResponse(databaseIDS)
    if not result:
        return CACHE
    data = result.get("data")
    if data:
        for databaseID in databaseIDS:
            CACHE[databaseID] = copy.deepcopy(data[str(databaseID)]["statistics"]["random"])
    return CACHE


def getStatisticData(databaseIDS):
    result = urlResponse(databaseIDS)
    if not result:
        return {}
    data = result.get("data")
    if data:
        return {databaseID: data[str(databaseID)]["statistics"]["random"] for databaseID in databaseIDS}

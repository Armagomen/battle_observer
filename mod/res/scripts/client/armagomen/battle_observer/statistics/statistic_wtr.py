import datetime

from armagomen.battle_observer.core import settings
from armagomen.battle_observer.statistics.statistic_data_loader import getStatisticForUser
from armagomen.constants import STATISTICS
from gui.shared.personality import ServicesLocator
from skeletons.gui.app_loader import GuiGlobalSpaceID

WTR_COLORS = ((2960, "bad"), (4520, "normal"), (6367, "good"), (8543, "very_good"), (10217, "unique"))
COLORS = settings.statistics[STATISTICS.COLORS]
DEFAULT_COLOR = "#fafafa"


class Cache(object):

    def __init__(self):
        self.data = {}
        self.timeDelta = datetime.datetime.now() + datetime.timedelta(minutes=120)
        ServicesLocator.appLoader.onGUISpaceEntered += self.clearCache

    def clearCache(self, spaceID):
        if spaceID == GuiGlobalSpaceID.LOBBY:
            currentTime = datetime.datetime.now()
            if currentTime >= self.timeDelta:
                self.timeDelta = currentTime + datetime.timedelta(minutes=120)
                self.data.clear()


cache = Cache()


def getWTR(data):
    return int(data.get("global_rating", 0))


def getPercent(data):
    wins = float(data["statistics"]["random"]["wins"])
    battles = int(data["statistics"]["random"]["battles"])
    if wins:
        return wins / battles * 100, battles
    return 0.0, battles


def getNickName(data):
    return data.get("nickname")


def getColor(wtr):
    result = "very_bad"
    for value, colorName in WTR_COLORS:
        if wtr >= value:
            result = colorName
        else:
            break
    return COLORS.get(result, DEFAULT_COLOR)


def getStatisticString(databaseID, clanTag):
    if databaseID not in cache.data:
        data = getStatisticForUser(databaseID)
        if data is not None:
            wtr = getWTR(data)
            winRate, battles = getPercent(data)
            clanTag = "[{}]".format(clanTag) if clanTag else ""
            cache.data[databaseID] = {"WTR": wtr, "colorWTR": getColor(wtr), "winRate": winRate, "battles": battles,
                                      "nickname": getNickName(data), "clanTag": clanTag}
        else:
            return None
    return cache.data[databaseID]

from armagomen.battle_observer.core import settings
from armagomen.battle_observer.statistics.statistic_data_loader import getStatisticForUser
from armagomen.constants import STATISTICS

WTR_COLORS = ((2971, "bad"), (4530, "normal"), (6370, "good"), (8525, "very_good"), (10158, "unique"))
COLORS = settings.statistics[STATISTICS.COLORS]
DEFAULT_COLOR = "#fafafa"
CACHE = {}


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
    if databaseID not in CACHE:
        data = getStatisticForUser(databaseID)
        if data is not None:
            wtr = getWTR(data)
            winRate, battles = getPercent(data)
            clanTag = "[{}]".format(clanTag) if clanTag else ""
            CACHE[databaseID] = {"WTR": wtr, "colorWTR": getColor(wtr), "winRate": winRate, "battles": battles,
                                 "nickname": getNickName(data), "clanTag": clanTag}
        else:
            return None
    return CACHE[databaseID]

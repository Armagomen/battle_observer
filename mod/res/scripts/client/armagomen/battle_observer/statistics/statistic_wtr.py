from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import PANELS
from armagomen.utils.common import logError

WTR_COLORS = ((2971, "bad"), (4530, "normal"), (6370, "good"), (8525, "very_good"), (10158, "unique"))
COLORS = settings.players_panels[PANELS.STATISTIC_COLORS]
DEFAULT_COLOR = "#fafafa"
CACHE = {}


def getWTR(data):
    return int(data.get("global_rating", 0))


def getPercent(data):
    wins = int(data["statistics"]["random"]["wins"])
    battles = int(data["statistics"]["random"]["battles"])
    if wins:
        return float(wins) / battles * 100, battles
    return 0.0, battles


def getColor(wtr):
    result = "very_bad"
    for value, colorName in WTR_COLORS:
        if wtr >= value:
            result = colorName
        else:
            break
    return COLORS.get(result, DEFAULT_COLOR)


def getStatisticString(databaseID, users):
    if databaseID not in CACHE:
        try:
            data = users[databaseID]
            wtr = getWTR(data)
            color = getColor(wtr)
            winRate, battles = getPercent(data)
            values = {"WTR": wtr, "colorWTR": color, "winRate": winRate, "battles": battles}
            CACHE[databaseID] = settings.players_panels[PANELS.STATISTIC_PATTERN] % values
        except (ValueError, KeyError, ZeroDivisionError) as error:
            logError("{}.getStatisticString {}".format(__package__, repr(error)))
            return ""
    return CACHE[databaseID]

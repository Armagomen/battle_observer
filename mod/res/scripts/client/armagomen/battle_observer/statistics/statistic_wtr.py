from math import log, floor

from armagomen.battle_observer.core import settings
from armagomen.battle_observer.statistics.statistic_data_loader import statisticLoader
from armagomen.constants import STATISTICS


class StatisticsWTR(object):
    DEFAULT_COLOR = "#fafafa"
    DEFAULT_RATING = 0
    DEFAULT_WIN_RATE = 0.0
    K = 1000.0
    UNITS = ['', 'K', 'M', 'G', 'T', 'P']

    def __init__(self):
        self.colors = settings.statistics[STATISTICS.COLORS]
        self.wtr_ranges = ((2960, "bad"), (4520, "normal"), (6367, "good"), (8543, "very_good"), (10217, "unique"))

    def getPercent(self, data):
        random = data["statistics"]["random"]
        battles = int(random["battles"])
        if battles:
            return float(random["wins"]) / battles * 100, self.battlesFormat(battles)
        return self.DEFAULT_WIN_RATE, str(battles)

    def battlesFormat(self, battles):
        magnitude = int(floor(log(battles, self.K)))
        return '%.1f%s' % (battles / self.K ** magnitude, self.UNITS[magnitude])

    def getColor(self, wtr):
        result = "very_bad"
        for value, colorName in self.wtr_ranges:
            if wtr >= value:
                result = colorName
            else:
                break
        return self.colors.get(result, self.DEFAULT_COLOR)

    def getStatisticsData(self, databaseID, clanTag):
        data = statisticLoader.getStatisticForUser(databaseID)
        if data is not None:
            wtr = int(data.get("global_rating", self.DEFAULT_RATING))
            winRate, battles = self.getPercent(data)
            return {"WTR": wtr, "colorWTR": self.getColor(wtr), "winRate": winRate,
                    "battles": battles, "nickname": data.get("nickname"),
                    "clanTag": "[{}]".format(clanTag) if clanTag else ""}
        else:
            return None


wtr_rating = StatisticsWTR()

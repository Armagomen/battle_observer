import datetime

from armagomen.battle_observer.core import settings
from armagomen.battle_observer.statistics.statistic_data_loader import statisticLoader
from armagomen.constants import STATISTICS
from gui.shared.personality import ServicesLocator
from skeletons.gui.app_loader import GuiGlobalSpaceID


class WTRCache(object):

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
                statisticLoader.clear()


class StatisticsWTR(object):
    DEFAULT_COLOR = "#fafafa"
    DEFAULT_RATING = 0
    DEFAULT_WIN_RATE = 0.0

    def __init__(self):
        self.cache = WTRCache()
        self.colors = settings.statistics[STATISTICS.COLORS]
        self.wtr_ranges = ((2960, "bad"), (4520, "normal"), (6367, "good"), (8543, "very_good"), (10217, "unique"))

    def getPercent(self, data):
        battles = int(data["statistics"]["random"]["battles"])
        if battles:
            return float(data["statistics"]["random"]["wins"]) / battles * 100, battles
        return self.DEFAULT_WIN_RATE, battles

    def getColor(self, wtr):
        result = "very_bad"
        for value, colorName in self.wtr_ranges:
            if wtr >= value:
                result = colorName
            else:
                break
        return self.colors.get(result, self.DEFAULT_COLOR)

    def getStatisticsData(self, databaseID, clanTag):
        if databaseID not in self.cache.data:
            data = statisticLoader.getStatisticForUser(databaseID)
            if data is not None:
                wtr = int(data.get("global_rating", self.DEFAULT_RATING))
                winRate, battles = self.getPercent(data)
                self.cache.data[databaseID] = {"WTR": wtr, "colorWTR": self.getColor(wtr), "winRate": winRate,
                                               "battles": battles, "nickname": data.get("nickname"),
                                               "clanTag": "[{}]".format(clanTag) if clanTag else ""}
            else:
                return None
        return self.cache.data[databaseID]


wtr_rating = StatisticsWTR()

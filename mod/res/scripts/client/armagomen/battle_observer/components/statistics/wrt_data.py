from math import floor, log

from armagomen.battle_observer.components.statistics.statistic_data_loader import statisticLoader
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import STATISTICS
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider


class WTRStatisticsAndIcons(object):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)

    COLOR_WTR = 'colorWTR'
    DEFAULT_COLOR = "#fafafa"
    DEFAULT_WIN_RATE = 0.0
    K = 1000.0
    UNITS = ['', 'k', 'm', 'g', 't', 'p']

    def __init__(self):
        self.settings = settings.statistics
        self.vehicle_types = settings.vehicle_types
        self.wtr_ranges = ((2960, "bad"), (4520, "normal"), (6367, "good"), (8543, "very_good"), (10217, "unique"))
        self.cache = {}

    @property
    def vehicleTextColorEnabled(self):
        return self.settings[STATISTICS.CHANGE_VEHICLE_COLOR]

    def getPattern(self, isEnemy):
        if isEnemy:
            return self.settings[STATISTICS.FULL_RIGHT], self.settings[STATISTICS.CUT_RIGHT]
        else:
            return self.settings[STATISTICS.FULL_LEFT], self.settings[STATISTICS.CUT_LEFT]

    def updateAllItems(self):
        arenaDP = self.sessionProvider.getArenaDP()
        allyTeam = arenaDP.getNumberOfTeam()
        for vInfo in arenaDP.getVehiclesInfoIterator():
            accountDBID = vInfo.player.accountDBID
            result = self.getStatisticsData(accountDBID, vInfo.player.clanAbbrev) if accountDBID else None
            fullName = None
            cutName = None
            vehicleTextColor = None
            if result is not None:
                full, cut = self.getPattern(vInfo.team != allyTeam)
                fullName = full % result
                cutName = cut % result
                vehicleTextColor = result[self.COLOR_WTR] if self.vehicleTextColorEnabled else None
            self.cache[vInfo.vehicleID] = {"fullName": fullName, "cutName": cutName,
                                           "iconMultiplier": self.settings[STATISTICS.ICON_BLACKOUT],
                                           "vehicleTextColor": vehicleTextColor}

    def __getPercent(self, data):
        random = data["statistics"]["random"]
        battles = int(random["battles"])
        if battles:
            return float(random["wins"]) / battles * 100, self.__battlesFormat(battles)
        return self.DEFAULT_WIN_RATE, str(battles)

    def __battlesFormat(self, battles):
        if battles >= self.K:
            magnitude = int(floor(log(battles, self.K)))
            return '%.1f%s' % (battles / self.K ** magnitude, self.UNITS[magnitude])
        return battles

    def __getColor(self, wtr):
        result = "very_bad"
        for value, colorName in self.wtr_ranges:
            if wtr >= value:
                result = colorName
            else:
                break
        return self.settings[STATISTICS.COLORS].get(result, self.DEFAULT_COLOR)

    def getStatisticsData(self, databaseID, clanTag):
        data = statisticLoader.getStatisticForUser(databaseID)
        if data is not None:
            wtr = int(data.get("global_rating", 0))
            winRate, battles = self.__getPercent(data)
            return {"WTR": wtr, "colorWTR": self.__getColor(wtr), "winRate": winRate,
                    "battles": battles, "nickname": data.get("nickname"),
                    "clanTag": "[{}]".format(clanTag) if clanTag else ""}
        else:
            return None

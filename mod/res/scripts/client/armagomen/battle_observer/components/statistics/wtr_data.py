from math import floor, log

from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import STATISTICS
from armagomen.utils.common import logDebug


class WTRStatistics(object):
    COLOR_WTR = 'colorWTR'
    DEFAULT_COLOR = "#fafafa"
    DEFAULT_WIN_RATE = 0.0
    K = 1000.0
    UNITS = ['', 'k', 'm', 'g', 't', 'p']

    def __init__(self):
        self.settings = settings.statistics
        self.vehicle_types = settings.vehicle_types
        self.wtr_ranges = ((3028, "bad"), (4578, "normal"), (6423, "good"), (8642, "very_good"), (10431, "unique"))
        self.itemsData = {}

    def getPattern(self, isEnemy, data):
        logDebug("isEnemy: {}, data:{}", isEnemy, data)
        if isEnemy:
            return self.settings[STATISTICS.FULL_RIGHT] % data, self.settings[STATISTICS.CUT_RIGHT] % data
        else:
            return self.settings[STATISTICS.FULL_LEFT] % data, self.settings[STATISTICS.CUT_LEFT] % data

    def updateAllItems(self, arenaDP, loadedData):
        allyTeam = arenaDP.getNumberOfTeam()
        for accountDBID in loadedData:
            vehicleID = arenaDP.getVehIDByAccDBID(accountDBID)
            vehInfo = arenaDP.getVehicleInfo(vehicleID)
            itemData = self.buildItemData(vehInfo.player.clanAbbrev, loadedData[accountDBID])
            full, cut = self.getPattern(vehInfo.team != allyTeam, itemData)
            textColor = itemData[self.COLOR_WTR] if self.settings[STATISTICS.CHANGE_VEHICLE_COLOR] else None
            self.itemsData[vehicleID] = {"fullName": full, "cutName": cut, "vehicleTextColor": textColor}

    def __getWinRateAndBattlesCount(self, data):
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

    def buildItemData(self, clanTag, data):
        wtr = int(data.get("global_rating", 0))
        winRate, battles = self.__getWinRateAndBattlesCount(data)
        return {"WTR": wtr, self.COLOR_WTR: self.__getColor(wtr), "winRate": winRate,
                "battles": battles, "nickname": data.get("nickname"),
                "clanTag": "[{}]".format(clanTag) if clanTag else ""}

from math import floor, log

from armagomen._constants import STATISTICS
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.logging import logDebug
from gui.battle_control import avatar_getter


class WTRStatistics(object):
    COLOR_WTR = 'colorWTR'
    DEFAULT_COLOR = "#fafafa"
    DEFAULT_WIN_RATE = 0.0
    K = 1000.0
    UNITS = ['', 'k', 'm', 'g', 't', 'p']

    def __init__(self):
        self.settings = user_settings.statistics
        self.wtr_ranges = ((3154, "bad"), (4698, "normal"), (6578, "good"), (8929, "very_good"), (10736, "unique"))
        self.itemsData = {}

    def getPattern(self, isEnemy, itemData):
        logDebug("WTRStatistics: isEnemy={}, data={}", isEnemy, itemData)
        if isEnemy:
            return self.settings[STATISTICS.FULL_RIGHT] % itemData, self.settings[STATISTICS.CUT_RIGHT] % itemData
        else:
            return self.settings[STATISTICS.FULL_LEFT] % itemData, self.settings[STATISTICS.CUT_LEFT] % itemData

    def updateAllItems(self, arenaDP, loadedData):
        player_team = avatar_getter.getPlayerTeam()
        for accountDBID, value in loadedData.iteritems():
            if not value:
                continue
            vehicle_id = arenaDP.getVehIDByAccDBID(int(accountDBID))
            veh_info = arenaDP.getVehicleInfo(vehicle_id)
            item_data = self.buildItemData(veh_info.player.clanAbbrev, value)
            full, cut = self.getPattern(veh_info.team != player_team, item_data)
            text_color = item_data[self.COLOR_WTR] if self.settings[STATISTICS.CHANGE_VEHICLE_COLOR] else None
            self.itemsData[vehicle_id] = {"fullName": full, "cutName": cut, "vehicleTextColor": text_color}

    def __getWinRateAndBattlesCount(self, data):
        random = data["statistics"]["random"]
        battles = int(random["battles"])
        if battles:
            return round(float(random["wins"]) / battles * 100, 2), self.__battlesFormat(battles)
        return self.DEFAULT_WIN_RATE, str(battles)

    def __battlesFormat(self, battles):
        if battles >= self.K:
            magnitude = int(floor(log(battles, self.K)))
            return '%.1f%s' % (battles / self.K ** magnitude, self.UNITS[magnitude])
        return str(battles)

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
        win_rate, battles = self.__getWinRateAndBattlesCount(data)
        return {"WTR": wtr, self.COLOR_WTR: self.__getColor(wtr), "winRate": win_rate,
                "battles": battles, "nickname": data.get("nickname"),
                "clanTag": "[{}]".format(clanTag) if clanTag else ""}

from math import floor, log

from armagomen.battle_observer.components.statistics.statistic_data_loader import statisticLoader
from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta
from armagomen.constants import STATISTICS, VEHICLE_TYPES, GLOBAL
from armagomen.utils.events import g_events


class StatsMeta(BaseModMeta):
    COLOR_WTR = 'colorWTR'
    DEFAULT_COLOR = "#fafafa"
    DEFAULT_WIN_RATE = 0.0
    K = 1000.0
    UNITS = ['', 'k', 'm', 'g', 't', 'p']

    def __init__(self):
        super(StatsMeta, self).__init__()
        self.wtr_ranges = ((2960, "bad"), (4520, "normal"), (6367, "good"), (8543, "very_good"), (10217, "unique"))

    def py_getIconMultiplier(self):
        return self.settings[STATISTICS.ICON_BLACKOUT]

    def getIconColor(self, classTag):
        return self.vehicle_types[VEHICLE_TYPES.CLASS_COLORS].get(classTag, GLOBAL.EMPTY_LINE)

    def as_updateVehicleS(self, isEnemy, vehicleID, iconColor, fullName, cutName, vehicleTextColor):
        if self._isDAAPIInited():
            self.flashObject.as_updateVehicle(isEnemy, vehicleID, iconColor, fullName, cutName, vehicleTextColor)

    def as_isComponentVisibleS(self, alias):
        return self.flashObject.as_isComponentVisible(alias) if self._isDAAPIInited() else False

    @property
    def vehicleTextColorEnabled(self):
        return self.settings[STATISTICS.CHANGE_VEHICLE_COLOR]

    def getPattern(self, isEnemy):
        g_events.updateVehicleData -= self._updateVehicleData
        raise NotImplementedError('Method must be override!: %s.%s', self.__class__.__name__, 'getPattern')

    def _updateVehicleData(self, isEnemy, vehicleID):
        vInfo = self._arenaDP.getVehicleInfo(vehicleID)
        accountDBID = vInfo.player.accountDBID
        iconColor = self.getIconColor(vInfo.vehicleType.classTag)
        result = self.getStatisticsData(accountDBID, vInfo.player.clanAbbrev) if accountDBID else None
        if result is not None:
            fullName, cut = self.getPattern(isEnemy)
            cutName = cut % result if cut else None
            vehicleTextColor = result[self.COLOR_WTR] if self.vehicleTextColorEnabled else None
            self.as_updateVehicleS(isEnemy, vehicleID, iconColor, fullName % result, cutName, vehicleTextColor)
        else:
            self.as_updateVehicleS(isEnemy, vehicleID, iconColor, None, None, None)

    def _populate(self):
        super(StatsMeta, self)._populate()
        g_events.updateVehicleData += self._updateVehicleData

    def _dispose(self):
        g_events.updateVehicleData -= self._updateVehicleData
        super(StatsMeta, self)._dispose()

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

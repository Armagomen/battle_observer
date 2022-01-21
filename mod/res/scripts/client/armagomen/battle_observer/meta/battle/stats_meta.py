from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta
from armagomen.battle_observer.statistics.statistic_wtr import wtr_rating
from armagomen.constants import STATISTICS, VEHICLE_TYPES, GLOBAL
from armagomen.utils.events import g_events


class StatsMeta(BaseModMeta):
    COLOR_WTR = 'colorWTR'

    def py_getIconMultiplier(self):
        return self.settings[STATISTICS.ICON_BLACKOUT]

    def getIconColor(self, classTag):
        return self.vehicle_types[VEHICLE_TYPES.CLASS_COLORS].get(classTag, GLOBAL.EMPTY_LINE)

    def as_updateVehicleS(self, isEnemy, vehicleID, iconColor, fullName, cutName, vehicleTextColor):
        if self._isDAAPIInited():
            self.flashObject.as_updateVehicle(isEnemy, vehicleID, iconColor, fullName, cutName, vehicleTextColor)

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
        result = wtr_rating.getStatisticsData(accountDBID, vInfo.player.clanAbbrev) if accountDBID else None
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

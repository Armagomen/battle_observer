from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta
from armagomen.constants import STATISTICS, VEHICLE_TYPES, GLOBAL


class StatsMeta(BaseModMeta):

    def py_getIconMultiplier(self):
        return self.settings[STATISTICS.ICON_BLACKOUT]

    def py_getIconColor(self, classTag):
        return self.vehicle_types[VEHICLE_TYPES.CLASS_COLORS].get(classTag, GLOBAL.EMPTY_LINE)

    def as_updateInfoS(self):
        return self.flashObject.as_updateInfo() if self._isDAAPIInited() else None

    def as_updateVehicleS(self, isEnemy, vehicleID, *args):
        if self._isDAAPIInited():
            self.flashObject.as_updateVehicle(isEnemy, vehicleID, *args)

from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta

class StatisticsAndIconsMeta(BaseModMeta):

    def as_update_wgr_dataS(self, itemsData):
        if self._isDAAPIInited():
            self.flashObject.as_update_wgr_data(itemsData)

    def as_updateByVehicleID(self, vehicleID, isEnemy):
        if self._isDAAPIInited():
            self.flashObject.as_updateByVehicleID(vehicleID, isEnemy)

    def as_updateALL(self, *args):
        if self._isDAAPIInited():
            self.flashObject.as_updateALL()
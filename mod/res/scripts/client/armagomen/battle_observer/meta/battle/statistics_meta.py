from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class StatisticsMeta(BaseModMeta):

    def as_updateDeadS(self, vehicleID):
        if self._isDAAPIInited():
            self.flashObject.as_updateDead(vehicleID)

    def as_ChangeModeS(self, value):
        if self._isDAAPIInited():
            self.flashObject.as_ChangeMode(value)

    def as_createItem(self, vehicleID, data, defaultMode):
        if self._isDAAPIInited():
            self.flashObject.createItem(vehicleID, data, defaultMode)

    def getItemData(self, vehicleID):
        raise NotImplementedError
from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class StatisticsMeta(BaseModMeta):

    def as_updateDeadS(self, vehicleID):
        if self._isDAAPIInited():
            self.flashObject.as_updateDead(vehicleID)

    def on_altModeS(self, enabled):
        if self._isDAAPIInited():
            self.flashObject.on_altMode(enabled)

    def as_createItem(self, vehicleID, isEnemy, data):
        if self._isDAAPIInited():
            self.flashObject.createItem(vehicleID, isEnemy, data)
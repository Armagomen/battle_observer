from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class PlayersPanelsMeta(BaseModMeta):

    def __init__(self):
        super(PlayersPanelsMeta, self).__init__()

    def onAddedToStorage(self, vehicleID, isEnemy):
        raise NotImplementedError

    def as_addHealthBarS(self, vehID, barColor, visible):
        if self._isDAAPIInited():
            self.flashObject.as_addHealthBar(vehID, barColor, visible)

    def as_addDamageS(self, vehID, params):
        if self._isDAAPIInited():
            self.flashObject.as_addDamage(vehID, params)

    def as_updateDamageS(self, vehicleID, text):
        if self._isDAAPIInited():
            self.flashObject.as_updateDamage(vehicleID, text)

    def as_setVehicleDeadS(self, vehicleID):
        if self._isDAAPIInited():
            self.flashObject.as_setVehicleDead(vehicleID)

    def as_updateHealthBarS(self, vehicleID, percent, textField):
        if self._isDAAPIInited():
            self.flashObject.as_updateHealthBar(vehicleID, percent, textField)

    def as_setHealthBarsVisibleS(self, visible):
        if self._isDAAPIInited():
            self.flashObject.as_setHealthBarsVisible(visible)

    def as_setPlayersDamageVisibleS(self, visible):
        if self._isDAAPIInited():
            self.flashObject.as_setPlayersDamageVisible(visible)

    def as_colorBlindBarsS(self, color):
        if self._isDAAPIInited():
            self.flashObject.as_colorBlindBars(color)

    def updateDamageLogPosition(self):
        if self._isDAAPIInited():
            self.flashObject.as_updateDamageLogPosition()

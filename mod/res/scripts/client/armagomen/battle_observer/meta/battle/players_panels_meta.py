from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class PlayersPanelsMeta(BaseModMeta):

    def __init__(self):
        super(PlayersPanelsMeta, self).__init__()

    def onAddedToStorage(self, vehicleID, isEnemy):
        pass

    def as_AddVehIdToListS(self, vehID, isEnemy):
        return self.flashObject.as_AddVehIdToList(vehID, isEnemy) if self._isDAAPIInited() else None

    def as_addHealthBarS(self, vehID, color, bgColor, settings, teamName, startVisible):
        return self.flashObject.as_addHealthBar(vehID, color, bgColor, settings, teamName,
                                                startVisible) if self._isDAAPIInited() else None

    def as_addDamageS(self, vehID, params):
        return self.flashObject.as_addDamage(vehID, params) if self._isDAAPIInited() else None

    def as_updateDamageS(self, vehicleID, text):
        return self.flashObject.as_updateDamage(vehicleID, text) if self._isDAAPIInited() else None

    def as_setVehicleDeadS(self, vehicleID):
        return self.flashObject.as_setVehicleDead(vehicleID) if self._isDAAPIInited() else None

    def as_updateHealthBarS(self, vehicleID, scale, textField):
        return self.flashObject.as_updateHealthBar(vehicleID, scale, textField) if self._isDAAPIInited() else None

    def as_setHealthBarsVisibleS(self, visible):
        return self.flashObject.as_setHealthBarsVisible(visible) if self._isDAAPIInited() else None

    def as_setPlayersDamageVisibleS(self, visible):
        return self.flashObject.as_setPlayersDamageVisible(visible) if self._isDAAPIInited() else None

    def as_colorBlindBarsS(self, color):
        return self.flashObject.as_colorBlindBars(color) if self._isDAAPIInited() else None

    def as_setSpottedPositionS(self, vehicleID):
        return self.flashObject.as_setSpottedPosition(vehicleID) if self._isDAAPIInited() else None

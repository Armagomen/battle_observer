from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class PlayersPanelsMeta(BaseModMeta):

    def __init__(self):
        super(PlayersPanelsMeta, self).__init__()

    def onAddedToStorage(self, vehicleID, isEnemy):
        pass

    def as_AddVehIdToListS(self, vehID, isEnemy):
        return self.flashObject.as_AddVehIdToList(vehID, isEnemy) if self._isDAAPIInited() else None

    def as_AddPPanelBarS(self, vehID, color, bgColor, settings, teamName, startVisible):
        return self.flashObject.as_AddPPanelBar(vehID, color, bgColor, settings, teamName,
                                                startVisible) if self._isDAAPIInited() else None

    def as_AddTextFieldS(self, vehID, name, params, teamName):
        return self.flashObject.as_AddTextField(vehID, name, params, teamName) if self._isDAAPIInited() else None

    def as_updateTextFieldS(self, vehicleID, name, text):
        return self.flashObject.as_updateTextField(vehicleID, name, text) if self._isDAAPIInited() else None

    def as_setVehicleDeadS(self, vehicleID):
        return self.flashObject.as_setVehicleDead(vehicleID) if self._isDAAPIInited() else None

    def as_updatePPanelBarS(self, vehicleID, scale, textField):
        return self.flashObject.as_updatePPanelBar(vehicleID, scale, textField) if self._isDAAPIInited() else None

    def as_setVehicleIconColorS(self, vehID, color, multiplier, enemy):
        return self.flashObject.as_setVehicleIconColor(vehID, color, multiplier,
                                                       enemy) if self._isDAAPIInited() else None

    def as_setHPbarsVisibleS(self, vehID, visible):
        return self.flashObject.as_setHPbarsVisible(vehID, visible) if self._isDAAPIInited() else None

    def as_setPlayersDamageVisibleS(self, visible):
        return self.flashObject.as_setPlayersDamageVisible(visible) if self._isDAAPIInited() else None

    def as_colorBlindPPbarsS(self, vehicleID, color):
        return self.flashObject.as_colorBlindPPbars(vehicleID, color) if self._isDAAPIInited() else None

    def as_setSpottedPositionS(self, vehicleID):
        return self.flashObject.as_setSpottedPosition(vehicleID) if self._isDAAPIInited() else None

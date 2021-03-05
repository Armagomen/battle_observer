from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class PlayersPanelsMeta(BaseModMeta):

    def __init__(self):
        super(PlayersPanelsMeta, self).__init__()

    def as_AddVehIdToListS(self, vehID):
        return self.flashObject.as_AddVehIdToList(vehID) if self._isDAAPIInited() else None

    def as_AddPPanelBarS(self, vehID, color, settings, teamName, startVisible):
        return self.flashObject.as_AddPPanelBar(vehID, color, settings, teamName,
                                                startVisible) if self._isDAAPIInited() else None

    def as_AddTextFieldS(self, vehID, name, params, teamName):
        return self.flashObject.as_AddTextField(vehID, name, params, teamName) if self._isDAAPIInited() else None

    def as_updateTextFieldS(self, vehicleID, name, text):
        return self.flashObject.as_updateTextField(vehicleID, name, text) if self._isDAAPIInited() else None

    def as_updatePPanelBarS(self, vehicleID, currHP, maxHP, textField):
        return self.flashObject.as_updatePPanelBar(vehicleID, currHP, maxHP,
                                                   textField) if self._isDAAPIInited() else None

    def as_setVehicleIconColorS(self, vehID, color, multipler, enemy):
        return self.flashObject.as_setVehicleIconColor(vehID, color, multipler,
                                                       enemy) if self._isDAAPIInited() else None

    def as_setHPbarsVisibleS(self, vehID, visible):
        return self.flashObject.as_setHPbarsVisible(vehID, visible) if self._isDAAPIInited() else None

    def as_setPlayersDamageVisibleS(self, visible):
        return self.flashObject.as_setPlayersDamageVisible(visible) if self._isDAAPIInited() else None

    def as_colorBlindPPbarsS(self, vehicleID, color):
        return self.flashObject.as_colorBlindPPbars(vehicleID, color) if self._isDAAPIInited() else None

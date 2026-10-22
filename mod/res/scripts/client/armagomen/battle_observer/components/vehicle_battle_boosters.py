from adisp import adisp_process
from armagomen._constants import MAIN
from armagomen._logger import IALogger
from armagomen.battle_observer.settings.interface import IBOSettingsLoader
from armagomen.battle_observer.shared.on_vehicle_change import OnVehicleChangeSubscribed
from armagomen.utils.common import delayedCall
from gui.shared.gui_items.processors.vehicle import VehicleAutoBattleBoosterEquipProcessor
from helpers import dependency


class BattleBoosters(OnVehicleChangeSubscribed):
    settingsLoader = dependency.descriptor(IBOSettingsLoader)
    logger = dependency.descriptor(IALogger)

    def __init__(self):
        super(BattleBoosters, self).__init__()

    @adisp_process
    def changeValue(self, vehicle, value):
        yield VehicleAutoBattleBoosterEquipProcessor(vehicle, value).request()

    @delayedCall(0.3)
    def onVehicleChanged(self, vehicle):
        if not self.settingsLoader.getSetting(MAIN.NAME, MAIN.DIRECTIVES):
            return
        if vehicle is None or vehicle.isLocked:
            return
        if not hasattr(vehicle, "battleBoosters") or vehicle.battleBoosters is None:
            self.logger.logInfo("No battle boosters available for this vehicle: {}", vehicle.userName)
            return
        isAuto = vehicle.isAutoBattleBoosterEquip()
        boosters = vehicle.battleBoosters.installed.getItems()
        for battleBooster in boosters:
            value = battleBooster.inventoryCount > 0
            if value != isAuto:
                self.changeValue(vehicle, value)
                self.logger.logInfo("VehicleAutoBattleBoosterEquipProcessor: value={} vehicle={}, booster={}",
                                    value, vehicle.userName, battleBooster.userName)

    def fini(self):
        super(BattleBoosters, self).fini()


b_boosters = BattleBoosters()


def fini():
    b_boosters.fini()

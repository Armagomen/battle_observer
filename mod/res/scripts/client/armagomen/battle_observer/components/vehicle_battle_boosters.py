from adisp import adisp_process
from armagomen._constants import MAIN
from armagomen.battle_observer.settings import IBOSettingsLoader
from armagomen.utils.events import g_events
from armagomen.utils import isSpecialVehicle
from armagomen.utils.logging import logInfo
from gui.shared.gui_items.processors.vehicle import VehicleAutoBattleBoosterEquipProcessor
from helpers import dependency


class BattleBoosters(object):
    settingsLoader = dependency.descriptor(IBOSettingsLoader)

    def __init__(self):
        g_events.onVehicleChangedDelayed += self.onVehicleChanged

    @adisp_process
    def changeValue(self, vehicle, value):
        yield VehicleAutoBattleBoosterEquipProcessor(vehicle, value).request()

    def onVehicleChanged(self, vehicle):
        if not self.settingsLoader.getSetting(MAIN.NAME, MAIN.DIRECTIVES):
            return
        if vehicle is None or vehicle.isLocked or isSpecialVehicle(vehicle):
            return
        if not hasattr(vehicle, "battleBoosters") or vehicle.battleBoosters is None:
            logInfo("No battle boosters available for this vehicle: {}", vehicle.userName)
            return
        isAuto = vehicle.isAutoBattleBoosterEquip()
        boosters = vehicle.battleBoosters.installed.getItems()
        for battleBooster in boosters:
            value = battleBooster.inventoryCount > 0
            if value != isAuto:
                self.changeValue(vehicle, value)
                logInfo("VehicleAutoBattleBoosterEquipProcessor: value={} vehicle={}, booster={}",
                        value, vehicle.userName, battleBooster.userName)

    def fini(self):
        g_events.onVehicleChangedDelayed -= self.onVehicleChanged


b_boosters = BattleBoosters()


def fini():
    b_boosters.fini()

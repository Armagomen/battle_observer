from adisp import adisp_process
from armagomen._constants import MAIN
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.events import g_events
from armagomen.utils.logging import logDebug, logInfo
from gui.shared.gui_items.processors.vehicle import VehicleAutoBattleBoosterEquipProcessor


@adisp_process
def changeValue(vehicle, value):
    yield VehicleAutoBattleBoosterEquipProcessor(vehicle, value).request()


def onVehicleChanged(vehicle):
    if not user_settings.main[MAIN.DIRECTIVES]:
        return
    if vehicle is None or vehicle.isLocked or vehicle.isInBattle:
        return
    if not hasattr(vehicle, "battleBoosters") or vehicle.battleBoosters is None:
        logDebug("No battle boosters available for this vehicle: {}", vehicle.userName)
        return
    isAuto = vehicle.isAutoBattleBoosterEquip()
    boosters = vehicle.battleBoosters.installed.getItems()
    for battleBooster in boosters:
        value = battleBooster.inventoryCount > 0
        if value != isAuto:
            changeValue(vehicle, value)
            logInfo("VehicleAutoBattleBoosterEquipProcessor: value={} vehicle={}, booster={}".format(
                value, vehicle.userName, battleBooster.userName))


g_events.onVehicleChangedDelayed += onVehicleChanged

from CurrentVehicle import g_currentVehicle
from adisp import AdispException, process
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import MAIN
from armagomen.utils.common import logInfo, logDebug, logError, callback
from debug_utils import LOG_CURRENT_EXCEPTION
from gui.shared.gui_items.processors.vehicle import VehicleAutoBattleBoosterEquipProcessor


@process
def changeValue(vehicle, value):
    yield VehicleAutoBattleBoosterEquipProcessor(vehicle, value).request()


def onVehicleChanged():
    if not settings.main[MAIN.DIRECTIVES]:
        return
    vehicle = g_currentVehicle.item
    if vehicle is None or vehicle.isLocked or vehicle.isInBattle:
        return
    if not hasattr(vehicle, "battleBoosters") or vehicle.battleBoosters is None:
        logDebug("No battle boosters available for this vehicle: {}", vehicle.name)
        return
    isAuto = vehicle.isAutoBattleBoosterEquip()
    boosters = vehicle.battleBoosters.installed.getItems()
    for battleBooster in boosters:
        value = battleBooster.inventoryCount > 0
        if value != isAuto:
            try:
                callback(1.0, lambda: changeValue(vehicle, value))
                logInfo("VehicleAutoBattleBoosterEquipProcessor: value={} vehicle={}, booster={}".format(
                    value, vehicle.userName, battleBooster.userName))
            except AdispException as error:
                logError(repr(error))
                LOG_CURRENT_EXCEPTION()


g_currentVehicle.onChanged += onVehicleChanged

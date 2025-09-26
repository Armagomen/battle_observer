from adisp import adisp_process
from armagomen._constants import MAIN
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.events import g_events
from armagomen.utils.logging import logInfo
from gui.shared.gui_items.processors.vehicle import VehicleAutoBattleBoosterEquipProcessor


@adisp_process
def changeValue(vehicle, value):
    yield VehicleAutoBattleBoosterEquipProcessor(vehicle, value).request()


def isSpecialVehicle(vehicle):
    flags = ('isOnlyForFunRandomBattles', 'isOnlyForBattleRoyaleBattles', 'isOnlyForMapsTrainingBattles',
             'isOnlyForClanWarsBattles', 'isOnlyForComp7Battles', 'isOnlyForEventBattles', 'isOnlyForEpicBattles')
    return any(getattr(vehicle, f, False) for f in flags)


def onVehicleChanged(vehicle):
    if not user_settings.main[MAIN.DIRECTIVES]:
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
            changeValue(vehicle, value)
            logInfo("VehicleAutoBattleBoosterEquipProcessor: value={} vehicle={}, booster={}",
                    value, vehicle.userName, battleBooster.userName)


g_events.onVehicleChangedDelayed += onVehicleChanged


def fini():
    g_events.onVehicleChangedDelayed -= onVehicleChanged

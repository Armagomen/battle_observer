from CurrentVehicle import g_currentVehicle
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import MAIN
from armagomen.utils.common import logInfo, logDebug
from armagomen.utils.events import g_events
from gui.shared.gui_items.Vehicle import Vehicle
from gui.shared.gui_items.processors.vehicle import VehicleAutoBattleBoosterEquipProcessor
from gui.shared.utils import decorators


@decorators.process('techMaintenance')
def boosterEquip(vehicle, value):
    if vehicle is not None:
        result = yield VehicleAutoBattleBoosterEquipProcessor(vehicle, value).request()
        if result.success:
            logInfo("The isAutoBattleBoosterEquip is %s for '%s'" % (value, vehicle.userName))


def onVehicleChanged():
    if not settings.main[MAIN.DIRECTIVES]:
        return
    vehicle = g_currentVehicle.item  # type: Vehicle
    if g_currentVehicle.isLocked() or g_currentVehicle.isInBattle():
        return
    if not hasattr(vehicle, "battleBoosters") or vehicle.battleBoosters is None:
        logDebug("No battle boosters available for this vehicle: {}", vehicle.name)
        return
    for battleBooster in vehicle.battleBoosters.installed.getItems():
        value = battleBooster.inventoryCount > 0
        if value != vehicle.isAutoBattleBoosterEquip():
            boosterEquip(vehicle, value)


g_events.onHangarVehicleChanged += onVehicleChanged

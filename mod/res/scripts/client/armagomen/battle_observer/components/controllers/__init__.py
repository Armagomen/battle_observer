from armagomen.battle_observer.components.controllers.current_vehicle_data import CurrentVehicleCachedData
from armagomen.battle_observer.components.controllers.players_damage_controller import PlayersDamageController

cachedVehicleData = CurrentVehicleCachedData()
damage_controller = PlayersDamageController()


def fini():
    cachedVehicleData.fini()

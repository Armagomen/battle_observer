from armagomen.battle_observer.shared.battle.keys_listener import IBOKeysListener
from armagomen.battle_observer.shared.battle.piercing_randomizer import IBOPiercingRandomizer
from armagomen.battle_observer.shared.battle.players_damage import IBOPlayersDamageController
from armagomen.battle_observer.shared.battle.view_settings import IViewSettings
from armagomen.battle_observer.shared.current_vehicle_data import IBOCurrentVehicleCachedData
from armagomen.battle_observer.shared.online import IBOOnline

__all__ = ('IBOCurrentVehicleCachedData', 'IBOPlayersDamageController', 'IBOKeysListener', 'IBOPiercingRandomizer', 'IBOOnline',
           'IViewSettings')


def register_services():
    from helpers.dependency import _g_manager, DependencyManager
    from armagomen.battle_observer.shared.battle.keys_listener import KeysListener
    from armagomen.battle_observer.shared.battle.piercing_randomizer import PiercingRandomizer
    from armagomen.battle_observer.shared.battle.players_damage import PlayersDamageController
    from armagomen.battle_observer.shared.battle.view_settings import ViewSettingsAS
    from armagomen.battle_observer.shared.current_vehicle_data import CurrentVehicleCachedData
    from armagomen.battle_observer.shared.online import Online

    services = ((IBOOnline, Online),
                (IBOPlayersDamageController, PlayersDamageController),
                (IBOCurrentVehicleCachedData, CurrentVehicleCachedData),
                (IBOKeysListener, KeysListener),
                (IBOPiercingRandomizer, PiercingRandomizer),
                (IViewSettings, ViewSettingsAS))

    manager = _g_manager  # type: DependencyManager

    for interface, service in services:
        manager.addInstance(interface, service(), finalizer='fini')


inited = False
if not inited:
    register_services()
    inited = True

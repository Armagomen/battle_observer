def register_services():
    from helpers.dependency import _g_manager, DependencyManager

    from armagomen.battle_observer.shared.battle.keys_listener import KeysListener
    from armagomen.battle_observer.shared.interface import IBOKeysListener

    from armagomen.battle_observer.shared.battle.piercing_randomizer import PiercingRandomizer
    from armagomen.battle_observer.shared.interface import IBOPiercingRandomizer

    from armagomen.battle_observer.shared.battle.players_damage import PlayersDamageController
    from armagomen.battle_observer.shared.interface import IBOPlayersDamageController

    from armagomen.battle_observer.shared.battle.view_settings import ViewSettingsAS
    from armagomen.battle_observer.shared.interface import IViewSettings

    from armagomen.battle_observer.shared.current_vehicle_data import CurrentVehicleCachedData
    from armagomen.battle_observer.shared.interface import IBOCurrentVehicleCachedData

    from armagomen.battle_observer.shared.online import Online
    from armagomen.battle_observer.shared.interface import IBOOnline

    from armagomen.battle_observer.shared.battle.statistics_loader import StatisticsDataLoader
    from armagomen.battle_observer.shared.interface import IStatisticsDataLoader

    services = ((IBOOnline, Online),
                (IBOPlayersDamageController, PlayersDamageController),
                (IBOCurrentVehicleCachedData, CurrentVehicleCachedData),
                (IBOKeysListener, KeysListener),
                (IBOPiercingRandomizer, PiercingRandomizer),
                (IViewSettings, ViewSettingsAS),
                (IStatisticsDataLoader, StatisticsDataLoader))

    manager = _g_manager  # type: DependencyManager

    for interface, service in services:
        manager.addInstance(interface, service(), finalizer='fini')

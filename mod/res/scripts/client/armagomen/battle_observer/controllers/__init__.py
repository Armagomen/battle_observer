from ._skeletons.current_vehicle_dara import IBOCurrentVehicleCachedData
from ._skeletons.keys_listener import IBOKeysListener
from ._skeletons.players_damage import IBOPlayersDamageController
from ._skeletons.piercing_randomizer import IPiercingRandomizer

__all__ = ('IBOCurrentVehicleCachedData', 'IBOPlayersDamageController', 'IBOKeysListener')


def init_controllers():
    from helpers.dependency import _g_manager, DependencyManager

    from .current_vehicle_data import CurrentVehicleCachedData
    from .players_damage import PlayersDamageController
    from .keys_listener import KeysListener
    from .piercing_randomizer import PiercingRandomizer

    services = ((IBOPlayersDamageController, PlayersDamageController),
                (IBOCurrentVehicleCachedData, CurrentVehicleCachedData),
                (IBOKeysListener, KeysListener),
                (IPiercingRandomizer, PiercingRandomizer)
                )

    manager = _g_manager  # type: DependencyManager

    for interface, obj in services:
        manager.addInstance(interface, obj(), finalizer='fini')
        manager.getService(interface).init()

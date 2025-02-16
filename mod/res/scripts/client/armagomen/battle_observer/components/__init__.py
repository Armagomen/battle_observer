from importlib import import_module

from debug_utils import LOG_CURRENT_EXCEPTION
from realm import CURRENT_REALM

components = {}

replay_disable = (
    'auto_claim_clan_reward',
    'crew',
    'dispersion',
    'donate_messages',
    'excluded_maps',
    'friends',
    'hangar_efficiency',
    'premium_time',
    'save_shot_lite',
    'service_channel_filter',
    'vehicle_battle_boosters',
)

lesta_disable = (
    'auto_claim_clan_reward',
    'crew',
)


def loadComponents(is_replay):
    load = (
        'for_wg_fixes',
        'auto_claim_clan_reward',
        'camera_manager',
        'common',
        'crew',
        'dispersion',
        'donate_messages',
        'effects',
        'excluded_maps',
        'friends',
        'hangar_efficiency',
        'minimap_plugins',
        'premium_time',
        'replace_vehicle_info',
        'save_shot_lite',
        'service_channel_filter',
        'shot_result_plugin',
        'vehicle_battle_boosters',
    )

    for moduleName in load:
        if moduleName in replay_disable and is_replay or CURRENT_REALM == "RU" and moduleName in lesta_disable:
            continue
        try:
            components[moduleName] = import_module("{}.{}".format(__package__, moduleName))
        except Exception:
            LOG_CURRENT_EXCEPTION()

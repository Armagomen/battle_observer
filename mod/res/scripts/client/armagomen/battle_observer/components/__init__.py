from importlib import import_module

from armagomen._constants import IS_LESTA


def loadComponents(is_replay):
    components = {}
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
        'donate_messages',
    )

    for moduleName in load:
        if moduleName in replay_disable and is_replay or IS_LESTA and moduleName in lesta_disable:
            continue
        try:
            components[moduleName] = import_module("{}.{}".format(__package__, moduleName))
        except Exception:
            from debug_utils import LOG_CURRENT_EXCEPTION
            LOG_CURRENT_EXCEPTION()

    return components

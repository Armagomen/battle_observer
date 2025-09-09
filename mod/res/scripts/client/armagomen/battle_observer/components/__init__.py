from importlib import import_module

from armagomen.utils.logging import logError


def loadComponents(is_replay):
    components = {}

    load = [
        'for_wg_fixes',
        'common',
        'effects',
        'minimap_plugins',
        'replace_vehicle_info',
        'shot_result_plugin',
        "controllers"
    ]

    not_replay = [
        'camera_manager',
        'crew',
        'dispersion',
        'excluded_maps',
        'friends',
        'save_shot_lite',
        'service_channel_filter',
        'vehicle_battle_boosters',
        'auto_claim_clan_reward',
        'donate_messages'
    ]

    wg_only = ['auto_claim_clan_reward', 'donate_messages']

    if not is_replay:
        load.extend(not_replay)

    for moduleName in load:
        try:
            module = import_module("{}.{}".format(__package__, moduleName))
        except Exception as error:
            from debug_utils import LOG_CURRENT_EXCEPTION
            LOG_CURRENT_EXCEPTION()
            logError('{}: {}', moduleName, repr(error))
        else:
            components[moduleName] = module

    return components

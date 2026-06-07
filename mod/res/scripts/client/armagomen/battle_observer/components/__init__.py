from importlib import import_module

from armagomen import IALogger
from helpers import dependency


def loadComponents(is_replay):
    logger = dependency.instance(IALogger)
    components = {}

    load = [
        'for_wg_fixes',
        'common',
        'effects',
        'minimap_plugins',
        'replace_vehicle_info',
        'shot_result_plugin'
    ]

    not_replay = [
        'camera_manager',
        'crew',
        'dispersion',
        'excluded_maps',
        'friends',
        'service_channel_filter',
        'vehicle_battle_boosters',
        'auto_claim_clan_reward',
        'system_messages'
    ]

    if not is_replay:
        load.extend(not_replay)

    logger.logInfo("Loading components: {}", load)

    for moduleName in load:
        try:
            module = import_module("{}.{}".format(__package__, moduleName))
        except Exception as error:
            from debug_utils import LOG_CURRENT_EXCEPTION
            LOG_CURRENT_EXCEPTION()
            logger.logError('{}: {}', moduleName, str(error))
        else:
            components[moduleName] = module

    return components

def loadComponents(is_replay):
    components = {}

    load = {
        'for_wg_fixes',
        'common',
        'effects',
        'minimap_plugins',
        'replace_vehicle_info',
        'shot_result_plugin'
    }

    not_replay = {
        'camera_manager',
        'crew',
        'dispersion',
        'excluded_maps',
        'friends',
        'service_channel_filter',
        'vehicle_battle_boosters',
        'auto_claim_clan_reward',
        'system_messages'
    }

    if not is_replay:
        load.update(not_replay)

    from armagomen.utils.common import IS_COMMON_TEST
    if IS_COMMON_TEST:
        load.discard('system_messages')
        load.discard('auto_claim_clan_reward')

    from helpers import dependency
    from armagomen._logger import IALogger
    logger = dependency.instance(IALogger)
    logger.logInfo("Loading components: {}", load)

    from importlib import import_module
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

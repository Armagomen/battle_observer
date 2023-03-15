from debug_utils import LOG_CURRENT_EXCEPTION


def loadComponents():
    modules = (
        'camera',
        'common',
        'crew',
        'dispersion',
        'donate_messages',
        'effects',
        'for_wg_fixes',
        'friends',
        'minimap_plugins',
        'postmortem',
        'premium_time',
        'replace_vehicle_info',
        'save_shot_lite',
        'service_channel_filter',
        'shot_result_plugin',
        'tank_carousel',
        'vehicle_battle_boosters',
        'wg_logs_fixes',
    )

    for moduleName in modules:
        try:
            __import__("{}.{}".format(__package__, moduleName))
        except Exception:
            LOG_CURRENT_EXCEPTION()

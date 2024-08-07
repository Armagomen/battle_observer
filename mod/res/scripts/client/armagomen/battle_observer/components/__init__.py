from importlib import import_module

from debug_utils import LOG_CURRENT_EXCEPTION

_modules = {}


def loadComponents():
    load = (
        'auto_claim_clan_reward',
        'camera',
        'common',
        'crew',
        'dispersion',
        'donate_messages',
        'effects',
        'excluded_maps',
        'for_wg_fixes',
        'friends',
        'hangar_efficiency',
        'minimap_plugins',
        'postmortem',
        'premium_time',
        'replace_vehicle_info',
        'save_shot_lite',
        'service_channel_filter',
        'shot_result_plugin',
        'vehicle_battle_boosters',
        'wg_logs_fixes',
    )
    for moduleName in load:
        try:
            _modules[moduleName] = import_module("{}.{}".format(__package__, moduleName))
        except Exception:
            LOG_CURRENT_EXCEPTION()

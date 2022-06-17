from armagomen.utils.common import logError, closeClient
from debug_utils import LOG_CURRENT_EXCEPTION


class ComponentsLoader(object):

    def __init__(self):
        self.modules = {
            'common': None,
            'badges': None,
            'camera': None,
            'dispersion': None,
            'donate_messages': None,
            'effects': None,
            'friends': None,
            'minimap_plugins': None,
            'postmortem': None,
            'premium_time': None,
            'save_shoot_lite': None,
            'service_channel_filter': None,
            'shot_result_plugin': None,
            'tank_carousel': None,
            'wg_logs_fixes': None,
            'vehicle_battle_boosters': None,
            'crew': None,
            'statistics.statistic_data_loader': None,
            'for_tests': None
        }

    def start(self):
        for moduleName in self.modules:
            try:
                self.modules[moduleName] = __import__("{}.{}".format(__package__, moduleName))
            except ImportError as error:
                LOG_CURRENT_EXCEPTION()
                logError(error.message)
                closeClient()

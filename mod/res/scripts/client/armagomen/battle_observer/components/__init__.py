from debug_utils import LOG_CURRENT_EXCEPTION, CRITICAL_ERROR


class ComponentsLoader(object):

    def __init__(self):
        self.modules = {
            'badges': None,
            'camera': None,
            'common': None,
            'crew': None,
            'dispersion': None,
            'donate_messages': None,
            'effects': None,
            'for_wg_fixes': None,
            'friends': None,
            'minimap_plugins': None,
            'postmortem': None,
            'premium_time': None,
            'save_shoot_lite': None,
            'service_channel_filter': None,
            'shot_result_plugin': None,
            'tank_carousel': None,
            'vehicle_battle_boosters': None,
            'wg_logs_fixes': None,
        }
        self.start()

    def start(self):
        for moduleName in self.modules:
            try:
                self.modules[moduleName] = __import__("{}.{}".format(__package__, moduleName))
            except ImportError as error:
                LOG_CURRENT_EXCEPTION()
                CRITICAL_ERROR(error.message)

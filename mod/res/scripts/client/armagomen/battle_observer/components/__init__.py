import sys

from armagomen.utils.common import logWarning
from debug_utils import LOG_CURRENT_EXCEPTION


class ComponentsLoader(object):

    def __init__(self):
        self.modules = {
            'camera': None,
            'postmortem': None,
            'badges': None,
            'friends': None,
            'save_shoot_lite': None,
            'dispersion': None,
            'effects': None,
            'minimap_plugins': None,
            'wg_logs_fixes': None,
            'service_channel_filter': None,
            'tank_carousel': None,
            'shot_result_plugin': None,
            'hide_server': None,
            'premium_time': None
        }

    def start(self):
        for moduleName in self.modules:
            path = "{}.{}".format(__package__, moduleName)
            if path in sys.modules or self.modules[moduleName] is not None:
                logWarning("{} module already loaded".format(path))
            else:
                try:
                    self.modules[moduleName] = __import__(path)
                except ImportError:
                    LOG_CURRENT_EXCEPTION()

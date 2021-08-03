import sys

from armagomen.utils.common import logWarning
from debug_utils import LOG_CURRENT_EXCEPTION


class ComponentsLoader(object):

    def __init__(self):
        self.modules = {
            'badges': None,
            'camera': None,
            'dispersion': None,
            'donate_messages': None,
            'effects': None,
            'friends': None,
            'hide_server': None,
            'minimap_plugins': None,
            'postmortem': None,
            'premium_time': None,
            'played_together': None,
            'save_shoot_lite': None,
            'service_channel_filter': None,
            'shot_result_plugin': None,
            'tank_carousel': None,
            'wg_logs_fixes': None,
            'tmen_xp': None
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

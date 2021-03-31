import sys

from armagomen.utils.common import logWarning
from debug_utils import LOG_CURRENT_EXCEPTION


class ComponentsLoader(object):

    def __init__(self):
        self.modules = (
            'camera',
            'postmortem',
            'badges',
            'friends',
            'save_shoot_lite',
            'dispersion',
            'effects',
            'minimap_plugins',
            'wg_logs_fixes',
            'service_channel_filter',
            'tank_carousel',
            'shot_result_plugin'
        )

    def start(self):
        for modulePath in self.modules:
            self.loadModule("{}.{}".format(__package__, modulePath))

    @staticmethod
    def loadModule(modulePath):
        if modulePath in sys.modules:
            logWarning("{} module already loaded".format(modulePath))
            return
        try:
            __import__(modulePath)
        except ImportError:
            LOG_CURRENT_EXCEPTION()

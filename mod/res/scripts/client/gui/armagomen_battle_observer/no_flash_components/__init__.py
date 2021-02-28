import sys

from debug_utils import LOG_CURRENT_EXCEPTION
from ..core.utils.common import logWarning


class Loader(object):
    MOD_PATH = "gui.armagomen_battle_observer.no_flash_components.{}"

    def __init__(self):
        self.modules = (
            'camera', 'badges', 'friends', 'save_shoot_lite', 'dispersion_circle', 'effects', 'minimap_plugins',
            'wg_logs_fixes', 'service_channel_filter', 'tank_carousel'
        )

    def start(self):
        for modulePath in self.modules:
            self.loadModule(self.MOD_PATH.format(modulePath))

    @staticmethod
    def loadModule(modulePath):
        if modulePath in sys.modules:
            logWarning("{} module already loaded".format(modulePath))
            return
        try:
            __import__(modulePath)
        except ImportError:
            LOG_CURRENT_EXCEPTION()

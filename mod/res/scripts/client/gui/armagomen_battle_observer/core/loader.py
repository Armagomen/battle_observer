import sys

from debug_utils import LOG_CURRENT_EXCEPTION
from .bo_constants import MOD_PATH
from .bw_utils import logWarning


class Loader(object):

    def __init__(self):
        self.modules = (
            'core.battle_core',
            'core.analytics',
            'no_flash_comp.camera',
            'no_flash_comp.badges',
            'no_flash_comp.save_shoot_lite',
            'no_flash_comp.dispersion_circle',
            'no_flash_comp.effects',
            'no_flash_comp.minimap_plugins',
            'no_flash_comp.wg_logs_fixes',
            'hangar.service_channel_filter',
            'hangar.tank_carousel'
        )

    def start(self):
        for modulePath in self.modules:
            self.loadModule(MOD_PATH.format(modulePath))

    def loadModule(self, modulePath):
        if modulePath in sys.modules:
            logWarning("{} module already loaded".format(modulePath))
            return
        try:
            __import__(modulePath)
        except ImportError:
            LOG_CURRENT_EXCEPTION()


m_Loader = Loader()

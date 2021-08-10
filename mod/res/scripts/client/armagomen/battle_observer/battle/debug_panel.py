from collections import defaultdict

from account_helpers.settings_core.settings_constants import GRAPHICS
from armagomen.battle_observer.meta.battle.debug_panel_meta import DebugPanelMeta
from armagomen.constants import DEBUG_PANEL, GLOBAL, COLORS
from gui.battle_control.controllers import debug_ctrl
from gui.shared.personality import ServicesLocator

debug_ctrl._UPDATE_INTERVAL = 0.6


class DebugPanel(DebugPanelMeta, debug_ctrl.IDebugPanel):

    def __init__(self):
        super(DebugPanel, self).__init__()
        self.__colors = None
        self.data = defaultdict(lambda: GLOBAL.CONFIG_ERROR, PING=GLOBAL.ZERO, FPS=GLOBAL.ZERO)

    def _populate(self):
        super(DebugPanel, self)._populate()
        self.__colors = (self.settings[COLORS.NAME][DEBUG_PANEL.PING_COLOR],
                         self.settings[COLORS.NAME][DEBUG_PANEL.LAG_COLOR])
        self.data.update(fpsColor=self.settings[COLORS.NAME][DEBUG_PANEL.FPS_COLOR],
                         PingLagColor=self.settings[COLORS.NAME][DEBUG_PANEL.LAG_COLOR])

    @staticmethod
    def isVerticalSync():
        return bool(ServicesLocator.settingsCore.getSetting(GRAPHICS.VERTICAL_SYNC))

    @staticmethod
    def getRefreshRate():
        return ServicesLocator.settingsCore.getSetting(GRAPHICS.REFRESH_RATE)

    def updateDebugInfo(self, ping, fps, isLaggingNow, *args, **kwargs):
        lag = self.__colors[isLaggingNow]
        if self.data[DEBUG_PANEL.FPS] != fps or self.data[DEBUG_PANEL.PING] != ping or self.data[DEBUG_PANEL.LAG] != lag:
            self.data[DEBUG_PANEL.LAG] = lag
            self.data[DEBUG_PANEL.PING] = ping
            self.data[DEBUG_PANEL.FPS] = fps
            self.as_fpsPingS(self.settings[DEBUG_PANEL.TEXT][DEBUG_PANEL.TEMPLATE] % self.data, fps, ping)

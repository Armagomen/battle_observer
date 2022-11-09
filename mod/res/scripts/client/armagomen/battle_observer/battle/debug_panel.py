from collections import defaultdict

from account_helpers.settings_core.settings_constants import GRAPHICS
from armagomen.battle_observer.meta.battle.debug_panel_meta import DebugPanelMeta
from armagomen.constants import DEBUG_PANEL, GLOBAL, COLORS
from gui.battle_control.controllers.debug_ctrl import IDebugPanel
from gui.shared.personality import ServicesLocator


class DebugPanel(DebugPanelMeta, IDebugPanel):

    def __init__(self):
        super(DebugPanel, self).__init__()
        self._isLaggingNow = False
        self.data = defaultdict(lambda: GLOBAL.CONFIG_ERROR, PING=GLOBAL.ZERO, FPS=GLOBAL.ZERO)

    def _populate(self):
        super(DebugPanel, self)._populate()
        self.data.update(fpsColor=self.settings[COLORS.NAME][DEBUG_PANEL.FPS_COLOR],
                         pingColor=self.getPingColor(self._isLaggingNow))

    @staticmethod
    def isVerticalSync():
        return bool(ServicesLocator.settingsCore.getSetting(GRAPHICS.VERTICAL_SYNC))

    @staticmethod
    def getRefreshRate():
        return ServicesLocator.settingsCore.getSetting(GRAPHICS.REFRESH_RATE)

    def getPingColor(self, isLaggingNow):
        if isLaggingNow:
            return self.settings[COLORS.NAME][DEBUG_PANEL.LAG_COLOR]
        return self.settings[COLORS.NAME][DEBUG_PANEL.PING_COLOR]

    def updateDebugInfo(self, ping, fps, isLaggingNow, fpsReplay=-1):
        if self._isLaggingNow != isLaggingNow:
            self.data[DEBUG_PANEL.PING_COLOR] = self.getPingColor(isLaggingNow)
            self._isLaggingNow = isLaggingNow
        self.data[DEBUG_PANEL.PING] = ping
        self.data[DEBUG_PANEL.FPS] = fps
        self.as_fpsPingS(self.settings[DEBUG_PANEL.TEXT][DEBUG_PANEL.TEMPLATE] % self.data, fps, ping)

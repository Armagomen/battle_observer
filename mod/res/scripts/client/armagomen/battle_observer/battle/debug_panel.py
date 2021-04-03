from collections import defaultdict

from account_helpers.settings_core.settings_constants import GRAPHICS
from armagomen.battle_observer.core.bo_constants import DEBUG_PANEL, GLOBAL, COLORS
from armagomen.battle_observer.meta.battle.debug_panel_meta import DebugPanelMeta
from gui.battle_control.controllers import debug_ctrl
from gui.shared.personality import ServicesLocator

debug_ctrl._UPDATE_INTERVAL = 0.4


class DebugPanel(DebugPanelMeta, debug_ctrl.IDebugPanel):

    def __init__(self):
        super(DebugPanel, self).__init__()
        self.template = None
        self.__colors = None
        self.macroDict = None

    def _populate(self):
        super(DebugPanel, self)._populate()
        self.template = self.settings[DEBUG_PANEL.TEXT][DEBUG_PANEL.TEMPLATE]
        self.__colors = (self.settings[COLORS.NAME][DEBUG_PANEL.PING_COLOR],
                         self.settings[COLORS.NAME][DEBUG_PANEL.LAG_COLOR])
        self.macroDict = defaultdict(lambda: GLOBAL.CONFIG_ERROR,
                                     fpsColor=self.settings[COLORS.NAME][DEBUG_PANEL.FPS_COLOR],
                                     PingLagColor=self.settings[COLORS.NAME][DEBUG_PANEL.LAG_COLOR],
                                     PING=GLOBAL.ZERO, FPS=GLOBAL.ZERO)
        self.as_startUpdateS(self.settings,
                             ServicesLocator.settingsCore.getSetting(GRAPHICS.VERTICAL_SYNC),
                             ServicesLocator.settingsCore.getSetting(GRAPHICS.REFRESH_RATE))

    def updateDebugInfo(self, ping, fps, isLaggingNow, fpsReplay=-1):
        self.macroDict[DEBUG_PANEL.LAG] = self.__colors[isLaggingNow]
        self.macroDict[DEBUG_PANEL.PING] = ping
        self.macroDict[DEBUG_PANEL.FPS] = fps
        self.as_fpsPingS(self.template % self.macroDict, fps, ping)

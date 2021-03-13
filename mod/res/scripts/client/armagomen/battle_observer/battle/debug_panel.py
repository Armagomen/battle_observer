from collections import defaultdict

from account_helpers.settings_core.settings_constants import GRAPHICS
from armagomen.battle_observer.core import config
from armagomen.battle_observer.core.bo_constants import DEBUG_PANEL, GLOBAL, COLORS
from armagomen.battle_observer.meta.battle.debug_panel_meta import DebugPanelMeta
from gui.battle_control.controllers import debug_ctrl
from gui.shared.personality import ServicesLocator

debug_ctrl._UPDATE_INTERVAL = 0.4


class DebugPanel(DebugPanelMeta, debug_ctrl.IDebugPanel):

    def __init__(self):
        super(DebugPanel, self).__init__()
        self.template = config.debug_panel[DEBUG_PANEL.TEXT][DEBUG_PANEL.TEMPLATE]
        self.colors = (config.debug_panel[COLORS.NAME][DEBUG_PANEL.PING_COLOR],
                       config.debug_panel[COLORS.NAME][DEBUG_PANEL.LAG_COLOR])
        self.macroDict = defaultdict(lambda: GLOBAL.CONFIG_ERROR,
                                     fpsColor=config.debug_panel[COLORS.NAME][DEBUG_PANEL.FPS_COLOR],
                                     PingLagColor=config.debug_panel[COLORS.NAME][DEBUG_PANEL.LAG_COLOR],
                                     PING=GLOBAL.ZERO, FPS=GLOBAL.ZERO)

    def _populate(self):
        super(DebugPanel, self)._populate()
        self.as_startUpdateS(config.debug_panel,
                             ServicesLocator.settingsCore.getSetting(GRAPHICS.VERTICAL_SYNC),
                             ServicesLocator.settingsCore.getSetting(GRAPHICS.REFRESH_RATE))

    def updateDebugInfo(self, ping, fps, isLaggingNow, fpsReplay=-1):
        self.macroDict[DEBUG_PANEL.LAG] = self.colors[isLaggingNow]
        self.macroDict[DEBUG_PANEL.PING] = ping
        self.macroDict[DEBUG_PANEL.FPS] = fps
        self.as_fpsPingS(self.template % self.macroDict, fps, ping)

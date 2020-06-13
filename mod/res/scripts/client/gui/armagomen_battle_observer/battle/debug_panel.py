from account_helpers.settings_core.settings_constants import GRAPHICS
from gui.battle_control.controllers.debug_ctrl import IDebugPanel
from gui.shared.personality import ServicesLocator
from ..core.bo_constants import DEBUG_PANEL, GLOBAL, COLORS
from ..core.config import cfg
from ..core.core import SafeDict
from ..meta.battle.debug_panel_meta import DebugPanelMeta


class DebugPanel(DebugPanelMeta, IDebugPanel):

    def __init__(self):
        super(DebugPanel, self).__init__()
        self.template = cfg.debug_panel[DEBUG_PANEL.TEXT][DEBUG_PANEL.TEMPLATE]
        self.colors = (cfg.debug_panel[COLORS.NAME][DEBUG_PANEL.PING_COLOR],
                       cfg.debug_panel[COLORS.NAME][DEBUG_PANEL.LAG_COLOR])
        self.macroDict = SafeDict()
        self.macroDict[DEBUG_PANEL.FPS_COLOR] = cfg.debug_panel[COLORS.NAME][DEBUG_PANEL.FPS_COLOR]
        self.macroDict[DEBUG_PANEL.LAG] = cfg.debug_panel[COLORS.NAME][DEBUG_PANEL.LAG_COLOR]
        self.macroDict[DEBUG_PANEL.PING] = GLOBAL.ZERO
        self.macroDict[DEBUG_PANEL.FPS] = GLOBAL.ZERO

    def _populate(self):
        super(DebugPanel, self)._populate()
        self.as_startUpdateS(cfg.debug_panel,
                             ServicesLocator.settingsCore.getSetting(GRAPHICS.VERTICAL_SYNC),
                             ServicesLocator.settingsCore.getSetting(GRAPHICS.REFRESH_RATE))

    def updateDebugInfo(self, ping, fps, isLaggingNow, fpsReplay=-1):
        self.macroDict[DEBUG_PANEL.LAG] = self.colors[isLaggingNow]
        self.macroDict[DEBUG_PANEL.PING] = ping
        self.macroDict[DEBUG_PANEL.FPS] = fps
        self.as_fpsPingS(self.template % self.macroDict, fps, ping)

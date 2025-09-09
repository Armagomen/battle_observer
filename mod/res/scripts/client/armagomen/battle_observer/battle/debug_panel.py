from armagomen.battle_observer.meta.battle.debug_panel_meta import DebugPanelMeta
from armagomen.utils.common import toggleOverride
from gui.Scaleform.daapi.view.battle.shared.debug_panel import DebugPanel as _DP


class DebugPanel(DebugPanelMeta):

    def __init__(self):
        super(DebugPanel, self).__init__()

    def _populate(self):
        super(DebugPanel, self)._populate()
        toggleOverride(_DP, "updateDebugInfo", self.updateDebugInfo, True)

    def _dispose(self):
        toggleOverride(_DP, "updateDebugInfo", self.updateDebugInfo, False)
        super(DebugPanel, self)._dispose()

    def updateDebugInfo(self, base, debug, ping, fps, isLaggingNow, fpsReplay):
        self.as_updateS(ping, fps, isLaggingNow)

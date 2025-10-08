from armagomen.battle_observer.meta.battle.debug_panel_meta import DebugPanelMeta
from armagomen.utils.common import toggleOverride
from gui.Scaleform.daapi.view.battle.shared.debug_panel import DebugPanel


class _DebugPanel(DebugPanelMeta):

    def __init__(self):
        super(_DebugPanel, self).__init__()

    def _populate(self):
        super(_DebugPanel, self)._populate()
        toggleOverride(DebugPanel, "updateDebugInfo", self.updateDebugInfo, True)

    def _dispose(self):
        toggleOverride(DebugPanel, "updateDebugInfo", self.updateDebugInfo, False)
        super(_DebugPanel, self)._dispose()

    def updateDebugInfo(self, base, debug, ping, fps, isLaggingNow, fpsReplay):
        self.as_updateS(ping, fps, isLaggingNow)

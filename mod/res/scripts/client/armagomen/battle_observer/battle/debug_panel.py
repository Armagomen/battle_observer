from armagomen.battle_observer.meta.battle.debug_panel_meta import DebugPanelMeta
from gui.battle_control.controllers.debug_ctrl import IDebugPanel


class DebugPanel(DebugPanelMeta, IDebugPanel):

    def __init__(self):
        super(DebugPanel, self).__init__()

    def updateDebugInfo(self, ping, fps, isLaggingNow, fpsReplay):
        self.as_updateS(ping, fps, isLaggingNow)


class DebugPanelLesta(DebugPanelMeta):

    def __init__(self):
        super(DebugPanelLesta, self).__init__()

    def updateDebugInfo(self, ping, fps, isLaggingNow):
        self.as_updateS(ping, fps, isLaggingNow)

    def updateReplayDebugInfo(self, ping, fps, isLaggingNow, fpsReplay):
        self.as_updateS(ping, fps, isLaggingNow)

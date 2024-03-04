import BigWorld

from armagomen.utils.common import overrideMethod
from BattleReplay import g_replayCtrl
from gui.battle_control.controllers import debug_ctrl

debug_ctrl._UPDATE_INTERVAL = 0.3


@overrideMethod(debug_ctrl.DebugController, "setViewComponents")
def setViewComponents(base, controller, *args):
    controller._debugPanelUI = args


@overrideMethod(debug_ctrl.DebugController, "_update")
def updateDebug(base, controller):
    fps = BigWorld.getFPS()[1]
    if g_replayCtrl.isPlaying:
        fpsReplay = g_replayCtrl.fps
        ping = g_replayCtrl.ping
        isLaggingNow = g_replayCtrl.isLaggingNow
    else:
        fpsReplay = -1
        isLaggingNow = BigWorld.statLagDetected()
        ping = BigWorld.statPing()
        controller.statsCollector.update()
        if g_replayCtrl.isRecording:
            g_replayCtrl.setFpsPingLag(fps, ping, isLaggingNow)

    try:
        ping = int(ping)
        fps = int(fps)
    except (ValueError, OverflowError):
        fps = ping = 0

    if controller._debugPanelUI is not None:
        for control in controller._debugPanelUI:
            control.updateDebugInfo(ping, fps, isLaggingNow, fpsReplay=fpsReplay)

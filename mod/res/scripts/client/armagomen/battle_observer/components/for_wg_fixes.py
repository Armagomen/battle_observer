from BigWorld import getFPS, statLagDetected, statPing

from BattleReplay import g_replayCtrl as replayCtrl
from armagomen.utils.common import overrideMethod
from gui.battle_control.controllers import debug_ctrl

debug_ctrl._UPDATE_INTERVAL = 0.5


@overrideMethod(debug_ctrl.DebugController, "setViewComponents")
def setViewComponents(base, controller, *args):
    controller._debugPanelUI = args


@overrideMethod(debug_ctrl.DebugController, "_update")
def setViewComponents(base, controller):
    if replayCtrl.isPlaying and not replayCtrl.isBattleSimulation and replayCtrl.fps > 0 or replayCtrl.isServerSideReplay:
        fps = getFPS()[1]
        fpsReplay = int(replayCtrl.fps)
        ping = replayCtrl.ping
        isLaggingNow = replayCtrl.isLaggingNow
    else:
        fpsReplay = -1
        isLaggingNow = statLagDetected()
        ping = statPing()
        fps = getFPS()[1]
        controller.statsCollector.update()
        if replayCtrl.isRecording:
            replayCtrl.setFpsPingLag(fps, ping, isLaggingNow)
    try:
        ping = int(ping)
        fps = int(fps)
    except (ValueError, OverflowError):
        return

    if controller._debugPanelUI is not None:
        for control in controller._debugPanelUI:
            control.updateDebugInfo(ping, fps, isLaggingNow, fpsReplay=fpsReplay)

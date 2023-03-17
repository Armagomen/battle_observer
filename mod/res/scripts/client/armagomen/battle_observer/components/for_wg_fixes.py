import BigWorld

from BattleReplay import g_replayCtrl, isServerSideReplay
from DogTagComponent import DogTagComponent
from armagomen.utils.common import overrideMethod
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


@overrideMethod(DogTagComponent, "_isObserving")
def _isObserving(base, *args):
    if isServerSideReplay():
        return True
    else:
        vehicle = getattr(BigWorld.player(), "vehicle", None)
        if vehicle is not None:
            return not vehicle.isPlayerVehicle
    return False

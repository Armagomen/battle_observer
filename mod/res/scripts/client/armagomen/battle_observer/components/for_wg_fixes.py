import BigWorld

from armagomen._constants import DAMAGE_LOG, GLOBAL
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import overrideMethod
from BattleReplay import g_replayCtrl
from gui.battle_control.battle_constants import PERSONAL_EFFICIENCY_TYPE as _ETYPE
from gui.battle_control.controllers import debug_ctrl
from gui.Scaleform.daapi.view.battle.shared.damage_log_panel import _LogViewComponent, DamageLogPanel

debug_ctrl._UPDATE_INTERVAL = 0.4


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
        fpsReplay = int(fpsReplay)
    except (ValueError, OverflowError):
        fps = ping = fpsReplay = 0

    if controller._debugPanelUI is not None:
        for control in controller._debugPanelUI:
            control.updateDebugInfo(ping, fps, isLaggingNow, fpsReplay=fpsReplay)


class WG_Logs_Fix(object):
    BASE_WG_LOGS = (DamageLogPanel._addToTopLog, DamageLogPanel._updateTopLog,
                    DamageLogPanel._updateBottomLog, DamageLogPanel._addToBottomLog)

    def __init__(self):
        self.validated = {}
        overrideMethod(_LogViewComponent, "addToLog")(self.addToLog)

    def addToLog(self, base, component, event):
        if user_settings.wg_logs[GLOBAL.ENABLED]:
            return base(component, [e for e in event if not self.validated.get(e.getType(), False)])
        return base(component, event)

    def onModSettingsChanged(self, config, blockID):
        if blockID == DAMAGE_LOG.WG_LOGS_FIX:
            self.validated.update(self.validateSettings(config))
            DamageLogPanel._addToTopLog, DamageLogPanel._updateTopLog, \
                DamageLogPanel._updateBottomLog, DamageLogPanel._addToBottomLog = \
                reversed(self.BASE_WG_LOGS) if config[DAMAGE_LOG.WG_POS] else self.BASE_WG_LOGS

    @staticmethod
    def validateSettings(config):
        return {_ETYPE.RECEIVED_CRITICAL_HITS: config[DAMAGE_LOG.WG_CRITICS],
                _ETYPE.BLOCKED_DAMAGE: config[DAMAGE_LOG.WG_BLOCKED],
                _ETYPE.ASSIST_DAMAGE: config[DAMAGE_LOG.WG_ASSIST],
                _ETYPE.STUN: config[DAMAGE_LOG.WG_ASSIST]}


logs_fix = WG_Logs_Fix()

user_settings.onModSettingsChanged += logs_fix.onModSettingsChanged
logs_fix.onModSettingsChanged(user_settings.wg_logs, DAMAGE_LOG.WG_LOGS_FIX)


def fini():
    user_settings.onModSettingsChanged -= logs_fix.onModSettingsChanged

import BigWorld

from armagomen._constants import DAMAGE_LOG, GLOBAL
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import cancelOverride, overrideMethod
from BattleReplay import g_replayCtrl
from gui.battle_control.battle_constants import PERSONAL_EFFICIENCY_TYPE as _ETYPE
from gui.battle_control.controllers import debug_ctrl
from gui.Scaleform.daapi.view.battle.shared.damage_log_panel import _LogViewComponent, DamageLogPanel


class Debug_ctrl_fix(object):
    debug_ctrl._UPDATE_INTERVAL = 0.4

    @staticmethod
    @overrideMethod(debug_ctrl.DebugController)
    def debug_init(base, ctrl, *args):
        base(ctrl, *args)
        ctrl._debugPanelUI = []

    @staticmethod
    @overrideMethod(debug_ctrl.DebugController, "setViewComponents")
    def setViewComponents(base, controller, *args):
        controller._debugPanelUI = args

    @staticmethod
    @overrideMethod(debug_ctrl.DebugController, "clearViewComponents")
    def clearViewComponents(base, controller, *args):
        controller._debugPanelUI = []

    @staticmethod
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

        for ui in controller._debugPanelUI:
            ui.updateDebugInfo(ping, fps, isLaggingNow, fpsReplay=fpsReplay)


fix_debug = Debug_ctrl_fix()


class WG_Logs_Fix(object):
    BASE_WG_LOGS = (DamageLogPanel._addToTopLog, DamageLogPanel._updateTopLog,
                    DamageLogPanel._updateBottomLog, DamageLogPanel._addToBottomLog)

    def __init__(self):
        self.validated = {}

    def addToLog(self, base, component, event):
        return base(component, [e for e in event if not self.validated.get(e.getType(), False)])

    def onModSettingsChanged(self, config, blockID):
        if blockID == DAMAGE_LOG.WG_LOGS_FIX:
            if config[GLOBAL.ENABLED]:
                overrideMethod(_LogViewComponent, "addToLog")(self.addToLog)
                self.validated.update(self.validateSettings(config))
            else:
                cancelOverride(_LogViewComponent, "addToLog", "addToLog")
            self.updatePositions(config)

    def updatePositions(self, config):
        DamageLogPanel._addToTopLog, DamageLogPanel._updateTopLog, \
            DamageLogPanel._updateBottomLog, DamageLogPanel._addToBottomLog = \
            reversed(self.BASE_WG_LOGS) if config[GLOBAL.ENABLED] and config[DAMAGE_LOG.WG_POS] else self.BASE_WG_LOGS

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

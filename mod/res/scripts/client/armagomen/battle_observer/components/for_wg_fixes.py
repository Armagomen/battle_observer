import BigWorld

from armagomen._constants import DAMAGE_LOG, GLOBAL
from armagomen.battle_observer.components.controllers import squad_controller
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import overrideMethod, xvmInstalled
from BattleReplay import g_replayCtrl
from constants import ATTACK_REASONS, SPECIAL_VEHICLE_HEALTH
from gui.battle_control.battle_constants import PERSONAL_EFFICIENCY_TYPE as _ETYPE
from gui.battle_control.controllers import debug_ctrl
from gui.Scaleform.daapi.view.battle.shared.damage_log_panel import _LogViewComponent, DamageLogPanel
from gui.Scaleform.daapi.view.battle.shared.markers2d.vehicle_plugins import VehicleMarkerPlugin

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


BASE_WG_LOGS = (DamageLogPanel._addToTopLog, DamageLogPanel._updateTopLog,
                DamageLogPanel._updateBottomLog, DamageLogPanel._addToBottomLog)

validated = {}


@overrideMethod(_LogViewComponent, "addToLog")
def addToLog(base, component, event):
    if user_settings.wg_logs[GLOBAL.ENABLED]:
        return base(component, [e for e in event if not validated.get(e.getType(), False)])
    return base(component, event)


def onModSettingsChanged(config, blockID):
    if blockID == DAMAGE_LOG.WG_LOGS_FIX:
        validated.update(validateSettings(config))
        DamageLogPanel._addToTopLog, DamageLogPanel._updateTopLog, \
            DamageLogPanel._updateBottomLog, DamageLogPanel._addToBottomLog = \
            reversed(BASE_WG_LOGS) if config[DAMAGE_LOG.WG_POS] else BASE_WG_LOGS


def validateSettings(config):
    return {_ETYPE.RECEIVED_CRITICAL_HITS: config[DAMAGE_LOG.WG_CRITICS],
            _ETYPE.BLOCKED_DAMAGE: config[DAMAGE_LOG.WG_BLOCKED],
            _ETYPE.ASSIST_DAMAGE: config[DAMAGE_LOG.WG_ASSIST],
            _ETYPE.STUN: config[DAMAGE_LOG.WG_ASSIST]}


user_settings.onModSettingsChanged += onModSettingsChanged
onModSettingsChanged(user_settings.wg_logs, DAMAGE_LOG.WG_LOGS_FIX)


# squad damage fix
@overrideMethod(VehicleMarkerPlugin, "_updateVehicleHealth")
def _updateVehicleHealth(base, plugin, vehicleID, handle, newHealth, aInfo, attackReasonID):
    if xvmInstalled:
        return base(plugin, vehicleID, handle, newHealth, aInfo, attackReasonID)
    if newHealth < 0 and not SPECIAL_VEHICLE_HEALTH.IS_AMMO_BAY_DESTROYED(newHealth):
        newHealth = 0
    if g_replayCtrl.isPlaying and g_replayCtrl.isTimeWarpInProgress:
        plugin._invokeMarker(handle, 'setHealth', newHealth)
    else:
        members = squad_controller.members
        yellow = False if aInfo is None or not members else aInfo.vehicleID in members
        plugin._invokeMarker(handle, 'updateHealth', newHealth, yellow, ATTACK_REASONS[attackReasonID])


def fini():
    global onModSettingsChanged
    user_settings.onModSettingsChanged -= onModSettingsChanged

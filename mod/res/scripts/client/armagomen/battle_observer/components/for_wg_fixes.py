import BigWorld

from BattleReplay import g_replayCtrl, isServerSideReplay
from DogTagComponent import DogTagComponent
from armagomen.utils.common import overrideMethod, callback
from avatar_components.avatar_chat_key_handling import AvatarChatKeyHandling, _logger
from chat_commands_consts import _PERSONAL_MESSAGE_MUTE_DURATION
from gui.Scaleform.daapi.view.battle.epic.page import EpicBattlePage
from gui.Scaleform.daapi.view.battle.shared.markers2d.vehicle_plugins import VehicleMarkerPlugin, MarkerState
from gui.Scaleform.genConsts.BATTLE_MARKER_STATES import BATTLE_MARKER_STATES
from gui.battle_control.controllers import debug_ctrl
from gui.sounds.epic_sound_constants import EPIC_SOUND

debug_ctrl._UPDATE_INTERVAL = 0.5


@overrideMethod(debug_ctrl.DebugController, "setViewComponents")
def setViewComponents(base, controller, *args):
    controller._debugPanelUI = args


@overrideMethod(debug_ctrl.DebugController, "_update")
def updateDebug(base, controller):
    if g_replayCtrl.isPlaying and not g_replayCtrl.isBattleSimulation and g_replayCtrl.fps > 0 or isServerSideReplay():
        fps = BigWorld.getFPS()[1]
        fpsReplay = int(g_replayCtrl.fps)
        ping = g_replayCtrl.ping
        isLaggingNow = g_replayCtrl.isLaggingNow
    else:
        fpsReplay = -1
        isLaggingNow = BigWorld.statLagDetected()
        ping = BigWorld.statPing()
        fps = BigWorld.getFPS()[1]
        controller.statsCollector.update()
        if g_replayCtrl.isRecording:
            g_replayCtrl.setFpsPingLag(fps, ping, isLaggingNow)
    try:
        ping = int(ping)
        fps = int(fps)
    except (ValueError, OverflowError):
        return

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


# fix AttributeError: 'NoneType' object has no attribute 'translation' in AvatarChatKeyHandling
@overrideMethod(AvatarChatKeyHandling, "__playSoundNotificationOnCommandReceived")
def playSoundNotificationOnCommandReceived(base, self, cmd, markerType, useSoundNotification=False,
                                           notificationName=None, enableVoice=True):
    if cmd.isEpicGlobalMessage():
        if self.soundNotifications:
            self.soundNotifications.play(EPIC_SOUND.BF_EB_GLOBAL_MESSAGE)
    else:
        matrixProvider = self._AvatarChatKeyHandling__getMatrixProvider(cmd, markerType).matrixProvider
        if matrixProvider is None:
            return
        if notificationName is None:
            notificationName = cmd.getSoundEventName(useSoundNotification)
        if enableVoice and cmd.isReceiver():
            if not self._AvatarChatKeyHandling__arePrivateVoiceOverBlocked:
                self._AvatarChatKeyHandling__arePrivateVoiceOverBlocked = True
                self._AvatarChatKeyHandling__callbackDelayer.delayCallback(
                    _PERSONAL_MESSAGE_MUTE_DURATION, self._AvatarChatKeyHandling__onPrivateVoiceOverBlockedReset)
            else:
                enableVoice = False
                _logger.info('Voice was blocked for the receiver of a private message due to flood prevention system!')
        sentByPlayer = self._AvatarChatKeyHandling__getVehicleIDForCmdSender(cmd) == self.playerVehicleID
        self._AvatarChatKeyHandling__playSoundNotification(notificationName, matrixProvider.translation, enableVoice,
                                                           sentByPlayer)


# ValueError: list.remove(x): x not in list in VehicleMarkerPlugin
@overrideMethod(VehicleMarkerPlugin, "_updateStatusMarkerState")
def _updateStatusMarkerState(base, self, vehicleID, isShown, handle, statusID, duration, animated, isSourceVehicle,
                             blinkAnim=True):
    activeStatuses = self._markersStates[vehicleID]
    marker = MarkerState(statusID, isSourceVehicle)
    isStatusActive = self._VehicleMarkerPlugin__isStatusActive(statusID, activeStatuses)
    if isShown and not isStatusActive:
        activeStatuses.append(marker)
        self._markersStates[vehicleID] = activeStatuses
    elif not isShown and isStatusActive and marker in self._markersStates[vehicleID]:
        self._markersStates[vehicleID].remove(marker)
    if self._markersStates[vehicleID]:
        activeStatuses = sorted(self._markersStates[vehicleID], key=self._getMarkerStatusPriority, reverse=False)
        self._markersStates[vehicleID] = activeStatuses
        currentlyActiveStatusID = self._markersStates[vehicleID][0].statusID
        currentlyActiveIsSourceVehicle = self._markersStates[vehicleID][0].isSourceVehicle
    else:
        currentlyActiveStatusID = -1
        currentlyActiveIsSourceVehicle = False
    currentActiveMarker = MarkerState(currentlyActiveStatusID, currentlyActiveIsSourceVehicle)
    if statusID in (BATTLE_MARKER_STATES.STUN_STATE, BATTLE_MARKER_STATES.HEALING_STATE):
        isSourceVehicle = True
    elif statusID == BATTLE_MARKER_STATES.DEBUFF_STATE:
        isSourceVehicle = False
    if isShown:
        self._invokeMarker(handle, 'showStatusMarker', statusID,
                           self._getMarkerStatusPriority(MarkerState(statusID, isSourceVehicle)), isSourceVehicle,
                           duration, currentlyActiveStatusID, self._getMarkerStatusPriority(currentActiveMarker),
                           animated, blinkAnim)
    elif self._VehicleMarkerPlugin__canUpdateStatus(handle):
        self._invokeMarker(handle, 'hideStatusMarker', statusID, currentlyActiveStatusID, animated,
                           currentlyActiveIsSourceVehicle)


@overrideMethod(EpicBattlePage, "__onRespawnVisibility")
def _onRespawnVisibility(base, *args, **kwargs):
    callback(1.0, base, *args, **kwargs)

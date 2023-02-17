# coding=utf-8
from PlayerEvents import g_playerEvents
from armagomen.battle_observer.meta.battle.sixth_sense_meta import SixthSenseMeta
from armagomen.constants import SIXTH_SENSE
from armagomen.utils.timers import SixthSenseTimer
from gui.battle_control.battle_constants import VEHICLE_VIEW_STATE
from helpers import getClientLanguage

_STATES_TO_HIDE = {VEHICLE_VIEW_STATE.SWITCHING, VEHICLE_VIEW_STATE.RESPAWNING,
                   VEHICLE_VIEW_STATE.DESTROYED, VEHICLE_VIEW_STATE.CREW_DEACTIVATED}

language = getClientLanguage()
if language == "uk":
    DEFAULT_MESSAGE = "Виявили: {} сек."
elif language in ("ru", "be"):
    DEFAULT_MESSAGE = "Обнаружили: {} сек."
else:
    DEFAULT_MESSAGE = "Detected: {} sec."

RADIO = 'improvedRadioCommunication'
RADIO_DURATION = 2


class SixthSense(SixthSenseMeta, SixthSenseTimer):

    def __init__(self):
        super(SixthSense, self).__init__()
        self.radio_installed = False

    def _populate(self):
        super(SixthSense, self)._populate()
        if self.settings[SIXTH_SENSE.PLAY_TICK_SOUND]:
            self.setSound(self._arenaVisitor.type.getCountdownTimerSound())
        g_playerEvents.onRoundFinished += self._onRoundFinished
        ctrl = self.sessionProvider.shared.vehicleState
        if ctrl is not None:
            ctrl.onVehicleStateUpdated += self._onVehicleStateUpdated
        optional_devices = self.sessionProvider.shared.optionalDevices
        if optional_devices is not None:
            optional_devices.onDescriptorDevicesChanged += self.onDevicesChanged

    def _dispose(self):
        self.destroyTimer()
        g_playerEvents.onRoundFinished -= self._onRoundFinished
        ctrl = self.sessionProvider.shared.vehicleState
        if ctrl is not None:
            ctrl.onVehicleStateUpdated -= self._onVehicleStateUpdated
        optional_devices = self.sessionProvider.shared.optionalDevices
        if optional_devices is not None:
            optional_devices.onDescriptorDevicesChanged -= self.onDevicesChanged
        super(SixthSense, self)._dispose()

    def onDevicesChanged(self, devices):
        self.radio_installed = RADIO in (device.groupName for device in devices if device is not None)

    def _onVehicleStateUpdated(self, state, value):
        if state == VEHICLE_VIEW_STATE.OBSERVED_BY_ENEMY and value:
            time = self.settings[SIXTH_SENSE.TIME]
            if self.radio_installed:
                time -= RADIO_DURATION
            self.show(time)
        elif state in _STATES_TO_HIDE:
            self.hide()

    def _onRoundFinished(self, *args):
        self.hide()

    def handleTimer(self, timeLeft):
        self.as_updateTimerS(DEFAULT_MESSAGE.format(timeLeft))

    def show(self, seconds):
        super(SixthSense, self).show(seconds)
        self.as_showS()

    def hide(self):
        super(SixthSense, self).hide()
        self.as_hideS()

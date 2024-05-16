# coding=utf-8
from random import choice

from armagomen._constants import GLOBAL, SIXTH_SENSE
from armagomen.battle_observer.meta.battle.sixth_sense_meta import SixthSenseMeta
from armagomen.utils.timers import SixthSenseTimer
from gui.battle_control.battle_constants import VEHICLE_VIEW_STATE
from helpers import getClientLanguage
from PlayerEvents import g_playerEvents

_STATES_TO_HIDE = {VEHICLE_VIEW_STATE.SWITCHING, VEHICLE_VIEW_STATE.RESPAWNING,
                   VEHICLE_VIEW_STATE.DESTROYED, VEHICLE_VIEW_STATE.CREW_DEACTIVATED}

if getClientLanguage() == "uk":
    MESSAGES = ("Засікли: <font color='#daff8f'>{}</font> сек.",
                "Викрито: <font color='#daff8f'>{}</font> сек.",
                "Тікай: <font color='#daff8f'>{}</font> сек.",
                "Ховайся: <font color='#daff8f'>{}</font> сек.",
                "Роби маневр: <font color='#daff8f'>{}</font> сек.",
                "Ой, світло дали: <font color='#daff8f'>{}</font> сек.")
else:
    MESSAGES = ("Detected: <font color='#daff8f'>{}</font> sec.",
                "Hide: <font color='#daff8f'>{}</font> sec.",
                "Run: <font color='#daff8f'>{}</font> sec.")

RADIO = 'improvedRadioCommunication'
RADIO_DURATION = 2


class SixthSense(SixthSenseMeta, SixthSenseTimer):

    def __init__(self):
        super(SixthSense, self).__init__()
        self.radio_installed = False
        self.__visible = False
        self.__message = None

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

    def getNewRandomMessage(self):
        message = " "
        if self.settings[SIXTH_SENSE.ENABLED_RANDOM_MESSAGES]:
            message = choice(MESSAGES)
            if message == self.__message:
                message = self.getNewRandomMessage()
        return message

    def _onVehicleStateUpdated(self, state, value):
        if state == VEHICLE_VIEW_STATE.OBSERVED_BY_ENEMY and value:
            time = self.settings[SIXTH_SENSE.TIME]
            if self.radio_installed:
                time -= RADIO_DURATION
            self.__message = self.getNewRandomMessage()
            self.show(time)
        elif state in _STATES_TO_HIDE:
            self.hide()

    def _onRoundFinished(self, *args):
        self.hide()

    def handleTimer(self, timeLeft):
        self.as_updateTimerS(self.__message.format(timeLeft))
        if timeLeft == GLOBAL.ZERO:
            self.hide()

    def show(self, seconds):
        if not self.__visible:
            self.as_showS()
            self.__visible = True
        self.timeTicking(seconds)

    def hide(self):
        if self.__visible:
            self.cancelCallback()
            self.as_hideS()
            self.__visible = False

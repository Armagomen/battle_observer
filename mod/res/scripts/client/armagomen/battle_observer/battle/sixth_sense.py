# coding=utf-8
from random import choice

from armagomen._constants import SIXTH_SENSE
from armagomen.battle_observer.meta.battle.sixth_sense_meta import SixthSenseMeta
from gui.battle_control.battle_constants import VEHICLE_VIEW_STATE
from helpers import getClientLanguage
from PlayerEvents import g_playerEvents
from SoundGroups import g_instance

_STATES_TO_HIDE = {VEHICLE_VIEW_STATE.SWITCHING, VEHICLE_VIEW_STATE.RESPAWNING,
                   VEHICLE_VIEW_STATE.DESTROYED, VEHICLE_VIEW_STATE.CREW_DEACTIVATED}

if getClientLanguage().lower() in ("uk", "be"):
    MESSAGES = ("Засікли: <font color='#daff8f'>{}</font> сек.",
                "Викрито: <font color='#daff8f'>{}</font> сек.",
                "Тікай: <font color='#daff8f'>{}</font> сек.",
                "Ховайся: <font color='#daff8f'>{}</font> сек.",
                "Роби маневр: <font color='#daff8f'>{}</font> сек.")
else:
    MESSAGES = ("Detected: <font color='#daff8f'>{}</font> sec.",
                "Hide: <font color='#daff8f'>{}</font> sec.",
                "Run: <font color='#daff8f'>{}</font> sec.")

RADIO = 'improvedRadioCommunication'
RADIO_DURATION = 1.5


class SixthSense(SixthSenseMeta):

    def __init__(self):
        super(SixthSense, self).__init__()
        self.radio_installed = False
        self.__sounds = dict()
        self.__visible = False
        self.__message = None
        self.__radar = None
        self.__soundID = None
        try:
            from constants import DIRECT_DETECTION_TYPE
            self.__radar = DIRECT_DETECTION_TYPE.STEALTH_RADAR
        except:
            pass

    def callWWISE(self, wwiseEventName):
        if wwiseEventName in self.__sounds:
            sound = self.__sounds[wwiseEventName]
        else:
            sound = g_instance.getSound2D(wwiseEventName)
            self.__sounds[wwiseEventName] = sound
        if sound is not None:
            if sound.isPlaying:
                sound.stop()
            sound.play()

    def _populate(self):
        super(SixthSense, self)._populate()
        if self.settings[SIXTH_SENSE.PLAY_TICK_SOUND]:
            self.__soundID = self._arenaVisitor.type.getCountdownTimerSound()
        g_playerEvents.onRoundFinished += self._onRoundFinished
        ctrl = self.sessionProvider.shared.vehicleState
        if ctrl is not None:
            ctrl.onVehicleStateUpdated += self._onVehicleStateUpdated
        optional_devices = self.sessionProvider.shared.optionalDevices
        if optional_devices is not None:
            optional_devices.onDescriptorDevicesChanged += self.onDevicesChanged

    def _dispose(self):
        if self.sessionProvider.isReplayPlaying and self._getPyReloading():
            self.hide()
        for sound in self.__sounds.values():
            sound.stop()
        self.__sounds.clear()
        self.__soundID = None
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
        message = choice(MESSAGES)
        if message == self.__message:
            message = self.getNewRandomMessage()
        return message

    def _onVehicleStateUpdated(self, state, value):
        if state == VEHICLE_VIEW_STATE.OBSERVED_BY_ENEMY:
            if value.get('isObserved', False):
                if self.isComp7Battle():
                    if value.get("detectionType", 0) == self.__radar:
                        time = 2
                    else:
                        time = 4
                else:
                    time = self.settings[SIXTH_SENSE.TIME]
                    if self.radio_installed:
                        time -= RADIO_DURATION
                self.__message = self.getNewRandomMessage()
                self.as_showS(time)
            else:
                self.as_hideS()
        elif state in _STATES_TO_HIDE:
            self.as_hideS()

    def _onRoundFinished(self, *args):
        self.as_hideS()

    def getTimerString(self, timeLeft):
        return self.__message.format(timeLeft)

    def playSound(self):
        if self.__soundID is not None:
            self.callWWISE(self.__soundID)


class SixthSenseLesta(SixthSense):

    def _onVehicleStateUpdated(self, state, value):
        if state == VEHICLE_VIEW_STATE.OBSERVED_BY_ENEMY:
            if value:
                self.as_showS(0)
            else:
                self.as_hideS()
        elif state in _STATES_TO_HIDE:
            self.as_hideS()

from random import choice

import ResMgr

from armagomen._constants import SIXTH_SENSE
from armagomen.battle_observer.meta.battle.sixth_sense_meta import SixthSenseMeta
from armagomen.utils.logging import logError, logInfo
from constants import DIRECT_DETECTION_TYPE
from gui.battle_control import avatar_getter
from gui.battle_control.battle_constants import VEHICLE_VIEW_STATE
from items.components.supply_slot_categories import SupplySlotFactorLevels
from PlayerEvents import g_playerEvents
from SoundGroups import g_instance

_STATES_TO_HIDE = {VEHICLE_VIEW_STATE.SWITCHING, VEHICLE_VIEW_STATE.RESPAWNING,
                   VEHICLE_VIEW_STATE.DESTROYED, VEHICLE_VIEW_STATE.CREW_DEACTIVATED}

BASE_TIME = 10.0
COMP7_TIME_REDUCTION = 6.0
RADIO = 'radioCommunication'
RADIO_DURATION = 1.5
RADIO_DURATION_BONUS = 2.0


class SixthSense(SixthSenseMeta):

    def __init__(self):
        super(SixthSense, self).__init__()
        self.__sounds = dict()
        self.__soundID = None
        self.__time = BASE_TIME
        self.__isComp7Battle = False

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
        self.__isComp7Battle = self.isComp7Battle()
        if self.__isComp7Battle:
            self.updateTime(diff=COMP7_TIME_REDUCTION)
        if self.settings[SIXTH_SENSE.PLAY_TICK_SOUND]:
            self.__soundID = self._arenaVisitor.type.getCountdownTimerSound()
        g_playerEvents.onRoundFinished += self._onRoundFinished
        ctrl = self.sessionProvider.shared.vehicleState
        if ctrl is not None:
            ctrl.onVehicleStateUpdated += self._onVehicleStateUpdated
        optional_devices = self.sessionProvider.shared.optionalDevices
        if optional_devices is not None and not self.__isComp7Battle:
            optional_devices.onDescriptorDevicesChanged += self.onDescriptorDevicesChanged

    def _dispose(self):
        if self.sessionProvider.isReplayPlaying and self._getPyReloading():
            self.as_hideS()
        for sound in self.__sounds.values():
            sound.stop()
        self.__sounds.clear()
        self.__soundID = None
        g_playerEvents.onRoundFinished -= self._onRoundFinished
        ctrl = self.sessionProvider.shared.vehicleState
        if ctrl is not None:
            ctrl.onVehicleStateUpdated -= self._onVehicleStateUpdated
        optional_devices = self.sessionProvider.shared.optionalDevices
        if optional_devices is not None and not self.__isComp7Battle:
            optional_devices.onDescriptorDevicesChanged -= self.onDescriptorDevicesChanged
        super(SixthSense, self)._dispose()

    def onDescriptorDevicesChanged(self, devices):
        diff = 0.0
        for device in devices:
            if device and RADIO in device.tags:
                descr = avatar_getter.getPlayerVehicle().typeDescriptor
                improved = device.defineActiveLevel(descr) == SupplySlotFactorLevels.IMPROVED
                diff = RADIO_DURATION_BONUS if improved else RADIO_DURATION
                break
        self.updateTime(diff=diff)

    DETECTION_TYPE_TO_TIME = {DIRECT_DETECTION_TYPE.STEALTH_RADAR: 2.0, DIRECT_DETECTION_TYPE.SPECIAL_RECON: 0}

    def _onVehicleStateUpdated(self, state, value):
        if state == VEHICLE_VIEW_STATE.OBSERVED_BY_ENEMY:
            if value.get('isObserved', False):
                detectionType = value.get("detectionType", 0)
                self.as_showS(self.DETECTION_TYPE_TO_TIME.get(detectionType, self.__time))
            else:
                self.as_hideS()
        elif state in _STATES_TO_HIDE:
            self.as_hideS()
            if not self.__isComp7Battle:
                self.updateTime()

    def updateTime(self, diff=0.0):
        new_time = BASE_TIME - diff
        if new_time != self.__time:
            logInfo("SixthSense - Updated time from {} to {}", self.__time, new_time)
            self.__time = new_time

    def _onRoundFinished(self, *args):
        self.as_hideS()

    def playSound(self):
        if self.__soundID is not None:
            self.callWWISE(self.__soundID)

    def getIconPatch(self):
        try:
            directory = "gui/maps/icons/battle_observer/sixth_sense/"
            flash_path = '../../' + directory
            if self.settings[SIXTH_SENSE.RANDOM]:
                folder = ResMgr.openSection(directory).keys()
                ResMgr.purge(directory, True)
                return flash_path + choice(folder)
            else:
                return flash_path + self.settings[SIXTH_SENSE.ICON_NAME]

        except Exception as e:
            logError(repr(e))
            return super(SixthSense, self).getIconPatch()

from random import choice

from armagomen._constants import SIXTH_SENSE
from armagomen.battle_observer.meta.battle.sixth_sense_meta import SixthSenseMeta
from armagomen.utils.common import getPlayer, SIXTH_SENSE_LIST
from armagomen.utils.logging import logError
from constants import DIRECT_DETECTION_TYPE
from gui.battle_control.battle_constants import VEHICLE_VIEW_STATE
from items.components.supply_slot_categories import SupplySlotFactorLevels
from PlayerEvents import g_playerEvents
from SoundGroups import g_instance

_STATES_TO_HIDE = {VEHICLE_VIEW_STATE.SWITCHING, VEHICLE_VIEW_STATE.RESPAWNING}
_DESTROYED = {VEHICLE_VIEW_STATE.DESTROYED, VEHICLE_VIEW_STATE.CREW_DEACTIVATED}
_STATES_TO_HIDE.update(_DESTROYED)

BASE_TIME = 10.0
COMP7_TIME = 4.0
STEALTH_RADAR_TIME = 2.0
SPECIAL_RECON_TITE = 7.0
RADIO = 'radioCommunication'
RADIO_DURATION = 8.5
RADIO_DURATION_BONUS = 8.0


class SixthSense(SixthSenseMeta):

    def __init__(self):
        super(SixthSense, self).__init__()
        self.__sounds = dict()
        self.__soundID = None
        self.__isComp7Battle = False
        self.__isRadioInstalled = False
        self.__isRadioInstalledInBonusSlot = False

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
        player = getPlayer()
        device = next((d for d in devices if d and RADIO in d.tags), None)
        self.__isRadioInstalled = device is not None
        if self.__isRadioInstalled and player is not None:
            descr = player.getVehicleDescriptor()
            self.__isRadioInstalledInBonusSlot = device.defineActiveLevel(descr) == SupplySlotFactorLevels.IMPROVED
        else:
            self.__isRadioInstalledInBonusSlot = False

    def getCurrentLampTime(self, value):
        if self.__isComp7Battle:
            detectionType = value.get("detectionType", 0)
            if detectionType == DIRECT_DETECTION_TYPE.STEALTH_RADAR:
                return STEALTH_RADAR_TIME
            elif detectionType == DIRECT_DETECTION_TYPE.SPECIAL_RECON:
                return SPECIAL_RECON_TITE
            else:
                return COMP7_TIME
        elif self.__isRadioInstalled:
            return RADIO_DURATION_BONUS if self.__isRadioInstalledInBonusSlot else RADIO_DURATION
        return BASE_TIME

    def _onVehicleStateUpdated(self, state, value):
        if state == VEHICLE_VIEW_STATE.OBSERVED_BY_ENEMY:
            if value.get('isObserved', False):
                self.as_showS(self.getCurrentLampTime(value))
            else:
                self.as_hideS()
        elif state in _STATES_TO_HIDE:
            self.as_hideS()
            if state in _DESTROYED:
                self.__isRadioInstalled = False

    def _onRoundFinished(self, *args):
        self.as_hideS()

    def playSound(self):
        if self.__soundID is not None:
            self.callWWISE(self.__soundID)

    def getIconName(self):
        try:
            if self.settings[SIXTH_SENSE.RANDOM]:
                return choice(SIXTH_SENSE_LIST)
            else:
                return self.settings[SIXTH_SENSE.ICON_NAME]

        except Exception as e:
            logError(repr(e))
            return super(SixthSense, self).getIconName()

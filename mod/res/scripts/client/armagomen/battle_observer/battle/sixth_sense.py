from armagomen._constants import SIXTH_SENSE
from armagomen.battle_observer.meta.battle.sixth_sense_meta import SixthSenseMeta
from armagomen.utils.common import SIXTH_SENSE_LIST
from BigWorld import callback, cancelCallback
from constants import DIRECT_DETECTION_TYPE
from gui.battle_control.battle_constants import VEHICLE_VIEW_STATE
from items.components.supply_slot_categories import SupplySlotFactorLevels
from PlayerEvents import g_playerEvents

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


class SixthSenseTimer(object):

    def __init__(self):
        super(SixthSenseTimer, self).__init__()
        self.__callbackID = None
        self.__interval = 0.1
        self.__time = self.__timeLeft = BASE_TIME
        self.__sound = None

    def setTime(self, time):
        self.__time = time
        self.__timeLeft = time

    def setTickSound(self, soundID):
        from SoundGroups import g_instance
        self.__sound = g_instance.getSound2D(soundID)

    def playTickSound(self):
        if self.__sound is None:
            return
        self.__sound.play()

    def restartTimer(self):
        self.stopTimer()
        self.__timeLeft = self.__time
        self.startTimer()

    def startTimer(self):
        if self.__callbackID is None:
            self.__invoke()

    def stopTimer(self):
        if self.__callbackID is not None:
            cancelCallback(self.__callbackID)
            self.__callbackID = None

    def isTimerStarted(self):
        return self.__callbackID is not None

    def __invoke(self):
        self.__callbackID = callback(self.__interval, self.__invoke)
        if self.__timeLeft.is_integer() and self.__timeLeft != self.__time:
            self.playTickSound()
        self.updateFunc(self.__timeLeft, self.__timeLeft / self.__time)
        if self.__timeLeft <= 0.0:
            self.stopTimer()
            return
        self.__timeLeft = round(self.__timeLeft - self.__interval, 1)

    def updateFunc(self, timeLeft, radialPercentage):
        raise NotImplementedError

    def handleStopAndHide(self):
        if self.isTimerStarted():
            self.stopTimer()
            self.updateFunc(0.0, 0.0)


class SixthSense(SixthSenseTimer, SixthSenseMeta):

    def __init__(self):
        super(SixthSense, self).__init__()
        self.__isComp7Battle = False
        self.__isRadioInstalled = False
        self.__isRadioInstalledInBonusSlot = False

    def _populate(self):
        super(SixthSense, self)._populate()
        self.__isComp7Battle = self.isComp7Battle()
        if self.settings[SIXTH_SENSE.PLAY_TICK_SOUND]:
            self.setTickSound(self._arenaVisitor.type.getCountdownTimerSound())
        g_playerEvents.onRoundFinished += self._onRoundFinished
        ctrl = self.sessionProvider.shared.vehicleState
        if ctrl is not None:
            ctrl.onVehicleStateUpdated += self._onVehicleStateUpdated
        g_playerEvents.onObservedByEnemy += self._onObservedByEnemy
        optional_devices = self.sessionProvider.shared.optionalDevices
        if optional_devices is not None and not self.__isComp7Battle:
            optional_devices.onDescriptorDevicesChanged += self.onDescriptorDevicesChanged

    def _dispose(self):
        self.handleStopAndHide()
        g_playerEvents.onObservedByEnemy -= self._onObservedByEnemy
        g_playerEvents.onRoundFinished -= self._onRoundFinished
        ctrl = self.sessionProvider.shared.vehicleState
        if ctrl is not None:
            ctrl.onVehicleStateUpdated -= self._onVehicleStateUpdated
        optional_devices = self.sessionProvider.shared.optionalDevices
        if optional_devices is not None and not self.__isComp7Battle:
            optional_devices.onDescriptorDevicesChanged -= self.onDescriptorDevicesChanged
        super(SixthSense, self)._dispose()

    def onDescriptorDevicesChanged(self, devices):
        from BigWorld import player
        _player = player()
        device = next((d for d in devices if d and RADIO in d.tags), None)
        self.__isRadioInstalled = device is not None
        if self.__isRadioInstalled and _player is not None:
            descr = _player.getVehicleDescriptor()
            self.__isRadioInstalledInBonusSlot = device.defineActiveLevel(descr) == SupplySlotFactorLevels.IMPROVED
        else:
            self.__isRadioInstalledInBonusSlot = False

    def getCurrentLampTime(self, detectionType):
        if self.__isComp7Battle:
            if detectionType == DIRECT_DETECTION_TYPE.STEALTH_RADAR:
                return STEALTH_RADAR_TIME
            elif detectionType == DIRECT_DETECTION_TYPE.SPECIAL_RECON:
                return SPECIAL_RECON_TITE
            else:
                return COMP7_TIME
        elif self.__isRadioInstalled:
            return RADIO_DURATION_BONUS if self.__isRadioInstalledInBonusSlot else RADIO_DURATION
        return BASE_TIME

    def _onObservedByEnemy(self, detectionType, isObserved):
        if isObserved:
            self.setTime(self.getCurrentLampTime(detectionType))
            self.as_show()
            self.startTimer()
        else:
            self.handleStopAndHide()

    def _onVehicleStateUpdated(self, state, *args, **kwargs):
        if state in _STATES_TO_HIDE:
            self.handleStopAndHide()
            if state in _DESTROYED:
                self.__isRadioInstalled = False

    def _onRoundFinished(self, *args, **kwargs):
        self.handleStopAndHide()

    def getIconName(self):
        if self.settings[SIXTH_SENSE.RANDOM]:
            from random import choice
            icon = choice(SIXTH_SENSE_LIST)
        else:
            icon = self.settings.get(SIXTH_SENSE.ICON_NAME, "").strip()
        if not icon or not icon.lower().endswith(".png"):
            return super(SixthSense, self).getIconName()
        return icon

    def updateFunc(self, timeLeft, radialPercentage):
        self.as_invoke(timeLeft, radialPercentage)

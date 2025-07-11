from collections import defaultdict
from math import ceil, log

from armagomen._constants import DISPERSION_TIMER, GLOBAL, POSTMORTEM_MODES
from armagomen.battle_observer.meta.battle.dispersion_timer_meta import DispersionTimerMeta
from armagomen.utils.common import cancelOverride, getPlayer, overrideMethod
from gui.battle_control.avatar_getter import getInputHandler
from VehicleGunRotator import VehicleGunRotator

TIMER, PERCENT = ("timer", "percent")
MAXIMUM = 100


class DispersionTimer(DispersionTimerMeta):

    def __init__(self):
        super(DispersionTimer, self).__init__()
        self.macro = defaultdict(float, timer=0.0, percent=0)
        self.min_angle = 1.0
        self.isPostmortem = False

    def _populate(self):
        super(DispersionTimer, self)._populate()
        ctrl = self.sessionProvider.shared.crosshair
        if ctrl is not None:
            ctrl.onCrosshairPositionChanged += self.as_onCrosshairPositionChangedS
        handler = getInputHandler()
        if handler is not None and hasattr(handler, "onCameraChanged"):
            handler.onCameraChanged += self.onCameraChanged
        optional_devices = self.sessionProvider.shared.optionalDevices
        if optional_devices is not None:
            optional_devices.onDescriptorDevicesChanged += self.onDevicesChanged
        self.min_angle = getPlayer().getOwnVehicleShotDispersionAngle(0.0)[1]
        overrideMethod(VehicleGunRotator, "updateRotationAndGunMarker")(self.updateRotationAndGunMarker)

    def _dispose(self):
        ctrl = self.sessionProvider.shared.crosshair
        if ctrl is not None:
            ctrl.onCrosshairPositionChanged -= self.as_onCrosshairPositionChangedS
        handler = getInputHandler()
        if handler is not None and hasattr(handler, "onCameraChanged"):
            handler.onCameraChanged -= self.onCameraChanged
        optional_devices = self.sessionProvider.shared.optionalDevices
        if optional_devices is not None:
            optional_devices.onDescriptorDevicesChanged -= self.onDevicesChanged
        cancelOverride(VehicleGunRotator, "updateRotationAndGunMarker", "updateRotationAndGunMarker")
        super(DispersionTimer, self)._dispose()

    def onDevicesChanged(self, devices):
        self.min_angle = getPlayer().getOwnVehicleShotDispersionAngle(0.0)[1]

    def updateRotationAndGunMarker(self, base, rotator, *args, **kwargs):
        base(rotator, *args, **kwargs)
        self.updateDispersion(rotator)

    def onCameraChanged(self, ctrlMode, vehicleID=None):
        self.isPostmortem = ctrlMode in POSTMORTEM_MODES
        if self.isPostmortem:
            self.min_angle = 1.0
            self.as_updateTimerTextS(GLOBAL.EMPTY_LINE)

    def updateDispersion(self, gunRotator):
        type_descriptor = gunRotator._avatar.vehicleTypeDescriptor
        if type_descriptor is None or self.isPostmortem:
            return self.as_updateTimerTextS(GLOBAL.EMPTY_LINE)
        aiming_angle = gunRotator.dispersionAngle
        diff = self.min_angle / aiming_angle
        percent = int(ceil(diff * MAXIMUM))
        self.macro[TIMER] = round(type_descriptor.gun.aimingTime * abs(min(0.0, log(diff))), 2)
        self.macro[GLOBAL.COLOR] = self.settings[GLOBAL.COLOR if percent < MAXIMUM else DISPERSION_TIMER.DONE_COLOR]
        self.macro[PERCENT] = percent
        self.as_updateTimerTextS(self.settings[DISPERSION_TIMER.TEMPLATE] % self.macro)

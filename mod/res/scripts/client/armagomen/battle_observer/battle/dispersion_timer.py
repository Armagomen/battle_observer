from collections import defaultdict
from math import log, ceil

from armagomen._constants import GLOBAL, POSTMORTEM, DISPERSION_TIMER
from armagomen.battle_observer.meta.battle.dispersion_timer_meta import DispersionTimerMeta
from armagomen.utils.common import logDebug
from armagomen.utils.events import g_events
from gui.battle_control.avatar_getter import getInputHandler

TIMER, PERCENT = ("timer", "percent")


class DispersionTimer(DispersionTimerMeta):

    def __init__(self):
        super(DispersionTimer, self).__init__()
        self.macro = defaultdict(lambda: GLOBAL.CONFIG_ERROR, timer=GLOBAL.ZERO, percent=GLOBAL.ZERO)
        self.min_angle = GLOBAL.F_ONE
        self.isPostmortem = False

    def _populate(self):
        super(DispersionTimer, self)._populate()
        ctrl = self.sessionProvider.shared.crosshair
        if ctrl is not None:
            ctrl.onCrosshairPositionChanged += self.as_onCrosshairPositionChangedS
        handler = getInputHandler()
        if handler is not None and hasattr(handler, "onCameraChanged"):
            handler.onCameraChanged += self.onCameraChanged
        g_events.onDispersionAngleChanged += self.updateDispersion

    def _dispose(self):
        ctrl = self.sessionProvider.shared.crosshair
        if ctrl is not None:
            ctrl.onCrosshairPositionChanged -= self.as_onCrosshairPositionChangedS
        handler = getInputHandler()
        if handler is not None and hasattr(handler, "onCameraChanged"):
            handler.onCameraChanged -= self.onCameraChanged
        g_events.onDispersionAngleChanged -= self.updateDispersion
        super(DispersionTimer, self)._dispose()

    def onCameraChanged(self, ctrlMode, vehicleID=None):
        self.isPostmortem = ctrlMode in POSTMORTEM.MODES
        if self.isPostmortem:
            self.min_angle = GLOBAL.F_ONE
            self.as_updateTimerTextS(GLOBAL.EMPTY_LINE)

    def updateDispersion(self, gunRotator):
        type_descriptor = gunRotator._avatar.vehicleTypeDescriptor
        if type_descriptor is None or self.isPostmortem:
            return self.as_updateTimerTextS(GLOBAL.EMPTY_LINE)
        aiming_angle = gunRotator.dispersionAngle
        if self.min_angle > aiming_angle:
            self.min_angle = aiming_angle
            logDebug("DispersionTimer - renew min dispersion angle {}", self.min_angle)
        percent = int(ceil(self.min_angle / aiming_angle * 100))
        if percent < 100:
            self.macro[TIMER] = round(type_descriptor.gun.aimingTime * log(aiming_angle / self.min_angle), GLOBAL.TWO)
            self.macro[GLOBAL.COLOR] = self.settings[GLOBAL.COLOR]
        else:
            self.macro[TIMER] = GLOBAL.ZERO
            self.macro[GLOBAL.COLOR] = self.settings[DISPERSION_TIMER.DONE_COLOR]
        self.macro[PERCENT] = percent
        self.as_updateTimerTextS(self.settings[DISPERSION_TIMER.TEMPLATE] % self.macro)

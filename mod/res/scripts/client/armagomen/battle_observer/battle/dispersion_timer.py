from collections import defaultdict
from math import log, ceil

from armagomen.battle_observer.meta.battle.dispersion_timer_meta import DispersionTimerMeta
from armagomen.constants import DISPERSION, GLOBAL, POSTMORTEM, DISPERSION_TIME
from armagomen.utils.common import logDebug
from armagomen.utils.events import g_events
from gui.battle_control.avatar_getter import getInputHandler


class DispersionTimer(DispersionTimerMeta):

    def __init__(self):
        super(DispersionTimer, self).__init__()
        self.macro = defaultdict(lambda: GLOBAL.CONFIG_ERROR, timer=GLOBAL.ZERO, percent=GLOBAL.ZERO)
        self.min_angle = GLOBAL.F_ONE
        self.isPostmortem = False

    def _populate(self):
        super(DispersionTimer, self)._populate()
        self.macro.update(color=self.settings[DISPERSION.TIMER_COLOR],
                          color_done=self.settings[DISPERSION.TIMER_DONE_COLOR])
        ctrl = self.sessionProvider.shared.crosshair
        if ctrl is not None:
            ctrl.onCrosshairPositionChanged += self.as_onCrosshairPositionChangedS

    def _dispose(self):
        ctrl = self.sessionProvider.shared.crosshair
        if ctrl is not None:
            ctrl.onCrosshairPositionChanged -= self.as_onCrosshairPositionChangedS
        super(DispersionTimer, self)._dispose()

    def onCameraChanged(self, ctrlMode, vehicleID=None):
        self.isPostmortem = ctrlMode in POSTMORTEM.MODES
        if self.isPostmortem:
            self.min_angle = GLOBAL.F_ONE
            self.as_updateTimerTextS(GLOBAL.EMPTY_LINE)

    def updateDispersion(self, gunRotator):
        if self.isPostmortem:
            return
        vehicleTypeDescriptor = gunRotator._avatar.vehicleTypeDescriptor
        if vehicleTypeDescriptor is None:
            return self.as_updateTimerTextS(GLOBAL.EMPTY_LINE)
        aimingTime = vehicleTypeDescriptor.gun.aimingTime
        dispersionAngle = gunRotator.dispersionAngle
        if self.min_angle > dispersionAngle:
            self.min_angle = dispersionAngle
            logDebug("DispersionTimer - renew min dispersion angle {}", self.min_angle)
        self.macro[DISPERSION_TIME.TIMER] = round(aimingTime, GLOBAL.TWO) * log(dispersionAngle / self.min_angle)
        percent = int(ceil(self.min_angle / dispersionAngle * 100))
        self.macro[DISPERSION_TIME.PERCENT] = percent
        template = DISPERSION.TIMER_REGULAR_TEMPLATE if percent < 100 else DISPERSION.TIMER_DONE_TEMPLATE
        self.as_updateTimerTextS(self.settings[template] % self.macro)

    def onBattleSessionStart(self):
        super(DispersionTimer, self).onBattleSessionStart()
        handler = getInputHandler()
        if handler is not None and hasattr(handler, "onCameraChanged"):
            handler.onCameraChanged += self.onCameraChanged
        g_events.onDispersionAngleChanged += self.updateDispersion

    def onBattleSessionStop(self):
        handler = getInputHandler()
        if handler is not None and hasattr(handler, "onCameraChanged"):
            handler.onCameraChanged -= self.onCameraChanged
        g_events.onDispersionAngleChanged -= self.updateDispersion
        super(DispersionTimer, self).onBattleSessionStop()

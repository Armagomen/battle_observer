from collections import defaultdict
from math import log, ceil

from armagomen.battle_observer.meta.battle.dispersion_timer_meta import DispersionTimerMeta
from armagomen.constants import DISPERSION, GLOBAL, POSTMORTEM, DISPERSION_TIME
from armagomen.utils.common import logInfo
from armagomen.utils.events import g_events
from gui.battle_control import avatar_getter


class DispersionTimer(DispersionTimerMeta):

    def __init__(self):
        super(DispersionTimer, self).__init__()
        self.macro = defaultdict(lambda: GLOBAL.CONFIG_ERROR, timer=GLOBAL.F_ZERO, percent=GLOBAL.ZERO)
        self.min_angle = None
        self.isPostmortem = False
        self.timing = 0.0
        self.percent = 0.0

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
            self.min_angle = None
            self.as_updateTimerTextS(GLOBAL.EMPTY_LINE)

    def updateDispersion(self, gunRotator):
        if self.isPostmortem:
            return
        update = False
        dispersionAngle = gunRotator.dispersionAngle
        aimingTime = self._player.vehicleTypeDescriptor.gun.aimingTime
        if self.min_angle is None or self.min_angle > dispersionAngle:
            self.min_angle = dispersionAngle
            if self.isDebug:
                logInfo("DispersionTimer - renew min dispersion angle %s" % self.min_angle)
        timing = round(aimingTime, GLOBAL.TWO) * log(dispersionAngle / self.min_angle)
        if self.timing != timing:
            self.macro[DISPERSION_TIME.TIMER] = timing
            self.timing = timing
            update = True
        percent = int(ceil(self.min_angle / dispersionAngle * 100))
        if self.percent != percent:
            self.macro[DISPERSION_TIME.PERCENT] = percent
            self.percent = percent
            update = True
        if update:
            if percent == 100:
                self.as_updateTimerTextS(self.settings[DISPERSION.TIMER_DONE_TEMPLATE] % self.macro)
            else:
                self.as_updateTimerTextS(self.settings[DISPERSION.TIMER_REGULAR_TEMPLATE] % self.macro)

    def onEnterBattlePage(self):
        super(DispersionTimer, self).onEnterBattlePage()
        handler = avatar_getter.getInputHandler()
        if handler is not None:
            handler.onCameraChanged += self.onCameraChanged
        g_events.onDispersionAngleChanged += self.updateDispersion

    def onExitBattlePage(self):
        handler = avatar_getter.getInputHandler()
        if handler is not None:
            handler.onCameraChanged -= self.onCameraChanged
        g_events.onDispersionAngleChanged -= self.updateDispersion
        super(DispersionTimer, self).onExitBattlePage()

from collections import defaultdict
from math import log

from armagomen.battle_observer.meta.battle.dispersion_timer_meta import DispersionTimerMeta
from armagomen.constants import DISPERSION, GLOBAL, POSTMORTEM, DISPERSION_TIME
from armagomen.utils.common import events, logInfo
from gui.battle_control import avatar_getter


class DispersionTimer(DispersionTimerMeta):

    def __init__(self):
        super(DispersionTimer, self).__init__()
        self.timer_regular = None
        self.timer_done = None
        self.macro = None
        self.max_angle = None
        self.isPostmortem = False

    def _populate(self):
        super(DispersionTimer, self)._populate()
        self.timer_regular = self.settings[DISPERSION.TIMER_REGULAR_TEMPLATE]
        self.timer_done = self.settings[DISPERSION.TIMER_DONE_TEMPLATE]
        self.macro = defaultdict(lambda: GLOBAL.CONFIG_ERROR,
                                 color=self.settings[DISPERSION.TIMER_COLOR],
                                 color_done=self.settings[DISPERSION.TIMER_DONE_COLOR],
                                 timer=None, percent=None)
        self.as_startUpdateS(self.settings)

    def onCameraChanged(self, ctrlMode, vehicleID=None):
        self.as_onControlModeChangedS(ctrlMode)
        self.isPostmortem = ctrlMode in POSTMORTEM.MODES
        if self.isPostmortem:
            self.as_updateTimerTextS(GLOBAL.EMPTY_LINE)

    def updateDispersion(self, avatar, dispersionAngle):
        if self.isPostmortem:
            return
        if self.max_angle is None:
            self.max_angle = dispersionAngle
            if self.isDebug:
                logInfo("DispersionTimer - renew max dispersion angle %s" % self.max_angle)
        timing = round(avatar.vehicleTypeDescriptor.gun.aimingTime, GLOBAL.ONE) * log(dispersionAngle / self.max_angle)
        percent = int(self.max_angle / dispersionAngle * 100)
        if self.macro[DISPERSION_TIME.TIMER] == timing and self.macro[DISPERSION_TIME.PERCENT] == percent:
            return
        self.macro[DISPERSION_TIME.TIMER] = timing
        self.macro[DISPERSION_TIME.PERCENT] = percent
        if timing <= GLOBAL.ZERO:
            self.as_updateTimerTextS(self.timer_done % self.macro)
        else:
            self.as_updateTimerTextS(self.timer_regular % self.macro)

    def onEnterBattlePage(self):
        super(DispersionTimer, self).onEnterBattlePage()
        handler = avatar_getter.getInputHandler()
        if handler is not None:
            handler.onCameraChanged += self.onCameraChanged
        events.onDispersionAngleChanged += self.updateDispersion

    def onExitBattlePage(self):
        handler = avatar_getter.getInputHandler()
        if handler is not None:
            handler.onCameraChanged -= self.onCameraChanged
        events.onDispersionAngleChanged -= self.updateDispersion
        super(DispersionTimer, self).onExitBattlePage()

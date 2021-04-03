from collections import defaultdict
from math import log

from armagomen.battle_observer.core.bo_constants import DISPERSION, GLOBAL, POSTMORTEM
from armagomen.battle_observer.meta.battle.dispersion_timer_meta import DispersionTimerMeta
from armagomen.utils.common import events
from gui.battle_control import avatar_getter


class DispersionTimer(DispersionTimerMeta):

    def __init__(self):
        super(DispersionTimer, self).__init__()
        self.timer_regular = None
        self.timer_done = None
        self.macro = None
        self.base_getAngle = None
        self.max_angle = 0.0
        self.aiming_time = 0.0

    def _populate(self):
        super(DispersionTimer, self)._populate()
        self.timer_regular = self.settings[DISPERSION.TIMER_REGULAR_TEMPLATE]
        self.timer_done = self.settings[DISPERSION.TIMER_DONE_TEMPLATE]
        self.macro = defaultdict(lambda: GLOBAL.CONFIG_ERROR,
                                 color=self.settings[DISPERSION.TIMER_COLOR],
                                 color_done=self.settings[DISPERSION.TIMER_DONE_COLOR],
                                 timer=GLOBAL.F_ZERO, percent=GLOBAL.ZERO)
        self.as_startUpdateS(self.settings)

    def onCameraChanged(self, ctrlMode, vehicleID=None):
        self.as_onControlModeChangedS(ctrlMode)
        if ctrlMode in POSTMORTEM.MODES:
            self.as_updateTimerTextS(GLOBAL.EMPTY_LINE)

    def updateDispersion(self, avatar, angle):
        if avatar.isVehicleAlive:
            angle = round(angle * 100, 2)
            if self.max_angle == GLOBAL.F_ZERO:
                self.max_angle = angle
                self.aiming_time = round(avatar.vehicleTypeDescriptor.gun.aimingTime, 1)
            timing = self.aiming_time * log(angle / self.max_angle)
            self.macro["timer"] = timing
            self.macro["percent"] = int(self.max_angle / angle * 100)
            if timing <= GLOBAL.ZERO:
                self.setDoneMessage()
            else:
                self.setRegularMessage()

    def setRegularMessage(self):
        self.as_updateTimerTextS(self.timer_regular % self.macro)

    def setDoneMessage(self):
        self.as_updateTimerTextS(self.timer_done % self.macro)

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

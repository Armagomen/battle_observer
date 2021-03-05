from collections import defaultdict
from math import log

from Avatar import PlayerAvatar
from gui.battle_control import avatar_getter

from armagomen.battle_observer.core import cfg
from armagomen.battle_observer.core.bo_constants import DISPERSION_CIRCLE, GLOBAL, POSTMORTEM
from armagomen.battle_observer.meta.battle.dispersion_timer_meta import DispersionTimerMeta


class DispersionTimer(DispersionTimerMeta):

    def __init__(self):
        super(DispersionTimer, self).__init__()
        self.timer_regular = cfg.dispersion_circle[DISPERSION_CIRCLE.TIMER_REGULAR_TEMPLATE]
        self.timer_done = cfg.dispersion_circle[DISPERSION_CIRCLE.TIMER_DONE_TEMPLATE]
        self.macro = defaultdict(lambda: GLOBAL.CONFIG_ERROR,
                                 {"color": cfg.dispersion_circle[DISPERSION_CIRCLE.TIMER_COLOR],
                                  "color_done": cfg.dispersion_circle[DISPERSION_CIRCLE.TIMER_DONE_COLOR],
                                  "timer": GLOBAL.F_ZERO, "percent": GLOBAL.ZERO})
        self.base_getAngle = None
        self.max_angle = 0.0
        self.aiming_time = 0.0

    def _populate(self):
        super(DispersionTimer, self)._populate()
        self.as_startUpdateS(cfg.dispersion_circle)

    def onCameraChanged(self, ctrlMode, vehicleID=None):
        self.as_onControlModeChangedS(ctrlMode)
        if ctrlMode in POSTMORTEM.MODES:
            self.as_updateTimerTextS(GLOBAL.EMPTY_LINE)

    def updateDispersion(self, avatar, *args, **kwargs):
        result = self.base_getAngle(avatar, *args, **kwargs)
        if avatar.isVehicleAlive:
            angle = round(result[GLOBAL.FIRST] * 100, 2)
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
        return result

    def setRegularMessage(self):
        self.as_updateTimerTextS(self.timer_regular % self.macro)

    def setDoneMessage(self):
        self.as_updateTimerTextS(self.timer_done % self.macro)

    def onEnterBattlePage(self):
        super(DispersionTimer, self).onEnterBattlePage()
        handler = avatar_getter.getInputHandler()
        if handler is not None:
            handler.onCameraChanged += self.onCameraChanged
        self.base_getAngle = PlayerAvatar.getOwnVehicleShotDispersionAngle
        PlayerAvatar.getOwnVehicleShotDispersionAngle = lambda *args, **kwargs: self.updateDispersion(*args, **kwargs)

    def onExitBattlePage(self):
        handler = avatar_getter.getInputHandler()
        if handler is not None:
            handler.onCameraChanged -= self.onCameraChanged
        PlayerAvatar.getOwnVehicleShotDispersionAngle = self.base_getAngle
        super(DispersionTimer, self).onExitBattlePage()

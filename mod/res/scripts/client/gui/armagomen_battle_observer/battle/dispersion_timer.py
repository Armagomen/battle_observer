from collections import defaultdict
from math import log

from AvatarInputHandler import AvatarInputHandler
from gui.battle_control import avatar_getter
from ..core.battle import cache
from ..core.bo_constants import DISPERSION_CIRCLE, GLOBAL
from ..core.config import cfg
from ..core.events import g_events
from ..meta.battle.dispersion_timer_meta import DispersionTimerMeta


class DispersionTimer(DispersionTimerMeta):

    def __init__(self):
        super(DispersionTimer, self).__init__()
        self.shotDispersionAngle = 0.0
        self.aimingTime = 0.0
        self.timer_regular = cfg.dispersion_circle[DISPERSION_CIRCLE.TIMER_REGULAR_TEMPLATE]
        self.timer_done = cfg.dispersion_circle[DISPERSION_CIRCLE.TIMER_DONE_TEMPLATE]
        self.macro = defaultdict(lambda: GLOBAL.CONFIG_ERROR,
                                 {"color": cfg.dispersion_circle[DISPERSION_CIRCLE.TIMER_COLOR],
                                  "color_done": cfg.dispersion_circle[DISPERSION_CIRCLE.TIMER_DONE_COLOR],
                                  "timer": 0.0, "percent": 0})

    def _populate(self):
        super(DispersionTimer, self)._populate()
        self.as_startUpdateS(cfg.dispersion_circle)
        g_events.onPlayerVehicleDeath += self.onPlayerVehicleDeath
        g_events.onDispersionAngleUpdate += self.onDispersionAngleUpdate

    def _dispose(self):
        g_events.onPlayerVehicleDeath -= self.onPlayerVehicleDeath
        g_events.onDispersionAngleUpdate -= self.onDispersionAngleUpdate
        super(DispersionTimer, self)._dispose()

    def onCameraChanged(self, ctrlMode, vehicleID=None):
        self.as_onControlModeChangedS(ctrlMode)

    def onDispersionAngleUpdate(self, angle):
        if cache.player is not None and cache.player.isVehicleAlive:
            if self.shotDispersionAngle != 0:
                qw = angle / self.shotDispersionAngle
            else:
                qw = 1.0
            timing = self.aimingTime * log(qw)
            if self.macro["timer"] != timing:
                self.macro["timer"] = timing
                self.macro["percent"] = int(min(1.0, self.shotDispersionAngle / angle) * 100)
            if not timing or timing < 0:
                self.setDoneMessage()
            else:
                self.setRegularMessage()

    def setRegularMessage(self):
        self.as_updateTimerTextS(self.timer_regular % self.macro)

    def setDoneMessage(self):
        self.as_updateTimerTextS(self.timer_done % self.macro)

    def onEnterBattlePage(self):
        super(DispersionTimer, self).onEnterBattlePage()
        if cache.player is not None:
            desc = cache.player.vehicle.typeDescriptor.gun
            self.shotDispersionAngle = desc.shotDispersionAngle
            self.aimingTime = desc.aimingTime
        handler = avatar_getter.getInputHandler()
        if handler is not None:
            if isinstance(handler, AvatarInputHandler):
                handler.onCameraChanged += self.onCameraChanged

    def onExitBattlePage(self):
        handler = avatar_getter.getInputHandler()
        if handler is not None:
            if isinstance(handler, AvatarInputHandler):
                handler.onCameraChanged -= self.onCameraChanged
        super(DispersionTimer, self).onExitBattlePage()

    def onPlayerVehicleDeath(self, killerID):
        self.as_updateTimerTextS("")

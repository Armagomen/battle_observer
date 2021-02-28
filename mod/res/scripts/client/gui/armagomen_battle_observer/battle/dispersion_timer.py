from collections import defaultdict
from math import log

from Avatar import PlayerAvatar
from AvatarInputHandler import AvatarInputHandler
from gui.battle_control import avatar_getter
from ..core import cfg, cache
from ..core.bo_constants import DISPERSION_CIRCLE, GLOBAL
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
                                  "timer": GLOBAL.F_ZERO, "percent": GLOBAL.ZERO})
        self.base_getAngle = None

    def _populate(self):
        super(DispersionTimer, self)._populate()
        self.as_startUpdateS(cfg.dispersion_circle)
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onVehicleKilled += self.onVehicleKilled

        self.base_getAngle = PlayerAvatar.getOwnVehicleShotDispersionAngle
        PlayerAvatar.getOwnVehicleShotDispersionAngle = lambda *args, **kwargs: self.updateDispersion(*args, **kwargs)

    def _dispose(self):
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onVehicleKilled -= self.onVehicleKilled
        PlayerAvatar.getOwnVehicleShotDispersionAngle = self.base_getAngle
        super(DispersionTimer, self)._dispose()

    def onCameraChanged(self, ctrlMode, vehicleID=None):
        self.as_onControlModeChangedS(ctrlMode)

    def updateDispersion(self, *args, **kwargs):
        result = self.base_getAngle(*args, **kwargs)
        if cache.player is not None and cache.player.isVehicleAlive:
            if self.shotDispersionAngle != GLOBAL.ZERO:
                qw = result[GLOBAL.FIRST] / self.shotDispersionAngle
            else:
                qw = 1.0
            timing = self.aimingTime * log(qw)
            if self.macro["timer"] != timing:
                self.macro["timer"] = timing
                self.macro["percent"] = int(min(GLOBAL.F_ONE, self.shotDispersionAngle / result[GLOBAL.FIRST]) * 100)
            if not timing or timing < GLOBAL.ZERO:
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

    def onVehicleKilled(self, targetID, *args, **kwargs):
        if cache.player.playerVehicleID == targetID:
            self.as_updateTimerTextS("")

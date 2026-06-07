from armagomen._constants import DISPERSION_TIMER, POSTMORTEM_MODES
from armagomen import IALogger
from armagomen.battle_observer.meta.battle.dispersion_timer_meta import DispersionTimerMeta
from armagomen.utils.common import cancelOverride, overrideMethod, percentToColor

from Avatar import PlayerAvatar
from constants import ARENA_PERIOD
from gui.battle_control.avatar_getter import getInputHandler
from helpers import dependency
from PlayerEvents import g_playerEvents

ERROR = "DispersionTimer getDispersionAngle override: {}"


class DispersionTimer(DispersionTimerMeta):
    logger = dependency.descriptor(IALogger)

    def __init__(self):
        super(DispersionTimer, self).__init__()
        self.ideal_angle = 0
        self.period = ARENA_PERIOD.IDLE
        self.is_alive = False
        self.is_battle_period = False
        self.tpl = None

    def _populate(self):
        super(DispersionTimer, self)._populate()
        timer = self.settings[DISPERSION_TIMER.TIMER]
        percent = self.settings[DISPERSION_TIMER.PERCENT]

        if timer or percent:
            g_playerEvents.onArenaPeriodChange += self.onArenaPeriodChange
            self.tpl = " - ".join(param[1] for param in ((timer, "{0:.1f}s."), (percent, "{1:.0%}")) if param[0])
            ctrl = self.sessionProvider.shared.crosshair
            if ctrl is not None:
                ctrl.onCrosshairPositionChanged += self.as_onCrosshairPositionChangedS
            handler = getInputHandler()
            if handler is not None and hasattr(handler, "onCameraChanged"):
                handler.onCameraChanged += self.onCameraChanged
            overrideMethod(PlayerAvatar, "getOwnVehicleShotDispersionAngle")(self.getDispersionAngle)
            arena = self._arenaVisitor.getArenaSubscription()
            if arena is not None:
                self.period = arena.period
                self.is_alive = self.getVehicleInfo().isAlive()
                self.toggleVisible()

    def _dispose(self):
        if self.tpl is not None:
            g_playerEvents.onArenaPeriodChange -= self.onArenaPeriodChange
            ctrl = self.sessionProvider.shared.crosshair
            if ctrl is not None:
                ctrl.onCrosshairPositionChanged -= self.as_onCrosshairPositionChangedS
            handler = getInputHandler()
            if handler is not None and hasattr(handler, "onCameraChanged"):
                handler.onCameraChanged -= self.onCameraChanged
            cancelOverride(PlayerAvatar, "getOwnVehicleShotDispersionAngle", "getDispersionAngle")
        super(DispersionTimer, self)._dispose()

    def toggleVisible(self):
        self.as_setComponentVisible(self.period == ARENA_PERIOD.BATTLE and self.is_alive)

    def onArenaPeriodChange(self, period, *args):
        self.period = period
        self.toggleVisible()

    def getDispersionAngle(self, base, avatar, turretRotationSpeed, *args, **kwargs):
        dispersionAngles = base(avatar, turretRotationSpeed, *args, **kwargs)
        try:
            self.updateTimer(avatar, turretRotationSpeed, dispersionAngles)
        except Exception as e:
            self.logger.logError(ERROR, e.message)
        return dispersionAngles

    def updateTimer(self, avatar, turretRotationSpeed, dispersionAngles):
        if turretRotationSpeed == 0.0 and not self.ideal_angle:
            self.ideal_angle = dispersionAngles[1]
        if self.period != ARENA_PERIOD.BATTLE:
            return
        diff = round(self.ideal_angle / dispersionAngles[0], 2)
        time = 0.0 if diff >= 1.0 else round(avatar.aimingInfo[1], 1) * (1.0 - diff)
        self.as_updateTimerTextS(self.tpl.format(time, diff), percentToColor(diff, color_blind=self._isColorBlind, as_int=True))

    def onCameraChanged(self, ctrlMode, *args, **kwargs):
        self.is_alive = ctrlMode not in POSTMORTEM_MODES
        self.toggleVisible()
        if not self.is_alive:
            self.ideal_angle = 0

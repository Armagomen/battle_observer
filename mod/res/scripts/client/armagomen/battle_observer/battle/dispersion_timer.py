from armagomen._constants import DISPERSION_TIMER, GLOBAL, POSTMORTEM_MODES
from armagomen.battle_observer.meta.battle.dispersion_timer_meta import DispersionTimerMeta
from armagomen.utils.common import cancelOverride, overrideMethod, percentToColor
from armagomen.utils.logging import logError
from Avatar import PlayerAvatar
from gui.battle_control.avatar_getter import getInputHandler


class DispersionTimer(DispersionTimerMeta):

    def __init__(self):
        super(DispersionTimer, self).__init__()
        self.ideal_angle = 0
        self.isPostmortem = False
        self.tpl = None

    def _populate(self):
        super(DispersionTimer, self)._populate()
        timer = self.settings[DISPERSION_TIMER.TIMER]
        percent = self.settings[DISPERSION_TIMER.PERCENT]

        if timer or percent:
            self.tpl = " - ".join(param[1] for param in ((timer, "{0:.1f}s."), (percent, "{1:d}%")) if param[0])
            ctrl = self.sessionProvider.shared.crosshair
            if ctrl is not None:
                ctrl.onCrosshairPositionChanged += self.as_onCrosshairPositionChangedS
            handler = getInputHandler()
            if handler is not None and hasattr(handler, "onCameraChanged"):
                handler.onCameraChanged += self.onCameraChanged
            overrideMethod(PlayerAvatar, "getOwnVehicleShotDispersionAngle")(self.getDispersionAngle)

    def _dispose(self):
        if self.tpl is not None:
            ctrl = self.sessionProvider.shared.crosshair
            if ctrl is not None:
                ctrl.onCrosshairPositionChanged -= self.as_onCrosshairPositionChangedS
            handler = getInputHandler()
            if handler is not None and hasattr(handler, "onCameraChanged"):
                handler.onCameraChanged -= self.onCameraChanged
            cancelOverride(PlayerAvatar, "getOwnVehicleShotDispersionAngle", "getDispersionAngle")
        super(DispersionTimer, self)._dispose()

    def getDispersionAngle(self, base, avatar, turretRotationSpeed, *args, **kwargs):
        dispersionAngles = base(avatar, turretRotationSpeed, *args, **kwargs)
        try:
            self.updateTimer(avatar, turretRotationSpeed, dispersionAngles)
        except Exception as e:
            logError(e)
        return dispersionAngles

    def updateTimer(self, avatar, turretRotationSpeed, dispersionAngles):
        if self.isPostmortem:
            self.as_updateTimerTextS(GLOBAL.EMPTY_LINE, 0)
        else:
            if turretRotationSpeed == 0.0 and not self.ideal_angle:
                self.ideal_angle = dispersionAngles[1]
            diff = round(self.ideal_angle / dispersionAngles[0], 2)
            time = 0.0 if diff >= 1.0 else round(avatar.aimingInfo[1], 1) * (1.0 - diff)
            self.as_updateTimerTextS(self.tpl.format(time, int(round(diff * 100))),
                                     percentToColor(diff, color_blind=self._isColorBlind, as_int=True))

    def onCameraChanged(self, ctrlMode, vehicleID=None):
        self.isPostmortem = ctrlMode in POSTMORTEM_MODES
        if self.isPostmortem:
            self.ideal_angle = 0
            self.as_updateTimerTextS(GLOBAL.EMPTY_LINE, 0)

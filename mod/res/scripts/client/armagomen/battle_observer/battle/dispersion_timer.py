from collections import defaultdict

from armagomen._constants import DISPERSION_TIMER, GLOBAL, POSTMORTEM_MODES
from armagomen.battle_observer.meta.battle.dispersion_timer_meta import DispersionTimerMeta
from armagomen.utils.common import cancelOverride, overrideMethod
from armagomen.utils.logging import logError
from Avatar import PlayerAvatar
from gui.battle_control.avatar_getter import getInputHandler


class DispersionTimer(DispersionTimerMeta):

    def __init__(self):
        super(DispersionTimer, self).__init__()
        self.macro = defaultdict(float, timer=0.0, percent=0)
        self.ideal_angle = 0
        self.isPostmortem = False
        self.tpl = ""

    def _populate(self):
        super(DispersionTimer, self)._populate()

        if self.settings[DISPERSION_TIMER.TIMER] and self.settings[DISPERSION_TIMER.PERCENT]:
            self.tpl = "<font color='{0}'>{1:.1f}s. - {2:d}%</font>"
        elif self.settings[DISPERSION_TIMER.PERCENT]:
            self.tpl = "<font color='{0}'>{2:d}%</font>"
        elif self.settings[DISPERSION_TIMER.TIMER]:
            self.tpl = "<font color='{0}'>{1:.1f}s.</font>"

        if self.tpl:
            ctrl = self.sessionProvider.shared.crosshair
            if ctrl is not None:
                ctrl.onCrosshairPositionChanged += self.as_onCrosshairPositionChangedS
            handler = getInputHandler()
            if handler is not None and hasattr(handler, "onCameraChanged"):
                handler.onCameraChanged += self.onCameraChanged
        overrideMethod(PlayerAvatar, "getOwnVehicleShotDispersionAngle")(self.getOwnVehicleShotDispersionAngle)

    def _dispose(self):
        if self.tpl:
            ctrl = self.sessionProvider.shared.crosshair
            if ctrl is not None:
                ctrl.onCrosshairPositionChanged -= self.as_onCrosshairPositionChangedS
            handler = getInputHandler()
            if handler is not None and hasattr(handler, "onCameraChanged"):
                handler.onCameraChanged -= self.onCameraChanged
                cancelOverride(PlayerAvatar, "getOwnVehicleShotDispersionAngle", "getOwnVehicleShotDispersionAngle")
        super(DispersionTimer, self)._dispose()

    def getOwnVehicleShotDispersionAngle(self, base, avatar, turretRotationSpeed, **kwargs):
        dispersionAngles = base(avatar, turretRotationSpeed, **kwargs)
        try:
            self.updateTimer(avatar, turretRotationSpeed, dispersionAngles)
        except Exception as e:
            logError(e)
        return dispersionAngles

    def updateTimer(self, avatar, turretRotationSpeed, dispersionAngles):
        if self.isPostmortem:
            self.as_updateTimerTextS(GLOBAL.EMPTY_LINE)
        else:
            if turretRotationSpeed == 0.0 and not self.ideal_angle:
                self.ideal_angle = dispersionAngles[1]
            diff = round(self.ideal_angle / dispersionAngles[0], 2)
            changeColor = diff >= 1.0
            self.as_updateTimerTextS(self.tpl.format(self.settings[DISPERSION_TIMER.DONE_COLOR if changeColor else GLOBAL.COLOR],
                                                     0.0 if changeColor else round(avatar.aimingInfo[1], 1) * (1.0 - diff),
                                                     int(round(diff * 100))
                                                     ))

    def onCameraChanged(self, ctrlMode, vehicleID=None):
        self.isPostmortem = ctrlMode in POSTMORTEM_MODES
        if self.isPostmortem:
            self.as_updateTimerTextS(GLOBAL.EMPTY_LINE)

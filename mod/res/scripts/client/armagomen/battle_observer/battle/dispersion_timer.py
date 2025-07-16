from collections import deque

from armagomen._constants import DISPERSION_TIMER, GLOBAL, POSTMORTEM_MODES
from armagomen.battle_observer.meta.battle.dispersion_timer_meta import DispersionTimerMeta
from armagomen.utils.common import cancelOverride, overrideMethod, percentToRGB
from armagomen.utils.logging import logError
from Avatar import PlayerAvatar
from gui.battle_control.avatar_getter import getInputHandler


class DispersionTimer(DispersionTimerMeta):

    def __init__(self):
        super(DispersionTimer, self).__init__()
        self.ideal_angle = 0
        self.isPostmortem = False
        self.tpl = None
        self.temp = deque(maxlen=3)

    def _populate(self):
        super(DispersionTimer, self)._populate()
        timer = self.settings[DISPERSION_TIMER.TIMER]
        percent = self.settings[DISPERSION_TIMER.PERCENT]

        if timer or percent:
            time_str = "{1:.1f}s." if timer else ""
            percent_str = "{2:d}%" if percent else ""
            separator = " - " if timer and percent else ""
            self.tpl = "<font color='{0}'>{1}{2}{3}</font>".format('{0}', time_str, separator, percent_str)

            ctrl = self.sessionProvider.shared.crosshair
            if ctrl is not None:
                ctrl.onCrosshairPositionChanged += self.as_onCrosshairPositionChangedS
            handler = getInputHandler()
            if handler is not None and hasattr(handler, "onCameraChanged"):
                handler.onCameraChanged += self.onCameraChanged
        overrideMethod(PlayerAvatar, "getOwnVehicleShotDispersionAngle")(self.getOwnVehicleShotDispersionAngle)

    def _dispose(self):
        if self.tpl is not None:
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
            time = 0.0 if changeColor else round(avatar.aimingInfo[1], 1) * (1.0 - diff)
            if time > 2.0:
                self.temp.append(time)
                time = sum(self.temp) / len(self.temp)
            elif len(self.temp):
                self.temp.clear()
            self.as_updateTimerTextS(self.tpl.format(percentToRGB(diff, color_blind=self._isColorBlind), time, int(round(diff * 100))))

    def onCameraChanged(self, ctrlMode, vehicleID=None):
        self.isPostmortem = ctrlMode in POSTMORTEM_MODES
        if self.isPostmortem:
            self.ideal_angle = 0
            self.as_updateTimerTextS(GLOBAL.EMPTY_LINE)

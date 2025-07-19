from armagomen._constants import FLIGHT_TIME, GLOBAL, POSTMORTEM_MODES
from armagomen.battle_observer.meta.battle.flight_time_meta import FlightTimeMeta
from armagomen.utils.common import getPlayer
from gui.battle_control import avatar_getter
from math_utils import VectorConstant


class FlightTime(FlightTimeMeta):

    def __init__(self):
        super(FlightTime, self).__init__()
        self.tpl = None

    def _populate(self):
        super(FlightTime, self)._populate()

        time = self.settings[FLIGHT_TIME.TIME]
        distance = self.settings[FLIGHT_TIME.DISTANCE]

        if time or distance:
            time_str = "{0:.1f} s." if time else ""
            percent_str = "{1:.1f} m." if distance else ""
            separator = " - " if time and distance else ""
            self.tpl = "<font color='{0}'>{1}{2}{3}</font>".format(self.settings[GLOBAL.COLOR], time_str, separator, percent_str)

            ctrl = self.sessionProvider.shared.crosshair
            if ctrl is not None:
                ctrl.onCrosshairPositionChanged += self.as_onCrosshairPositionChangedS
                ctrl.onGunMarkerStateChanged += self.__onGunMarkerStateChanged
            handler = avatar_getter.getInputHandler()
            if handler is not None and hasattr(handler, "onCameraChanged"):
                handler.onCameraChanged += self.onCameraChanged
            self.as_flightTimeS(self.tpl.format(0.0, 0.0))

    def _dispose(self):
        if self.tpl is not None:
            ctrl = self.sessionProvider.shared.crosshair
            if ctrl is not None:
                ctrl.onCrosshairPositionChanged -= self.as_onCrosshairPositionChangedS
                ctrl.onGunMarkerStateChanged -= self.__onGunMarkerStateChanged
            handler = avatar_getter.getInputHandler()
            if handler is not None and hasattr(handler, "onCameraChanged"):
                handler.onCameraChanged -= self.onCameraChanged
        super(FlightTime, self)._dispose()

    def onCameraChanged(self, ctrlMode, *args, **kwargs):
        if ctrlMode in POSTMORTEM_MODES:
            self.as_flightTimeS(GLOBAL.EMPTY_LINE)

    def __onGunMarkerStateChanged(self, markerType, position, *args, **kwargs):
        player = getPlayer()
        if player is None:
            return self.as_flightTimeS(GLOBAL.EMPTY_LINE)
        shotPos, shotVec = player.gunRotator.getCurShotPosition()
        flatDist = position.flatDistTo(shotPos)
        time = flatDist / shotVec.flatDistTo(VectorConstant.Vector3Zero)
        self.as_flightTimeS(self.tpl.format(time, flatDist))

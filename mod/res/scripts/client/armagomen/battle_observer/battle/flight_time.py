from collections import defaultdict

from armagomen._constants import FLIGHT_TIME, GLOBAL, POSTMORTEM_MODES
from armagomen.battle_observer.meta.battle.flight_time_meta import FlightTimeMeta
from armagomen.utils.common import getPlayer
from gui.battle_control import avatar_getter
from math_utils import VectorConstant


class FlightTime(FlightTimeMeta):

    def __init__(self):
        super(FlightTime, self).__init__()
        self.macrosDict = defaultdict(lambda: GLOBAL.CONFIG_ERROR, flightTime=GLOBAL.ZERO, distance=GLOBAL.ZERO)

    def _populate(self):
        super(FlightTime, self)._populate()
        ctrl = self.sessionProvider.shared.crosshair
        if ctrl is not None:
            ctrl.onCrosshairPositionChanged += self.as_onCrosshairPositionChangedS
            ctrl.onGunMarkerStateChanged += self.__onGunMarkerStateChanged
        handler = avatar_getter.getInputHandler()
        if handler is not None and hasattr(handler, "onCameraChanged"):
            handler.onCameraChanged += self.onCameraChanged

    def _dispose(self):
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
        self.macrosDict[FLIGHT_TIME.M_FLIGHT_TIME] = flatDist / shotVec.flatDistTo(VectorConstant.Vector3Zero)
        self.macrosDict[FLIGHT_TIME.M_DISTANCE] = flatDist
        self.as_flightTimeS(self.settings[FLIGHT_TIME.TEMPLATE] % self.macrosDict)

import math_utils
from armagomen._constants import FLIGHT_TIME, GLOBAL, POSTMORTEM_MODES
from armagomen.battle_observer.meta.battle.flight_time_meta import FlightTimeMeta
from armagomen.utils.common import getPlayer
from gui.battle_control import avatar_getter
from items.utils import getVehicleShotSpeedByFactors


class FlightTime(FlightTimeMeta):

    def __init__(self):
        super(FlightTime, self).__init__()
        self.tpl = None

    def _populate(self):
        super(FlightTime, self)._populate()
        time = self.settings[FLIGHT_TIME.TIME]
        distance = self.settings[FLIGHT_TIME.DISTANCE]

        if time or distance:
            self.tpl = " - ".join(param[1] for param in ((time, "{0:.2f}s"), (distance, "{1:.1f}m")) if param[0])
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

    def __onGunMarkerStateChanged(self, markerType, gunMarkerState, *args, **kwargs):
        player = getPlayer()
        if player is None:
            return self.as_flightTimeS(GLOBAL.EMPTY_LINE)
        targetPosition = gunMarkerState.position
        vDesc = player.getVehicleDescriptor()
        gunInstallationSlot = vDesc.gunInstallations[gunMarkerState.gunInstallationIndex]
        shot = vDesc.shot if gunInstallationSlot.isMainInstallation() else gunInstallationSlot.gun.shots[0]
        vehAttrs = self.sessionProvider.shared.feedback.getVehicleAttrs()
        shotPos, shotVel, _ = player.gunRotator.getShotParams(targetPosition, ignoreYawLimits=True, overrideShotDescr=shot)
        flyTime, dist = self.getFlyData(targetPosition, shotVel, shotPos, shot, vehAttrs)
        self.as_flightTimeS(self.tpl.format(flyTime, dist))

    @staticmethod
    def getFlyData(targetPosition, shotVelVector, shotPos, shot, vehAttrs):
        distAxis = targetPosition - shotPos
        distAxis.y = 0
        distAxis.normalise()
        shotVelDA = shotVelVector.dot(distAxis)
        if math_utils.almostZero(shotVelDA):
            shotVel, _ = getVehicleShotSpeedByFactors(vehAttrs, shot.speed)
            if shotVel != 0:
                return shot.maxDistance / shotVel, shot.maxDistance
            return 0.0, 0
        shotVelDA, _ = getVehicleShotSpeedByFactors(vehAttrs, shotVelDA)
        dist = targetPosition.dot(distAxis) - shotPos.dot(distAxis)
        return dist / shotVelDA, dist

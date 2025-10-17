from armagomen._constants import FLIGHT_TIME, GLOBAL, POSTMORTEM_MODES
from armagomen.battle_observer.meta.battle.flight_time_meta import FlightTimeMeta
from armagomen.utils.common import getPlayer
from AvatarInputHandler.spg_marker_helpers.spg_marker_helpers import getSPGShotFlyTime
from gui.battle_control import avatar_getter


class FlightTime(FlightTimeMeta):

    def __init__(self):
        super(FlightTime, self).__init__()
        self.tpl = None

    def _populate(self):
        super(FlightTime, self)._populate()
        time = self.settings[FLIGHT_TIME.TIME]
        distance = self.settings[FLIGHT_TIME.DISTANCE]

        if time or distance:
            self.tpl = " - ".join(param[1] for param in ((time, "{0:.2f}s."), (distance, "{1:.1f}m.")) if param[0])
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
        gunMarkerPosition = gunMarkerState.position
        vDesc = player.getVehicleDescriptor()
        gunInstallationSlot = vDesc.gunInstallations[gunMarkerState.gunInstallationIndex]
        shot = vDesc.shot if gunInstallationSlot.isMainInstallation() else gunInstallationSlot.gun.shots[0]
        vehAttrs = self.sessionProvider.shared.feedback.getVehicleAttrs()
        shotPos, shotVel, shotGravity = player.gunRotator.getShotParams(gunMarkerPosition, ignoreYawLimits=True, overrideShotDescr=shot)
        flyTime = getSPGShotFlyTime(gunMarkerPosition, shotVel, shotPos, shot.maxDistance, shot.speed, vehAttrs)
        self.as_flightTimeS(self.tpl.format(flyTime, gunMarkerPosition.flatDistTo(shotPos)))

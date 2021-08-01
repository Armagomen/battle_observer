from collections import defaultdict

from armagomen.battle_observer.meta.battle.flight_time_meta import FlightTimeMeta
from armagomen.constants import FLIGHT_TIME, GLOBAL, POSTMORTEM
from armagomen.utils.common import vector3
from gui.battle_control import avatar_getter
from gui.shared.gui_items.Vehicle import VEHICLE_CLASS_NAME

VECTOR = vector3(GLOBAL.F_ZERO, GLOBAL.F_ZERO, GLOBAL.F_ZERO)


class FlightTime(FlightTimeMeta):

    def __init__(self):
        super(FlightTime, self).__init__()
        self.template = None
        self.shared = self.sessionProvider.shared
        self.macrosDict = defaultdict(lambda: GLOBAL.CONFIG_ERROR, flightTime=GLOBAL.ZERO, distance=GLOBAL.ZERO)

    def _populate(self):
        super(FlightTime, self)._populate()
        self.template = self.settings[FLIGHT_TIME.TEMPLATE]
        ctrl = self.sessionProvider.shared.crosshair
        if ctrl is not None:
            ctrl.onCrosshairPositionChanged += self.as_onCrosshairPositionChanged
        self.as_startUpdateS(self.settings)

    def _dispose(self):
        ctrl = self.sessionProvider.shared.crosshair
        if ctrl is not None:
            ctrl.onCrosshairPositionChanged -= self.as_onCrosshairPositionChanged
        super(FlightTime, self)._dispose()

    def showOnCurrentTank(self):
        if self.settings[FLIGHT_TIME.SPG_ONLY]:
            return VEHICLE_CLASS_NAME.SPG in self._player.vehicleTypeDescriptor.type.tags
        return True

    def onEnterBattlePage(self):
        super(FlightTime, self).onEnterBattlePage()
        if self.showOnCurrentTank():
            if self.shared.crosshair:
                self.shared.crosshair.onGunMarkerStateChanged += self.__onGunMarkerStateChanged
            handler = avatar_getter.getInputHandler()
            if handler is not None:
                handler.onCameraChanged += self.onCameraChanged

    def onExitBattlePage(self):
        if self.showOnCurrentTank():
            if self.shared.crosshair:
                self.shared.crosshair.onGunMarkerStateChanged -= self.__onGunMarkerStateChanged
            handler = avatar_getter.getInputHandler()
            if handler is not None:
                handler.onCameraChanged += self.onCameraChanged
        super(FlightTime, self).onExitBattlePage()

    def onCameraChanged(self, ctrlMode, *args, **kwargs):
        if ctrlMode in POSTMORTEM.MODES:
            self.as_flightTimeS(GLOBAL.EMPTY_LINE)

    def __onGunMarkerStateChanged(self, markerType, position, *args, **kwargs):
        shotPos, shotVec = self._player.gunRotator.getCurShotPosition()
        flatDist = position.flatDistTo(shotPos)
        self.macrosDict[FLIGHT_TIME.M_FLIGHT_TIME] = flatDist / shotVec.flatDistTo(VECTOR)
        self.macrosDict[FLIGHT_TIME.M_DISTANCE] = flatDist
        self.as_flightTimeS(self.template % self.macrosDict)

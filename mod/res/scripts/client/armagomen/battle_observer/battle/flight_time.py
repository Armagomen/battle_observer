from collections import defaultdict

from armagomen.battle_observer.core import config
from armagomen.battle_observer.core.constants import FLIGHT_TIME, GLOBAL, POSTMORTEM
from armagomen.battle_observer.meta.battle.flight_time_meta import FlightTimeMeta
from armagomen.utils.common import vector3
from gui.battle_control import avatar_getter
from gui.shared.gui_items.Vehicle import VEHICLE_CLASS_NAME

VECTOR = vector3(GLOBAL.F_ZERO, GLOBAL.F_ZERO, GLOBAL.F_ZERO)
config = config.flight_time


class FlightTime(FlightTimeMeta):

    def __init__(self):
        super(FlightTime, self).__init__()
        self.template = config[FLIGHT_TIME.TEMPLATE]
        self.isSPG = False
        self.shared = self.sessionProvider.shared
        self.macrosDict = defaultdict(lambda: GLOBAL.CONFIG_ERROR, flightTime=GLOBAL.ZERO, distance=GLOBAL.ZERO)

    def _populate(self):
        super(FlightTime, self)._populate()
        self.as_startUpdateS(config)

    def checkSpgOnlyConfig(self):
        if config[FLIGHT_TIME.SPG_ONLY]:
            return self.isSPG
        return True

    def onEnterBattlePage(self):
        super(FlightTime, self).onEnterBattlePage()
        self.isSPG = VEHICLE_CLASS_NAME.SPG in self._player.vehicleTypeDescriptor.type.tags
        if self.checkSpgOnlyConfig():
            if self.shared.crosshair:
                self.shared.crosshair.onGunMarkerStateChanged += self.__onGunMarkerStateChanged
            handler = avatar_getter.getInputHandler()
            if handler is not None:
                handler.onCameraChanged += self.onCameraChanged

    def onExitBattlePage(self):
        if self.checkSpgOnlyConfig():
            if self.shared.crosshair:
                self.shared.crosshair.onGunMarkerStateChanged -= self.__onGunMarkerStateChanged
            handler = avatar_getter.getInputHandler()
            if handler is not None:
                handler.onCameraChanged += self.onCameraChanged
        super(FlightTime, self).onExitBattlePage()

    def onCameraChanged(self, ctrlMode, *args, **kwargs):
        self.as_onControlModeChangedS(ctrlMode)
        if ctrlMode in POSTMORTEM.MODES:
            self.as_flightTimeS(GLOBAL.EMPTY_LINE)

    def __onGunMarkerStateChanged(self, markerType, position, *args, **kwargs):
        shotPos, shotVec = self._player.gunRotator.getCurShotPosition()
        flatDist = position.flatDistTo(shotPos)
        self.macrosDict[FLIGHT_TIME.M_FLIGHT_TIME] = flatDist / shotVec.flatDistTo(VECTOR)
        self.macrosDict[FLIGHT_TIME.M_DISTANCE] = flatDist
        self.as_flightTimeS(self.template % self.macrosDict)

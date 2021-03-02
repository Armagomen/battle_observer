from collections import defaultdict

from gui.battle_control import avatar_getter
from gui.shared.gui_items.Vehicle import VEHICLE_CLASS_NAME
from ..core import cfg, cache
from ..core.bo_constants import FLIGHT_TIME, GLOBAL, POSTMORTEM
from ..core.utils.common import vector3
from ..meta.battle.flight_time_meta import FlightTimeMeta

VECTOR = vector3(GLOBAL.F_ZERO, GLOBAL.F_ZERO, GLOBAL.F_ZERO)
config = cfg.flight_time


class FlightTime(FlightTimeMeta):

    def __init__(self):
        super(FlightTime, self).__init__()
        self.template = config[FLIGHT_TIME.TEMPLATE]
        self.isSPG = False
        self.shared = self.sessionProvider.shared
        self.macrosDict = defaultdict(lambda: GLOBAL.CONFIG_ERROR,
                                      {FLIGHT_TIME.M_FLIGHT_TIME: GLOBAL.ZERO, FLIGHT_TIME.M_DISTANCE: GLOBAL.ZERO})

    def _populate(self):
        super(FlightTime, self)._populate()
        self.as_startUpdateS(config)

    def checkSpgOnlyConfig(self):
        if config[FLIGHT_TIME.SPG_ONLY]:
            return self.isSPG
        return True

    def onEnterBattlePage(self):
        super(FlightTime, self).onEnterBattlePage()
        self.isSPG = VEHICLE_CLASS_NAME.SPG in cache.player.vehicleTypeDescriptor.type.tags
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
        shotPos, shotVec = cache.player.gunRotator.getCurShotPosition()
        flatDist = position.flatDistTo(shotPos)
        self.macrosDict[FLIGHT_TIME.M_FLIGHT_TIME] = flatDist / shotVec.flatDistTo(VECTOR)
        self.macrosDict[FLIGHT_TIME.M_DISTANCE] = flatDist
        self.as_flightTimeS(self.template % self.macrosDict)

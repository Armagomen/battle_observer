from collections import defaultdict

from armagomen.battle_observer.meta.battle.distance_to_enemy_meta import DistanceMeta
from armagomen.constants import GLOBAL, DISTANCE, POSTMORTEM
from armagomen.utils.timers import CyclicTimerEvent
from gui.battle_control import avatar_getter


class Distance(DistanceMeta):

    def __init__(self):
        super(Distance, self).__init__()
        self.template = None
        self.shared = self.sessionProvider.shared
        self.macrosDict = defaultdict(lambda: GLOBAL.CONFIG_ERROR, distance=GLOBAL.ZERO, name=GLOBAL.EMPTY_LINE)
        self.timeEvent = CyclicTimerEvent(0.2, self.updateDistance)
        self.positionsCache = {}
        self.isPostmortem = False
        self.vehicles = {}

    def _populate(self):
        super(Distance, self)._populate()
        self.template = self.settings[DISTANCE.TEMPLATE]
        self.as_startUpdateS(self.settings)

    def __onVehicleEnterWorld(self, vProxy, vInfo, _):
        if self.isPostmortem:
            return
        if self._player.team != vInfo.team and vProxy.isAlive():
            self.vehicles[vProxy.id] = vProxy
            self.positionsCache[vProxy.id] = vProxy.position

    def __onVehicleLeaveWorld(self, vId):
        if self.isPostmortem:
            return
        if vId in self.vehicles and not self.vehicles[vId].isAlive():
            del self.vehicles[vId]
            del self.positionsCache[vId]

    def updateDistance(self):
        distance = GLOBAL.ZERO
        vehicleID = GLOBAL.ZERO
        for vehID, entity in self.vehicles.iteritems():
            if not entity.isDestroyed and entity.position != self.positionsCache[vehID]:
                self.positionsCache[vehID] = entity.position
            dist = int(self._player.vehicle.position.distTo(self.positionsCache[vehID]))
            if distance and dist >= distance:
                continue
            distance = dist
            vehicleID = vehID
        if distance:
            self.macrosDict[DISTANCE.TANK_NAME] = self._arenaDP.getVehicleInfo(vehicleID).vehicleType.shortName
            self.macrosDict[DISTANCE.DIST] = distance
            self.as_setDistanceS(self.template % self.macrosDict)
        else:
            self.as_setDistanceS(GLOBAL.EMPTY_LINE)

    def onEnterBattlePage(self):
        super(Distance, self).onEnterBattlePage()
        handler = avatar_getter.getInputHandler()
        if handler is not None:
            handler.onCameraChanged += self.onCameraChanged
        ctrl = self.sessionProvider.shared.feedback
        ctrl.onMinimapVehicleAdded += self.__onVehicleEnterWorld
        ctrl.onMinimapVehicleRemoved += self.__onVehicleLeaveWorld
        self.timeEvent.start()

    def onExitBattlePage(self):
        self.timeEvent.stop()
        handler = avatar_getter.getInputHandler()
        if handler is not None:
            handler.onCameraChanged -= self.onCameraChanged
        ctrl = self.sessionProvider.shared.feedback
        ctrl.onMinimapVehicleAdded -= self.__onVehicleEnterWorld
        ctrl.onMinimapVehicleRemoved -= self.__onVehicleLeaveWorld
        super(Distance, self).onExitBattlePage()

    def onCameraChanged(self, ctrlMode, *args, **kwargs):
        self.as_onControlModeChangedS(ctrlMode)
        self.isPostmortem = ctrlMode in POSTMORTEM.MODES
        if self.isPostmortem:
            self.timeEvent.stop()
            self.positionsCache.clear()
            self.vehicles.clear()
            self.as_setDistanceS(GLOBAL.EMPTY_LINE)

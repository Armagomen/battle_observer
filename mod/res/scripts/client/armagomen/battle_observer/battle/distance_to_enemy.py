from collections import defaultdict

from armagomen._constants import DISTANCE, GLOBAL, POSTMORTEM_MODES
from armagomen.battle_observer.meta.battle.distance_to_enemy_meta import DistanceMeta
from armagomen.utils.common import getPlayer
from gui.battle_control.avatar_getter import getDistanceToTarget, getInputHandler
from gui.battle_control.battle_constants import PLAYER_GUI_PROPS


class Distance(DistanceMeta):

    def __init__(self):
        super(Distance, self).__init__()
        self.macrosDict = defaultdict(lambda: GLOBAL.CONFIG_ERROR, distance=GLOBAL.ZERO, name=GLOBAL.EMPTY_LINE)
        self.isPostmortem = False
        self.vehicles = {}

    def _populate(self):
        super(Distance, self)._populate()
        ctrl = self.sessionProvider.shared.crosshair
        if ctrl is not None:
            ctrl.onCrosshairPositionChanged += self.as_onCrosshairPositionChangedS
        handler = getInputHandler()
        if handler is not None and hasattr(handler, "onCameraChanged"):
            handler.onCameraChanged += self.onCameraChanged
        feedback = self.sessionProvider.shared.feedback
        if feedback is not None:
            feedback.onVehicleMarkerAdded += self.onVehicleMarkerAdded
            feedback.onVehicleMarkerRemoved += self.onVehicleMarkerRemoved
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onVehicleKilled += self.onVehicleMarkerRemoved

    def _dispose(self):
        ctrl = self.sessionProvider.shared.crosshair
        if ctrl is not None:
            ctrl.onCrosshairPositionChanged -= self.as_onCrosshairPositionChangedS
        self.as_setUpdateEnabled(False)
        handler = getInputHandler()
        if handler is not None and hasattr(handler, "onCameraChanged"):
            handler.onCameraChanged -= self.onCameraChanged
        feedback = self.sessionProvider.shared.feedback
        if feedback is not None:
            feedback.onVehicleMarkerAdded -= self.onVehicleMarkerAdded
            feedback.onVehicleMarkerRemoved -= self.onVehicleMarkerRemoved
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onVehicleKilled -= self.onVehicleMarkerRemoved
        super(Distance, self)._dispose()

    def onVehicleMarkerAdded(self, vProxy, vInfo, guiProps):
        if self.isPostmortem:
            return
        if guiProps == PLAYER_GUI_PROPS.enemy and vProxy.isAlive():
            self.vehicles[vInfo.vehicleID] = vProxy
        self.as_setUpdateEnabled(bool(self.vehicles))

    def onVehicleMarkerRemoved(self, vehicleID, *args, **kwargs):
        if self.isPostmortem:
            return
        if vehicleID in self.vehicles:
            self.vehicles.pop(vehicleID)
        self.as_setUpdateEnabled(bool(self.vehicles))

    def getUpdatedDistance(self):
        distance = None
        vehicle_name = None
        player = getPlayer()
        for entity in self.vehicles.itervalues():
            dist = getDistanceToTarget(entity, avatar=player)
            if distance is None or dist < distance:
                distance = dist
                vehicle_name = entity.typeDescriptor.type.shortUserString
        self.macrosDict[DISTANCE.TANK_NAME] = vehicle_name
        self.macrosDict[DISTANCE.DIST] = distance
        return self.settings[DISTANCE.TEMPLATE] % self.macrosDict

    def onCameraChanged(self, ctrlMode, *args, **kwargs):
        self.isPostmortem = ctrlMode in POSTMORTEM_MODES
        if self.isPostmortem:
            self.vehicles.clear()
            self.as_setUpdateEnabled(False)

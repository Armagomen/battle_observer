from collections import defaultdict

from PlayerEvents import g_playerEvents
from armagomen.battle_observer.meta.battle.distance_to_enemy_meta import DistanceMeta
from armagomen.constants import GLOBAL, DISTANCE, POSTMORTEM
from armagomen.utils.common import logDebug
from armagomen.utils.timers import CyclicTimerEvent
from constants import ARENA_PERIOD, ARENA_PERIOD_NAMES
from gui.battle_control import avatar_getter


class Distance(DistanceMeta):

    def __init__(self):
        super(Distance, self).__init__()
        self.macrosDict = defaultdict(lambda: GLOBAL.CONFIG_ERROR, distance=GLOBAL.ZERO, name=GLOBAL.EMPTY_LINE)
        self.timeEvent = None
        self.isPostmortem = False
        self.vehicles = {}

    def _populate(self):
        super(Distance, self)._populate()
        ctrl = self.sessionProvider.shared.crosshair
        if ctrl is not None:
            ctrl.onCrosshairPositionChanged += self.as_onCrosshairPositionChangedS
        g_playerEvents.onArenaPeriodChange += self.onArenaPeriodChange

    def _dispose(self):
        ctrl = self.sessionProvider.shared.crosshair
        if ctrl is not None:
            ctrl.onCrosshairPositionChanged -= self.as_onCrosshairPositionChangedS
        g_playerEvents.onArenaPeriodChange -= self.onArenaPeriodChange
        super(Distance, self)._dispose()

    def onArenaPeriodChange(self, period, *args):
        if period == ARENA_PERIOD.BATTLE and self.timeEvent is None:
            self.timeEvent = CyclicTimerEvent(0.5, self.updateDistance)
            self.timeEvent.start()
        elif self.timeEvent is not None:
            self.timeEvent.stop()
            self.timeEvent = None
        logDebug("Distance: onArenaPeriodChange: {}", ARENA_PERIOD_NAMES[period])

    def onEnterBattlePage(self):
        super(Distance, self).onEnterBattlePage()
        handler = avatar_getter.getInputHandler()
        if handler is not None and hasattr(handler, "onCameraChanged"):
            handler.onCameraChanged += self.onCameraChanged
        feedback = self.sessionProvider.shared.feedback
        if feedback is not None:
            feedback.onMinimapVehicleAdded += self.onMinimapVehicleAdded
            feedback.onMinimapVehicleRemoved += self.removeVehicle
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onVehicleKilled += self.removeVehicle

    def onExitBattlePage(self):
        if self.timeEvent is not None:
            self.timeEvent.stop()
            self.timeEvent = None
        handler = avatar_getter.getInputHandler()
        if handler is not None and hasattr(handler, "onCameraChanged"):
            handler.onCameraChanged -= self.onCameraChanged
        feedback = self.sessionProvider.shared.feedback
        if feedback is not None:
            feedback.onMinimapVehicleAdded -= self.onMinimapVehicleAdded
            feedback.onMinimapVehicleRemoved -= self.removeVehicle
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onVehicleKilled -= self.removeVehicle
        super(Distance, self).onExitBattlePage()

    def onMinimapVehicleAdded(self, vProxy, vInfo, _):
        if self.isPostmortem:
            return
        if self._player.team != vInfo.team and vProxy.isAlive():
            self.vehicles[vInfo.vehicleID] = vProxy

    def removeVehicle(self, vehicleID, *args, **kwargs):
        if vehicleID in self.vehicles:
            self.vehicles.pop(vehicleID)

    def updateDistance(self):
        distance = None
        vehicleName = None
        for entity in self.vehicles.itervalues():
            dist = self._player.position.distTo(entity.position)
            if distance is None or dist < distance:
                distance = dist
                vehicleName = entity.typeDescriptor.type.shortUserString
        if distance is None:
            return self.as_setDistanceS(GLOBAL.EMPTY_LINE)
        self.macrosDict[DISTANCE.TANK_NAME] = vehicleName
        self.macrosDict[DISTANCE.DIST] = distance
        self.as_setDistanceS(self.settings[DISTANCE.TEMPLATE] % self.macrosDict)

    def onCameraChanged(self, ctrlMode, *args, **kwargs):
        self.isPostmortem = ctrlMode in POSTMORTEM.MODES
        if self.isPostmortem:
            if self.timeEvent is not None:
                self.timeEvent.stop()
            self.vehicles.clear()
            self.as_setDistanceS(GLOBAL.EMPTY_LINE)

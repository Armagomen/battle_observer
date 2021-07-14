from collections import defaultdict

from armagomen.battle_observer.meta.battle.distance_to_enemy_meta import DistanceMeta
from armagomen.constants import GLOBAL, DISTANCE, POSTMORTEM
from armagomen.utils.common import getEntity
from armagomen.utils.timers import CyclicTimerEvent
from gui.battle_control import avatar_getter
from gui.battle_control.controllers.battle_field_ctrl import IBattleFieldListener


class Distance(DistanceMeta, IBattleFieldListener):

    def __init__(self):
        super(Distance, self).__init__()
        self.template = None
        self.enemies = set()
        self.shared = self.sessionProvider.shared
        self.macrosDict = defaultdict(lambda: GLOBAL.CONFIG_ERROR, distance=GLOBAL.ZERO, name=GLOBAL.EMPTY_LINE)
        self.timeEvent = CyclicTimerEvent(0.2, self.updateDistance)
        self.positionsCache = {}

    def _populate(self):
        super(Distance, self)._populate()
        self.template = self.settings[DISTANCE.TEMPLATE]
        self.as_startUpdateS(self.settings)

    def updateDeadVehicles(self, aliveAllies, deadAllies, aliveEnemies, deadEnemies):
        self.enemies = aliveEnemies.difference(deadEnemies)
        for vehicleID in deadEnemies:
            if vehicleID in self.positionsCache:
                del self.positionsCache[vehicleID]
        self.updateDistance()

    def updateDistance(self):
        for vehID in self.enemies:
            entity = getEntity(vehID)
            if entity is not None and entity.isAlive():
                self.positionsCache[vehID] = entity.position
            if vehID not in self.positionsCache:
                continue
            dist = int((self.positionsCache[vehID] - self._player.position).length)
            if self.macrosDict[DISTANCE.DIST] and dist >= self.macrosDict[DISTANCE.DIST]:
                continue
            self.macrosDict[DISTANCE.DIST] = dist
            self.macrosDict[DISTANCE.TANK_NAME] = self._arenaDP.getVehicleInfo(vehID).vehicleType.shortName

        if self.macrosDict[DISTANCE.DIST]:
            self.as_setDistanceS(self.template % self.macrosDict)
            self.macrosDict[DISTANCE.DIST] = GLOBAL.ZERO
            self.macrosDict[DISTANCE.TANK_NAME] = GLOBAL.EMPTY_LINE
        else:
            self.as_setDistanceS(GLOBAL.EMPTY_LINE)

    def onEnterBattlePage(self):
        super(Distance, self).onEnterBattlePage()
        handler = avatar_getter.getInputHandler()
        if handler is not None:
            handler.onCameraChanged += self.onCameraChanged
        self.timeEvent.start()

    def onExitBattlePage(self):
        self.timeEvent.stop()
        handler = avatar_getter.getInputHandler()
        if handler is not None:
            handler.onCameraChanged -= self.onCameraChanged
        super(Distance, self).onExitBattlePage()

    def onCameraChanged(self, ctrlMode, *args, **kwargs):
        self.as_onControlModeChangedS(ctrlMode)
        if ctrlMode in POSTMORTEM.MODES:
            self.timeEvent.stop()
            self.positionsCache.clear()
            self.as_setDistanceS(GLOBAL.EMPTY_LINE)

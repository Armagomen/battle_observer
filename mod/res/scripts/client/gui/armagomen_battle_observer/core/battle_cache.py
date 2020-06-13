from collections import defaultdict

from PlayerEvents import g_playerEvents
from avatar_components.team_healthbar_mechanic import TeamHealthbarMechanic
from gui.battle_control.arena_visitor import _ArenaBonusTypeVisitor
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider
from .bo_constants import VEHICLE, COLORS, GLOBAL
from .bw_utils import getEntity
from .config import cfg
from .core import overrideMethod
from .events import g_events


class BattleCache(object):

    def __init__(self):
        self.playersDamage = defaultdict(int)
        self.__teams = {}
        self.errorKeysSet = set()
        self.observers = set()
        self.logsEnable = False
        self.tankAvgDamage = GLOBAL.ZERO
        self.__allyTeam = None
        self.__enemyTeam = None
        self.__arenaDP = None
        self.player = None
        g_playerEvents.onAvatarBecomeNonPlayer += self.clear

    def clear(self):
        self.playersDamage.clear()
        self.observers.clear()
        self.__teams.clear()
        self.tankAvgDamage = GLOBAL.ZERO
        self.__allyTeam = None
        self.__enemyTeam = None
        self.__arenaDP = None
        self.logsEnable = False
        self.player = None

    @property
    def allyTeam(self):
        if self.__allyTeam is None:
            self.__allyTeam = self.arenaDP.getNumberOfTeam()
        return self.__allyTeam

    @property
    def enemyTeam(self):
        if self.__enemyTeam is None:
            self.__enemyTeam = self.arenaDP.getNumberOfTeam(enemy=True)
        return self.__enemyTeam

    @property
    def teams(self):
        if not self.__teams:
            self.__teams = {self.allyTeam: COLORS.C_GREEN, self.enemyTeam: COLORS.C_RED}
        return self.__teams

    @property
    def arenaDP(self):
        if self.__arenaDP is None:
            self.__arenaDP = dependency.instance(IBattleSessionProvider).getArenaDP()
        return self.__arenaDP


cache = BattleCache()


class HealthWorker(object):
    def __init__(self):
        self.__cache = {}
        self.currents = defaultdict(int)
        self.maximums = defaultdict(int)
        self.isCacheUpdateInProgress = False
        g_playerEvents.onAvatarBecomeNonPlayer += self.clear

    @property
    def cache(self):
        if not self.__cache:
            self.updateCache()
        return self.__cache

    def addVehicle(self, vInfo):
        vehicle_id = vInfo.vehicleID
        team = vInfo.team
        maximum = vInfo.vehicleType.maxHealth
        vehicle = self.__cache.get(vehicle_id)
        is_alive = vInfo.isAlive()
        if vehicle is None:
            current = maximum if is_alive else GLOBAL.ZERO
            self.__cache[vehicle_id] = {VEHICLE.CUR: current, VEHICLE.MAX: maximum,
                                        VEHICLE.TEAM: team, VEHICLE.PERCENT: 100.0}
            g_events.onVehicleAddPanels(vehicle_id, vInfo.vehicleType)
        else:
            entity = getEntity(vehicle_id)
            if entity is not None:
                current = max(entity.health, GLOBAL.ZERO)
            else:
                current = maximum if is_alive else GLOBAL.ZERO
            vehicle[VEHICLE.CUR] = current
            vehicle[VEHICLE.MAX] = maximum
            vehicle[VEHICLE.PERCENT] = float(current) / maximum * 100
        if not self.isCacheUpdateInProgress:
            self.setTeamMaximum(team)
            self.setTeamCurrent(team)
            g_events.updateHealthPoints(team, self.getTeamCurrent(team), self.getTeamMaximum(team),
                                        vehicle_id, self.__cache[vehicle_id])

    def getVehicle(self, vehicle_id):
        return self.cache[vehicle_id]

    def getTeamCurrent(self, team):
        if not self.currents[team]:
            self.setTeamCurrent(team)
        return self.currents[team]

    def getTeamMaximum(self, team):
        if not self.maximums[team]:
            self.setTeamMaximum(team)
        return self.maximums[team]

    def setTeamCurrent(self, team):
        current = GLOBAL.ZERO
        for vehicleDict in self.cache.itervalues():
            if vehicleDict[VEHICLE.TEAM] == team:
                current += vehicleDict[VEHICLE.CUR]
        self.currents[team] = current

    def setTeamMaximum(self, team):
        maximum = GLOBAL.ZERO
        for vehicleDict in self.cache.itervalues():
            if vehicleDict[VEHICLE.TEAM] == team:
                maximum += vehicleDict[VEHICLE.MAX]
        self.maximums[team] = maximum

    def setNewHealth(self, team, vehicle_id, health, attackerID=0):
        new_health = max(GLOBAL.ZERO, health)
        vehicle = self.cache[vehicle_id]
        if new_health != vehicle[VEHICLE.CUR]:
            if attackerID and attackerID != vehicle_id:
                cache.playersDamage[attackerID] += vehicle[VEHICLE.CUR] - new_health
                g_events.onPlayersDamaged(attackerID)
            vehicle[VEHICLE.CUR] = new_health
            self.setTeamCurrent(team)
            g_events.updateHealthPoints(team, self.getTeamCurrent(team), self.getTeamMaximum(team),
                                        vehicle_id, vehicle)
            if attackerID != cache.player.playerVehicleID:
                g_events.onMainGunHealthChanged(attackerID, team)

    def updateCache(self):
        self.isCacheUpdateInProgress = True
        for vInfo in cache.arenaDP.getVehiclesInfoIterator():
            if not vInfo.isObserver():
                self.addVehicle(vInfo)
            else:
                cache.observers.add(vInfo.vehicleID)
        for team in cache.teams:
            self.setTeamCurrent(team)
            self.setTeamMaximum(team)
        self.isCacheUpdateInProgress = False

    def clear(self):
        self.__cache.clear()
        self.currents.clear()
        self.maximums.clear()

    @staticmethod
    @overrideMethod(_ArenaBonusTypeVisitor, "hasHealthBar")
    def hasHealthBar(base, *args):
        if cfg.hp_bars[GLOBAL.ENABLED]:
            return False
        return base(*args)

    @staticmethod
    @overrideMethod(TeamHealthbarMechanic, "onBecomePlayer")
    def onBecomePlayer(base, b_self):
        if cfg.hp_bars[GLOBAL.ENABLED]:
            b_self._TeamHealthbarMechanic__enabled = False
            b_self._TeamHealthbarMechanic__lastTeamHealthPercentage = None
        else:
            return base(b_self)


g_health = HealthWorker()

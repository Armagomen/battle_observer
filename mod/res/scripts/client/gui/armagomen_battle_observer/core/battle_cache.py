from collections import defaultdict

from PlayerEvents import g_playerEvents
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider
from .bo_constants import COLORS, GLOBAL


class BattleCache(object):

    def __init__(self):
        self.playersDamage = defaultdict(int)
        self.__teams = {}
        self.errorKeysSet = set()
        self.logsEnable = False
        self.tankAvgDamage = GLOBAL.ZERO
        self.__allyTeam = None
        self.__enemyTeam = None
        self.__arenaDP = None
        self.player = None
        g_playerEvents.onAvatarBecomeNonPlayer += self.clear

    def clear(self):
        self.playersDamage.clear()
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

    @staticmethod
    def getArenaVisitor():
        return dependency.instance(IBattleSessionProvider).arenaVisitor


cache = BattleCache()

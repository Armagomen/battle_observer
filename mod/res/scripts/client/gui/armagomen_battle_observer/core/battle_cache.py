from collections import defaultdict

from PlayerEvents import g_playerEvents
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider


class BattleCache(object):

    def __init__(self):
        self.playersDamage = defaultdict(int)
        self.errorKeysSet = set()
        self.logsEnable = False
        self.tankAvgDamage = 0
        self.player = None
        g_playerEvents.onAvatarBecomeNonPlayer += self.clear

    def clear(self):
        self.playersDamage.clear()
        self.tankAvgDamage = 0
        self.logsEnable = False
        self.player = None

    @property
    def arenaDP(self):
        return dependency.instance(IBattleSessionProvider).getArenaDP()

    @staticmethod
    def getArenaVisitor():
        return dependency.instance(IBattleSessionProvider).arenaVisitor


cache = BattleCache()

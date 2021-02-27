from collections import defaultdict

from PlayerEvents import g_playerEvents
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider
from ..utils.bw_utils import getPlayer


class BattleCache(object):

    def __init__(self):
        self.playersDamage = defaultdict(int)
        self.errorKeysSet = set()
        self.logsEnable = False
        self.tankAvgDamage = 0
        self._player = None
        g_playerEvents.onAvatarBecomeNonPlayer += self.clear

    def clear(self):
        self.playersDamage.clear()
        self.tankAvgDamage = 0
        self.logsEnable = False
        self._player = None

    @property
    def player(self):
        if self._player is None:
            self._player = getPlayer()
        return self._player

    @property
    def arenaDP(self):
        return dependency.instance(IBattleSessionProvider).getArenaDP()

    @staticmethod
    def getArenaVisitor():
        return dependency.instance(IBattleSessionProvider).arenaVisitor

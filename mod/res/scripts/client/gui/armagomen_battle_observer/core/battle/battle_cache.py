from collections import defaultdict

from Event import SafeEvent
from PlayerEvents import g_playerEvents
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider
from ..utils.common import getPlayer


class BattleCache(object):

    def __init__(self):
        g_playerEvents.onAvatarBecomeNonPlayer += self.clear
        self.onModSettingsChanged = SafeEvent()
        self.playersDamage = defaultdict(int)
        self.errorKeysSet = set()
        self.logsEnable = False
        self.tankAvgDamage = 0
        self._player = None

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

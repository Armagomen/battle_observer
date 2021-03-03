from collections import defaultdict

from Event import SafeEvent
from PlayerEvents import g_playerEvents


class BattleCache(object):

    def __init__(self):
        g_playerEvents.onAvatarBecomeNonPlayer += self.clear
        self.onModSettingsChanged = SafeEvent()
        self.playersDamage = defaultdict(int)
        self.errorKeysSet = set()
        self.logsEnable = False
        self.tankAvgDamage = 0

    def clear(self):
        self.playersDamage.clear()
        self.tankAvgDamage = 0
        self.logsEnable = False

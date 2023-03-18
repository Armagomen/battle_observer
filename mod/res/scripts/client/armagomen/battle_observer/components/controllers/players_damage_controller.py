from collections import defaultdict

from Event import SafeEvent
from PlayerEvents import g_playerEvents
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider


class PlayersDamageController(object):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)

    def __init__(self):
        self.onPlayerDamaged = SafeEvent()
        self.playersDamage = defaultdict(int)
        g_playerEvents.onAvatarBecomePlayer += self.start
        g_playerEvents.onAvatarBecomeNonPlayer += self.stop

    def start(self):
        self.playersDamage.clear()
        arena = self.sessionProvider.arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onVehicleHealthChanged += self.onVehicleHealthChanged

    def stop(self):
        arena = self.sessionProvider.arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onVehicleHealthChanged -= self.onVehicleHealthChanged

    def onVehicleHealthChanged(self, targetID, attackerID, damage):
        self.playersDamage[attackerID] += damage
        self.onPlayerDamaged(attackerID, self.playersDamage[attackerID])

    def getPlayerDamage(self, vehicleID):
        return self.playersDamage[vehicleID]


damage_controller = PlayersDamageController()

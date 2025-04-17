from collections import defaultdict

from Event import SafeEvent
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider


class PlayersDamageController(object):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)

    def __init__(self):
        self.onPlayerDamaged = SafeEvent()
        self.__damages = defaultdict(int)

    def start(self):
        self.__damages.clear()
        arena = self.sessionProvider.arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onVehicleHealthChanged += self.onVehicleHealthChanged

    def stop(self):
        arena = self.sessionProvider.arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onVehicleHealthChanged -= self.onVehicleHealthChanged

    def onVehicleHealthChanged(self, targetID, attackerID, damage):
        if damage > 0:
            self.__damages[attackerID] += damage
            self.onPlayerDamaged(attackerID, self.__damages[attackerID])

    def getPlayerDamage(self, vehicleID):
        return self.__damages[vehicleID]

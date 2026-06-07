from collections import defaultdict

from armagomen import IALogger
from Event import SafeEvent
from helpers import dependency
from skeletons.gui.app_loader import GuiGlobalSpaceID, IAppLoader
from skeletons.gui.battle_session import IBattleSessionProvider


class IBOPlayersDamageController(object):
    __slots__ = ()

    def fini(self):
        raise NotImplementedError

    def getPlayerDamage(self, vehicleID):
        raise NotImplementedError


class PlayersDamageController(IBOPlayersDamageController):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)
    appLoader = dependency.descriptor(IAppLoader)
    logger = dependency.descriptor(IALogger)

    def __init__(self):
        self.logger.logInfo("Initializing PlayersDamageController")
        self.onPlayerDamaged = SafeEvent()
        self.__damages = defaultdict(int)
        self.__prevSpaceID = GuiGlobalSpaceID.LOBBY
        self.appLoader.onGUISpaceEntered += self.subscribe
        self.appLoader.onGUISpaceLeft += self.unsubscribe

    def fini(self):
        self.appLoader.onGUISpaceEntered -= self.subscribe
        self.appLoader.onGUISpaceLeft -= self.unsubscribe
        self.logger.logInfo("Finished PlayersDamageController")

    def subscribe(self, spaceID):
        if spaceID == GuiGlobalSpaceID.LOBBY and self.__prevSpaceID in (GuiGlobalSpaceID.BATTLE, GuiGlobalSpaceID.BATTLE_LOADING):
            self.__damages.clear()
        self.__prevSpaceID = spaceID
        if spaceID == GuiGlobalSpaceID.BATTLE:
            arena = self.sessionProvider.arenaVisitor.getArenaSubscription()
            if arena is not None:
                arena.onVehicleHealthChanged += self.__onVehicleHealthChanged

    def unsubscribe(self, spaceID):
        if spaceID == GuiGlobalSpaceID.BATTLE:
            arena = self.sessionProvider.arenaVisitor.getArenaSubscription()
            if arena is not None:
                arena.onVehicleHealthChanged -= self.__onVehicleHealthChanged

    def __onVehicleHealthChanged(self, targetID, attackerID, damage):
        if damage > 0:
            self.__damages[attackerID] += damage
            self.onPlayerDamaged(attackerID, self.__damages[attackerID])

    def getPlayerDamage(self, vehicleID):
        return self.__damages[vehicleID]

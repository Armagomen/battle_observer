from helpers import dependency
from PlayerEvents import g_playerEvents
from skeletons.gui.battle_session import IBattleSessionProvider


class Squad(object):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)
    __slots__ = ("__squad_mans",)

    def __init__(self):
        self.__squad_mans = set()

    def start(self):
        g_playerEvents.onAvatarReady += self.updateSquadMans
        dynSquads = self.sessionProvider.dynamic.dynSquads
        if dynSquads is not None:
            dynSquads.onDynSquadCreatedOrJoined += self.updateSquadMans

    def stop(self):
        g_playerEvents.onAvatarReady -= self.updateSquadMans
        dynSquads = self.sessionProvider.dynamic.dynSquads
        if dynSquads is not None:
            dynSquads.onDynSquadCreatedOrJoined -= self.updateSquadMans

    def updateSquadMans(self, *args):
        self.__squad_mans.clear()
        arenaDP = self.sessionProvider.getArenaDP()
        playerVehicleID = arenaDP.getPlayerVehicleID()
        playerSquad = arenaDP.getVehicleInfo(playerVehicleID).squadIndex
        if not playerSquad:
            self.__squad_mans.add(playerVehicleID)
        else:
            for vInfo in arenaDP.getVehiclesInfoIterator():
                if not vInfo.isEnemy() and playerSquad == vInfo.squadIndex:
                    self.__squad_mans.add(vInfo.vehicleID)

    @property
    def members(self):
        return self.__squad_mans

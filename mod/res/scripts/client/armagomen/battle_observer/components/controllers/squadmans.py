from helpers import dependency
from PlayerEvents import g_playerEvents
from skeletons.gui.battle_session import IBattleSessionProvider


class SquadMans(object):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)

    def __init__(self):
        self.__squad_mans = set()
        g_playerEvents.onAvatarReady += self.updateSquadMans

    def updateSquadMans(self):
        self.__squad_mans.clear()
        arenaDP = self.sessionProvider.getArenaDP()
        for vInfo in arenaDP.getVehiclesInfoIterator():
            if arenaDP.isSquadMan(vInfo.vehicleID):
                self.__squad_mans.add(vInfo.vehicleID)
        self.__squad_mans.add(arenaDP.getPlayerVehicleID(forceUpdate=True))

    @property
    def squad(self):
        return self.__squad_mans

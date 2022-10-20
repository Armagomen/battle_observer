from armagomen.battle_observer.meta.battle.team_bases_meta import TeamBasesMeta
from armagomen.constants import TEAM_BASES
from armagomen.utils.common import callback
from gui.Scaleform.daapi.view.battle.classic.team_bases_panel import getSettingItem
from gui.battle_control.controllers import team_bases_ctrl
from helpers import time_utils

_MAX_INVADERS_COUNT = 3


class TeamBases(TeamBasesMeta, team_bases_ctrl.ITeamBasesListener):

    def __init__(self):
        super(TeamBases, self).__init__()
        self.basesDict = {}

    def onExitBattlePage(self):
        self.removeTeamsBases()
        super(TeamBases, self).onExitBattlePage()

    def addCapturingTeamBase(self, clientID, playerTeam, points, rate, timeLeft, invadersCnt, capturingStopped):
        item = getSettingItem(clientID, playerTeam, self.sessionProvider.arenaVisitor.type.getID())
        self.basesDict[clientID] = item
        self.as_addTeamBaseS(item.getColor(), points, self.getInvadersCount(invadersCnt),
                             time_utils.getTimeLeftFormat(timeLeft), item.getCapturingString(points))
        if capturingStopped:
            if invadersCnt > 0:
                self.blockTeamBaseCapturing(clientID, points)
            else:
                self.stopTeamBaseCapturing(clientID, points)

    def addCapturedTeamBase(self, clientID, playerTeam, timeLeft, invadersCnt):
        item = self.basesDict.get(clientID, None)
        if item:
            self.as_updateCaptureTextS(item.getColor(), item.getCapturedString())
        else:
            item = getSettingItem(clientID, playerTeam, self.sessionProvider.arenaVisitor.type.getID())
            self.basesDict[clientID] = item
            self.as_addTeamBaseS(item.getColor(), TEAM_BASES.HUNDRED, self.getInvadersCount(invadersCnt),
                                 time_utils.getTimeLeftFormat(timeLeft), item.getCapturedString())

    def updateTeamBasePoints(self, clientID, points, rate, timeLeft, invadersCnt):
        item = self.basesDict.get(clientID, None)
        if item:
            self.as_updateBaseS(item.getColor(), points, self.getInvadersCount(invadersCnt),
                                time_utils.getTimeLeftFormat(timeLeft), item.getCapturingString(points))

    def blockTeamBaseCapturing(self, clientID, points):
        item = self.basesDict.get(clientID, None)
        if item:
            self.as_updateCaptureTextS(item.getColor(), item.getBlockedString())

    def stopTeamBaseCapturing(self, clientID, points):
        item = self.basesDict.get(clientID, None)
        if item:
            self.as_updateCaptureTextS(item.getColor(), item.getCapturingString(points))

    def setTeamBaseCaptured(self, clientID, playerTeam):
        item = self.basesDict.get(clientID, None)
        if item:
            self.as_updateCaptureTextS(item.getColor(), item.getCapturedString())
            callback(5.0, self.removeTeamBase, clientID)

    def removeTeamBase(self, clientID):
        if clientID in self.basesDict:
            self.as_removeTeamBaseS(self.basesDict.pop(clientID).getColor())

    def removeTeamsBases(self):
        for item in self.basesDict.itervalues():
            self.as_removeTeamBaseS(item.getColor())
        self.basesDict.clear()

    @staticmethod
    def getInvadersCount(count):
        return count if count <= _MAX_INVADERS_COUNT else _MAX_INVADERS_COUNT

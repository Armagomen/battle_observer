from armagomen._constants import TEAM_BASES
from armagomen.battle_observer.meta.battle.team_bases_meta import TeamBasesMeta
from armagomen.utils.common import addCallback
from gui.battle_control.controllers.team_bases_ctrl import ITeamBasesListener
from gui.Scaleform.daapi.view.battle.classic.team_bases_panel import _getSettingItem
from helpers import time_utils

_MAX_INVADERS_COUNT = 3


class TeamBases(TeamBasesMeta, ITeamBasesListener):

    def __init__(self):
        super(TeamBases, self).__init__()
        self.basesDict = {}

    def _dispose(self):
        self.removeTeamsBases()
        super(TeamBases, self)._dispose()

    def addCapturingTeamBase(self, clientID, playerTeam, points, rate, timeLeft, invadersCnt, capturingStopped):
        item = _getSettingItem(clientID, playerTeam, self.sessionProvider.arenaVisitor.type.getID())
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
            item = _getSettingItem(clientID, playerTeam, self.sessionProvider.arenaVisitor.type.getID())
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
            addCallback(5.0, self.removeTeamBase, clientID)

    def removeTeamBase(self, clientID):
        if clientID in self.basesDict:
            self.as_removeTeamBaseS(self.basesDict.pop(clientID).getColor())

    def removeTeamsBases(self):
        for item in self.basesDict.values():
            self.as_removeTeamBaseS(item.getColor())
        self.basesDict.clear()

    @staticmethod
    def getInvadersCount(count):
        return min(count, _MAX_INVADERS_COUNT)

from gui.Scaleform.daapi.view.battle.classic.team_bases_panel import _getSettingItem
from gui.battle_control.controllers import team_bases_ctrl
from helpers import time_utils
from ..core.bo_constants import TEAM_BASES
from ..core import cfg
from ..core.utils.bw_utils import callback
from ..meta.battle.team_bases_meta import TeamBasesMeta


class TeamBases(TeamBasesMeta, team_bases_ctrl.ITeamBasesListener):

    def __init__(self):
        super(TeamBases, self).__init__()
        self.basesDict = {}

    def _populate(self):
        super(TeamBases, self)._populate()
        self.as_startUpdateS(cfg.team_bases_panel)

    def onExitBattlePage(self):
        self.removeTeamsBases()
        super(TeamBases, self).onExitBattlePage()

    def addCapturingTeamBase(self, clientID, playerTeam, points, rate, timeLeft, invadersCnt, capturingStopped):
        item = _getSettingItem(clientID, playerTeam, self.sessionProvider.arenaVisitor.type.getID())
        self.basesDict[clientID] = item
        self.as_addTeamBaseS(item.getColor(), points, self.getInvadersCountStr(invadersCnt),
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
            self.as_addTeamBaseS(item.getColor(), TEAM_BASES.HUNDRED, self.getInvadersCountStr(invadersCnt),
                                 time_utils.getTimeLeftFormat(timeLeft), item.getCapturedString())

    def updateTeamBasePoints(self, clientID, points, rate, timeLeft, invadersCnt):
        item = self.basesDict.get(clientID, None)
        if item:
            self.as_updateBaseS(item.getColor(), points, rate, self.getInvadersCountStr(invadersCnt),
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
            callback(4.0, lambda: self.removeTeamBase(clientID))

    def removeTeamBase(self, clientID):
        if clientID in self.basesDict:
            self.as_removeTeamBaseS(self.basesDict.pop(clientID).getColor())

    def removeTeamsBases(self):
        for item in self.basesDict.itervalues():
            self.as_removeTeamBaseS(item.getColor())
        self.basesDict.clear()

    @staticmethod
    def getInvadersCountStr(count):
        return str(min(count, 3))

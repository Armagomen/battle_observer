from .base_mod_meta import BaseModMeta


class TeamBasesMeta(BaseModMeta):

    def __init__(self):
        super(TeamBasesMeta, self).__init__()

    def as_addTeamBaseS(self, team, points, invadersCnt, time, text):
        return self.flashObject.as_addTeamBase(team, points, invadersCnt, time, text) if self._isDAAPIInited() else None

    def as_updateBaseS(self, team, points, rate, invadersCnt, time, text):
        return self.flashObject.as_updateBase(team, points, rate, invadersCnt, time,
                                              text) if self._isDAAPIInited() else None

    def as_updateCaptureTextS(self, team, text):
        return self.flashObject.as_updateCaptureText(team, text) if self._isDAAPIInited() else None

    def as_removeTeamBaseS(self, team):
        return self.flashObject.as_removeTeamBase(team) if self._isDAAPIInited() else None

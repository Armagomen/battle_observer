from .base_mod_meta import BaseModMeta


class WgCompMeta(BaseModMeta):

    def __init__(self):
        super(WgCompMeta, self).__init__()

    def as_moveQuestsS(self, move):
        return self.flashObject.as_moveQuests(move) if self._isDAAPIInited() else None

    def as_hideShadowInPreBattleS(self):
        return self.flashObject.as_hideShadowInPreBattle() if self._isDAAPIInited() else None

    def as_hideMessengerS(self):
        return self.flashObject.as_hideMessenger() if self._isDAAPIInited() else None

    def as_enableAnimationS(self, param):
        return self.flashObject.as_enableAnimation(param) if self._isDAAPIInited() else None

    def as_moveTeamBasesPanelS(self):
        return self.flashObject.as_moveTeamBasesPanel() if self._isDAAPIInited() else None

from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider

from ...core.bo_constants import GLOBAL
from ...core.bw_utils import logInfo
from ...core.config import cfg
from ...core.events import g_events


class BaseModMeta(BaseDAAPIComponent):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)

    def __init__(self):
        super(BaseModMeta, self).__init__()
        self._name = "BaseModMeta"
        self._isReplay = self.sessionProvider.isReplayPlaying

    @staticmethod
    def getShadowSettings():
        return cfg.shadow_settings

    def getConfig(self):
        pass

    def _populate(self):
        super(BaseModMeta, self)._populate()
        g_events.onEnterBattlePage += self.onEnterBattlePage
        g_events.onExitBattlePage += self.onExitBattlePage
        if self._isDAAPIInited():
            self.flashObject.setCompVisible(False)
            self._name = self.flashObject.name.split("_")[GLOBAL.ONE]
            if GLOBAL.DEBUG_MODE:
                logInfo("battle module '%s' loaded" % self._name)

    def _dispose(self):
        g_events.onEnterBattlePage -= self.onEnterBattlePage
        g_events.onExitBattlePage -= self.onExitBattlePage
        super(BaseModMeta, self)._dispose()
        if GLOBAL.DEBUG_MODE:
            logInfo("battle module '%s' destroyed" % self._name)

    def onEnterBattlePage(self):
        if self._isDAAPIInited():
            self.flashObject.setCompVisible(True)

    def onExitBattlePage(self):
        if self._isDAAPIInited():
            self.flashObject.as_clearScene()

    def as_startUpdateS(self, *args):
        return self.flashObject.as_startUpdate(*args) if self._isDAAPIInited() else None

    def as_colorBlindS(self, enabled):
        return self.flashObject.as_colorBlind(enabled) if self._isDAAPIInited() else None

    def as_onControlModeChangedS(self, mode):
        return self.flashObject.as_onControlModeChanged(mode) if self._isDAAPIInited() else None


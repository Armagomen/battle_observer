from PlayerEvents import g_playerEvents
from armagomen.battle_observer.core import config
from armagomen.battle_observer.core.bo_constants import GLOBAL
from armagomen.utils.common import logInfo, getPlayer
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider


class BaseModMeta(BaseDAAPIComponent):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)

    def __init__(self):
        super(BaseModMeta, self).__init__()
        self._name = "BaseModMeta"
        self._isReplay = self.sessionProvider.isReplayPlaying
        self._arenaDP = self.sessionProvider.getArenaDP()
        self._arenaVisitor = self.sessionProvider.arenaVisitor
        self._player = getPlayer()

    @staticmethod
    def getShadowSettings():
        return config.shadow_settings

    def getConfig(self):
        pass

    def _populate(self):
        super(BaseModMeta, self)._populate()
        g_playerEvents.onAvatarReady += self.onEnterBattlePage
        g_playerEvents.onAvatarBecomeNonPlayer += self.onExitBattlePage
        if self._isDAAPIInited():
            self.flashObject.setCompVisible(False)
            self._name = self.flashObject.name.split("_")[GLOBAL.ONE]
            if GLOBAL.DEBUG_MODE:
                logInfo("battle module '%s' loaded" % self._name)

    def _dispose(self):
        g_playerEvents.onAvatarReady -= self.onEnterBattlePage
        g_playerEvents.onAvatarBecomeNonPlayer -= self.onExitBattlePage
        super(BaseModMeta, self)._dispose()
        if GLOBAL.DEBUG_MODE:
            logInfo("battle module '%s' destroyed" % self._name)

    def onEnterBattlePage(self):
        self._player = getPlayer()
        if self._isDAAPIInited():
            self.flashObject.setCompVisible(True)

    def onExitBattlePage(self):
        if self._isDAAPIInited():
            self.flashObject.setCompVisible(False)

    def as_startUpdateS(self, *args):
        return self.flashObject.as_startUpdate(*args) if self._isDAAPIInited() else None

    def as_colorBlindS(self, enabled):
        return self.flashObject.as_colorBlind(enabled) if self._isDAAPIInited() else None

    def as_onControlModeChangedS(self, mode):
        return self.flashObject.as_onControlModeChanged(mode) if self._isDAAPIInited() else None

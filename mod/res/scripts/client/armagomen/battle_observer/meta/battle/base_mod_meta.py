from PlayerEvents import g_playerEvents
from armagomen.battle_observer.core import settings
from armagomen.constants import ALIAS_TO_CONFIG_NAME, MAIN, COLORS, GLOBAL
from armagomen.utils.common import logInfo, getPlayer
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent
from gui.shared.personality import ServicesLocator
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider


class BaseModMeta(BaseDAAPIComponent):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)
    settingsCore = ServicesLocator.settingsCore
    isDebug = property(lambda self: settings.main[MAIN.DEBUG])

    def __init__(self):
        super(BaseModMeta, self).__init__()
        self._isReplay = self.sessionProvider.isReplayPlaying
        self._arenaDP = self.sessionProvider.getArenaDP()
        self._arenaVisitor = self.sessionProvider.arenaVisitor
        self._player = getPlayer()
        self.settings = None
        self.colors = settings.colors
        self.vehicle_types = settings.vehicle_types

    def getSettings(self):
        settings_name = ALIAS_TO_CONFIG_NAME.get(self.getAlias())
        if settings_name is not None:
            data = getattr(settings, settings_name, None)
            if self.isDebug:
                logInfo("Settings Name: %s - Settings Data: %s" % (settings_name, str(data)))
            if data is not None:
                return data
        return settings

    @staticmethod
    def animationEnabled():
        return settings.main[MAIN.ENABLE_BARS_ANIMATION]

    @staticmethod
    def getShadowSettings():
        return settings.shadow_settings

    def getConfig(self):
        return self.settings

    def getAlpha(self):
        return round(min(1.0, self.colors[COLORS.GLOBAL][GLOBAL.ALPHA] * 1.4), 2)

    def onDragFinished(self, x, y):
        self.settings["x"] = x
        self.settings["y"] = y

    def _populate(self):
        super(BaseModMeta, self)._populate()
        self.settings = self.getSettings()
        g_playerEvents.onAvatarReady += self.onEnterBattlePage
        g_playerEvents.onAvatarBecomeNonPlayer += self.onExitBattlePage
        if self._isDAAPIInited():
            self.flashObject.setCompVisible(False)
            if self.isDebug:
                logInfo("battle module '%s' loaded" % self.getAlias())

    def _dispose(self):
        g_playerEvents.onAvatarReady -= self.onEnterBattlePage
        g_playerEvents.onAvatarBecomeNonPlayer -= self.onExitBattlePage
        super(BaseModMeta, self)._dispose()
        if self.isDebug:
            logInfo("battle module '%s' destroyed" % self.getAlias())

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

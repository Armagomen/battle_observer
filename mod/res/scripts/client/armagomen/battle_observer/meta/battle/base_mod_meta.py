from PlayerEvents import g_playerEvents
from account_helpers.settings_core.settings_constants import GRAPHICS
from armagomen.battle_observer.core import settings as g_settings
from armagomen.constants import ALIAS_TO_CONFIG_NAME, MAIN, COLORS, GLOBAL
from armagomen.utils.common import logInfo, getPlayer
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent
from gui.shared.personality import ServicesLocator
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider


class BaseModMeta(BaseDAAPIComponent):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)
    settingsCore = ServicesLocator.settingsCore
    isDebug = property(lambda self: g_settings.main[MAIN.DEBUG])

    def __init__(self):
        super(BaseModMeta, self).__init__()
        self._arenaDP = self.sessionProvider.getArenaDP()
        self._arenaVisitor = self.sessionProvider.arenaVisitor
        self._player = getPlayer()
        self.settings = None
        self.colors = g_settings.colors
        self.vehicle_types = g_settings.vehicle_types

    def setSettings(self):
        settings_name = ALIAS_TO_CONFIG_NAME.get(self.getAlias())
        settings = None
        if settings_name is not None:
            settings = getattr(g_settings, settings_name, None)
            if self.isDebug:
                logInfo("Settings Name: %s - Settings Data: %s" % (settings_name, str(settings)))
        self.settings = settings if settings is not None else g_settings

    @staticmethod
    def animationEnabled():
        return g_settings.main[MAIN.ENABLE_BARS_ANIMATION]

    @staticmethod
    def getShadowSettings():
        return g_settings.shadow_settings

    def getSettings(self):
        if self.settings is None:
            self.setSettings()
        return self.settings

    def getColors(self):
        return self.colors

    def getAlpha(self):
        return round(min(1.0, self.colors[COLORS.GLOBAL][GLOBAL.ALPHA] * 1.4), 2)

    @staticmethod
    def doLog(*args):
        logInfo(", ".join(str(arg) for arg in args))

    def isColorBlind(self):
        return bool(self.settingsCore.getSetting(GRAPHICS.COLOR_BLIND))

    def _populate(self):
        super(BaseModMeta, self)._populate()
        self.setSettings()
        g_playerEvents.onAvatarReady += self.onEnterBattlePage
        g_playerEvents.onAvatarBecomeNonPlayer += self.onExitBattlePage
        if self._isDAAPIInited():
            self.flashObject.setCompVisible(False)
            if self.isDebug:
                logInfo("battle module '%s' loaded" % self.getAlias())
        self.as_onAfterPopulateS()

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

    def as_onCrosshairPositionChangedS(self, x, y):
        return self.flashObject.as_onCrosshairPositionChanged(x, y) if self._isDAAPIInited() else None

    def as_onAfterPopulateS(self):
        return self.flashObject.as_onAfterPopulate() if self._isDAAPIInited() else None

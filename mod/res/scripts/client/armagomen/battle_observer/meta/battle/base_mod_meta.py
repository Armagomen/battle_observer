from account_helpers.settings_core.settings_constants import GRAPHICS
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import ALIAS_TO_CONFIG_NAME, COLORS, GLOBAL
from armagomen.utils.common import logInfo, logDebug
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent
from gui.shared.personality import ServicesLocator
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider


class BaseModMeta(BaseDAAPIComponent):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)
    settingsCore = ServicesLocator.settingsCore

    def __init__(self):
        super(BaseModMeta, self).__init__()
        self._arenaDP = self.sessionProvider.getArenaDP()
        self._arenaVisitor = self.sessionProvider.arenaVisitor
        self.settings = None
        self.colors = settings.colors
        self.vehicle_types = settings.vehicle_types

    def setSettings(self):
        settings_name = ALIAS_TO_CONFIG_NAME.get(self.getAlias(), GLOBAL.EMPTY_LINE)
        self.settings = getattr(settings, settings_name, None) or settings

    @property
    def gui(self):
        return self.sessionProvider.arenaVisitor.gui

    @staticmethod
    def getShadowSettings():
        return settings.shadow_settings

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
        for arg in args:
            info = "{}:{} - {}".format(arg.__name__, arg, dir(arg))
            logInfo(info)

    def isColorBlind(self):
        return bool(self.settingsCore.getSetting(GRAPHICS.COLOR_BLIND))

    def _populate(self):
        super(BaseModMeta, self)._populate()
        self.setSettings()
        self.as_onAfterPopulateS()
        logDebug("battle module '{}' loaded", self.getAlias())

    def _dispose(self):
        super(BaseModMeta, self)._dispose()
        logDebug("battle module '{}' destroyed", self.getAlias())

    def isPostmortemSwitchedToAnotherVehicle(self):
        observedVehID = self.sessionProvider.shared.vehicleState.getControllingVehicleID()
        return self.playerVehicleID != observedVehID

    @property
    def playerVehicleID(self):
        return self._arenaDP.getPlayerVehicleID()

    def as_setComponentVisible(self, param):
        return self.flashObject.setCompVisible(param) if self._isDAAPIInited() else None

    def as_startUpdateS(self, *args):
        return self.flashObject.as_startUpdate(*args) if self._isDAAPIInited() else None

    def as_colorBlindS(self, enabled):
        return self.flashObject.as_colorBlind(enabled) if self._isDAAPIInited() else None

    def as_onCrosshairPositionChangedS(self, x, y):
        return self.flashObject.as_onCrosshairPositionChanged(x, y) if self._isDAAPIInited() else None

    def as_onAfterPopulateS(self):
        return self.flashObject.as_onAfterPopulate() if self._isDAAPIInited() else None

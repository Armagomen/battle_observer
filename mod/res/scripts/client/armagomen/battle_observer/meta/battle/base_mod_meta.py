from account_helpers.settings_core.settings_constants import GRAPHICS
from armagomen._constants import VEHICLE_TYPES_COLORS
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.logging import logDebug, logInfo
from constants import ARENA_BONUS_TYPE
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent
from helpers import dependency
from skeletons.account_helpers.settings_core import ISettingsCore
from skeletons.gui.battle_session import IBattleSessionProvider


class BaseModMeta(BaseDAAPIComponent):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)
    settingsCore = dependency.descriptor(ISettingsCore)

    def __init__(self):
        super(BaseModMeta, self).__init__()
        self.settings = None

    def setAlias(self, alias):
        super(BaseModMeta, self).setAlias(alias)
        self.settings = user_settings.getSettingDictByAliasBattle(alias)

    @property
    def _arenaDP(self):
        return self.sessionProvider.getArenaDP()

    @property
    def _arenaVisitor(self):
        return self.sessionProvider.arenaVisitor

    def isComp7Battle(self):
        return self._arenaVisitor.getArenaBonusType() == ARENA_BONUS_TYPE.COMP7

    @property
    def gui(self):
        return self._arenaVisitor.gui

    def isSPG(self):
        return self.getVehicleInfo().isSPG()

    def getVehicleInfo(self, vID=None):
        return self._arenaDP.getVehicleInfo(vID)

    def getSettings(self):
        return self.settings

    @staticmethod
    def getColors():
        return user_settings.colors

    @staticmethod
    def getVehicleClassColors():
        return user_settings.colors[VEHICLE_TYPES_COLORS.NAME]

    @staticmethod
    def getVehicleClassColor(classTag):
        return user_settings.colors[VEHICLE_TYPES_COLORS.NAME].get(classTag, VEHICLE_TYPES_COLORS.UNKNOWN)

    def doLog(self, *args):
        for arg in args:
            logInfo("{}: {}", self.getAlias(), arg)

    def isColorBlind(self):
        return bool(self.settingsCore.getSetting(GRAPHICS.COLOR_BLIND))

    def _populate(self):
        super(BaseModMeta, self)._populate()
        logDebug("battle module '{}' loaded", self.getAlias())

    def _dispose(self):
        super(BaseModMeta, self)._dispose()
        logDebug("battle module '{}' destroyed", self.getAlias())

    def isPlayerVehicle(self):
        vehicle = self.sessionProvider.shared.vehicleState.getControllingVehicle()
        if vehicle is not None:
            return vehicle.isPlayerVehicle
        observed_veh_id = self.sessionProvider.shared.vehicleState.getControllingVehicleID()
        return self.playerVehicleID == observed_veh_id or observed_veh_id == 0

    @property
    def playerVehicleID(self):
        return self._arenaDP.getPlayerVehicleID()

    def as_setComponentVisible(self, param):
        return self.flashObject.setCompVisible(param) if self._isDAAPIInited() else None

    def as_colorBlindS(self, enabled):
        return self.flashObject.as_colorBlind(enabled) if self._isDAAPIInited() else None

    def as_onCrosshairPositionChangedS(self, x, y):
        return self.flashObject.as_onCrosshairPositionChanged(x, y) if self._isDAAPIInited() else None

from account_helpers.settings_core.settings_constants import GRAPHICS
from armagomen._constants import VEHICLE_TYPES_COLORS
from armagomen.battle_observer.settings import IBOSettingsLoader
from armagomen.utils.logging import logDebug, logInfo
from constants import ARENA_BONUS_TYPE
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent
from helpers import dependency
from skeletons.account_helpers.settings_core import ISettingsCore
from skeletons.gui.battle_session import IBattleSessionProvider


class BaseModMeta(BaseDAAPIComponent):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)
    settingsCore = dependency.descriptor(ISettingsCore)
    settingsLoader = dependency.descriptor(IBOSettingsLoader)

    def __init__(self):
        super(BaseModMeta, self).__init__()
        self.settings = {}
        self._isColorBlind = self.isColorBlind()

    def setAlias(self, alias):
        super(BaseModMeta, self).setAlias(alias)
        self.settings.update(self.settingsLoader.getSettingDictByAliasBattle(alias))

    @property
    def _arenaDP(self):
        return self.sessionProvider.getArenaDP()

    @property
    def _arenaVisitor(self):
        return self.sessionProvider.arenaVisitor

    def isComp7Battle(self):
        return self._arenaVisitor.getArenaBonusType() in (ARENA_BONUS_TYPE.COMP7, ARENA_BONUS_TYPE.COMP7_LIGHT)

    @property
    def gui(self):
        return self._arenaVisitor.gui

    def isSPG(self):
        return self.getVehicleInfo().isSPG()

    def getVehicleInfo(self, vID=None):
        return self._arenaDP.getVehicleInfo(vID)

    def getSettings(self):
        return self.settings

    def getColors(self):
        return self.settingsLoader.settings.colors

    def getVehicleClassColors(self):
        return self.settingsLoader.settings.colors[VEHICLE_TYPES_COLORS.NAME]

    def getVehicleClassColor(self, classTag):
        return self.settingsLoader.settings.colors[VEHICLE_TYPES_COLORS.NAME].get(classTag, VEHICLE_TYPES_COLORS.UNKNOWN)

    def doLog(self, *args):
        for arg in args:
            logInfo("{}: {}", self.getAlias(), arg)

    def isColorBlind(self):
        return bool(self.settingsCore.getSetting(GRAPHICS.COLOR_BLIND))

    def onColorblindUpdated(self, blind):
        pass

    def onSettingsApplied(self, diff):
        if GRAPHICS.COLOR_BLIND in diff:
            self._isColorBlind = bool(diff[GRAPHICS.COLOR_BLIND])
            self.onColorblindUpdated(self._isColorBlind)

    def _populate(self):
        super(BaseModMeta, self)._populate()
        logDebug("battle module '{}' loaded", self.getAlias())
        self.settingsCore.onSettingsApplied += self.onSettingsApplied

    def _dispose(self):
        super(BaseModMeta, self)._dispose()
        logDebug("battle module '{}' destroyed", self.getAlias())
        self.settingsCore.onSettingsApplied -= self.onSettingsApplied

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
        if self._isDAAPIInited():
            self.flashObject.setCompVisible(param)

    def as_colorBlindS(self, enabled):
        if self._isDAAPIInited():
            self.flashObject.as_colorBlind(enabled)

    def as_onCrosshairPositionChangedS(self, x, y):
        if self._isDAAPIInited():
            self.flashObject.as_onCrosshairPositionChanged(x, y)

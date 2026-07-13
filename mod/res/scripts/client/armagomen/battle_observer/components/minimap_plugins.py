from math import degrees

from armagomen import IALogger
from armagomen._constants import GLOBAL, MINIMAP
from armagomen.battle_observer.settings import IBOSettingsLoader
from armagomen.utils.common import IS_XVM_INSTALLED, overrideMethod, toggleOverride
from constants import ARENA_GUI_TYPE, VISIBILITY
from gui.Scaleform.daapi.view.battle.shared.minimap import plugins
from gui.Scaleform.daapi.view.battle.shared.minimap.component import MinimapComponent
from gui.Scaleform.daapi.view.battle.shared.minimap.entries import VehicleEntry
from gui.Scaleform.daapi.view.battle.shared.minimap.settings import CONTAINER_NAME
from helpers import dependency


class PersonalEntriesPlugin(plugins.PersonalEntriesPlugin):
    settingsLoader = dependency.descriptor(IBOSettingsLoader)

    def start(self):
        super(PersonalEntriesPlugin, self).start()
        if self.settingsLoader.getSetting(MINIMAP.NAME, MINIMAP.YAW) and self.__yawLimits is None:
            vInfo = self._arenaDP.getVehicleInfo()
            yawLimits = vInfo.vehicleType.turretYawLimits
            if yawLimits is not None:
                self.__yawLimits = (degrees(yawLimits[0]), degrees(yawLimits[1]))

    def _calcCircularVisionRadius(self):
        if self.settingsLoader.getSetting(MINIMAP.NAME, MINIMAP.VIEW_RADIUS):
            vehAttrs = self.sessionProvider.shared.feedback.getVehicleAttrs()
            return vehAttrs.get('circularVisionRadius', VISIBILITY.MIN_RADIUS)
        return super(PersonalEntriesPlugin, self)._calcCircularVisionRadius()


class ArenaVehiclesPlugin(plugins.ArenaVehiclesPlugin):
    settingsLoader = dependency.descriptor(IBOSettingsLoader)

    __slots__ = ('__showDestroyNames',)

    def __init__(self, *args, **kwargs):
        super(ArenaVehiclesPlugin, self).__init__(*args, **kwargs)
        self.__showDestroyNames = self.settingsLoader.getSetting(MINIMAP.NAME, MINIMAP.SHOW_NAMES)

    def start(self):
        super(ArenaVehiclesPlugin, self).start()
        toggleOverride(VehicleEntry, "updatePosition", self.entryUpdatePosition, True)

    def stop(self):
        toggleOverride(VehicleEntry, "updatePosition", self.entryUpdatePosition, False)
        super(ArenaVehiclesPlugin, self).stop()

    @staticmethod
    def entryUpdatePosition(base, entry, position):
        if entry.isAlive():
            base(entry, position)

    def isAlive(self, vehicleID):
        return self._arenaDP.getVehicleInfo(vehicleID).isAlive()

    def _showVehicle(self, vehicleID, location):
        if self.isAlive(vehicleID):
            super(ArenaVehiclesPlugin, self)._showVehicle(vehicleID, location)

    def _hideVehicle(self, entry):
        if entry.isAlive():
            super(ArenaVehiclesPlugin, self)._hideVehicle(entry)

    def __setDestroyed(self, vehicleID, entry):
        self.__clearAoIToFarCallback(vehicleID)
        if entry.isAlive():
            entry._isAlive = False
            if not entry.isInAoI():
                if entry.wasSpotted():
                    self._setInAoI(entry, True)
                else:
                    self.__setActive(entry, False)
                    return
            self._invoke(entry.getID(), 'setDead', True)
            self._move(entry.getID(), CONTAINER_NAME.DEAD_VEHICLES)

    def __switchToVehicle(self, prevCtrlID):
        pass

    def _getDisplayedName(self, vInfo):
        if vInfo.isAlive() or self.__showDestroyNames:
            return super(ArenaVehiclesPlugin, self)._getDisplayedName(vInfo)
        return ''


@overrideMethod(MinimapComponent, "_setupPlugins")
def _setupPlugins(base, plugin, arenaVisitor):
    _plugins = base(plugin, arenaVisitor)
    try:
        settingsLoader = dependency.instance(IBOSettingsLoader)
        minimap = settingsLoader.getComponentDict(MINIMAP.NAME)
        if not IS_XVM_INSTALLED and minimap.get(GLOBAL.ENABLED, False):
            if arenaVisitor.gui.guiType in ARENA_GUI_TYPE.RANDOM_RANGE and minimap.get(MINIMAP.DEATH_PERMANENT, False):
                _plugins['vehicles'] = ArenaVehiclesPlugin
            _plugins['personal'] = PersonalEntriesPlugin
    except Exception as err:
        logger = dependency.instance(IALogger)
        logger.logError("MinimapComponent _setupPlugins {} {}", err.args, str(err))
    return _plugins

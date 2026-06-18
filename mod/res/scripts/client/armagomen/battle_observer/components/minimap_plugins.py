from math import degrees

from armagomen._constants import BATTLES_RANGE, GLOBAL, MINIMAP
from armagomen import IALogger
from armagomen.battle_observer.settings import IBOSettingsLoader
from armagomen.utils.common import IS_XVM_INSTALLED, overrideMethod
from constants import VISIBILITY
from gui.Scaleform.daapi.view.battle.shared.minimap import plugins
from gui.Scaleform.daapi.view.battle.shared.minimap.component import MinimapComponent
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

    def __init__(self, *args, **kwargs):
        super(ArenaVehiclesPlugin, self).__init__(*args, **kwargs)
        self.__showDestroyEntries = self.__isDestroyImmediately = True
        self.__showDestroyNames = self.settingsLoader.getSetting(MINIMAP.NAME, MINIMAP.SHOW_NAMES)

    def _showVehicle(self, vehicleID, location):
        entry = self._entries[vehicleID]
        if entry.isAlive():
            super(ArenaVehiclesPlugin, self)._showVehicle(vehicleID, location)

    def _hideVehicle(self, entry):
        if entry.isAlive() and entry.isActive():
            super(ArenaVehiclesPlugin, self)._hideVehicle(entry)

    def __setDestroyed(self, vehicleID, entry):
        if self.__isDestroyImmediately:
            self._setInAoI(entry, True)
        super(ArenaVehiclesPlugin, self).__setDestroyed(vehicleID, entry)

    def __switchToVehicle(self, prevCtrlID):
        if self.__isDestroyImmediately:
            return
        super(ArenaVehiclesPlugin, self).__switchToVehicle(prevCtrlID)

    def _getDisplayedName(self, vInfo):
        if vInfo.isAlive() or self.__showDestroyNames:
            return super(ArenaVehiclesPlugin, self)._getDisplayedName(vInfo)
        return ''


@overrideMethod(MinimapComponent, "_setupPlugins")
def _setupPlugins(base, plugin, arenaVisitor):
    _plugins = base(plugin, arenaVisitor)
    try:
        settingsLoader = dependency.instance(IBOSettingsLoader)
        allowedMode = arenaVisitor.gui.guiType in BATTLES_RANGE
        minimap = settingsLoader.getComponentDict(MINIMAP.NAME)
        if not IS_XVM_INSTALLED and allowedMode and minimap.get(GLOBAL.ENABLED, False):
            if minimap.get(MINIMAP.DEATH_PERMANENT, False):
                _plugins['vehicles'] = ArenaVehiclesPlugin
            _plugins['personal'] = PersonalEntriesPlugin
    except Exception as err:
        logger = dependency.instance(IALogger)
        logger.logError("MinimapComponent _setupPlugins {} {}", err.args, str(err))
    return _plugins

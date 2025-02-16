from math import degrees

from armagomen._constants import BATTLES_RANGE, GLOBAL, MINIMAP
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import overrideMethod, xvmInstalled
from armagomen.utils.logging import logError
from constants import VISIBILITY
from gui.Scaleform.daapi.view.battle.shared.minimap import plugins
from gui.Scaleform.daapi.view.battle.shared.minimap.component import MinimapComponent


class PersonalEntriesPlugin(plugins.PersonalEntriesPlugin):

    def start(self):
        super(PersonalEntriesPlugin, self).start()
        if user_settings.minimap[MINIMAP.YAW] and self.__yawLimits is None:
            vInfo = self._arenaDP.getVehicleInfo()
            yawLimits = vInfo.vehicleType.turretYawLimits
            if yawLimits is not None:
                self.__yawLimits = (degrees(yawLimits[0]), degrees(yawLimits[1]))

    def _calcCircularVisionRadius(self):
        if user_settings.minimap[MINIMAP.VIEW_RADIUS]:
            vehAttrs = self.sessionProvider.shared.feedback.getVehicleAttrs()
            return vehAttrs.get('circularVisionRadius', VISIBILITY.MIN_RADIUS)
        return super(PersonalEntriesPlugin, self)._calcCircularVisionRadius()


class ArenaVehiclesPlugin(plugins.ArenaVehiclesPlugin):

    def __init__(self, *args, **kwargs):
        super(ArenaVehiclesPlugin, self).__init__(*args, **kwargs)
        self.__showDestroyEntries = user_settings.minimap[MINIMAP.DEATH_PERMANENT]
        self.__isDestroyImmediately = user_settings.minimap[MINIMAP.DEATH_PERMANENT]
        self.__showDestroyNames = user_settings.minimap[MINIMAP.SHOW_NAMES] and self.__isDestroyImmediately

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
        allowedMode = arenaVisitor.gui.guiType in BATTLES_RANGE
        if not xvmInstalled and allowedMode and user_settings.minimap[GLOBAL.ENABLED]:
            if user_settings.minimap[MINIMAP.DEATH_PERMANENT]:
                _plugins['vehicles'] = ArenaVehiclesPlugin
            _plugins['personal'] = PersonalEntriesPlugin
    except Exception as err:
        logError(repr(err))
    finally:
        return _plugins

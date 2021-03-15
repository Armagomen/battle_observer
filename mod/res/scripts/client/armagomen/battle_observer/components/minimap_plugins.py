from math import degrees

from armagomen.battle_observer.core import config
from armagomen.battle_observer.core.bo_constants import GLOBAL, MINIMAP
from armagomen.utils.common import overrideMethod
from gui.Scaleform.daapi.view.battle.shared.minimap.component import MinimapComponent
from gui.Scaleform.daapi.view.battle.shared.minimap.plugins import PersonalEntriesPlugin, ArenaVehiclesPlugin
from gui.Scaleform.daapi.view.battle.shared.minimap.settings import CONTAINER_NAME
from gui.battle_control import matrix_factory
from gui.battle_control.battle_constants import VEHICLE_LOCATION


class BOPersonalEntriesPlugin(PersonalEntriesPlugin):

    def __init__(self, *args, **kwargs):
        super(BOPersonalEntriesPlugin, self).__init__(*args, **kwargs)

    def start(self):
        super(BOPersonalEntriesPlugin, self).start()
        if self._PersonalEntriesPlugin__yawLimits is None:
            vInfo = self._arenaDP.getVehicleInfo()
            yawLimits = vInfo.vehicleType.turretYawLimits
            if yawLimits is not None:
                self._PersonalEntriesPlugin__yawLimits = (degrees(yawLimits[0]), degrees(yawLimits[1]))


class VehiclesPlugin(ArenaVehiclesPlugin):

    def __init__(self, *args, **kwargs):
        super(VehiclesPlugin, self).__init__(*args, **kwargs)

    def _showVehicle(self, vehicleID, location):
        entry = self._entries.get(vehicleID, None)
        if entry is not None and entry.isAlive():
            matrix = matrix_factory.makeVehicleMPByLocation(vehicleID, location, self._arenaVisitor.getArenaPositions())
            if matrix is not None:
                self._ArenaVehiclesPlugin__setLocationAndMatrix(entry, location, matrix)
                self._setInAoI(entry, True)
                self._ArenaVehiclesPlugin__setActive(entry, True)

    def _hideVehicle(self, entry):
        if entry.isAlive() and entry.isActive():
            matrix = entry.getMatrix()
            if matrix is not None:
                matrix = matrix_factory.convertToLastSpottedVehicleMP(matrix)
            self._setInAoI(entry, False)
            self._ArenaVehiclesPlugin__setLocationAndMatrix(entry, VEHICLE_LOCATION.UNDEFINED, matrix)

    def _ArenaVehiclesPlugin__setDestroyed(self, vehicleID, entry):
        self._ArenaVehiclesPlugin__clearAoIToFarCallback(vehicleID)
        if not entry.wasSpotted() and entry.setAlive(False) and entry.getMatrix() is not None:
            if not entry.isActive():
                self._ArenaVehiclesPlugin__setActive(entry, True)
            if entry.isActive() and not entry.isInAoI():
                self._setInAoI(entry, True)
            self._invoke(entry._entryID, 'setDead', True)
            self._move(entry._entryID, CONTAINER_NAME.DEAD_VEHICLES)
            self._invoke(entry._entryID, self._showNames)
        else:
            self._ArenaVehiclesPlugin__setActive(entry, False)

    @property
    def _showNames(self):
        if config.minimap[MINIMAP.DEATH_PERMANENT] and config.minimap[MINIMAP.SHOW_NAMES]:
            return 'showVehicleName'
        return 'hideVehicleName'


@overrideMethod(MinimapComponent, "_setupPlugins")
def _setupPlugins(base, plugin, arenaVisitor):
    plugins = base(plugin, arenaVisitor)
    if config.minimap[GLOBAL.ENABLED]:
        if config.minimap[MINIMAP.DEATH_PERMANENT]:
            plugins['vehicles'] = VehiclesPlugin
        plugins['personal'] = BOPersonalEntriesPlugin
    return plugins

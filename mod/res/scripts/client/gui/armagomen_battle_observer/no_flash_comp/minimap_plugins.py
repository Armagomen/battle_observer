from math import degrees

from constants import IS_DEVELOPMENT
from gui.Scaleform.daapi.view.battle.shared.minimap import plugins
from gui.Scaleform.daapi.view.battle.shared.minimap.component import MinimapComponent
from gui.Scaleform.daapi.view.battle.shared.minimap.settings import CONTAINER_NAME
from gui.battle_control import matrix_factory
from gui.battle_control.battle_constants import VEHICLE_LOCATION
from ..core.bo_constants import GLOBAL, MINIMAP
from ..core.config import cfg
from ..core.core import overrideMethod

SHOW_NAMES = ('hideVehicleName', 'showVehicleName')


class BOPersonalEntriesPlugin(plugins.PersonalEntriesPlugin):

    def __init__(self, *args, **kwargs):
        super(BOPersonalEntriesPlugin, self).__init__(*args, **kwargs)

    def start(self):
        super(BOPersonalEntriesPlugin, self).start()
        if self._PersonalEntriesPlugin__yawLimits is None:
            vInfo = self._arenaDP.getVehicleInfo()
            yawLimits = vInfo.vehicleType.turretYawLimits
            if yawLimits is not None:
                self._PersonalEntriesPlugin__yawLimits = (degrees(yawLimits[0]), degrees(yawLimits[1]))


class VehiclesPlugin(plugins.ArenaVehiclesPlugin):

    def __init__(self, *args, **kwargs):
        super(VehiclesPlugin, self).__init__(*args, **kwargs)

    def _ArenaVehiclesPlugin__showVehicle(self, vehicleID, location):
        entry = self._entries.get(vehicleID, None)
        if entry is not None and entry.isAlive():
            matrix = matrix_factory.makeVehicleMPByLocation(vehicleID, location, self._arenaVisitor.getArenaPositions())
            if matrix is not None:
                self._ArenaVehiclesPlugin__setLocationAndMatrix(entry, location, matrix)
                self._ArenaVehiclesPlugin__setInAoI(entry, True)
                self._ArenaVehiclesPlugin__setActive(entry, True)

    def _ArenaVehiclesPlugin__hideVehicle(self, entry):
        if entry.isAlive() and entry.isActive():
            matrix = entry.getMatrix()
            if matrix is not None:
                matrix = matrix_factory.convertToLastSpottedVehicleMP(matrix)
            self._ArenaVehiclesPlugin__setInAoI(entry, False)
            self._ArenaVehiclesPlugin__setLocationAndMatrix(entry, VEHICLE_LOCATION.UNDEFINED, matrix)

    def _ArenaVehiclesPlugin__setDestroyed(self, vehicleID, entry):
        self._ArenaVehiclesPlugin__clearAoIToFarCallback(vehicleID)
        if not entry.wasSpotted() and entry.setAlive(False) and entry.getMatrix() is not None:
            if not entry.isActive():
                self._ArenaVehiclesPlugin__setActive(entry, True)
            if entry.isActive() and not entry.isInAoI():
                self._ArenaVehiclesPlugin__setInAoI(entry, True)
            self._invoke(entry._entryID, 'setDead', True)
            self._move(entry._entryID, CONTAINER_NAME.DEAD_VEHICLES)
            self._invoke(entry._entryID,
                         SHOW_NAMES[int(cfg.minimap[MINIMAP.DEATH_PERMANENT] and cfg.minimap[MINIMAP.SHOW_NAMES])])
        else:
            self._ArenaVehiclesPlugin__setActive(entry, False)


@overrideMethod(MinimapComponent, "_setupPlugins")
def _setupPlugins(base, plugin, arenaVisitor):
    if cfg.minimap[GLOBAL.ENABLED]:
        setup = {'equipments': plugins.EquipmentsPlugin,
                 'vehicles': VehiclesPlugin if cfg.minimap[MINIMAP.DEATH_PERMANENT] else plugins.ArenaVehiclesPlugin,
                 'personal': BOPersonalEntriesPlugin,
                 'area': plugins.AreaStaticMarkerPlugin}
        if IS_DEVELOPMENT:
            setup['teleport'] = plugins.TeleportPlugin
        return setup
    else:
        return base(plugin, arenaVisitor)

from math import degrees

from armagomen.battle_observer.core import viewSettings
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import GLOBAL, MINIMAP
from armagomen.utils.common import overrideMethod, xvmInstalled
from armagomen.utils.keys_listener import g_keysListener
from constants import VISIBILITY
from gui.Scaleform.daapi.view.battle.shared.minimap import plugins
from gui.Scaleform.daapi.view.battle.shared.minimap.component import MinimapComponent
from gui.battle_control import avatar_getter
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider


class MinimapZoomPlugin(object):
    arenaVisitor = dependency.descriptor(IBattleSessionProvider).arenaVisitor

    def __init__(self):
        self.__battleView_as = None
        self.isComp7Page = False
        self.enabled = settings.minimap[GLOBAL.ENABLED] and settings.minimap[MINIMAP.ZOOM] and not xvmInstalled

    def init(self, flashObject):
        self.__battleView_as = flashObject
        self.__battleView_as.as_createMimimapCentered()
        self.isComp7Page = self.arenaVisitor.gui.isComp7Battle()
        g_keysListener.registerComponent(self.onKeyPressed, keyList=settings.minimap[MINIMAP.ZOOM_KEY])

    def fini(self):
        self.__battleView_as = None

    def onKeyPressed(self, isKeyDown):
        """hot key event"""
        if self.isComp7Page and self.arenaVisitor.isArenaNotStarted():
            return
        self.__battleView_as.as_zoomMimimapCentered(isKeyDown)
        avatar_getter.setForcedGuiControlMode(isKeyDown, enableAiming=False)


class PersonalEntriesPlugin(plugins.PersonalEntriesPlugin):

    def start(self):
        super(PersonalEntriesPlugin, self).start()
        if settings.minimap[MINIMAP.YAW] and self.__yawLimits is None:
            vInfo = self._arenaDP.getVehicleInfo()
            yawLimits = vInfo.vehicleType.turretYawLimits
            if yawLimits is not None:
                self.__yawLimits = (degrees(yawLimits[0]), degrees(yawLimits[1]))

    def _calcCircularVisionRadius(self):
        if settings.minimap[MINIMAP.VIEW_RADIUS]:
            vehAttrs = self.sessionProvider.shared.feedback.getVehicleAttrs()
            return vehAttrs.get('circularVisionRadius', VISIBILITY.MIN_RADIUS)
        return super(PersonalEntriesPlugin, self)._calcCircularVisionRadius()


class ArenaVehiclesPlugin(plugins.ArenaVehiclesPlugin):

    def __init__(self, *args, **kwargs):
        super(ArenaVehiclesPlugin, self).__init__(*args, **kwargs)
        self.__showDestroyEntries = settings.minimap[MINIMAP.DEATH_PERMANENT]
        self.__isDestroyImmediately = settings.minimap[MINIMAP.DEATH_PERMANENT]

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
        self._invoke(entry.getID(), self._showNames)

    def __switchToVehicle(self, prevCtrlID):
        if self.__isDestroyImmediately:
            return
        super(ArenaVehiclesPlugin, self).__switchToVehicle(prevCtrlID)

    @property
    def _showNames(self):
        if self.__showDestroyEntries and settings.minimap[MINIMAP.SHOW_NAMES]:
            return 'showVehicleName'
        return 'hideVehicleName'


@overrideMethod(MinimapComponent, "_setupPlugins")
def _setupPlugins(base, plugin, arenaVisitor):
    _plugins = base(plugin, arenaVisitor)
    if not arenaVisitor.gui.isComp7Battle() and settings.minimap[GLOBAL.ENABLED] and viewSettings.notEpicBattle() \
            and not xvmInstalled:
        if settings.minimap[MINIMAP.DEATH_PERMANENT]:
            _plugins['vehicles'] = ArenaVehiclesPlugin
        _plugins['personal'] = PersonalEntriesPlugin
    return _plugins

from math import degrees

from armagomen._constants import BATTLES_RANGE, GLOBAL, MINIMAP
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.utils.common import overrideMethod, xvmInstalled
from armagomen.utils.keys_listener import g_keysListener
from armagomen.utils.logging import logError
from constants import ARENA_PERIOD, VISIBILITY
from gui.battle_control import avatar_getter
from gui.Scaleform.daapi.view.battle.shared.minimap import plugins
from gui.Scaleform.daapi.view.battle.shared.minimap.component import MinimapComponent
from helpers import dependency
from PlayerEvents import g_playerEvents
from skeletons.gui.battle_session import IBattleSessionProvider


class MinimapZoomPlugin(object):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)

    def __init__(self):
        self.__battleView_as = None
        self.__started = False
        self.isComp7Page = False

    def init(self, flashObject):
        self.__battleView_as = flashObject
        g_playerEvents.onAvatarReady += self.onAvatarReady

    def onAvatarReady(self):
        if self.__started:
            return
        self.__battleView_as.as_createMimimapCentered()
        self.isComp7Page = self.sessionProvider.arenaVisitor.gui.isComp7Battle()
        g_keysListener.registerComponent(self.onKeyPressed, keyList=settings.minimap[MINIMAP.ZOOM_KEY])
        self.__started = True

    def fini(self):
        g_playerEvents.onAvatarReady -= self.onAvatarReady
        self.__battleView_as = None

    def onKeyPressed(self, isKeyDown):
        """hot key event"""
        if self.isComp7Page and self.sessionProvider.arenaVisitor.getArenaPeriod() != ARENA_PERIOD.BATTLE:
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

    def __switchToVehicle(self, prevCtrlID):
        if self.__isDestroyImmediately:
            return
        super(ArenaVehiclesPlugin, self).__switchToVehicle(prevCtrlID)

    def _getDisplayedName(self, vInfo):
        if not vInfo.isAlive() and not settings.minimap[MINIMAP.SHOW_NAMES]:
            return ''
        return super(ArenaVehiclesPlugin, self)._getDisplayedName(vInfo)


@overrideMethod(MinimapComponent, "_setupPlugins")
def _setupPlugins(base, plugin, arenaVisitor):
    _plugins = base(plugin, arenaVisitor)
    try:
        allowedMode = arenaVisitor.gui.guiType in BATTLES_RANGE
        if not xvmInstalled and allowedMode and settings.minimap[GLOBAL.ENABLED]:
            if settings.minimap[MINIMAP.DEATH_PERMANENT]:
                _plugins['vehicles'] = ArenaVehiclesPlugin
            _plugins['personal'] = PersonalEntriesPlugin
    except Exception as err:
        logError(repr(err))
    finally:
        return _plugins

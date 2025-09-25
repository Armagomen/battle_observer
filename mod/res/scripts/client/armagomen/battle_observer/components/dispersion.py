import aih_constants
from account_helpers.settings_core.settings_constants import GAME
from armagomen._constants import DISPERSION, GLOBAL
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import getPlayer, toggleOverride
from armagomen.utils.events import g_events
from AvatarInputHandler import gun_marker_ctrl
from BattleReplay import g_replayCtrl
from constants import SERVER_TICK_LENGTH
from gui.battle_control.controllers.crosshair_proxy import CrosshairDataProxy
from gui.Scaleform.daapi.view.battle.shared.crosshair import gm_factory
from gui.Scaleform.daapi.view.battle.shared.crosshair.container import CrosshairPanelContainer
from gui.Scaleform.genConsts.GUN_MARKER_VIEW_CONSTANTS import GUN_MARKER_VIEW_CONSTANTS as _CONSTANTS
from helpers import dependency
from skeletons.account_helpers.settings_core import ISettingsCore
from VehicleGunRotator import VehicleGunRotator

DEV_FACTORIES_COLLECTION = (gm_factory._DevControlMarkersFactory, gm_factory._OptionalMarkersFactory, gm_factory._EquipmentMarkersFactory)
LINKAGES = {
    _CONSTANTS.DEBUG_SPG_GUN_MARKER_NAME: _CONSTANTS.GUN_MARKER_SPG_LINKAGE,
    _CONSTANTS.DEBUG_ARCADE_GUN_MARKER_NAME: _CONSTANTS.GUN_MARKER_LINKAGE,
    _CONSTANTS.DEBUG_SNIPER_GUN_MARKER_NAME: _CONSTANTS.GUN_MARKER_LINKAGE,
    _CONSTANTS.DEBUG_DUAL_GUN_ARCADE_MARKER_NAME: _CONSTANTS.DUAL_GUN_ARCADE_MARKER_LINKAGE,
    _CONSTANTS.DEBUG_DUAL_GUN_SNIPER_MARKER_NAME: _CONSTANTS.DUAL_GUN_SNIPER_MARKER_LINKAGE,
    _CONSTANTS.DEBUG_TWIN_GUN_ARCADE_MARKER_NAME: _CONSTANTS.TWIN_GUN_MARKER_LINKAGE,
    _CONSTANTS.DEBUG_TWIN_GUN_SNIPER_MARKER_NAME: _CONSTANTS.TWIN_GUN_MARKER_LINKAGE}

gm_factory._GUN_MARKER_LINKAGES.update(LINKAGES)

aih_constants.GUN_MARKER_MIN_SIZE = 10.0
aih_constants.SPG_GUN_MARKER_MIN_SIZE = 20.0

REPLACE_TYPES = {gun_marker_ctrl._MARKER_TYPE.CLIENT, gun_marker_ctrl._MARKER_TYPE.DUAL_ACC}


def get_dispersion_scale_setting(marker_type):
    replace_setting = user_settings.dispersion_circle[DISPERSION.REPLACE]
    server_setting = user_settings.dispersion_circle[DISPERSION.SERVER]
    result = False
    if marker_type == gun_marker_ctrl._MARKER_TYPE.SERVER:
        result = replace_setting or server_setting
    elif marker_type in REPLACE_TYPES:
        result = replace_setting
    return float(user_settings.dispersion_circle[DISPERSION.SCALE]) if result else 1.0


class _DefaultGunMarkerController(gun_marker_ctrl._DefaultGunMarkerController):

    def __init__(self, gunMakerType, dataProvider, **kwargs):
        super(_DefaultGunMarkerController, self).__init__(gunMakerType, dataProvider, **kwargs)
        self.__scaleConfig = get_dispersion_scale_setting(gunMakerType)

    def __updateScreenRatio(self):
        super(_DefaultGunMarkerController, self).__updateScreenRatio()
        self.__screenRatio *= self.__scaleConfig


class _DualAccMarkerController(_DefaultGunMarkerController):

    def _replayReader(self, replayCtrl):
        return replayCtrl.getDualAccMarkerSize

    def _replayWriter(self, replayCtrl):
        return replayCtrl.setDualAccMarkerSize


class SPGController(gun_marker_ctrl._SPGGunMarkerController):

    def __init__(self, gunMakerType, dataProvider, **kwargs):
        super(SPGController, self).__init__(gunMakerType, dataProvider, **kwargs)
        self.__scaleConfig = get_dispersion_scale_setting(gunMakerType)

    def _updateDispersionData(self):
        self._size *= self.__scaleConfig
        dispersionAngle = self._gunRotator.dispersionAngle * self.__scaleConfig
        isServerAim = self._gunMarkerType == gun_marker_ctrl._MARKER_TYPE.SERVER
        if g_replayCtrl.isRecording and (g_replayCtrl.isServerAim and isServerAim or not isServerAim):
            g_replayCtrl.setSPGGunMarkerParams(dispersionAngle, 0.0)
        self._dataProvider.setupConicDispersion(dispersionAngle)


class DispersionCircle(object):
    settingsCore = dependency.descriptor(ISettingsCore)

    def __init__(self):
        g_events.onModSettingsChanged += self.onModSettingsChanged

    def fini(self):
        g_events.onModSettingsChanged -= self.onModSettingsChanged

    def createOverrideComponents(self, base, *args):
        self.disableWGServerMarker()
        getPlayer().cell.setServerMarker(True)
        if len(args) == 2:
            return gm_factory._GunMarkersFactories(*DEV_FACTORIES_COLLECTION).create(*args)
        return gm_factory._GunMarkersFactories(*DEV_FACTORIES_COLLECTION).override(*args)

    @staticmethod
    def useDefaultGunMarkers(*args, **kwargs):
        return False

    @staticmethod
    def useGunMarker(*args, **kwargs):
        return True

    @staticmethod
    def onPass(*args, **kwargs):
        pass

    @staticmethod
    def setShotPosition(base, rotator, vehicleID, sPos, sVec, dispersionAngle, forceValueRefresh=False):
        gunMarkerInfo = rotator._VehicleGunRotator__getGunMarkerInfo(
            sPos, sVec, rotator.getCurShotDispersionAngles(), rotator._VehicleGunRotator__gunIndex)
        supportMarkersInfo = rotator._VehicleGunRotator__getSupportMarkersInfo()
        rotator._avatar.inputHandler.updateServerGunMarker(gunMarkerInfo, supportMarkersInfo, SERVER_TICK_LENGTH)

    def disableWGServerMarker(self):
        if self.settingsCore.applySetting(GAME.ENABLE_SERVER_AIM, False) is not None:
            self.settingsCore.applyStorages(False)
            self.settingsCore.clearStorages()

    @staticmethod
    def setGunMarkerColor(base, cr_panel, markerType, color):
        base(cr_panel, gun_marker_ctrl._MARKER_TYPE.SERVER, color)
        return base(cr_panel, markerType, color)

    def onModSettingsChanged(self, name, data):
        if name != DISPERSION.NAME:
            return
        isEnabled = data[GLOBAL.ENABLED]
        replace = isEnabled and data[DISPERSION.REPLACE]
        server = isEnabled and data[DISPERSION.SERVER]
        toggleOverride(gun_marker_ctrl, "createGunMarker", self.createGunMarker_WG, replace or server)
        self.toggleServerCrossOverrides(server)

    def toggleServerCrossOverrides(self, enable):
        server_overrides = (
            (gm_factory, "createComponents", self.createOverrideComponents),
            (gm_factory, "overrideComponents", self.createOverrideComponents),
            (gun_marker_ctrl, "useDefaultGunMarkers", self.useDefaultGunMarkers),
            (gun_marker_ctrl, "useClientGunMarker", self.useGunMarker),
            (gun_marker_ctrl, "useServerGunMarker", self.useGunMarker),
            (VehicleGunRotator, "applySettings", self.onPass),
            (VehicleGunRotator, "setShotPosition", self.setShotPosition),
            (CrosshairDataProxy, "__onServerGunMarkerStateChanged", self.onPass),
            (CrosshairPanelContainer, "setGunMarkerColor", self.setGunMarkerColor)
        )
        for obj, method_name, func in server_overrides:
            toggleOverride(obj, method_name, func, enable)

    def createGunMarker_WG(self, baseCreateGunMarker, isStrategic):
        if isStrategic:
            return self.createStrategicGunMarker()
        else:
            return self.createDefaultGunMarker()

    @staticmethod
    def createDefaultGunMarker(*args):
        factory = gun_marker_ctrl._GunMarkersDPFactory()
        client = _DefaultGunMarkerController(gun_marker_ctrl._MARKER_TYPE.CLIENT, factory.getClientProvider())
        server = _DefaultGunMarkerController(gun_marker_ctrl._MARKER_TYPE.SERVER, factory.getServerProvider())
        dual = _DualAccMarkerController(gun_marker_ctrl._MARKER_TYPE.DUAL_ACC, factory.getDualAccuracyProvider())
        return gun_marker_ctrl._GunMarkersDecorator(client, server, dual)

    @staticmethod
    def createStrategicGunMarker(*args):
        factory = gun_marker_ctrl._GunMarkersDPFactory()
        client = SPGController(gun_marker_ctrl._MARKER_TYPE.CLIENT, factory.getClientSPGProvider())
        server = SPGController(gun_marker_ctrl._MARKER_TYPE.SERVER, factory.getServerSPGProvider())
        dual = gun_marker_ctrl._EmptyGunMarkerController(gun_marker_ctrl._MARKER_TYPE.UNDEFINED, None)
        return gun_marker_ctrl._GunMarkersDecorator(client, server, dual)


dispersion_circle = DispersionCircle()


def fini():
    dispersion_circle.fini()

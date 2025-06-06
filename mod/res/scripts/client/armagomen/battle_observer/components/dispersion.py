import aih_constants
from account_helpers.settings_core.settings_constants import GAME
from armagomen._constants import DISPERSION, GLOBAL, IS_WG_CLIENT
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import cancelOverride, getPlayer, overrideMethod
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

CLIENT = gun_marker_ctrl._MARKER_TYPE.CLIENT
SERVER = gun_marker_ctrl._MARKER_TYPE.SERVER
DUAL_ACC = gun_marker_ctrl._MARKER_TYPE.DUAL_ACC
EMPTY = gun_marker_ctrl._MARKER_TYPE.UNDEFINED

DEV_FACTORIES_COLLECTION = (gm_factory._DevControlMarkersFactory, gm_factory._OptionalMarkersFactory, gm_factory._EquipmentMarkersFactory)
LINKAGES = {
    _CONSTANTS.DEBUG_SPG_GUN_MARKER_NAME: _CONSTANTS.GUN_MARKER_SPG_LINKAGE,
    _CONSTANTS.DEBUG_ARCADE_GUN_MARKER_NAME: _CONSTANTS.GUN_MARKER_LINKAGE,
    _CONSTANTS.DEBUG_SNIPER_GUN_MARKER_NAME: _CONSTANTS.GUN_MARKER_LINKAGE,
    _CONSTANTS.DEBUG_DUAL_GUN_ARCADE_MARKER_NAME: _CONSTANTS.DUAL_GUN_ARCADE_MARKER_LINKAGE,
    _CONSTANTS.DEBUG_DUAL_GUN_SNIPER_MARKER_NAME: _CONSTANTS.DUAL_GUN_SNIPER_MARKER_LINKAGE
}
if IS_WG_CLIENT:
    LINKAGES.update({_CONSTANTS.DEBUG_TWIN_GUN_ARCADE_MARKER_NAME: _CONSTANTS.TWIN_GUN_MARKER_LINKAGE,
                     _CONSTANTS.DEBUG_TWIN_GUN_SNIPER_MARKER_NAME: _CONSTANTS.TWIN_GUN_MARKER_LINKAGE})

gm_factory._GUN_MARKER_LINKAGES.update(LINKAGES)

aih_constants.GUN_MARKER_MIN_SIZE /= 2
aih_constants.SPG_GUN_MARKER_MIN_SIZE /= 2

REPLACE = (CLIENT, DUAL_ACC)


def getSetting(gunMakerType):
    _replace = user_settings.dispersion_circle[DISPERSION.REPLACE]
    _server = user_settings.dispersion_circle[DISPERSION.SERVER]
    return _replace or _server if gunMakerType == SERVER else _replace if gunMakerType in REPLACE else False


class _DefaultGunMarkerController(gun_marker_ctrl._DefaultGunMarkerController):

    def __init__(self, gunMakerType, dataProvider, **kwargs):
        super(_DefaultGunMarkerController, self).__init__(gunMakerType, dataProvider, **kwargs)
        self.__scaleConfig = float(user_settings.dispersion_circle[DISPERSION.SCALE]) if getSetting(gunMakerType) else 1.0

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
        self.__scaleConfig = float(user_settings.dispersion_circle[DISPERSION.SCALE]) if getSetting(gunMakerType) else 1.0

    def _updateDispersionData(self):
        self._size *= self.__scaleConfig
        dispersionAngle = self._gunRotator.dispersionAngle * self.__scaleConfig
        isServerAim = self._gunMarkerType == SERVER
        if g_replayCtrl.isRecording and (g_replayCtrl.isServerAim and isServerAim or not isServerAim):
            g_replayCtrl.setSPGGunMarkerParams(dispersionAngle, 0.0)
        self._dataProvider.setupConicDispersion(dispersionAngle)


def disable_server_aim():
    settingsCore = dependency.instance(ISettingsCore)
    if settingsCore.getSetting(GAME.ENABLE_SERVER_AIM):
        settingsCore.applySettings({GAME.ENABLE_SERVER_AIM: 0})
        settingsCore.applyStorages(False)
        settingsCore.clearStorages()


class DispersionCircle(object):

    def __init__(self):
        user_settings.onModSettingsChanged += self.onModSettingsChanged
        self.enabled = False

    def fini(self):
        user_settings.onModSettingsChanged -= self.onModSettingsChanged

    def addServerCrossOverrides(self):
        overrideMethod(gm_factory, "createComponents")(self.createOverrideComponents)
        overrideMethod(gm_factory, "overrideComponents")(self.createOverrideComponents)
        overrideMethod(gun_marker_ctrl, "useDefaultGunMarkers")(self.useDefaultGunMarkers)
        overrideMethod(gun_marker_ctrl, "useClientGunMarker")(self.useGunMarker)
        overrideMethod(gun_marker_ctrl, "useServerGunMarker")(self.useGunMarker)
        overrideMethod(VehicleGunRotator, "applySettings")(self.onPass)
        overrideMethod(VehicleGunRotator, "setShotPosition")(self.setShotPositionWG if IS_WG_CLIENT else self.setShotPositionLesta)
        overrideMethod(CrosshairDataProxy, "__onServerGunMarkerStateChanged")(self.onPass)
        overrideMethod(CrosshairPanelContainer, "setGunMarkerColor")(self.setGunMarkerColor)

    @staticmethod
    def cancelServerCrossOverride():
        cancelOverride(gm_factory, "createComponents", "createOverrideComponents")
        cancelOverride(gm_factory, "overrideComponents", "createOverrideComponents")
        cancelOverride(gun_marker_ctrl, "useDefaultGunMarkers", "useDefaultGunMarkers")
        cancelOverride(gun_marker_ctrl, "useClientGunMarker", "useGunMarker")
        cancelOverride(gun_marker_ctrl, "useServerGunMarker", "useGunMarker")
        cancelOverride(VehicleGunRotator, "applySettings", "onPass")
        cancelOverride(VehicleGunRotator, "setShotPosition", "setShotPositionWG" if IS_WG_CLIENT else "setShotPositionLesta")
        cancelOverride(CrosshairDataProxy, "__onServerGunMarkerStateChanged", "onPass")
        cancelOverride(CrosshairPanelContainer, "setGunMarkerColor", "setGunMarkerColor")

    @staticmethod
    def createOverrideComponents(base, *args):
        disable_server_aim()
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
    def setShotPositionWG(base, rotator, vehicleID, sPos, sVec, dispersionAngle, forceValueRefresh=False):
        m_position = rotator._VehicleGunRotator__getGunMarkerPosition(sPos, sVec, rotator.getCurShotDispersionAngles())
        mPos, mDir, mSize, dualAccSize, mSizeOffset, collData = m_position
        rotator._avatar.inputHandler.updateServerGunMarker(mPos, mDir, mSize, mSizeOffset, SERVER_TICK_LENGTH, collData)

    @staticmethod
    def setShotPositionLesta(base, rotator, vehicleID, sPos, sVec, dispersionAngle, forceValueRefresh=False):
        m_position = rotator._VehicleGunRotator__getGunMarkerPosition(sPos, sVec, rotator.getCurShotDispersionAngles())
        mPos, mDir, mSize, mISize, dualAccSize, _, collData = m_position
        rotator._avatar.inputHandler.updateServerGunMarker(mPos, mDir, (mSize, mISize), SERVER_TICK_LENGTH, collData)

    @staticmethod
    def setGunMarkerColor(base, cr_panel, markerType, color):
        if markerType == CLIENT:
            base(cr_panel, SERVER, color)
        return base(cr_panel, markerType, color)

    def onModSettingsChanged(self, config, blockID):
        if blockID != DISPERSION.NAME:
            return
        replace = config[GLOBAL.ENABLED] and config[DISPERSION.REPLACE]
        server = config[GLOBAL.ENABLED] and config[DISPERSION.SERVER]
        enabled = replace or server
        if self.enabled != enabled:
            self.enabled = enabled
            if IS_WG_CLIENT:
                self.toggleGunMarker("createGunMarker", self.createGunMarker_WG, enabled)
            else:
                self.toggleGunMarker("createDefaultGunMarker", self.createDefaultGunMarker, enabled)
                self.toggleGunMarker("createStrategicGunMarker", self.createStrategicGunMarker, enabled)
                self.toggleGunMarker("createAssaultSpgGunMarker", self.createStrategicGunMarker, enabled)
        if server:
            self.addServerCrossOverrides()
        else:
            self.cancelServerCrossOverride()

    @staticmethod
    def toggleGunMarker(method_name, func, enable):
        if enable:
            overrideMethod(gun_marker_ctrl, method_name)(func)
        else:
            cancelOverride(gun_marker_ctrl, method_name, func.__name__)

    def createGunMarker_WG(self, baseCreateGunMarker, isStrategic):
        if isStrategic:
            return self.createStrategicGunMarker()
        else:
            return self.createDefaultGunMarker()

    @staticmethod
    def createDefaultGunMarker(*args):
        factory = gun_marker_ctrl._GunMarkersDPFactory()
        client = _DefaultGunMarkerController(CLIENT, factory.getClientProvider())
        server = _DefaultGunMarkerController(SERVER, factory.getServerProvider())
        dual = _DualAccMarkerController(DUAL_ACC, factory.getDualAccuracyProvider())
        return gun_marker_ctrl._GunMarkersDecorator(client, server, dual)

    @staticmethod
    def createStrategicGunMarker(*args):
        factory = gun_marker_ctrl._GunMarkersDPFactory()
        client = SPGController(CLIENT, factory.getClientSPGProvider())
        server = SPGController(SERVER, factory.getServerSPGProvider())
        dual = gun_marker_ctrl._EmptyGunMarkerController(EMPTY, None)
        return gun_marker_ctrl._GunMarkersDecorator(client, server, dual)


dispersion_circle = DispersionCircle()


def fini():
    dispersion_circle.fini()

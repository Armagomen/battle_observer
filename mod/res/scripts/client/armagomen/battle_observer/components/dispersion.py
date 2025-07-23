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
from PlayerEvents import g_playerEvents
from skeletons.account_helpers.settings_core import ISettingsCore
from VehicleGunRotator import VehicleGunRotator

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

aih_constants.GUN_MARKER_MIN_SIZE = 10.0
aih_constants.SPG_GUN_MARKER_MIN_SIZE = 20.0

REPLACE = (gun_marker_ctrl._MARKER_TYPE.CLIENT, gun_marker_ctrl._MARKER_TYPE.DUAL_ACC)


def getSetting(gunMakerType):
    _replace = user_settings.dispersion_circle[DISPERSION.REPLACE]
    _server = user_settings.dispersion_circle[DISPERSION.SERVER]
    return _replace or _server if gunMakerType == gun_marker_ctrl._MARKER_TYPE.SERVER else _replace if gunMakerType in REPLACE else False


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
        isServerAim = self._gunMarkerType == gun_marker_ctrl._MARKER_TYPE.SERVER
        if g_replayCtrl.isRecording and (g_replayCtrl.isServerAim and isServerAim or not isServerAim):
            g_replayCtrl.setSPGGunMarkerParams(dispersionAngle, 0.0)
        self._dataProvider.setupConicDispersion(dispersionAngle)


class DispersionCircle(object):

    def __init__(self):
        user_settings.onModSettingsChanged += self.onModSettingsChanged
        self.enabled = False

    def fini(self):
        user_settings.onModSettingsChanged -= self.onModSettingsChanged

    @staticmethod
    def createOverrideComponents(base, *args):
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
    def enableServerMarker():
        settingsCore = dependency.instance(ISettingsCore)
        if settingsCore.getSetting(GAME.ENABLE_SERVER_AIM):
            settingsCore.applySettings({GAME.ENABLE_SERVER_AIM: 0})
            settingsCore.applyStorages(False)
            settingsCore.clearStorages()
        getPlayer().cell.setServerMarker(True)

    @staticmethod
    def setGunMarkerColor(base, cr_panel, markerType, color):
        base(cr_panel, gun_marker_ctrl._MARKER_TYPE.SERVER, color)
        return base(cr_panel, markerType, color)

    def onModSettingsChanged(self, config, blockID):
        if blockID != DISPERSION.NAME:
            return

        isEnabled = config[GLOBAL.ENABLED]
        replace = isEnabled and config[DISPERSION.REPLACE]
        server = isEnabled and config[DISPERSION.SERVER]
        shouldOverride = replace or server

        if self.enabled != shouldOverride:
            self.enabled = shouldOverride
            self.toggleCreateGunMarkerOverride(shouldOverride)

        self.toggleServerCrossOverrides(server)

    def toggleServerCrossOverrides(self, enable):
        if enable:
            g_playerEvents.onAvatarReady += self.enableServerMarker
        else:
            g_playerEvents.onAvatarReady -= self.enableServerMarker

        server_overrides = (
            (gm_factory, "createComponents", self.createOverrideComponents),
            (gm_factory, "overrideComponents", self.createOverrideComponents),
            (gun_marker_ctrl, "useDefaultGunMarkers", self.useDefaultGunMarkers),
            (gun_marker_ctrl, "useClientGunMarker", self.useGunMarker),
            (gun_marker_ctrl, "useServerGunMarker", self.useGunMarker),
            (VehicleGunRotator, "applySettings", self.onPass),
            (VehicleGunRotator, "setShotPosition", self.setShotPositionWG if IS_WG_CLIENT else self.setShotPositionLesta),
            (CrosshairDataProxy, "__onServerGunMarkerStateChanged", self.onPass),
            (CrosshairPanelContainer, "setGunMarkerColor", self.setGunMarkerColor)
        )

        for obj, method_name, func in server_overrides:
            self.toggleOverride(obj, method_name, func, enable)

    def toggleCreateGunMarkerOverride(self, enable):
        if IS_WG_CLIENT:
            self.toggleOverride(gun_marker_ctrl, "createGunMarker", self.createGunMarker_WG, enable)
        else:
            self.toggleOverride(gun_marker_ctrl, "createDefaultGunMarker", self.createDefaultGunMarker, enable)
            self.toggleOverride(gun_marker_ctrl, "createStrategicGunMarker", self.createStrategicGunMarker, enable)
            self.toggleOverride(gun_marker_ctrl, "createAssaultSpgGunMarker", self.createStrategicGunMarker, enable)

    def createGunMarker_WG(self, baseCreateGunMarker, isStrategic):
        if isStrategic:
            return self.createStrategicGunMarker()
        else:
            return self.createDefaultGunMarker()

    @staticmethod
    def toggleOverride(obj, method_name, func, enable):
        if enable:
            overrideMethod(obj, method_name)(func)
        else:
            cancelOverride(obj, method_name, func.__name__)

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

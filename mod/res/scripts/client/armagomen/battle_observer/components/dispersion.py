import aih_constants
from armagomen._constants import DISPERSION, GLOBAL
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import getPlayer, isReplay, overrideMethod
from AvatarInputHandler import gun_marker_ctrl
from BattleReplay import g_replayCtrl
from constants import SERVER_TICK_LENGTH
from gui.battle_control.controllers.crosshair_proxy import CrosshairDataProxy
from gui.Scaleform.daapi.view.battle.shared.crosshair import gm_factory
from gui.Scaleform.daapi.view.battle.shared.crosshair.container import CrosshairPanelContainer
from gui.Scaleform.genConsts.GUN_MARKER_VIEW_CONSTANTS import GUN_MARKER_VIEW_CONSTANTS as _CONSTANTS
from VehicleGunRotator import VehicleGunRotator

CLIENT = gun_marker_ctrl._MARKER_TYPE.CLIENT
SERVER = gun_marker_ctrl._MARKER_TYPE.SERVER
DUAL_ACC = gun_marker_ctrl._MARKER_TYPE.DUAL_ACC
EMPTY = gun_marker_ctrl._MARKER_TYPE.UNDEFINED

DEV_FACTORIES_COLLECTION = (
    gm_factory._DevControlMarkersFactory,
    gm_factory._OptionalMarkersFactory,
    gm_factory._EquipmentMarkersFactory
)
LINKAGES = {
    _CONSTANTS.DEBUG_SPG_GUN_MARKER_NAME: _CONSTANTS.GUN_MARKER_SPG_LINKAGE,
    _CONSTANTS.DEBUG_ARCADE_GUN_MARKER_NAME: _CONSTANTS.GUN_MARKER_LINKAGE,
    _CONSTANTS.DEBUG_SNIPER_GUN_MARKER_NAME: _CONSTANTS.GUN_MARKER_LINKAGE,
    _CONSTANTS.DEBUG_DUAL_GUN_ARCADE_MARKER_NAME: _CONSTANTS.DUAL_GUN_ARCADE_MARKER_LINKAGE,
    _CONSTANTS.DEBUG_DUAL_GUN_SNIPER_MARKER_NAME: _CONSTANTS.DUAL_GUN_SNIPER_MARKER_LINKAGE
}

gm_factory._GUN_MARKER_LINKAGES.update(LINKAGES)

aih_constants.GUN_MARKER_MIN_SIZE = 12.0
aih_constants.SPG_GUN_MARKER_MIN_SIZE = 24.0

REPLACE = {CLIENT, DUAL_ACC}


def getSetting(gunMakerType):
    if gunMakerType in REPLACE:
        return user_settings.dispersion_circle[DISPERSION.REPLACE]
    elif gunMakerType == SERVER:
        return user_settings.dispersion_circle[DISPERSION.SERVER]
    return False


class _DefaultGunMarkerController(gun_marker_ctrl._DefaultGunMarkerController):

    def __init__(self, gunMakerType, dataProvider, **kwargs):
        super(_DefaultGunMarkerController, self).__init__(gunMakerType, dataProvider, **kwargs)
        self.__scaleConfig = float(user_settings.dispersion_circle[DISPERSION.SCALE]) if getSetting(
            gunMakerType) else 1.0

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
        self.__scaleConfig = float(user_settings.dispersion_circle[DISPERSION.SCALE]) if getSetting(
            gunMakerType) else 1.0

    def _updateDispersionData(self):
        self._size *= self.__scaleConfig
        dispersionAngle = self._gunRotator.dispersionAngle * self.__scaleConfig
        isServerAim = self._gunMarkerType == SERVER
        if g_replayCtrl.isRecording and (g_replayCtrl.isServerAim and isServerAim or not isServerAim):
            g_replayCtrl.setSPGGunMarkerParams(dispersionAngle, 0.0)
        self._dataProvider.setupConicDispersion(dispersionAngle)


class DispersionCircle(object):

    def __init__(self):
        self.enabled = False
        self.server = False
        user_settings.onModSettingsChanged += self.onModSettingsChanged
        overrideMethod(gm_factory, "createComponents")(self.createOverrideComponents)
        overrideMethod(gm_factory, "overrideComponents")(self.createOverrideComponents)
        overrideMethod(gun_marker_ctrl, "createGunMarker")(self.createGunMarker)
        overrideMethod(gun_marker_ctrl, "useDefaultGunMarkers")(self.useDefaultGunMarkers)
        overrideMethod(gun_marker_ctrl, "useClientGunMarker")(self.useGunMarker)
        overrideMethod(gun_marker_ctrl, "useServerGunMarker")(self.useGunMarker)
        overrideMethod(VehicleGunRotator, "applySettings")(self.applySettings)
        overrideMethod(VehicleGunRotator, "setShotPosition")(self.setShotPosition)
        overrideMethod(CrosshairDataProxy, "__onServerGunMarkerStateChanged")(self.onServerGunMarkerStateChanged)
        overrideMethod(CrosshairPanelContainer, "setGunMarkerColor")(self.setGunMarkerColor)

    def createOverrideComponents(self, base, *args):
        if not self.server:
            return base(*args)
        player = getPlayer()
        player.enableServerAim(True)
        if len(args) == 2:
            return gm_factory._GunMarkersFactories(*DEV_FACTORIES_COLLECTION).create(*args)
        return gm_factory._GunMarkersFactories(*DEV_FACTORIES_COLLECTION).override(*args)

    def useDefaultGunMarkers(self, base, *args, **kwargs):
        return not self.server or base(*args, **kwargs)

    def useGunMarker(self, base, *args, **kwargs):
        return self.server or base(*args, **kwargs)

    def applySettings(self, base, *args, **kwargs):
        return None if self.server else base(*args, **kwargs)

    def setShotPosition(self, base, rotator, vehicleID, sPos, sVec, dispersionAngle, forceValueRefresh=False):
        base(rotator, vehicleID, sPos, sVec, dispersionAngle, forceValueRefresh=forceValueRefresh)
        if not self.server:
            return
        m_position = rotator._VehicleGunRotator__getGunMarkerPosition(sPos, sVec, rotator.getCurShotDispersionAngles())
        mPos, mDir, mSize, dualAccSize, mSizeOffset, collData = m_position
        rotator._avatar.inputHandler.updateServerGunMarker(mPos, mDir, mSize, mSizeOffset, SERVER_TICK_LENGTH, collData)

    def onServerGunMarkerStateChanged(self, base, *args, **kwargs):
        return None if self.server else base(*args, **kwargs)

    def setGunMarkerColor(self, base, cr_panel, markerType, color):
        if self.server and markerType == CLIENT:
            base(cr_panel, SERVER, color)
        return base(cr_panel, markerType, color)

    def onModSettingsChanged(self, config, blockID):
        if blockID == DISPERSION.NAME:
            self.enabled = config[GLOBAL.ENABLED] and not isReplay()
            self.server = config[DISPERSION.SERVER] and self.enabled

    def createGunMarker(self, baseCreateGunMarker, isStrategic):
        if not self.enabled:
            return baseCreateGunMarker(isStrategic)
        factory = gun_marker_ctrl._GunMarkersDPFactory()
        if isStrategic:
            client = SPGController(CLIENT, factory.getClientSPGProvider())
            server = SPGController(SERVER, factory.getServerSPGProvider())
            dual = gun_marker_ctrl._EmptyGunMarkerController(EMPTY, None)
        else:
            client = _DefaultGunMarkerController(CLIENT, factory.getClientProvider())
            server = _DefaultGunMarkerController(SERVER, factory.getServerProvider())
            dual = _DualAccMarkerController(DUAL_ACC, factory.getDualAccuracyProvider())
        return gun_marker_ctrl._GunMarkersDecorator(client, server, dual)


dispersion_circle = DispersionCircle()
dispersion_circle.onModSettingsChanged(user_settings.dispersion_circle, DISPERSION.NAME)


def fini():
    user_settings.onModSettingsChanged -= dispersion_circle.onModSettingsChanged

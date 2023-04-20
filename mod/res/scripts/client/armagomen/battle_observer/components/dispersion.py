from GUI import screenResolution, WGGunMarkerDataProvider, WGSPGGunMarkerDataProvider
from Math import MatrixAnimation

import aih_constants
from AvatarInputHandler import gun_marker_ctrl
from BattleReplay import g_replayCtrl
from VehicleGunRotator import VehicleGunRotator
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import GLOBAL, DISPERSION
from armagomen.utils.common import overrideMethod, getPlayer
from constants import SERVER_TICK_LENGTH
from gui.Scaleform.daapi.view.battle.shared.crosshair import gm_factory
from gui.Scaleform.daapi.view.battle.shared.crosshair.container import CrosshairPanelContainer
from gui.Scaleform.genConsts.GUN_MARKER_VIEW_CONSTANTS import GUN_MARKER_VIEW_CONSTANTS as _CONSTANTS
from gui.battle_control.controllers.crosshair_proxy import CrosshairDataProxy

CLIENT = gun_marker_ctrl._MARKER_TYPE.CLIENT
SERVER = gun_marker_ctrl._MARKER_TYPE.SERVER

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
aih_constants.GUN_MARKER_MIN_SIZE = DISPERSION.GUN_MARKER_MIN_SIZE


class _DefaultGunMarkerController(gun_marker_ctrl._DefaultGunMarkerController):
    __scaleConfig = float(settings.dispersion_circle[DISPERSION.CIRCLE_SCALE_CONFIG])

    def __updateScreenRatio(self):
        self.__screenRatio = screenResolution()[0] * 0.5 * self.__scaleConfig


class SPGController(gun_marker_ctrl._SPGGunMarkerController):
    __scaleConfig = float(settings.dispersion_circle[DISPERSION.CIRCLE_SCALE_CONFIG])

    def _updateDispersionData(self):
        self._size *= self.__scaleConfig
        dispersionAngle = self._gunRotator.dispersionAngle * self.__scaleConfig
        isServerAim = self._gunMarkerType == SERVER
        if g_replayCtrl.isPlaying and g_replayCtrl.isClientReady:
            d, s = g_replayCtrl.getSPGGunMarkerParams()
            if d != DISPERSION.MINUS_ONE_F and s != DISPERSION.MINUS_ONE_F:
                dispersionAngle = d
        elif g_replayCtrl.isRecording and (g_replayCtrl.isServerAim and isServerAim or not isServerAim):
            g_replayCtrl.setSPGGunMarkerParams(dispersionAngle, GLOBAL.ZERO)
        self._dataProvider.setupConicDispersion(dispersionAngle)


class _GunMarkersDPFactory(gun_marker_ctrl._GunMarkersDPFactory):

    @staticmethod
    def _makeDefaultProvider():
        scale = settings.dispersion_circle[DISPERSION.CIRCLE_SCALE_CONFIG]
        limits = (aih_constants.GUN_MARKER_MIN_SIZE * scale, min(screenResolution()))
        dataProvider = WGGunMarkerDataProvider()
        dataProvider.positionMatrixProvider = MatrixAnimation()
        dataProvider.setStartSize(limits[GLOBAL.FIRST])
        dataProvider.sizeConstraint = limits
        return dataProvider

    @staticmethod
    def _makeSPGProvider():
        scale = settings.dispersion_circle[DISPERSION.CIRCLE_SCALE_CONFIG]
        dataProvider = WGSPGGunMarkerDataProvider(aih_constants.SPG_GUN_MARKER_ELEMENTS_COUNT,
                                                  aih_constants.SPG_GUN_MARKER_ELEMENTS_RATE)
        dataProvider.positionMatrixProvider = MatrixAnimation()
        dataProvider.maxTime = DISPERSION.MAX_TIME
        dataProvider.serverTickLength = SERVER_TICK_LENGTH
        dataProvider.sizeScaleRate = aih_constants.SPG_GUN_MARKER_SCALE_RATE * DISPERSION.SPG_GM_SCALE
        dataProvider.sizeConstraint = (aih_constants.SPG_GUN_MARKER_MIN_SIZE * scale,
                                       aih_constants.SPG_GUN_MARKER_MAX_SIZE * scale)
        dataProvider.setRelaxTime(SERVER_TICK_LENGTH)
        return dataProvider


class DispersionCircle(object):
    CREATE = "createComponents"

    def __init__(self):
        self.enabled = False
        self.hooksEnable = False
        self.replaceWGCircle = False
        settings.onModSettingsChanged += self.onModSettingsChanged
        overrideMethod(gm_factory, self.CREATE)(self.createOverrideComponents)
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
        if not self.hooksEnable:
            return base(*args)
        player = getPlayer()
        player.enableServerAim(self.hooksEnable)
        if base.__name__ == self.CREATE:
            return gm_factory._GunMarkersFactories(*DEV_FACTORIES_COLLECTION).create(*args)
        return gm_factory._GunMarkersFactories(*DEV_FACTORIES_COLLECTION).override(*args)

    def useDefaultGunMarkers(self, base, *args, **kwargs):
        return not self.hooksEnable or base(*args, **kwargs)

    def useGunMarker(self, base, *args, **kwargs):
        return self.hooksEnable or base(*args, **kwargs)

    def applySettings(self, base, *args, **kwargs):
        return None if self.hooksEnable else base(*args, **kwargs)

    def setShotPosition(self, base, rotator, vehicleID, sPos, sVec, dispersionAngle, forceValueRefresh=False):
        base(rotator, vehicleID, sPos, sVec, dispersionAngle, forceValueRefresh=forceValueRefresh)
        if not self.hooksEnable:
            return
        ePos, mDir, mSize, imSize, collData = \
            rotator._VehicleGunRotator__getGunMarkerPosition(sPos, sVec, rotator.getCurShotDispersionAngles())
        rotator._avatar.inputHandler.updateGunMarker2(ePos, mDir, (mSize, imSize), SERVER_TICK_LENGTH, collData)

    def onServerGunMarkerStateChanged(self, base, *args, **kwargs):
        return base(*args, **kwargs) if not self.hooksEnable else None

    def setGunMarkerColor(self, base, cr_panel, markerType, color):
        if self.hooksEnable and markerType == CLIENT:
            base(cr_panel, SERVER, color)
        return base(cr_panel, markerType, color)

    def onModSettingsChanged(self, config, blockID):
        if blockID == DISPERSION.NAME:
            self.enabled = config[GLOBAL.ENABLED] and not g_replayCtrl.isPlaying
            self.replaceWGCircle = config[DISPERSION.CIRCLE_REPLACE]
            self.hooksEnable = self.enabled and config[DISPERSION.CIRCLE_EXTRA_LAP]

    def createGunMarker(self, baseCreateGunMarker, isStrategic):
        if not self.enabled:
            return baseCreateGunMarker(isStrategic)
        bo_factory = _GunMarkersDPFactory()
        wg_factory = gun_marker_ctrl._GunMarkersDPFactory()
        if isStrategic:
            if self.replaceWGCircle:
                client = SPGController(CLIENT, bo_factory.getClientSPGProvider())
            else:
                client = gun_marker_ctrl._SPGGunMarkerController(CLIENT, wg_factory.getClientSPGProvider())
            server = SPGController(SERVER, bo_factory.getServerSPGProvider())
        else:
            if self.replaceWGCircle:
                client = _DefaultGunMarkerController(CLIENT, bo_factory.getClientProvider())
            else:
                client = gun_marker_ctrl._DefaultGunMarkerController(CLIENT, wg_factory.getClientProvider())
            server = _DefaultGunMarkerController(SERVER, bo_factory.getServerProvider())
        return gun_marker_ctrl._GunMarkersDecorator(client, server)


dispersion_circle = DispersionCircle()

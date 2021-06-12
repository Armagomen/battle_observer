from GUI import screenResolution, WGGunMarkerDataProvider, WGSPGGunMarkerDataProvider
from Math import MatrixAnimation

import aih_constants
from AvatarInputHandler import gun_marker_ctrl
from AvatarInputHandler.gun_marker_ctrl import _MARKER_TYPE, _MARKER_FLAG, \
    _SPGGunMarkerController, _DefaultGunMarkerController, _GunMarkersDecorator, _GunMarkersDPFactory
from BattleReplay import g_replayCtrl
from VehicleGunRotator import VehicleGunRotator
from armagomen.battle_observer.core import settings
from armagomen.constants import GLOBAL, DISPERSION
from armagomen.utils.common import overrideMethod, getPlayer
from constants import SERVER_TICK_LENGTH
from gui.Scaleform.daapi.view.battle.shared.crosshair import gm_factory
from gui.Scaleform.daapi.view.battle.shared.crosshair.container import CrosshairPanelContainer
from gui.Scaleform.genConsts.GUN_MARKER_VIEW_CONSTANTS import GUN_MARKER_VIEW_CONSTANTS as _CONSTANTS
from gui.battle_control.controllers.crosshair_proxy import CrosshairDataProxy
from gui.shared.personality import ServicesLocator
from helpers import dependency
from skeletons.gui.shared.utils import IHangarSpace

CLIENT = _MARKER_TYPE.CLIENT
SERVER = _MARKER_TYPE.SERVER

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


class ObserverGunMarkerController(_DefaultGunMarkerController):

    def __init__(self, *args, **kwargs):
        super(ObserverGunMarkerController, self).__init__(*args, **kwargs)

    def _DefaultGunMarkerController__updateScreenRatio(self):
        super(ObserverGunMarkerController, self)._DefaultGunMarkerController__updateScreenRatio()
        self._DefaultGunMarkerController__screenRatio *= DISPERSION.CIRCLE_SCALE


class ObserverSPGGunMarkerController(_SPGGunMarkerController):

    def __init__(self, *args, **kwargs):
        super(ObserverSPGGunMarkerController, self).__init__(*args, **kwargs)

    def _updateDispersionData(self):
        self._size *= DISPERSION.CIRCLE_SCALE
        dispersionAngle = self._gunRotator.dispersionAngle * DISPERSION.CIRCLE_SCALE
        isServerAim = self._gunMarkerType == SERVER
        if g_replayCtrl.isPlaying and g_replayCtrl.isClientReady:
            d, s = g_replayCtrl.getSPGGunMarkerParams()
            if d != DISPERSION.MINUS_ONE_F and s != DISPERSION.MINUS_ONE_F:
                dispersionAngle = d
        elif g_replayCtrl.isRecording and (g_replayCtrl.isServerAim and isServerAim or not isServerAim):
            g_replayCtrl.setSPGGunMarkerParams(dispersionAngle, GLOBAL.F_ZERO)
        self._dataProvider.setupConicDispersion(dispersionAngle)


class _DispersionDecorator(_GunMarkersDecorator):

    def __init__(self, clientMarker, serverMarker, replaceOriginalCircle, extraServerLap):
        super(_DispersionDecorator, self).__init__(clientMarker, serverMarker)
        self.__extraServerLap = extraServerLap
        self.__replaceOriginalCircle = replaceOriginalCircle

    def update(self, markerType, position, direction, size, relaxTime, collData):
        if self.__replaceOriginalCircle:
            super(_DispersionDecorator, self).update(markerType, position, direction, size, relaxTime, collData)
        else:
            if markerType == CLIENT:
                self.__updateClient(position, direction, size, relaxTime, collData)
                if not self.__extraServerLap:
                    self.__updateServer(position, direction, size, relaxTime, collData)
            elif markerType == SERVER and self.__extraServerLap:
                self.__updateServer(position, direction, size, relaxTime, collData)

    def __updateClient(self, position, direction, size, relaxTime, collData):
        self._GunMarkersDecorator__clientState = (position, direction, collData)
        if self._GunMarkersDecorator__gunMarkersFlags & _MARKER_FLAG.CLIENT_MODE_ENABLED:
            self._GunMarkersDecorator__clientMarker.update(CLIENT, position, direction, size, relaxTime, collData)

    def __updateServer(self, position, direction, size, relaxTime, collData):
        self._GunMarkersDecorator__serverState = (position, direction, collData)
        if self._GunMarkersDecorator__gunMarkersFlags & _MARKER_FLAG.SERVER_MODE_ENABLED:
            self._GunMarkersDecorator__serverMarker.update(SERVER, position, direction, size, relaxTime, collData)


class BOGunMarkersDPFactory(_GunMarkersDPFactory):

    def __init__(self, *args, **kwargs):
        super(BOGunMarkersDPFactory, self).__init__(*args, **kwargs)

    @staticmethod
    def _makeDefaultProvider():
        limits = (aih_constants.GUN_MARKER_MIN_SIZE * DISPERSION.CIRCLE_SCALE, min(screenResolution()))
        dataProvider = WGGunMarkerDataProvider()
        dataProvider.positionMatrixProvider = MatrixAnimation()
        dataProvider.setStartSize(limits[GLOBAL.FIRST])
        dataProvider.sizeConstraint = limits
        return dataProvider

    @staticmethod
    def _makeSPGProvider():
        dataProvider = WGSPGGunMarkerDataProvider(aih_constants.SPG_GUN_MARKER_ELEMENTS_COUNT,
                                                  aih_constants.SPG_GUN_MARKER_ELEMENTS_RATE)
        dataProvider.positionMatrixProvider = MatrixAnimation()
        dataProvider.maxTime = DISPERSION.MAX_TIME
        dataProvider.serverTickLength = SERVER_TICK_LENGTH
        dataProvider.sizeScaleRate = aih_constants.SPG_GUN_MARKER_SCALE_RATE * DISPERSION.SPG_GM_SCALE
        dataProvider.sizeConstraint = (aih_constants.SPG_GUN_MARKER_MIN_SIZE * DISPERSION.CIRCLE_SCALE,
                                       aih_constants.SPG_GUN_MARKER_MAX_SIZE * DISPERSION.CIRCLE_SCALE)
        dataProvider.setRelaxTime(SERVER_TICK_LENGTH)
        return dataProvider


class DispersionCircle(object):
    hangarSpace = dependency.descriptor(IHangarSpace)
    settingsCore = ServicesLocator.settingsCore

    def __init__(self):
        self.handleChanged = False
        self.enabled = False
        self.hooksEnable = False
        self.replaceOriginalCircle = False
        self.extraServerLap = False
        self.player = None
        settings.onModSettingsChanged += self.onModSettingsChanged
        overrideMethod(gun_marker_ctrl, "createGunMarker")(self.createGunMarker)
        overrideMethod(gm_factory, "createComponents")(self.createOverrideComponents)
        overrideMethod(gm_factory, "overrideComponents")(self.createOverrideComponents)
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
        self.player.base.setDevelopmentFeature(0, 'server_marker', True, '')
        if base.__name__ == "createComponents":
            return gm_factory._GunMarkersFactories(*DEV_FACTORIES_COLLECTION).create(*args)
        return gm_factory._GunMarkersFactories(*DEV_FACTORIES_COLLECTION).override(*args)

    def useDefaultGunMarkers(self, base, *args, **kwargs):
        return not self.hooksEnable or base(*args, **kwargs)

    def useGunMarker(self, base, *args, **kwargs):
        return self.hooksEnable or base(*args, **kwargs)

    def applySettings(self, base, *args, **kwargs):
        return None if self.hooksEnable else base(*args, **kwargs)

    def setShotPosition(self, base, gun, vehicleID, sPos, sVec, dispersionAngle, forceValueRefresh=False):
        if self.hooksEnable:
            mPos, mDir, mSize, imSize, collData = \
                gun._VehicleGunRotator__getGunMarkerPosition(sPos, sVec, gun._VehicleGunRotator__dispersionAngles)
            gun._VehicleGunRotator__lastShotPoint = mPos
            gun._avatar.inputHandler.updateGunMarker2(mPos, mDir, (mSize, imSize), SERVER_TICK_LENGTH, collData)
        else:
            return base(gun, vehicleID, sPos, sVec, dispersionAngle, forceValueRefresh=forceValueRefresh)

    def onServerGunMarkerStateChanged(self, base, *args, **kwargs):
        return base(*args, **kwargs) if not self.hooksEnable else None

    def setGunMarkerColor(self, base, cr_panel, markerType, color):
        if self.hooksEnable and markerType == _MARKER_TYPE.CLIENT:
            base(cr_panel, _MARKER_TYPE.SERVER, color)
        return base(cr_panel, markerType, color)

    def onModSettingsChanged(self, config, blockID):
        if blockID == DISPERSION.NAME:
            self.replaceOriginalCircle = config[DISPERSION.CIRCLE_REPLACE]
            self.extraServerLap = config[DISPERSION.CIRCLE_EXTRA_LAP]
            self.enabled = config[GLOBAL.ENABLED] and config[DISPERSION.ENABLED] and not \
                g_replayCtrl.isPlaying
            self.hooksEnable = self.enabled and (not self.replaceOriginalCircle or self.extraServerLap)
            DISPERSION.CIRCLE_SCALE = config[DISPERSION.CIRCLE_SCALE_CONFIG] * 0.01

    def createGunMarker(self, baseCreateGunMarker, isStrategic):
        if self.enabled:
            self.player = getPlayer()
            bo_factory = BOGunMarkersDPFactory()
            if isStrategic:
                if self.replaceOriginalCircle:
                    client = ObserverSPGGunMarkerController(CLIENT, bo_factory.getClientSPGProvider())
                else:
                    client = _SPGGunMarkerController(CLIENT, _GunMarkersDPFactory().getClientSPGProvider())
                server = ObserverSPGGunMarkerController(SERVER, bo_factory.getServerSPGProvider())
            else:
                if self.replaceOriginalCircle:
                    client = ObserverGunMarkerController(CLIENT, bo_factory.getClientProvider())
                else:
                    client = _DefaultGunMarkerController(CLIENT, _GunMarkersDPFactory().getClientProvider())
                server = ObserverGunMarkerController(SERVER, bo_factory.getServerProvider())
            return _DispersionDecorator(client, server, self.replaceOriginalCircle, self.extraServerLap)
        else:
            return baseCreateGunMarker(isStrategic)


dispersion_circle = DispersionCircle()

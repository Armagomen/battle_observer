from GUI import screenResolution, WGGunMarkerDataProvider, WGSPGGunMarkerDataProvider
from Math import MatrixAnimation

import aih_constants
from Avatar import PlayerAvatar
from AvatarInputHandler import gun_marker_ctrl
from AvatarInputHandler.gun_marker_ctrl import _MARKER_TYPE, _MARKER_FLAG, \
    _SPGGunMarkerController, _DefaultGunMarkerController, _GunMarkersDecorator, _GunMarkersDPFactory
from BattleReplay import g_replayCtrl
from VehicleGunRotator import VehicleGunRotator
from constants import SERVER_TICK_LENGTH
from gui.Scaleform.daapi.view.battle.shared.crosshair import gm_factory
from gui.Scaleform.daapi.view.battle.shared.crosshair.container import CrosshairPanelContainer
from gui.Scaleform.genConsts.GUN_MARKER_VIEW_CONSTANTS import GUN_MARKER_VIEW_CONSTANTS as _CONSTANTS
from gui.battle_control.controllers.crosshair_proxy import CrosshairDataProxy
from gui.shared.personality import ServicesLocator
from ..core.battle_cache import cache
from ..core.bo_constants import GLOBAL, DISPERSION_CIRCLE
from ..core.core import overrideMethod
from ..core.events import g_events

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

aih_constants.GUN_MARKER_MIN_SIZE = DISPERSION_CIRCLE.GUN_MARKER_MIN_SIZE

class ObserverGunMarkerController(_DefaultGunMarkerController):

    def __init__(self, *args, **kwargs):
        super(ObserverGunMarkerController, self).__init__(*args, **kwargs)

    def _DefaultGunMarkerController__updateScreenRatio(self):
        super(ObserverGunMarkerController, self)._DefaultGunMarkerController__updateScreenRatio()
        self._DefaultGunMarkerController__screenRatio *= DISPERSION_CIRCLE.CIRCLE_SCALE


class ObserverSPGGunMarkerController(_SPGGunMarkerController):

    def __init__(self, *args, **kwargs):
        super(ObserverSPGGunMarkerController, self).__init__(*args, **kwargs)

    def _updateDispersionData(self):
        self._size *= DISPERSION_CIRCLE.CIRCLE_SCALE
        dispersionAngle = self._gunRotator.dispersionAngle * DISPERSION_CIRCLE.CIRCLE_SCALE
        isServerAim = self._gunMarkerType == SERVER
        if g_replayCtrl.isPlaying and g_replayCtrl.isClientReady:
            d, s = g_replayCtrl.getSPGGunMarkerParams()
            if d != DISPERSION_CIRCLE.MINUS_ONE_F and s != DISPERSION_CIRCLE.MINUS_ONE_F:
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
        limits = (aih_constants.GUN_MARKER_MIN_SIZE * DISPERSION_CIRCLE.CIRCLE_SCALE, min(screenResolution()))
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
        dataProvider.maxTime = DISPERSION_CIRCLE.MAX_TIME
        dataProvider.serverTickLength = SERVER_TICK_LENGTH
        dataProvider.sizeScaleRate = aih_constants.SPG_GUN_MARKER_SCALE_RATE * DISPERSION_CIRCLE.SPG_GM_SCALE
        dataProvider.sizeConstraint = (aih_constants.SPG_GUN_MARKER_MIN_SIZE * DISPERSION_CIRCLE.CIRCLE_SCALE,
                                       aih_constants.SPG_GUN_MARKER_MAX_SIZE * DISPERSION_CIRCLE.CIRCLE_SCALE)
        dataProvider.setRelaxTime(SERVER_TICK_LENGTH)
        return dataProvider


class DispersionCircle(object):

    def __init__(self):
        self.enabled = False
        self.hooksEnable = False
        self.replaceOriginalCircle = False
        self.extraServerLap = False
        g_events.onSettingsChanged += self.onSettingsChanged

    def onSettingsChanged(self, config, blockID):
        if blockID == DISPERSION_CIRCLE.NAME:
            self.replaceOriginalCircle = config[DISPERSION_CIRCLE.CIRCLE_REPLACE]
            self.extraServerLap = config[DISPERSION_CIRCLE.CIRCLE_EXTRA_LAP]
            self.enabled = config[GLOBAL.ENABLED] and config[DISPERSION_CIRCLE.CIRCLE_ENABLED] and not \
                g_replayCtrl.isPlaying
            self.hooksEnable = self.enabled and (not self.replaceOriginalCircle or self.extraServerLap)
            DISPERSION_CIRCLE.CIRCLE_SCALE = round(config[DISPERSION_CIRCLE.CIRCLE_SCALE_CONFIG] / 100.0, 2)
            if self.enabled:
                gm_factory._GUN_MARKER_LINKAGES.update(LINKAGES)


    def enableServerAim(self, server=True):
        if not bool(ServicesLocator.settingsCore.getSetting(DISPERSION_CIRCLE.CIRCLE_SERVER)):
            cache.player.enableServerAim(server)

    @staticmethod
    def setShotPosition(gun, vehicleID, sPos, sVec, dispersionAngle, forceValueRefresh=False):
        mPos, mDir, mSize, imSize, collData = \
            gun._VehicleGunRotator__getGunMarkerPosition(sPos, sVec, gun._VehicleGunRotator__dispersionAngles)
        gun._avatar.inputHandler.updateGunMarker2(mPos, mDir, (mSize, imSize), SERVER_TICK_LENGTH, collData)
        gun._VehicleGunRotator__lastShotPoint = mPos

    def createGunMarker(self, baseCreateGunMarker, isStrategic):
        if self.enabled:
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


@overrideMethod(gm_factory, "createComponents")
def createComponents(base, *args):
    if dispersion_circle.hooksEnable:
        dispersion_circle.enableServerAim()
        return gm_factory._GunMarkersFactories(*DEV_FACTORIES_COLLECTION).create(*args)
    else:
        return base(*args)


@overrideMethod(gm_factory, "overrideComponents")
def overrideComponents(base, *args):
    if dispersion_circle.hooksEnable:
        dispersion_circle.enableServerAim()
        return gm_factory._GunMarkersFactories(*DEV_FACTORIES_COLLECTION).override(*args)
    else:
        return base(*args)


@overrideMethod(gun_marker_ctrl, "createGunMarker")
def createMarker(base, *args, **kwargs):
    return dispersion_circle.createGunMarker(base, *args, **kwargs)


@overrideMethod(gun_marker_ctrl, "useDefaultGunMarkers")
def useDefault(base, *args, **kwargs):
    return not dispersion_circle.hooksEnable or base(*args, **kwargs)


@overrideMethod(gun_marker_ctrl, "useClientGunMarker")
@overrideMethod(gun_marker_ctrl, "useServerGunMarker")
def useGunMarker(base, *args, **kwargs):
    return dispersion_circle.hooksEnable or base(*args, **kwargs)


@overrideMethod(PlayerAvatar, "enableServerAim")
def enableServerAim(base, avatar, enable):
    return base(avatar, dispersion_circle.hooksEnable or enable)


@overrideMethod(VehicleGunRotator, "applySettings")
def applySettings(base, *args, **kwargs):
    return None if dispersion_circle.hooksEnable else base(*args, **kwargs)


@overrideMethod(VehicleGunRotator, "setShotPosition")
def setShotPosition(base, *args, **kwargs):
    if dispersion_circle.hooksEnable:
        return dispersion_circle.setShotPosition(*args, **kwargs)
    else:
        return base(*args, **kwargs)


@overrideMethod(CrosshairDataProxy, "__onServerGunMarkerStateChanged")
def onServerGunMarkerStateChanged(base, *args, **kwargs):
    if not dispersion_circle.hooksEnable:
        return base(*args, **kwargs)


@overrideMethod(CrosshairPanelContainer, "setGunMarkerColor")
def setGunMarkerColor(base, cr_panel, markerType, color):
    if dispersion_circle.hooksEnable and markerType == _MARKER_TYPE.CLIENT:
        base(cr_panel, _MARKER_TYPE.SERVER, color)
    return base(cr_panel, markerType, color)

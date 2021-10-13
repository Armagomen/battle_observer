import math

from Avatar import PlayerAvatar
from AvatarInputHandler.DynamicCameras.ArcadeCamera import ArcadeCamera, MinMax
from AvatarInputHandler.DynamicCameras.ArtyCamera import ArtyCamera
from AvatarInputHandler.DynamicCameras.SniperCamera import SniperCamera
from AvatarInputHandler.DynamicCameras.StrategicCamera import StrategicCamera
from account_helpers.settings_core.options import SniperZoomSetting
from aih_constants import CTRL_MODE_NAME
from armagomen.battle_observer.core import settings
from armagomen.constants import ARCADE, GLOBAL, SNIPER, STRATEGIC, EFFECTS
from armagomen.utils.common import overrideMethod, getPlayer, logError, isReplay, callback

settingsCache = {"needReloadArcadeConfig": False, "needReloadStrategicConfig": False, SNIPER.DYN_ZOOM: False}


@overrideMethod(SniperCamera, "_readConfigs")
def sniper_create(base, camera, data):
    base(camera, data)
    if settings.effects[EFFECTS.NO_SNIPER_DYNAMIC] and camera.isCameraDynamic():
        camera.enableDynamicCamera(False)
    if not settings.zoom[GLOBAL.ENABLED] or isReplay() or not settings.zoom[SNIPER.ZOOM_STEPS][GLOBAL.ENABLED]:
        return
    if len(settings.zoom[SNIPER.ZOOM_STEPS][SNIPER.STEPS]) > GLOBAL.TWO:
        steps = settings.zoom[SNIPER.ZOOM_STEPS][SNIPER.STEPS]
        steps.sort()
        exposure_range = xrange(len(steps) + GLOBAL.ONE, GLOBAL.ONE, -GLOBAL.ONE)
        configs = (camera._cfg, camera._userCfg, camera._baseCfg)
        for cfg in configs:
            cfg[SNIPER.INCREASED_ZOOM] = True
            cfg[SNIPER.ZOOMS] = steps
        camera._SniperCamera__dynamicCfg[SNIPER.ZOOM_EXPOSURE] = [
            round(SNIPER.EXPOSURE_FACTOR * step, GLOBAL.ONE) for step in exposure_range
        ]


@overrideMethod(SniperCamera, "__getZooms")
def new__getZooms(base, camera):
    if not settings.zoom[GLOBAL.ENABLED] or isReplay() or not settings.zoom[SNIPER.ZOOM_STEPS][GLOBAL.ENABLED]:
        return base(camera)
    return camera._cfg['zooms']


@overrideMethod(SniperZoomSetting, "setSystemValue")
def setSystemValue(base, zoomSettings, value):
    return base(zoomSettings, GLOBAL.ZERO if settingsCache[SNIPER.DYN_ZOOM] else value)


@overrideMethod(SniperCamera, "enable")
def enable(base, camera, targetPos, saveZoom):
    if settingsCache[SNIPER.DYN_ZOOM]:
        player = getPlayer()
        saveZoom = True
        if settings.zoom[SNIPER.GUN_ZOOM]:
            targetPos = player.gunRotator.markerInfo[GLOBAL.FIRST]
        dist = player.position.distTo(targetPos)
        if settings.zoom[SNIPER.DYN_ZOOM][SNIPER.STEPS_ONLY]:
            dist_for_step = math.ceil(SNIPER.MAX_DIST / len(camera._cfg[SNIPER.ZOOMS]))
            index = int(math.floor(dist / dist_for_step))
            zoom = camera._cfg[SNIPER.ZOOMS][index]
        else:
            zoom = min(math.floor(dist / settings.zoom[SNIPER.DYN_ZOOM][SNIPER.METERS]),
                       camera._cfg[SNIPER.ZOOMS][GLOBAL.LAST])
        camera._cfg[SNIPER.ZOOM] = zoom
    return base(camera, targetPos, saveZoom)


def changeControlMode(avatar):
    input_handler = avatar.inputHandler
    if input_handler is not None and input_handler.ctrlModeName == CTRL_MODE_NAME.SNIPER:
        v_desc = avatar.getVehicleDescriptor()
        caliberSkip = v_desc.shot.shell.caliber <= SNIPER.MAX_CALIBER
        if caliberSkip or settings.zoom[SNIPER.SKIP_CLIP] and SNIPER.CLIP in v_desc.gun.tags:
            return
        aiming_system = input_handler.ctrl.camera.aimingSystem
        input_handler.onControlModeChanged(CTRL_MODE_NAME.ARCADE,
                                           prevModeName=input_handler.ctrlModeName,
                                           preferredPos=aiming_system.getDesiredShotPoint(),
                                           turretYaw=aiming_system.turretYaw,
                                           gunPitch=aiming_system.gunPitch,
                                           aimingMode=input_handler.ctrl._aimingMode,
                                           closesDist=False)


@overrideMethod(PlayerAvatar, "showTracer")
def showTracer(base, avatar, shooterID, *args):
    try:
        if settings.zoom[SNIPER.DISABLE_SNIPER] and settings.zoom[GLOBAL.ENABLED] and not isReplay():
            if shooterID == avatar.playerVehicleID:
                callback(max(settings.zoom[SNIPER.DISABLE_LATENCY], 0), lambda: changeControlMode(avatar))
    except Exception as err:
        logError("I can't get out of sniper mode. Error {0}.changeControlMode, {1}".format(__package__, err))
    finally:
        return base(avatar, shooterID, *args)


def onModSettingsChanged(config, blockID):
    if blockID == ARCADE.NAME:
        settingsCache["needReloadArcadeConfig"] = True
    elif blockID == STRATEGIC.NAME:
        settingsCache["needReloadStrategicConfig"] = True
    elif blockID == SNIPER.NAME:
        settingsCache[SNIPER.DYN_ZOOM] = config[GLOBAL.ENABLED] and not isReplay() and \
                                         config[SNIPER.DYN_ZOOM][GLOBAL.ENABLED]


settings.onModSettingsChanged += onModSettingsChanged


@overrideMethod(ArcadeCamera, "_readConfigs")
@overrideMethod(StrategicCamera, "_readConfigs")
@overrideMethod(ArtyCamera, "_readConfigs")
def reload_configs(base, camera, dataSection):
    if any(settingsCache.itervalues()):
        camera._baseCfg.clear()
        camera._userCfg.clear()
        camera._cfg.clear()
    base(camera, dataSection)


@overrideMethod(ArcadeCamera, "_readBaseCfg")
@overrideMethod(ArcadeCamera, "_readUserCfg")
def arcade_readConfigs(base, camera, *args, **kwargs):
    base(camera, *args, **kwargs)
    if settings.arcade_camera[GLOBAL.ENABLED]:
        baseName = base.__name__
        if baseName == "_readBaseCfg":
            cfg = camera._baseCfg
            cfg[ARCADE.DIST_RANGE] = MinMax(settings.arcade_camera[ARCADE.MIN], settings.arcade_camera[ARCADE.MAX])
            cfg[ARCADE.SCROLL_SENSITIVITY] = settings.arcade_camera[ARCADE.SCROLL_SENSITIVITY]
        elif baseName == "_readUserCfg":
            cfg = camera._userCfg
            cfg[ARCADE.START_DIST] = settings.arcade_camera[ARCADE.START_DEAD_DIST]
            cfg[ARCADE.START_ANGLE] = ARCADE.ANGLE
    settingsCache["needReloadArcadeConfig"] = False


@overrideMethod(StrategicCamera, "_readBaseCfg")
@overrideMethod(ArtyCamera, "_readBaseCfg")
def arty_readConfigs(base, camera, *args, **kwargs):
    base(camera, *args, **kwargs)
    if settings.strategic_camera[GLOBAL.ENABLED]:
        cfg = camera._baseCfg
        cfg[STRATEGIC.DIST_RANGE] = (settings.strategic_camera[STRATEGIC.MIN], settings.strategic_camera[STRATEGIC.MAX])
        cfg[STRATEGIC.SCROLL_SENSITIVITY] = settings.strategic_camera[ARCADE.SCROLL_SENSITIVITY]
    settingsCache["needReloadStrategicConfig"] = False

import math

from Avatar import PlayerAvatar
from AvatarInputHandler.DynamicCameras.ArcadeCamera import ArcadeCamera, MinMax
from AvatarInputHandler.DynamicCameras.ArtyCamera import ArtyCamera
from AvatarInputHandler.DynamicCameras.SniperCamera import SniperCamera
from AvatarInputHandler.DynamicCameras.StrategicCamera import StrategicCamera
from account_helpers.settings_core.options import SniperZoomSetting
from aih_constants import CTRL_MODE_NAME
from armagomen.battle_observer.core import settings
from armagomen.constants import ARCADE, GLOBAL, SNIPER, STRATEGIC
from armagomen.utils.common import overrideMethod, getPlayer, logError, isReplay, callback


def dynamicZoom():
    return settings.zoom[GLOBAL.ENABLED] and not isReplay() and settings.zoom[SNIPER.DYN_ZOOM][GLOBAL.ENABLED]


@overrideMethod(SniperCamera, "_readConfigs")
def sniper_create(base, camera, data):
    base(camera, data)
    if settings.zoom[GLOBAL.ENABLED] and not isReplay():
        if settings.zoom[SNIPER.ZOOM_STEPS][GLOBAL.ENABLED]:
            if len(settings.zoom[SNIPER.ZOOM_STEPS][SNIPER.STEPS]) > GLOBAL.TWO:
                steps = settings.zoom[SNIPER.ZOOM_STEPS][SNIPER.STEPS]
                steps.sort()
                exposure_range = xrange(len(steps) + GLOBAL.ONE, GLOBAL.ONE, -GLOBAL.ONE)
                configs = (camera._cfg, camera._userCfg, camera._baseCfg)
                for cfg in configs:
                    cfg[SNIPER.INCREASED_ZOOM] = True
                    cfg[SNIPER.ZOOMS] = steps
                camera._SniperCamera__dynamicCfg[SNIPER.ZOOM_EXPOSURE] = \
                    [round(SNIPER.EXPOSURE_FACTOR * step, GLOBAL.ONE) for step in exposure_range]


@overrideMethod(SniperZoomSetting, "setSystemValue")
def setSystemValue(base, zoomSettings, value):
    return base(zoomSettings, GLOBAL.ZERO if dynamicZoom() else value)


@overrideMethod(SniperCamera, "enable")
def enable(base, camera, targetPos, saveZoom):
    if dynamicZoom():
        player = getPlayer()
        saveZoom = True
        if settings.zoom[SNIPER.GUN_ZOOM]:
            targetPos = player.gunRotator.markerInfo[GLOBAL.FIRST]
        dist = targetPos.distTo(player.position)
        if settings.zoom[SNIPER.DYN_ZOOM][SNIPER.STEPS_ONLY]:
            dist_for_step = math.ceil(SNIPER.MAX_DIST / len(camera._cfg[SNIPER.ZOOMS]))
            index = int(math.ceil(dist / dist_for_step) - GLOBAL.ONE)
            zoom = camera._cfg[SNIPER.ZOOMS][index]
        else:
            zoom = min(round(dist / settings.zoom[SNIPER.DYN_ZOOM][SNIPER.METERS]),
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
                callback(settings.zoom[SNIPER.DISABLE_LATENCY], lambda: changeControlMode(avatar))
    except Exception as err:
        logError("I can't get out of sniper mode. Error {0}.changeControlMode, {1}".format(__package__, err))
    finally:
        return base(avatar, shooterID, *args)


@overrideMethod(ArcadeCamera, "_readConfigs")
def arcade_readConfigs(base, camera, data):
    base(camera, data)
    if settings.arcade_camera[GLOBAL.ENABLED]:
        configs = (camera._cfg, camera._userCfg, camera._baseCfg)
        for cfg in configs:
            if ARCADE.DIST_RANGE in cfg:
                cfg[ARCADE.DIST_RANGE] = MinMax(settings.arcade_camera[ARCADE.MIN], settings.arcade_camera[ARCADE.MAX])
            if ARCADE.START_DIST in cfg:
                cfg[ARCADE.START_DIST] = settings.arcade_camera[ARCADE.START_DEAD_DIST]
            if ARCADE.START_ANGLE in cfg:
                cfg[ARCADE.START_ANGLE] = ARCADE.ANGLE
        camera._cfg[ARCADE.SCROLL_SENSITIVITY] *= settings.arcade_camera[ARCADE.SCROLL_MULTIPLE]


@overrideMethod(StrategicCamera, "_readConfigs")
@overrideMethod(ArtyCamera, "_readConfigs")
def arty_readConfigs(base, camera, data):
    base(camera, data)
    if settings.strategic_camera[GLOBAL.ENABLED]:
        configs = (camera._cfg, camera._userCfg, camera._baseCfg)
        for cfg in configs:
            if STRATEGIC.DIST_RANGE in cfg:
                dist_range = (settings.strategic_camera[STRATEGIC.MIN], settings.strategic_camera[STRATEGIC.MAX])
                cfg[STRATEGIC.DIST_RANGE] = dist_range
        camera._cfg[ARCADE.SCROLL_SENSITIVITY] *= settings.strategic_camera[ARCADE.SCROLL_MULTIPLE]

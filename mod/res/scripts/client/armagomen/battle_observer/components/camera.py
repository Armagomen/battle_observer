import math
from collections import namedtuple

import TriggersManager
from account_helpers.settings_core.options import SniperZoomSetting
from aih_constants import CTRL_MODE_NAME
from armagomen._constants import ARCADE, EFFECTS, GLOBAL, SNIPER, STRATEGIC
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import callback, getPlayer, isReplay, overrideMethod
from AvatarInputHandler.DynamicCameras.ArcadeCamera import ArcadeCamera
from AvatarInputHandler.DynamicCameras.ArtyCamera import ArtyCamera
from AvatarInputHandler.DynamicCameras.SniperCamera import SniperCamera
from AvatarInputHandler.DynamicCameras.StrategicCamera import StrategicCamera
from debug_utils import LOG_CURRENT_EXCEPTION
from gui.battle_control.avatar_getter import getOwnVehiclePosition
from PlayerEvents import g_playerEvents

DEFAULT_X_METERS = 20.0
settingsCache = {SNIPER.DYN_ZOOM: False, SNIPER.METERS: DEFAULT_X_METERS, SNIPER.STEPS_ONLY: False}
MinMax = namedtuple('MinMax', ('min', 'max'))
camCache = {}


@overrideMethod(SniperCamera, "_readConfigs")
def sniper_readConfigs(base, camera, data):
    camera._baseCfg.clear()
    camera._userCfg.clear()
    camera._cfg.clear()
    base(camera, data)
    if not user_settings.zoom[GLOBAL.ENABLED] or isReplay():
        return
    if user_settings.effects[EFFECTS.NO_SNIPER_DYNAMIC] and camera.isCameraDynamic():
        camera.enableDynamicCamera(False)
    if user_settings.zoom[SNIPER.ZOOM_STEPS][GLOBAL.ENABLED]:
        steps = [step for step in user_settings.zoom[SNIPER.ZOOM_STEPS][SNIPER.STEPS] if step >= SNIPER.MIN_ZOOM]
        if len(steps) > 3:
            steps.sort()
            for cfg in (camera._cfg, camera._userCfg, camera._baseCfg):
                cfg[SNIPER.INCREASED_ZOOM] = True
                cfg[SNIPER.ZOOMS] = steps
            exposure = camera._SniperCamera__dynamicCfg[SNIPER.ZOOM_EXPOSURE]
            while len(steps) > len(exposure):
                exposure.insert(GLOBAL.FIRST, exposure[GLOBAL.ZERO] + SNIPER.EXPOSURE_FACTOR)
    if settingsCache[SNIPER.DYN_ZOOM]:
        camera.setSniperZoomSettings(-1)


@overrideMethod(SniperZoomSetting, "setSystemValue")
def setSystemValue(base, zoomSettings, value):
    return base(zoomSettings, GLOBAL.ZERO if settingsCache[SNIPER.DYN_ZOOM] else value)


def getZoom(distance, steps):
    zoom = math.floor(distance / DEFAULT_X_METERS)
    if settingsCache[SNIPER.STEPS_ONLY]:
        zoom = min(steps, key=lambda value: abs(value - zoom))
    if zoom < SNIPER.MIN_ZOOM:
        return SNIPER.MIN_ZOOM
    return zoom


@overrideMethod(SniperCamera, "enable")
def enable(base, camera, targetPos, saveZoom):
    if settingsCache[SNIPER.DYN_ZOOM]:
        saveZoom = True
        ownPosition = getOwnVehiclePosition()
        distance = (targetPos - ownPosition).length if ownPosition is not None else GLOBAL.ZERO
        if distance > SNIPER.MAX_DIST:
            distance = GLOBAL.ZERO
        camera._cfg[SNIPER.ZOOM] = getZoom(distance, camera._cfg[SNIPER.ZOOMS])
    return base(camera, targetPos, saveZoom)


@overrideMethod(ArcadeCamera, "_readConfigs")
@overrideMethod(StrategicCamera, "_readConfigs")
@overrideMethod(ArtyCamera, "_readConfigs")
def reload_configs(base, camera, dataSection):
    try:
        if camCache.setdefault(camera.__class__.__name__, True):
            camera._baseCfg.clear()
            camera._userCfg.clear()
            camera._cfg.clear()
            camCache[camera.__class__.__name__] = False
    except Exception:
        LOG_CURRENT_EXCEPTION()
    finally:
        return base(camera, dataSection)


@overrideMethod(ArcadeCamera, "_readBaseCfg")
@overrideMethod(ArcadeCamera, "_readUserCfg")
def arcade_readConfigs(base, camera, *args, **kwargs):
    base(camera, *args, **kwargs)
    if user_settings.arcade_camera[GLOBAL.ENABLED]:
        if base.__name__ == "_readBaseCfg":
            cfg = camera._baseCfg
            cfg[ARCADE.DIST_RANGE] = MinMax(user_settings.arcade_camera[ARCADE.MIN],
                                            user_settings.arcade_camera[ARCADE.MAX])
            cfg[ARCADE.SCROLL_SENSITIVITY] = user_settings.arcade_camera[ARCADE.SCROLL_SENSITIVITY]
        elif base.__name__ == "_readUserCfg":
            cfg = camera._userCfg
            cfg[ARCADE.START_DIST] = user_settings.arcade_camera[ARCADE.START_DEAD_DIST]


@overrideMethod(ArcadeCamera, "_updateProperties")
def arcade_updateProperties(base, camera, state=None):
    try:
        if user_settings.arcade_camera[GLOBAL.ENABLED] and state is not None:
            distRange = MinMax(user_settings.arcade_camera[ARCADE.MIN], user_settings.arcade_camera[ARCADE.MAX])
            scrollSensitivity = user_settings.arcade_camera[ARCADE.SCROLL_SENSITIVITY]
            state = state._replace(distRange=distRange, scrollSensitivity=scrollSensitivity)
    except Exception:
        LOG_CURRENT_EXCEPTION()
    finally:
        return base(camera, state=state)


@overrideMethod(StrategicCamera, "_readBaseCfg")
@overrideMethod(ArtyCamera, "_readBaseCfg")
def arty_readConfigs(base, camera, *args, **kwargs):
    base(camera, *args, **kwargs)
    if user_settings.strategic_camera[GLOBAL.ENABLED]:
        cfg = camera._baseCfg
        cfg[STRATEGIC.DIST_RANGE] = (
            user_settings.strategic_camera[STRATEGIC.MIN], user_settings.strategic_camera[STRATEGIC.MAX])
        cfg[STRATEGIC.SCROLL_SENSITIVITY] = user_settings.strategic_camera[ARCADE.SCROLL_SENSITIVITY]


class AfterShoot(TriggersManager.ITriggerListener):

    def __init__(self):
        g_playerEvents.onAvatarBecomePlayer += self.onStartScript
        g_playerEvents.onAvatarBecomeNonPlayer += self.onFinishScript
        self.enabled = False

    def onStartScript(self):
        if self.enabled:
            manager = TriggersManager.g_manager
            if manager:
                manager.addListener(self)

    def onFinishScript(self):
        if self.enabled:
            manager = TriggersManager.g_manager
            if manager:
                manager.delListener(self)

    def onTriggerActivated(self, params):
        if params.get('type') == TriggersManager.TRIGGER_TYPE.PLAYER_DISCRETE_SHOOT:
            callback(max(user_settings.zoom[SNIPER.DISABLE_LATENCY], 0), self.changeControlMode)

    @staticmethod
    def changeControlMode():
        avatar = getPlayer()
        input_handler = avatar.inputHandler
        if input_handler is not None and input_handler.ctrlModeName == CTRL_MODE_NAME.SNIPER:
            v_desc = avatar.getVehicleDescriptor()
            caliberSkip = v_desc.shot.shell.caliber <= SNIPER.MAX_CALIBER
            if caliberSkip or user_settings.zoom[SNIPER.SKIP_CLIP] and SNIPER.CLIP in v_desc.gun.tags:
                return
            aiming_system = input_handler.ctrl.camera.aimingSystem
            input_handler.onControlModeChanged(CTRL_MODE_NAME.ARCADE,
                                               prevModeName=input_handler.ctrlModeName,
                                               preferredPos=aiming_system.getDesiredShotPoint(),
                                               turretYaw=aiming_system.turretYaw,
                                               gunPitch=aiming_system.gunPitch,
                                               aimingMode=input_handler.ctrl._aimingMode,
                                               closesDist=False)


after_shoot = AfterShoot()


def onModSettingsChanged(config, blockID):
    if blockID in (ARCADE.NAME, STRATEGIC.NAME):
        for cam in camCache:
            camCache[cam] = True
    elif blockID == SNIPER.NAME:
        if not config[GLOBAL.ENABLED] or isReplay():
            return
        settingsCache[SNIPER.DYN_ZOOM] = config[SNIPER.DYN_ZOOM][GLOBAL.ENABLED]
        settingsCache[SNIPER.STEPS_ONLY] = config[SNIPER.DYN_ZOOM][SNIPER.STEPS_ONLY]
        after_shoot.enabled = config[SNIPER.DISABLE_SNIPER]


user_settings.onModSettingsChanged += onModSettingsChanged

onModSettingsChanged(user_settings.arcade_camera, ARCADE.NAME)
onModSettingsChanged(user_settings.strategic_camera, STRATEGIC.NAME)
onModSettingsChanged(user_settings.zoom, SNIPER.NAME)

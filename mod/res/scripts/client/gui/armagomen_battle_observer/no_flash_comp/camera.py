import BattleReplay
from AvatarInputHandler.AimingSystems.SniperAimingSystem import SniperAimingSystem
from AvatarInputHandler.DynamicCameras.ArcadeCamera import ArcadeCamera, MinMax
from AvatarInputHandler.DynamicCameras.ArtyCamera import ArtyCamera
from AvatarInputHandler.DynamicCameras.SniperCamera import SniperCamera
from AvatarInputHandler.DynamicCameras.StrategicCamera import StrategicCamera
from AvatarInputHandler.control_modes import PostMortemControlMode, SniperControlMode
from PlayerEvents import g_playerEvents
from aih_constants import CTRL_MODE_NAME
from constants import AOI
from gui import ClientHangarSpace
from gui.battle_control import avatar_getter
from ..core.battle_cache import cache
from ..core.bo_constants import ARCADE, GLOBAL, POSTMORTEM, SNIPER, STRATEGIC, MAIN
from ..core.bw_utils import callback
from ..core.config import cfg
from ..core.core import overrideMethod
from ..core.events import g_events


class ObserverSniperCamera(object):

    def __init__(self):
        enable = SniperCamera.enable
        create = SniperCamera.create
        SniperCamera.enable = lambda *args, **kwargs: self.enable(enable, *args, **kwargs)
        SniperCamera.create = lambda *args, **kwargs: self.create(create, *args, **kwargs)
        g_events.onSettingsChanged += self.onSettingsChanged
        self._params = None
        self._enableX = False
        self._zoomToGunMarker = False
        self._isDynamicZoomEnabled = False
        self._isDefaultZoomEnabled = False
        self._zoomStepsEnabled = False
        self._steps = SNIPER.DEFAULT_STEPS

    def onSettingsChanged(self, config, blockID):
        if blockID == SNIPER.NAME:
            self._params = (
                max(2.0, float(config[SNIPER.DEF_ZOOM][SNIPER.DEF_ZOOM_NUM])),
                max(2.0, float(config[SNIPER.DYN_ZOOM][SNIPER.MIN_ZOOM_NUM])),
                min(60.0, float(config[SNIPER.DYN_ZOOM][SNIPER.MAX_ZOOM_NUM])),
                max(10.0, float(config[SNIPER.DYN_ZOOM][SNIPER.METERS]))
            )
            self._enableX = config[GLOBAL.ENABLED] and not BattleReplay.g_replayCtrl.isPlaying
            self._zoomToGunMarker = config[SNIPER.DYN_ZOOM][SNIPER.GUN_ZOOM]
            self._isDynamicZoomEnabled = config[SNIPER.DYN_ZOOM][GLOBAL.ENABLED]
            self._isDefaultZoomEnabled = config[SNIPER.DEF_ZOOM][GLOBAL.ENABLED]
            self._zoomStepsEnabled = config[SNIPER.ZOOM_STEPS][GLOBAL.ENABLED]
            self._steps = config[SNIPER.ZOOM_STEPS][SNIPER.STEPS]

    def create(self, create, camera, onChangeControlMode=None):
        if self._enableX and self._zoomStepsEnabled:
            if self._steps:
                exposure_range = xrange(len(self._steps) + SNIPER.ONE, SNIPER.ONE, -SNIPER.ONE)
                camera._cfg[SNIPER.INCREASED_ZOOM] = True
                camera._cfg[SNIPER.ZOOMS] = self._steps
                camera._SniperCamera__dynamicCfg[SNIPER.ZOOM_EXPOSURE] = \
                    [round(SNIPER.EXPOSURE_FACTOR * step, SNIPER.ONE) for step in exposure_range]
        return create(camera, onChangeControlMode=onChangeControlMode)

    def enable(self, enable, camera, targetPos, saveZoom):
        if self._enableX:
            if self._zoomToGunMarker:
                targetPos = cache.player.gunRotator.markerInfo[GLOBAL.FIRST]
            if self._isDynamicZoomEnabled:
                dist = (targetPos - cache.player.getOwnVehiclePosition()).length
                if dist < AOI.VEHICLE_CIRCULAR_AOI_RADIUS:
                    zoom = round(dist / self._params[SNIPER.ZMX])
                    if zoom > self._params[SNIPER.MAX]:
                        zoom = self._params[SNIPER.MAX]
                    elif zoom < self._params[SNIPER.MIN]:
                        zoom = self._params[SNIPER.MIN]
                    camera._cfg[SNIPER.ZOOM] = zoom
                else:
                    camera._cfg[SNIPER.ZOOM] = self._params[SNIPER.DEF]
            elif self._isDefaultZoomEnabled:
                camera._cfg[SNIPER.ZOOM] = self._params[SNIPER.DEF]
        return enable(camera, targetPos, saveZoom or self._enableX)


class ObserverArcadeCamera(object):

    def __init__(self):
        base_create = ArcadeCamera.create

        def create(camera, pivotPos, onChangeControlMode=None, postmortemMode=False):
            if cfg.arcade_camera[GLOBAL.ENABLED]:
                config = camera._cfg
                config[ARCADE.DIST_RANGE] = MinMax(cfg.arcade_camera[ARCADE.MIN], cfg.arcade_camera[ARCADE.MAX])
                config[ARCADE.START_DIST] = cfg.arcade_camera[ARCADE.START_DEAD_DIST]
                config[ARCADE.START_ANGLE] = ARCADE.ANGLE
            return base_create(camera, pivotPos, onChangeControlMode=onChangeControlMode, postmortemMode=postmortemMode)

        ArcadeCamera.create = create


class ObserverStrategicCamera(object):

    def __init__(self):
        base_create = StrategicCamera.create

        def create(camera, onChangeControlMode=None):
            if cfg.strategic_camera[GLOBAL.ENABLED]:
                dist_range = (cfg.strategic_camera[STRATEGIC.MIN], cfg.strategic_camera[STRATEGIC.MAX])
                camera._userCfg[STRATEGIC.DIST_RANGE] = dist_range
                camera._cfg[STRATEGIC.DIST_RANGE] = dist_range
            return base_create(camera, onChangeControlMode=onChangeControlMode)

        StrategicCamera.create = create


class ObserverArtyCamera(object):

    def __init__(self):
        base_create = ArtyCamera.create

        def create(camera, onChangeControlMode=None):
            if cfg.strategic_camera[GLOBAL.ENABLED]:
                dist_range = (cfg.strategic_camera[STRATEGIC.MIN], cfg.strategic_camera[STRATEGIC.MAX])
                camera._userCfg[STRATEGIC.DIST_RANGE] = dist_range
                camera._cfg[STRATEGIC.DIST_RANGE] = dist_range
            return base_create(camera, onChangeControlMode=onChangeControlMode)

        ArtyCamera.create = create


class ObserverHangarCamera(object):

    def __init__(self):
        hangarCFG = ClientHangarSpace.hangarCFG
        customizationHangarCFG = ClientHangarSpace.customizationHangarCFG
        ClientHangarSpace.hangarCFG = lambda *a, **kw: self.hangarCFG(hangarCFG, *a, **kw)
        ClientHangarSpace.customizationHangarCFG = \
            lambda *a, **kw: self.customizationHangarCFG(customizationHangarCFG, *a, **kw)

    @staticmethod
    def hangarCFG(hangarCFG, *a, **kw):
        params = hangarCFG(*a, **kw)
        if cfg.hangar_camera[GLOBAL.ENABLED]:
            params.update(cfg.hangar_camera[GLOBAL.SETTINGS])
        return params

    @staticmethod
    def customizationHangarCFG(customizationHangarCFG, *a, **kw):
        params = customizationHangarCFG(*a, **kw)
        if cfg.hangar_camera[GLOBAL.ENABLED]:
            params.update(cfg.hangar_camera[GLOBAL.SETTINGS])
        return params


class DisableSniperModeAfterShoot(object):

    def __init__(self):
        g_playerEvents.onAvatarReady += self.battleLoading
        g_playerEvents.onAvatarBecomeNonPlayer += self.destroyBattle
        g_events.onSettingsChanged += self.onSettingsChanged
        self.skipClip = True
        self.enabled = False

    def onSettingsChanged(self, config, blockID):
        if blockID == SNIPER.NAME:
            self.enabled = config[SNIPER.DISABLE_AFTER_SHOOT] and config[GLOBAL.ENABLED] and \
                           not BattleReplay.g_replayCtrl.isPlaying
            self.skipClip = config[SNIPER.SKIP_CLIP]

    def battleLoading(self):
        if self.enabled:
            g_events.onPlayerShooting += self.disableSniper

    def destroyBattle(self):
        if self.enabled:
            g_events.onPlayerShooting -= self.disableSniper

    def disableSniper(self, avatar):
        input_handler = avatar.inputHandler
        if input_handler is not None and isinstance(input_handler.ctrl, SniperControlMode):
            if self.skipClip:
                v_desc = avatar.getVehicleDescriptor()
                if v_desc.shot.shell.caliber < SNIPER.MAX_CALIBER or SNIPER.CLIP in v_desc.gun.tags:
                    return
            aiming_system = input_handler.ctrl.camera.aimingSystem
            input_handler.onControlModeChanged(CTRL_MODE_NAME.ARCADE,
                                               prevModeName=input_handler.ctrlModeName,
                                               preferredPos=aiming_system.getDesiredShotPoint(),
                                               turretYaw=aiming_system.turretYaw,
                                               gunPitch=aiming_system.gunPitch,
                                               aimingMode=input_handler.ctrl._aimingMode,
                                               closesDist=False)


@overrideMethod(PostMortemControlMode, "enable")
def enablePostMortem(base_enable, mode, **kwargs):
    if POSTMORTEM.PARAMS in kwargs:
        kwargs[POSTMORTEM.PARAMS] = (mode.camera.angles, cfg.arcade_camera[ARCADE.START_DEAD_DIST])
    if not PostMortemControlMode.getIsPostmortemDelayEnabled():
        if cfg.arcade_camera[POSTMORTEM.TRANSITION] and kwargs.get(POSTMORTEM.DURATION) is None:
            avatar_getter.setForcedGuiControlMode(True, cursorVisible=False)
            callback_time = max(POSTMORTEM.CALLBACK_TIME_SEC, cfg.arcade_camera[POSTMORTEM.DURATION])
            kwargs[POSTMORTEM.DURATION] = callback_time
            callback(callback_time, lambda: avatar_getter.setForcedGuiControlMode(False))
    return base_enable(mode, **kwargs)


@overrideMethod(SniperAimingSystem, "__isTurretHasStaticYaw")
@overrideMethod(SniperControlMode, "getPreferredAutorotationMode")
def removeHandbrake(base, *args, **kwargs):
    return cfg.main[MAIN.REMOVE_HANDBRAKE] or base(*args, **kwargs)


@overrideMethod(SniperAimingSystem, "getPitchLimits")
def getPitchLimits(base_get, aimingSystem, turretYaw=0.0):
    if cfg.main[MAIN.REMOVE_HANDBRAKE]:
        aimingSystem.enableHorizontalStabilizerRuntime(True)
        aimingSystem.forceFullStabilization(True)
    return base_get(aimingSystem, turretYaw)


m_sniperCamera = ObserverSniperCamera()
m_arcadeCamera = ObserverArcadeCamera()
m_strategicCamera = ObserverStrategicCamera()
m_artyCamera = ObserverArtyCamera()
m_hangarCam = ObserverHangarCamera()
m_disableSniper = DisableSniperModeAfterShoot()

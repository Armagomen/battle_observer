import BattleReplay

if not BattleReplay.g_replayCtrl.isPlaying:
    from Avatar import PlayerAvatar
    from AvatarInputHandler.AimingSystems.SniperAimingSystem import SniperAimingSystem
    from AvatarInputHandler.DynamicCameras.ArcadeCamera import ArcadeCamera, MinMax
    from AvatarInputHandler.DynamicCameras.ArtyCamera import ArtyCamera
    from AvatarInputHandler.DynamicCameras.SniperCamera import SniperCamera
    from AvatarInputHandler.DynamicCameras.StrategicCamera import StrategicCamera
    from AvatarInputHandler.control_modes import PostMortemControlMode, SniperControlMode
    from aih_constants import CTRL_MODE_NAME
    from constants import AOI
    from gui.battle_control import avatar_getter
    from ..core.bo_constants import ARCADE, GLOBAL, POSTMORTEM, SNIPER, STRATEGIC, MAIN
    from ..core import cfg, cache
    from ..core.utils.common import callback, overrideMethod


    @overrideMethod(SniperCamera, "create")
    def create(base, *args, **kwargs):
        if cfg.zoom[GLOBAL.ENABLED] and cfg.zoom[SNIPER.ZOOM_STEPS][GLOBAL.ENABLED]:
            if cfg.zoom[SNIPER.ZOOM_STEPS][SNIPER.STEPS]:
                steps = cfg.zoom[SNIPER.ZOOM_STEPS][SNIPER.STEPS]
                exposure_range = xrange(len(steps) + SNIPER.ONE, SNIPER.ONE, -SNIPER.ONE)
                args[GLOBAL.ZERO]._cfg[SNIPER.INCREASED_ZOOM] = True
                args[GLOBAL.ZERO]._cfg[SNIPER.ZOOMS] = steps
                args[GLOBAL.ZERO]._SniperCamera__dynamicCfg[SNIPER.ZOOM_EXPOSURE] = \
                    [round(SNIPER.EXPOSURE_FACTOR * step, SNIPER.ONE) for step in exposure_range]
        return base(*args, **kwargs)


    @overrideMethod(SniperCamera, "enable")
    def enable(base, camera, targetPos, saveZoom):
        if cfg.zoom[GLOBAL.ENABLED]:
            saveZoom = saveZoom or cfg.zoom[GLOBAL.ENABLED]
            if cfg.zoom[SNIPER.DYN_ZOOM][SNIPER.GUN_ZOOM]:
                targetPos = cache.player.gunRotator.markerInfo[GLOBAL.FIRST]
            if cfg.zoom[SNIPER.DYN_ZOOM][GLOBAL.ENABLED]:
                maxZoom = max(camera._cfg[SNIPER.ZOOMS])
                minZoom = min(camera._cfg[SNIPER.ZOOMS])
                if SniperCamera._SNIPER_ZOOM_LEVEL != -1:
                    SniperCamera.setSniperZoomSettings(-1)
                dist = (targetPos - cache.player.getOwnVehiclePosition()).length
                if dist < AOI.VEHICLE_CIRCULAR_AOI_RADIUS:
                    zoom = round(dist / cfg.zoom[SNIPER.DYN_ZOOM][SNIPER.METERS])
                    if zoom > maxZoom:
                        zoom = maxZoom
                    elif zoom < minZoom:
                        zoom = minZoom
                    camera._cfg[SNIPER.ZOOM] = zoom
                else:
                    camera._cfg[SNIPER.ZOOM] = minZoom
        return base(camera, targetPos, saveZoom)


    def changeControlMode(avatar, shooterID):
        if cfg.zoom[SNIPER.DISABLE_AFTER_SHOOT] and cfg.zoom[GLOBAL.ENABLED] and shooterID == avatar.playerVehicleID:
            input_handler = avatar.inputHandler
            if input_handler is not None and isinstance(input_handler.ctrl, SniperControlMode):
                if cfg.zoom[SNIPER.SKIP_CLIP]:
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


    @overrideMethod(PlayerAvatar, "showTracer")
    def showTracer(base, avatar, shooterID, *args):
        changeControlMode(avatar, shooterID)
        return base(avatar, shooterID, *args)


    @overrideMethod(ArcadeCamera, "create")
    def create(base, camera, *args, **kwargs):
        if cfg.arcade_camera[GLOBAL.ENABLED]:
            config = camera._cfg
            config[ARCADE.DIST_RANGE] = MinMax(cfg.arcade_camera[ARCADE.MIN], cfg.arcade_camera[ARCADE.MAX])
            config[ARCADE.START_DIST] = cfg.arcade_camera[ARCADE.START_DEAD_DIST]
            config[ARCADE.START_ANGLE] = ARCADE.ANGLE
        return base(camera, *args, **kwargs)


    @overrideMethod(StrategicCamera, "create")
    @overrideMethod(ArtyCamera, "create")
    def create(base, camera, *args, **kwargs):
        if cfg.strategic_camera[GLOBAL.ENABLED]:
            dist_range = (cfg.strategic_camera[STRATEGIC.MIN], cfg.strategic_camera[STRATEGIC.MAX])
            camera._userCfg[STRATEGIC.DIST_RANGE] = dist_range
            camera._cfg[STRATEGIC.DIST_RANGE] = dist_range
        return base(camera, *args, **kwargs)


    @overrideMethod(PostMortemControlMode, "enable")
    def enablePostMortem(base, mode, **kwargs):
        if POSTMORTEM.PARAMS in kwargs:
            kwargs[POSTMORTEM.PARAMS] = (mode.camera.angles, cfg.arcade_camera[ARCADE.START_DEAD_DIST])
        if not PostMortemControlMode.getIsPostmortemDelayEnabled():
            avatar_getter.setForcedGuiControlMode(True)
            kwargs[POSTMORTEM.DURATION] = POSTMORTEM.CALLBACK_TIME_SEC
            callback(POSTMORTEM.CALLBACK_TIME_SEC, lambda: avatar_getter.setForcedGuiControlMode(False))
        return base(mode, **kwargs)


    @overrideMethod(SniperAimingSystem, "__isTurretHasStaticYaw")
    @overrideMethod(SniperControlMode, "getPreferredAutorotationMode")
    def removeHandbrake(base, *args, **kwargs):
        return cfg.main[MAIN.REMOVE_HANDBRAKE] or base(*args, **kwargs)


    @overrideMethod(SniperControlMode, "enable")
    def sniperControlMode_enable(base, controlMode, *args, **kwargs):
        result = base(controlMode, *args, **kwargs)
        if cfg.main[MAIN.REMOVE_HANDBRAKE]:
            controlMode._cam.aimingSystem.enableHorizontalStabilizerRuntime(True)
            controlMode._cam.aimingSystem.forceFullStabilization(True)
        return result
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
    from gui.battle_control import avatar_getter
    from armagomen.battle_observer.core.constants import ARCADE, GLOBAL, POSTMORTEM, SNIPER, STRATEGIC, MAIN
    from armagomen.battle_observer.core import config
    from armagomen.utils.common import callback, overrideMethod, getPlayer


    @overrideMethod(SniperCamera, "create")
    def create(base, *args, **kwargs):
        if config.zoom[GLOBAL.ENABLED] and config.zoom[SNIPER.ZOOM_STEPS][GLOBAL.ENABLED]:
            if config.zoom[SNIPER.ZOOM_STEPS][SNIPER.STEPS]:
                steps = config.zoom[SNIPER.ZOOM_STEPS][SNIPER.STEPS]
                steps.sort()
                exposure_range = xrange(len(steps) + SNIPER.ONE, SNIPER.ONE, -SNIPER.ONE)
                args[GLOBAL.ZERO]._cfg[SNIPER.INCREASED_ZOOM] = True
                args[GLOBAL.ZERO]._cfg[SNIPER.ZOOMS] = steps
                args[GLOBAL.ZERO]._SniperCamera__dynamicCfg[SNIPER.ZOOM_EXPOSURE] = \
                    [round(SNIPER.EXPOSURE_FACTOR * step, SNIPER.ONE) for step in exposure_range]
        return base(*args, **kwargs)


    @overrideMethod(SniperCamera, "enable")
    def enable(base, camera, targetPos, saveZoom):
        if config.zoom[GLOBAL.ENABLED]:
            if config.zoom[SNIPER.DYN_ZOOM][SNIPER.GUN_ZOOM]:
                targetPos = getPlayer().gunRotator.markerInfo[GLOBAL.FIRST]
            if config.zoom[SNIPER.DYN_ZOOM][GLOBAL.ENABLED]:
                minZoom, maxZoom = camera._cfg[SNIPER.ZOOMS][GLOBAL.FIRST], camera._cfg[SNIPER.ZOOMS][GLOBAL.LAST]
                if SniperCamera._SNIPER_ZOOM_LEVEL != -1:
                    SniperCamera.setSniperZoomSettings(-1)
                dist = (targetPos - getPlayer().getOwnVehiclePosition()).length
                zoom = round(dist / config.zoom[SNIPER.DYN_ZOOM][SNIPER.METERS])
                if zoom > maxZoom:
                    zoom = maxZoom
                elif zoom < minZoom:
                    zoom = minZoom
                camera._cfg[SNIPER.ZOOM] = zoom
        return base(camera, targetPos, saveZoom or config.zoom[GLOBAL.ENABLED])


    def changeControlMode(avatar, shooterID):
        if config.zoom[SNIPER.DISABLE_AFTER_SHOOT] and config.zoom[GLOBAL.ENABLED] and shooterID == avatar.playerVehicleID:
            input_handler = avatar.inputHandler
            if input_handler is not None and isinstance(input_handler.ctrl, SniperControlMode):
                if config.zoom[SNIPER.SKIP_CLIP]:
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
        if config.arcade_camera[GLOBAL.ENABLED]:
            cfg = camera._cfg
            cfg[ARCADE.DIST_RANGE] = MinMax(config.arcade_camera[ARCADE.MIN], config.arcade_camera[ARCADE.MAX])
            cfg[ARCADE.START_DIST] = config.arcade_camera[ARCADE.START_DEAD_DIST]
            cfg[ARCADE.START_ANGLE] = ARCADE.ANGLE
        return base(camera, *args, **kwargs)


    @overrideMethod(StrategicCamera, "create")
    @overrideMethod(ArtyCamera, "create")
    def create(base, camera, *args, **kwargs):
        if config.strategic_camera[GLOBAL.ENABLED]:
            dist_range = (config.strategic_camera[STRATEGIC.MIN], config.strategic_camera[STRATEGIC.MAX])
            camera._userCfg[STRATEGIC.DIST_RANGE] = dist_range
            camera._cfg[STRATEGIC.DIST_RANGE] = dist_range
        return base(camera, *args, **kwargs)


    @overrideMethod(PostMortemControlMode, "enable")
    def enablePostMortem(base, mode, **kwargs):
        if POSTMORTEM.PARAMS in kwargs:
            kwargs[POSTMORTEM.PARAMS] = (mode.camera.angles, config.arcade_camera[ARCADE.START_DEAD_DIST])
        if not PostMortemControlMode.getIsPostmortemDelayEnabled():
            kwargs[POSTMORTEM.CAM_MATRIX] = mode.camera.camera.matrix
            kwargs[POSTMORTEM.DURATION] = GLOBAL.ONE_SECOND
            avatar_getter.setForcedGuiControlMode(True)
            callback(POSTMORTEM.CALLBACK_TIME_SEC, lambda: avatar_getter.setForcedGuiControlMode(False))
        return base(mode, **kwargs)


    @overrideMethod(SniperAimingSystem, "__isTurretHasStaticYaw")
    @overrideMethod(SniperControlMode, "getPreferredAutorotationMode")
    def removeHandbrake(base, *args, **kwargs):
        return config.main[MAIN.REMOVE_HANDBRAKE] or base(*args, **kwargs)


    @overrideMethod(SniperControlMode, "enable")
    def sniperControlMode_enable(base, controlMode, *args, **kwargs):
        result = base(controlMode, *args, **kwargs)
        if config.main[MAIN.REMOVE_HANDBRAKE]:
            controlMode._cam.aimingSystem.enableHorizontalStabilizerRuntime(True)
            controlMode._cam.aimingSystem.forceFullStabilization(True)
        return result

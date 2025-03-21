import math
from collections import namedtuple

import ResMgr

import math_utils
from aih_constants import CTRL_MODE_NAME
from armagomen._constants import ARCADE, EFFECTS, GLOBAL, IS_LESTA, SNIPER, STRATEGIC
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import addCallback, getPlayer, isReplay, overrideMethod
from armagomen.utils.logging import logError
from AvatarInputHandler.control_modes import PostMortemControlMode
from AvatarInputHandler.DynamicCameras.SniperCamera import SniperCamera
from cgf_components.attack_artillery_fort_components import ISettingsCore
from gui.battle_control.avatar_getter import getInputHandler, getOwnVehiclePosition
from helpers import dependency
from PlayerEvents import g_playerEvents
from skeletons.gui.app_loader import GuiGlobalSpaceID, IAppLoader
from TriggersManager import g_manager, ITriggerListener, TRIGGER_TYPE

MinMax = namedtuple('MinMax', ('min', 'max'))


class ChangeCameraModeAfterShoot(ITriggerListener):

    def __init__(self):
        self.latency = 0
        self.skip_clip = False
        self.avatar = None
        self.__trigger_type = TRIGGER_TYPE.PLAYER_DISCRETE_SHOOT if not IS_LESTA else TRIGGER_TYPE.PLAYER_SHOOT

    def updateSettings(self, data):
        enabled = data[SNIPER.DISABLE_SNIPER] and data[GLOBAL.ENABLED]
        self.latency = float(data[SNIPER.DISABLE_LATENCY])
        self.skip_clip = data[SNIPER.SKIP_CLIP]
        if enabled:
            g_playerEvents.onAvatarReady += self.onStart
            g_playerEvents.onAvatarBecomeNonPlayer += self.onFinish
        else:
            g_playerEvents.onAvatarReady -= self.onStart
            g_playerEvents.onAvatarBecomeNonPlayer -= self.onFinish

    def onStart(self):
        self.avatar = getPlayer()
        g_manager.addListener(self)

    def onFinish(self):
        self.avatar = None
        g_manager.delListener(self)

    def onTriggerActivated(self, params):
        if params.get('type') == self.__trigger_type:
            addCallback(max(self.latency, 0), self.changeControlMode)

    def changeControlMode(self):
        if self.avatar is None or self.avatar.isObserver():
            return
        input_handler = self.avatar.inputHandler
        if input_handler is not None and input_handler.ctrlModeName == CTRL_MODE_NAME.SNIPER:
            v_desc = self.avatar.getVehicleDescriptor()
            caliber_skip = v_desc.shot.shell.caliber <= SNIPER.MAX_CALIBER
            if caliber_skip or self.skip_clip and SNIPER.CLIP in v_desc.gun.tags:
                return
            aiming_system = input_handler.ctrl.camera.aimingSystem
            input_handler.onControlModeChanged(CTRL_MODE_NAME.ARCADE,
                                               prevModeName=input_handler.ctrlModeName,
                                               preferredPos=aiming_system.getDesiredShotPoint(),
                                               turretYaw=aiming_system.turretYaw,
                                               gunPitch=aiming_system.gunPitch,
                                               aimingMode=input_handler.ctrl._aimingMode,
                                               closesDist=False,
                                               curVehicleID=self.avatar.playerVehicleID)


class CameraSettings(object):

    def __init__(self):
        self.enabled = False
        self.reset = False

    @staticmethod
    def getCamera(control_mode_name):
        input_handler = getInputHandler()
        if input_handler is not None and input_handler.ctrls:
            return input_handler.ctrls[control_mode_name].camera
        return None

    def resetToDefault(self, *args):
        ResMgr.purge('gui/avatar_input_handler.xml')
        self.reset = False


class Arcade(CameraSettings):

    def __init__(self):
        super(Arcade, self).__init__()
        self.config = user_settings.arcade_camera
        overrideMethod(PostMortemControlMode, "enable")(self.enablePostMortem)

    def update(self):
        camera = self.getCamera(CTRL_MODE_NAME.ARCADE)
        if camera is None:
            return logError("{} camera is Nome", CTRL_MODE_NAME.ARCADE)
        self.enabled = self.config[GLOBAL.ENABLED]
        if self.enabled:
            self.reset = True
            camera._cfg['distRange'] = MinMax(self.config[ARCADE.MIN], self.config[ARCADE.MAX])
            camera._cfg['scrollSensitivity'] = self.config[ARCADE.SCROLL_SENSITIVITY]
            camera._cfg['startDist'] = self.config[ARCADE.START_DEAD_DIST]
            camera._cfg['startAngle'] = -0.4
            if IS_LESTA:
                camera._ArcadeCamera__updateProperties(state=None)
            else:
                camera._updateProperties(state=None)
        elif self.reset:
            self.resetToDefault(camera)

    def resetToDefault(self, camera):
        super(Arcade, self).resetToDefault()
        cameraSec = ResMgr.openSection('gui/avatar_input_handler.xml/arcadeMode/camera/')
        camera._reloadConfigs(cameraSec)
        if IS_LESTA:
            camera._ArcadeCamera__updateProperties(state=None)
        else:
            camera._updateProperties(state=None)

    def enablePostMortem(self, base, mode, **kwargs):
        if self.enabled:
            if 'postmortemParams' in kwargs:
                kwargs['postmortemParams'] = (mode.camera.angles, self.config[ARCADE.START_DEAD_DIST])
                kwargs.setdefault('transitionDuration', 2.0)
        return base(mode, **kwargs)


class Strategic(CameraSettings):

    def __init__(self):
        super(Strategic, self).__init__()
        self.config = user_settings.strategic_camera

    def update(self):
        strategic = self.getCamera(CTRL_MODE_NAME.STRATEGIC)
        arty = self.getCamera(CTRL_MODE_NAME.ARTY)
        if strategic is None or arty is None:
            return logError("{} camera is Nome",
                            CTRL_MODE_NAME.STRATEGIC if not strategic else CTRL_MODE_NAME.ARTY)
        self.enabled = self.config[GLOBAL.ENABLED]
        if self.enabled:
            self.reset = True
            for camera in (strategic, arty):
                camera._cfg[STRATEGIC.DIST_RANGE] = (self.config[STRATEGIC.MIN], self.config[STRATEGIC.MAX])
                camera._cfg[STRATEGIC.SCROLL_SENSITIVITY] = self.config[STRATEGIC.SCROLL_SENSITIVITY]
        elif self.reset:
            self.resetToDefault(arty, strategic)

    def resetToDefault(self, arty, strategic):
        super(Strategic, self).resetToDefault()
        cameraSec_strategic = ResMgr.openSection('gui/avatar_input_handler.xml/strategicMode/camera/')
        cameraSec_arty = ResMgr.openSection('gui/avatar_input_handler.xml/artyMode/camera/')
        strategic._reloadConfigs(cameraSec_strategic)
        arty._reloadConfigs(cameraSec_arty)


class Sniper(CameraSettings):
    settingsCore = dependency.descriptor(ISettingsCore)
    DEFAULT_X_METERS = 25.0
    _SNIPER_ZOOM_LEVEL = None

    def __init__(self):
        super(Sniper, self).__init__()
        self.config = user_settings.zoom
        self._dyn_zoom = False
        self._steps_only = False
        self._steps_enabled = False
        self.after_shoot = ChangeCameraModeAfterShoot()
        self.min_max = MinMax(2, 25)
        overrideMethod(SniperCamera, "enable")(self.enable)

    def update(self):
        self.after_shoot.updateSettings(self.config)
        self.enabled = self.config[GLOBAL.ENABLED]
        self._dyn_zoom = self.config[SNIPER.DYN_ZOOM][GLOBAL.ENABLED] and self.enabled
        self._steps_only = self.config[SNIPER.DYN_ZOOM][SNIPER.STEPS_ONLY] and self._dyn_zoom
        camera = self.getCamera(CTRL_MODE_NAME.SNIPER)
        if camera is None:
            return logError("{} camera is Nome", CTRL_MODE_NAME.SNIPER)
        if user_settings.effects[EFFECTS.NO_SNIPER_DYNAMIC]:
            camera.enableDynamicCamera(False)
        else:
            camera.enableDynamicCamera(self.settingsCore.getSetting('dynamicCamera'))
        if self._dyn_zoom:
            self._SNIPER_ZOOM_LEVEL = int(camera._SNIPER_ZOOM_LEVEL)
            camera.setSniperZoomSettings(-1)
        elif self._SNIPER_ZOOM_LEVEL is not None:
            camera.setSniperZoomSettings(self._SNIPER_ZOOM_LEVEL)
            self._SNIPER_ZOOM_LEVEL = None
        self._steps_enabled = self.config[SNIPER.ZOOM_STEPS][GLOBAL.ENABLED] and self.enabled
        if self._steps_enabled:
            self.reset = True
            steps = self.config[SNIPER.ZOOM_STEPS][SNIPER.STEPS] or SNIPER.DEFAULT_STEPS
            camera._cfg[SNIPER.INCREASED_ZOOM] = True
            camera._cfg[SNIPER.ZOOMS] = steps
            exposure = camera._SniperCamera__dynamicCfg[SNIPER.ZOOM_EXPOSURE]
            while len(steps) > len(exposure):
                exposure.append(SNIPER.EXPOSURE_FACTOR)
        elif self.reset:
            self.resetToDefault(camera)
        self.min_max = MinMax(camera._cfg[SNIPER.ZOOMS][0], camera._cfg[SNIPER.ZOOMS][-1])

    def resetToDefault(self, camera):
        super(Sniper, self).resetToDefault()
        cameraSec = ResMgr.openSection('gui/avatar_input_handler.xml/sniperMode/camera/')
        camera._reloadConfigs(cameraSec)

    def getZoom(self, distance, steps):
        zoom = math.floor(distance / self.DEFAULT_X_METERS)
        if self._steps_only:
            zoom = min(steps, key=lambda value: abs(value - zoom))
        return math_utils.clamp(self.min_max.min, self.min_max.max, zoom)

    def enable(self, base, camera, targetPos, saveZoom):
        if self._dyn_zoom:
            saveZoom = True
            ownPosition = getOwnVehiclePosition()
            distance = (targetPos - ownPosition).length if ownPosition is not None else GLOBAL.ZERO
            if distance > SNIPER.MAX_DIST:
                distance = GLOBAL.ZERO
            camera._cfg[SNIPER.ZOOM] = self.getZoom(distance, camera._cfg[SNIPER.ZOOMS])
        return base(camera, targetPos, saveZoom)


class CameraManager(object):
    appLoader = dependency.descriptor(IAppLoader)

    def __init__(self):
        self.appLoader.onGUISpaceBeforeEnter += self.updateCameras
        self.__modes = (Arcade(), Sniper(), Strategic())

    def updateCameras(self, spaceID):
        if spaceID == GuiGlobalSpaceID.BATTLE_LOADING and not isReplay():
            for mode in self.__modes:
                mode.update()


camera_manager = CameraManager()


def fini():
    camera_manager.appLoader.onGUISpaceBeforeEnter -= camera_manager.updateCameras

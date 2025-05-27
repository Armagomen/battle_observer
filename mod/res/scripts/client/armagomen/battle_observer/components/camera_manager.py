from account_helpers.settings_core.settings_constants import GAME
from aih_constants import CTRL_MODE_NAME
from armagomen._constants import ARCADE, EFFECTS, GLOBAL, IS_WG_CLIENT, SNIPER, STRATEGIC
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import addCallback, cancelOverride, getPlayer, MinMax, overrideMethod, ResMgr
from armagomen.utils.logging import logDebug, logError
from AvatarInputHandler.control_modes import PostMortemControlMode
from AvatarInputHandler.DynamicCameras.SniperCamera import SniperCamera
from cgf_components.attack_artillery_fort_components import ISettingsCore
from gui.battle_control.avatar_getter import getInputHandler, getOwnVehiclePosition
from helpers import dependency
from math_utils import clamp
from PlayerEvents import g_playerEvents
from skeletons.gui.app_loader import GuiGlobalSpaceID, IAppLoader
from TriggersManager import ITriggerListener, TRIGGER_TYPE


class ChangeCameraModeAfterShoot(ITriggerListener):

    def __init__(self):
        self.latency = 0
        self.skip_clip = False
        self.avatar = None
        self.__trigger_type = TRIGGER_TYPE.PLAYER_DISCRETE_SHOOT if IS_WG_CLIENT else TRIGGER_TYPE.PLAYER_SHOOT

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
        from TriggersManager import g_manager
        self.avatar = getPlayer()
        g_manager.addListener(self)

    def onFinish(self):
        from TriggersManager import g_manager
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
    _CONTROL_MODE_NAME_TO_SEC = {
        CTRL_MODE_NAME.ARCADE: "gui/avatar_input_handler.xml/arcadeMode/camera/",
        CTRL_MODE_NAME.SNIPER: "gui/avatar_input_handler.xml/sniperMode/camera/",
        CTRL_MODE_NAME.ARTY: "gui/avatar_input_handler.xml/artyMode/camera/",
        CTRL_MODE_NAME.STRATEGIC: "gui/avatar_input_handler.xml/strategicMode/camera/",
    }

    def __init__(self):
        self.enabled = False
        self.reset = False

    @staticmethod
    def getCamera(control_mode_name):
        input_handler = getInputHandler()
        if input_handler is not None and input_handler.ctrls and control_mode_name in input_handler.ctrls:
            return input_handler.ctrls[control_mode_name].camera
        logError("{} camera is Nome", control_mode_name)
        return None

    def resetToDefault(self, control_mode_name):
        camera = self.getCamera(control_mode_name)
        if camera is not None:
            ResMgr.purge('gui/avatar_input_handler.xml')
            cameraSec = ResMgr.openSection(self._CONTROL_MODE_NAME_TO_SEC[control_mode_name])
            camera._reloadConfigs(cameraSec)
        self.reset = False


class Arcade(CameraSettings):

    def __init__(self):
        super(Arcade, self).__init__()
        self.config = user_settings.arcade_camera
        overrideMethod(PostMortemControlMode, "enable")(self.enablePostMortem)

    def update(self):
        camera = self.getCamera(CTRL_MODE_NAME.ARCADE)
        if camera is not None:
            self.enabled = self.config[GLOBAL.ENABLED]
            if self.enabled:
                self.reset = True
                camera._cfg[ARCADE.DIST_RANGE] = MinMax(self.config[ARCADE.MIN], self.config[ARCADE.MAX])
                camera._cfg[ARCADE.SCROLL_SENSITIVITY] = self.config[ARCADE.SCROLL_SENSITIVITY]
                camera._cfg[ARCADE.START_DIST] = self.config[ARCADE.START_DEAD_DIST]
                camera._cfg[ARCADE.START_ANGLE] = -0.4
                self.updateProperties(camera)
            elif self.reset:
                self.resetToDefault(CTRL_MODE_NAME.ARCADE)
                self.updateProperties(camera)

    @staticmethod
    def updateProperties(camera):
        if IS_WG_CLIENT:
            camera._updateProperties(state=None)
        else:
            camera._ArcadeCamera__updateProperties(state=None)

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
        self.enabled = self.config[GLOBAL.ENABLED]
        ctrl_mode_names = (CTRL_MODE_NAME.STRATEGIC, CTRL_MODE_NAME.ARTY)
        if self.enabled:
            self.reset = True
            for control_mode_name in ctrl_mode_names:
                camera = self.getCamera(control_mode_name)
                if camera is not None:
                    camera._cfg[STRATEGIC.DIST_RANGE] = (self.config[STRATEGIC.MIN], self.config[STRATEGIC.MAX])
                    camera._cfg[STRATEGIC.SCROLL_SENSITIVITY] = self.config[STRATEGIC.SCROLL_SENSITIVITY]
        elif self.reset:
            for control_mode_name in ctrl_mode_names:
                self.resetToDefault(control_mode_name)


class Sniper(CameraSettings):
    settingsCore = dependency.descriptor(ISettingsCore)
    DEFAULT_X_METERS = 18.0
    _SNIPER_ZOOM_LEVEL = None
    ZOOM = "zoom"
    ZOOMS = "zooms"
    MAX_DIST = 570.0

    def __init__(self):
        super(Sniper, self).__init__()
        self.config = user_settings.zoom
        self._dyn_zoom = False
        self._steps_only = False
        self._steps_enabled = False
        self.after_shoot = ChangeCameraModeAfterShoot()
        self.min_max = MinMax(2, 25)
        self.__player = None

    def applySniperSettings(self, param):
        self.settingsCore.applySettings({GAME.SNIPER_ZOOM: param})
        self.settingsCore.applyStorages(False)
        self.settingsCore.clearStorages()

    @staticmethod
    def linear_interpolate(x_vals_new):
        x_vals_old = [2.0, 4.0, 8.0, 16.0, 25.0]
        exposures_old = [0.6, 0.5, 0.4, 0.3, 0.2]
        exposures_new = []
        for x in x_vals_new:
            if x <= x_vals_old[0]:
                exposures_new.append(exposures_old[0])
            elif x >= x_vals_old[-1]:
                x1, x2 = x_vals_old[-2], x_vals_old[-1]
                y1, y2 = exposures_old[-2], exposures_old[-1]
                y_extrap = y2 + (y2 - y1) * ((x - x2) / float(x2 - x1))
                exposures_new.append(round(y_extrap, 2))
            else:
                for i in xrange(len(x_vals_old) - 1):
                    if x_vals_old[i] <= x <= x_vals_old[i + 1]:
                        x1, x2 = x_vals_old[i], x_vals_old[i + 1]
                        y1, y2 = exposures_old[i], exposures_old[i + 1]
                        y_interp = y1 + (y2 - y1) * ((x - x1) / float(x2 - x1))
                        exposures_new.append(round(y_interp, 2))
                        break
        return exposures_new

    def update(self):
        self.after_shoot.updateSettings(self.config)
        self.enabled = self.config[GLOBAL.ENABLED]
        self._dyn_zoom = self.config[SNIPER.DYN_ZOOM] and self.enabled
        self._steps_only = self.config[SNIPER.STEPS_ONLY] and self._dyn_zoom
        self.__player = getPlayer()
        camera = self.getCamera(CTRL_MODE_NAME.SNIPER)
        if camera is not None:
            dynamic = user_settings.effects[EFFECTS.NO_SNIPER_DYNAMIC]
            camera.enableDynamicCamera(False if dynamic else self.settingsCore.getSetting(GAME.DYNAMIC_CAMERA))
            if self._dyn_zoom:
                overrideMethod(SniperCamera, "enable")(self.enableSniper)
                zoom_level = self.settingsCore.getSetting(GAME.SNIPER_ZOOM)
                if zoom_level:
                    self._SNIPER_ZOOM_LEVEL = zoom_level
                    self.applySniperSettings(0)
            else:
                cancelOverride(SniperCamera, "enable", "enableSniper")
                if self._SNIPER_ZOOM_LEVEL is not None:
                    self.applySniperSettings(self._SNIPER_ZOOM_LEVEL)
                    self._SNIPER_ZOOM_LEVEL = None
            self._steps_enabled = self.config[SNIPER.ZOOM_STEPS] and self.enabled
            if self._steps_enabled:
                self.reset = True
                camera._cfg[SNIPER.INCREASED_ZOOM] = True
                steps = self.config[SNIPER.STEPS] or SNIPER.DEFAULT_STEPS
                if steps != camera._cfg[self.ZOOMS]:
                    new_exposure = self.linear_interpolate(steps)
                    camera._SniperCamera__dynamicCfg[SNIPER.ZOOM_EXPOSURE] = new_exposure
                    camera._cfg[self.ZOOMS] = steps
                    logDebug("UPDATE_ZOOMS = steps:{} exposure:{}", steps, new_exposure)
            elif self.reset:
                self.resetToDefault(CTRL_MODE_NAME.SNIPER)
            self.min_max = MinMax(camera._cfg[self.ZOOMS][0], camera._cfg[self.ZOOMS][-1])

    def enableSniper(self, base, camera, targetPos, saveZoom):
        ownPosition = getOwnVehiclePosition(self.__player)
        distance = (targetPos - ownPosition).length if ownPosition is not None else None
        if not distance or distance >= self.MAX_DIST:
            camera._cfg[self.ZOOM] = self.min_max.min
        else:
            zoom = round(distance / self.DEFAULT_X_METERS)
            if self._steps_only:
                zoom = min(camera._cfg[self.ZOOMS], key=lambda value: abs(value - zoom))
            camera._cfg[self.ZOOM] = clamp(self.min_max.min, self.min_max.max, zoom)
        return base(camera, targetPos, True)


class CameraManager(object):
    appLoader = dependency.descriptor(IAppLoader)

    def __init__(self):
        self.appLoader.onGUISpaceBeforeEnter += self.updateCameras
        self.__modes = (Arcade(), Sniper(), Strategic())

    def updateCameras(self, spaceID):
        if spaceID == GuiGlobalSpaceID.BATTLE_LOADING:
            for mode in self.__modes:
                mode.update()


camera_manager = CameraManager()


def fini():
    camera_manager.appLoader.onGUISpaceBeforeEnter -= camera_manager.updateCameras

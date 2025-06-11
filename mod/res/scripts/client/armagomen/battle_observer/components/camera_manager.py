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
            tags = v_desc.gun.tags
            if v_desc.shot.shell.caliber <= SNIPER.MAX_CALIBER or "autoShoot" in tags or self.skip_clip and "clip" in tags:
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
    settingsCore = dependency.descriptor(ISettingsCore)

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

    def applySettings(self, params):
        self.settingsCore.applySettings(params)
        self.settingsCore.applyStorages(False)
        self.settingsCore.clearStorages()


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
                if self.settingsCore.getSetting(GAME.COMMANDER_CAM) or self.settingsCore.getSetting(GAME.PRE_COMMANDER_CAM):
                    self.applySettings({GAME.COMMANDER_CAM: 0, GAME.PRE_COMMANDER_CAM: 0})
                camera._cfg[ARCADE.DIST_RANGE] = MinMax(self.config[ARCADE.MIN], self.config[ARCADE.MAX])
                camera._cfg[ARCADE.SCROLL_SENSITIVITY] = self.config[ARCADE.SCROLL_SENSITIVITY]
                camera._cfg[ARCADE.START_DIST] = self.config[ARCADE.START_DEAD_DIST]
                camera._cfg[ARCADE.START_ANGLE] = -0.18
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
    DEFAULT_X_METERS = 18.0
    _SNIPER_ZOOM_LEVEL = None
    ZOOM = "zoom"
    ZOOMS = "zooms"
    MAX_DIST = 580.0

    def __init__(self):
        super(Sniper, self).__init__()
        self.config = user_settings.zoom
        self._dyn_zoom = False
        self._change_steps = False
        self.after_shoot = ChangeCameraModeAfterShoot()
        self.min_max = MinMax(2, 25)
        self.__player = None

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
        self._change_steps = self.config[SNIPER.ZOOM_STEPS] and self.enabled
        self.__player = getPlayer()
        camera = self.getCamera(CTRL_MODE_NAME.SNIPER)
        if camera is not None:
            dynamic = user_settings.effects[EFFECTS.NO_SNIPER_DYNAMIC]
            camera.enableDynamicCamera(False if dynamic else bool(self.settingsCore.getSetting(GAME.DYNAMIC_CAMERA)))
            if self._dyn_zoom:
                overrideMethod(SniperCamera, "enable")(self.enableSniper)
                zoom_level = self.settingsCore.getSetting(GAME.SNIPER_ZOOM)
                if zoom_level and self._SNIPER_ZOOM_LEVEL is None:
                    self._SNIPER_ZOOM_LEVEL = zoom_level
                    self.applySettings({GAME.SNIPER_ZOOM: 0})
            else:
                cancelOverride(SniperCamera, "enable", "enableSniper")
                if self._SNIPER_ZOOM_LEVEL is not None:
                    self.applySettings({GAME.SNIPER_ZOOM: self._SNIPER_ZOOM_LEVEL})
                    self._SNIPER_ZOOM_LEVEL = None
            if self._change_steps or self._dyn_zoom:
                self.reset = True
                steps = sorted(self.config[SNIPER.STEPS]) if self._change_steps else SNIPER.DEFAULT_STEPS
                if steps and steps != camera._cfg[self.ZOOMS]:
                    new_exposure = self.linear_interpolate(steps)
                    camera._SniperCamera__dynamicCfg[SNIPER.ZOOM_EXPOSURE] = new_exposure
                    camera._cfg[self.ZOOMS] = steps
                    logDebug("UPDATE_ZOOMS = steps:{} exposure:{}", steps, new_exposure)
                if not self.settingsCore.getSetting(GAME.INCREASED_ZOOM):
                    self.applySettings({GAME.INCREASED_ZOOM: 1})
            elif self.reset:
                self.resetToDefault(CTRL_MODE_NAME.SNIPER)

    def getZoom(self, zooms, distance):
        if not distance or distance >= self.MAX_DIST:
            return zooms[0]
        else:
            target = round(distance / self.DEFAULT_X_METERS)
            return zooms[0] if target <= zooms[0] else max(x for x in zooms if x <= target)

    def enableSniper(self, base, camera, targetPos, saveZoom):
        ownPosition = getOwnVehiclePosition(self.__player)
        distance = (targetPos - ownPosition).length if ownPosition is not None else 0
        camera._cfg[self.ZOOM] = self.getZoom(camera._cfg[self.ZOOMS], distance)
        return base(camera, targetPos, True)


class CameraManager(object):
    appLoader = dependency.descriptor(IAppLoader)

    def __init__(self):
        self.appLoader.onGUISpaceBeforeEnter += self.updateCameras
        self.__modes = (Arcade(), Sniper(), Strategic())

    def fini(self):
        self.appLoader.onGUISpaceBeforeEnter -= self.updateCameras

    def updateCameras(self, spaceID):
        if spaceID == GuiGlobalSpaceID.BATTLE_LOADING:
            for mode in self.__modes:
                mode.update()


camera_manager = CameraManager()


def fini():
    camera_manager.fini()

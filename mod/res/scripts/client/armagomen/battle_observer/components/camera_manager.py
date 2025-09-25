import TriggersManager
from account_helpers.settings_core.settings_constants import GAME
from aih_constants import CTRL_MODE_NAME
from armagomen._constants import ARCADE, EFFECTS, GLOBAL, SNIPER, STRATEGIC
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import addCallback, getPlayer, isReplay, MinMax, ResMgr, toggleOverride
from armagomen.utils.events import g_events
from armagomen.utils.logging import logDebug, logError
from AvatarInputHandler.control_modes import PostMortemControlMode
from AvatarInputHandler.DynamicCameras.SniperCamera import SniperCamera
from cgf_components.attack_artillery_fort_components import ISettingsCore
from gui.battle_control.avatar_getter import getInputHandler, getOwnVehiclePosition
from helpers import dependency
from skeletons.gui.app_loader import GuiGlobalSpaceID, IAppLoader


class ChangeCameraModeAfterShoot(TriggersManager.ITriggerListener):

    def __init__(self, appLoader):
        self.latency = 0
        self.skip_clip = False
        self.appLoader = appLoader
        self.__trigger_type = TriggersManager.TRIGGER_TYPE.PLAYER_DISCRETE_SHOOT

    def updateSettings(self, data):
        enabled = data[SNIPER.DISABLE_SNIPER] and data[GLOBAL.ENABLED]
        self.latency = float(data[SNIPER.DISABLE_LATENCY])
        self.skip_clip = data[SNIPER.SKIP_CLIP]
        if enabled:
            self.appLoader.onGUISpaceEntered += self.onGUISpaceEntered
            self.appLoader.onGUISpaceLeft += self.onGUISpaceLeft
        else:
            self.appLoader.onGUISpaceEntered -= self.onGUISpaceEntered
            self.appLoader.onGUISpaceLeft -= self.onGUISpaceLeft

    def onGUISpaceEntered(self, spaceID):
        if spaceID == GuiGlobalSpaceID.BATTLE and not isReplay():
            TriggersManager.g_manager.addListener(self)

    def onGUISpaceLeft(self, spaceID):
        if spaceID == GuiGlobalSpaceID.BATTLE and not isReplay():
            TriggersManager.g_manager.delListener(self)

    def onTriggerActivated(self, params):
        if params.get('type') == self.__trigger_type:
            addCallback(max(self.latency, 0), self.changeControlMode)

    def changeControlMode(self):
        avatar = getPlayer()
        if avatar is None or avatar.isObserver():
            return
        input_handler = avatar.inputHandler
        if input_handler is not None and input_handler.ctrlModeName == CTRL_MODE_NAME.SNIPER:
            v_desc = avatar.getVehicleDescriptor()
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
                                               curVehicleID=avatar.playerVehicleID)


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
        self.isChanged = False
        self.config = {}

    def onModSettingsChanged(self, name, data):
        if name == self.name:
            self.config.update(data)
            self.isChanged = True

    @property
    def name(self):
        return None

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
        if any(self.settingsCore.applySetting(key, value) is not None for key, value in params.items()):
            self.settingsCore.applyStorages(False)
            self.settingsCore.clearStorages()


class Arcade(CameraSettings):

    @property
    def name(self):
        return ARCADE.NAME

    def update(self):
        camera = self.getCamera(CTRL_MODE_NAME.ARCADE)
        if camera is not None:
            if self.enabled != self.config[GLOBAL.ENABLED]:
                self.enabled = self.config[GLOBAL.ENABLED]
                toggleOverride(PostMortemControlMode, "enable", self.enablePostMortem, self.enabled)
            if self.enabled:
                self.reset = True
                self.applySettings({GAME.COMMANDER_CAM: 0, GAME.PRE_COMMANDER_CAM: 0})
                camera._cfg[ARCADE.DIST_RANGE] = MinMax(*self.config[ARCADE.DIST_RANGE])
                camera._cfg[ARCADE.SCROLL_SENSITIVITY] = self.config[ARCADE.SCROLL_SENSITIVITY]
                camera._cfg[ARCADE.START_DIST] = self.config[ARCADE.START_DEAD_DIST]
                camera._cfg[ARCADE.START_ANGLE] = -0.18
                camera._updateProperties(state=None)
            elif self.reset:
                self.resetToDefault(CTRL_MODE_NAME.ARCADE)
                camera._updateProperties(state=None)

    def enablePostMortem(self, base, mode, **kwargs):
        if 'postmortemParams' in kwargs:
            kwargs['postmortemParams'] = (mode.camera.angles, self.config[ARCADE.START_DEAD_DIST])
            kwargs.setdefault('transitionDuration', 2.0)
        return base(mode, **kwargs)


class Strategic(CameraSettings):

    def __init__(self):
        super(Strategic, self).__init__()

    @property
    def name(self):
        return STRATEGIC.NAME

    def update(self):
        self.enabled = self.config[GLOBAL.ENABLED]
        ctrl_mode_names = (CTRL_MODE_NAME.STRATEGIC, CTRL_MODE_NAME.ARTY)
        if self.enabled:
            self.reset = True
            for control_mode_name in ctrl_mode_names:
                camera = self.getCamera(control_mode_name)
                if camera is not None:
                    camera._cfg[STRATEGIC.DIST_RANGE] = self.config[STRATEGIC.DIST_RANGE]
                    camera._cfg[STRATEGIC.SCROLL_SENSITIVITY] = self.config[STRATEGIC.SCROLL_SENSITIVITY]
        elif self.reset:
            for control_mode_name in ctrl_mode_names:
                self.resetToDefault(control_mode_name)


class Sniper(CameraSettings):
    DEFAULT_X_METERS = 20.0
    ZOOM = "zoom"
    ZOOMS = "zooms"
    MAX_DIST = 600.0
    MIN_DIST = 50.0

    def __init__(self, appLoader):
        super(Sniper, self).__init__()
        self._dyn_zoom = False
        self.after_shoot = ChangeCameraModeAfterShoot(appLoader)

    @property
    def name(self):
        return SNIPER.NAME

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
        camera = self.getCamera(CTRL_MODE_NAME.SNIPER)
        if camera is not None:
            no_dynamic = user_settings.effects[EFFECTS.NO_SNIPER_DYNAMIC]
            camera.enableDynamicCamera(False if no_dynamic else bool(self.settingsCore.getSetting(GAME.DYNAMIC_CAMERA)))
            if self._dyn_zoom != self.config[SNIPER.DYN_ZOOM] and self.enabled:
                self._dyn_zoom = self.config[SNIPER.DYN_ZOOM] and self.enabled
                toggleOverride(SniperCamera, "enable", self.enableSniper, self._dyn_zoom)
            if self._dyn_zoom and self.settingsCore.getSetting(GAME.SNIPER_ZOOM):
                self.applySettings({GAME.SNIPER_ZOOM: 0})
            _change_steps = self.config[SNIPER.ZOOM_STEPS] and self.enabled
            if _change_steps or self._dyn_zoom:
                self.reset = True
                steps = sorted(self.config[SNIPER.STEPS]) if _change_steps else SNIPER.DEFAULT_STEPS
                if steps and steps != camera._cfg[self.ZOOMS]:
                    new_exposure = self.linear_interpolate(steps)
                    camera._SniperCamera__dynamicCfg[SNIPER.ZOOM_EXPOSURE] = new_exposure
                    camera._cfg[self.ZOOMS] = steps
                    logDebug("UPDATE_ZOOMS = steps:{} exposure:{}", steps, new_exposure)
                    self.applySettings({GAME.INCREASED_ZOOM: 1})
            elif self.reset:
                self.resetToDefault(CTRL_MODE_NAME.SNIPER)

    def getZoom(self, zooms, distance):
        if not distance or distance > self.MAX_DIST or distance < self.MIN_DIST:
            return zooms[0]
        else:
            target = (distance - self.MIN_DIST) / self.DEFAULT_X_METERS
            return min(zooms, key=lambda value: abs(value - target))

    def enableSniper(self, base, camera, targetPos, saveZoom):
        ownPosition = getOwnVehiclePosition()
        distance = (targetPos - ownPosition).length if ownPosition is not None else 0
        camera._cfg[self.ZOOM] = self.getZoom(camera._cfg[self.ZOOMS], distance)
        return base(camera, targetPos, True)


class CameraManager(object):
    appLoader = dependency.descriptor(IAppLoader)

    def __init__(self):
        self.appLoader.onGUISpaceBeforeEnter += self.updateCameras
        self.__modes = (Arcade(), Sniper(self.appLoader), Strategic())
        for mode in self.__modes:
            g_events.onModSettingsChanged += mode.onModSettingsChanged

    def fini(self):
        self.appLoader.onGUISpaceBeforeEnter -= self.updateCameras
        for mode in self.__modes:
            g_events.onModSettingsChanged -= mode.onModSettingsChanged

    def updateCameras(self, spaceID):
        if spaceID == GuiGlobalSpaceID.BATTLE_LOADING:
            for mode in self.__modes:
                if mode.isChanged:
                    mode.update()
                    mode.isChanged = False


camera_manager = CameraManager()


def fini():
    camera_manager.fini()

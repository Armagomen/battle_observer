import TriggersManager
from account_helpers.settings_core.settings_constants import GAME
from aih_constants import CTRL_MODE_NAME
from armagomen._constants import ARCADE, EFFECTS, GLOBAL, SNIPER, STRATEGIC
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import addCallback, getPlayer, MinMax, ResMgr, toggleOverride
from armagomen.utils.events import g_events
from armagomen.utils.logging import logDebug, logError
from AvatarInputHandler.control_modes import PostMortemControlMode
from AvatarInputHandler.DynamicCameras.SniperCamera import SniperCamera
from gui.battle_control.avatar_getter import getInputHandler, getOwnVehiclePosition
from helpers import dependency
from skeletons.account_helpers.settings_core import ISettingsCache, ISettingsCore
from skeletons.gui.app_loader import GuiGlobalSpaceID, IAppLoader
from skeletons.gui.battle_session import IBattleSessionProvider


class ChangeCameraModeAfterShoot(TriggersManager.ITriggerListener):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)

    def __init__(self, appLoader):
        self.latency = 0.0
        self.skip_clip = False
        self.appLoader = appLoader
        self.__trigger_type = TriggersManager.TRIGGER_TYPE.PLAYER_DISCRETE_SHOOT
        self.avatar = None
        self.enabled = False

    def updateSettings(self, data):
        enabled = data[SNIPER.DISABLE_SNIPER] and data[GLOBAL.ENABLED]
        self.latency = float(max(data[SNIPER.DISABLE_LATENCY], 0))
        self.skip_clip = data[SNIPER.SKIP_CLIP]
        if self.enabled != enabled:
            self.enabled = enabled
            self.toggleSubscribe(enabled)

    def toggleSubscribe(self, enabled):
        if enabled:
            self.appLoader.onGUISpaceEntered += self.onGUISpaceEntered
            self.appLoader.onGUISpaceLeft += self.onGUISpaceLeft
        else:
            self.appLoader.onGUISpaceEntered -= self.onGUISpaceEntered
            self.appLoader.onGUISpaceLeft -= self.onGUISpaceLeft

    def toggleTrigger(self, activate):
        TriggersManager.g_manager.addListener(self) if activate else TriggersManager.g_manager.delListener(self)
        logDebug("ChangeCameraModeAfterShoot/toggleTrigger: {}", activate)

    def onGUISpaceEntered(self, spaceID):
        if spaceID == GuiGlobalSpaceID.BATTLE:
            prebattleCtrl = self.sessionProvider.dynamic.prebattleSetup
            if prebattleCtrl is not None:
                prebattleCtrl.onSelectionConfirmed += self.__updateCurrVehicleInfo
            self.avatar = getPlayer()
            self.toggleTrigger(self.isTriggerEnabled())

    def onGUISpaceLeft(self, spaceID):
        if spaceID == GuiGlobalSpaceID.BATTLE:
            prebattleCtrl = self.sessionProvider.dynamic.prebattleSetup
            if prebattleCtrl is not None:
                prebattleCtrl.onSelectionConfirmed += self.__updateCurrVehicleInfo
            self.toggleTrigger(False)
            self.avatar = None

    def __updateCurrVehicleInfo(self):
        self.toggleTrigger(self.isTriggerEnabled())

    def onTriggerActivated(self, params):
        if params.get('type') == self.__trigger_type:
            addCallback(self.latency, self.changeControlMode)

    def isTriggerEnabled(self):
        vehicle = self.sessionProvider.getArenaDP().getVehicleInfo()
        if self.avatar is None or vehicle is None or vehicle.isSPG() or vehicle.vehicleType.level < 5 or vehicle.isAutoShootGunVehicle():
            return False
        descriptor = self.avatar.getVehicleDescriptor()
        if descriptor is None or self.skip_clip and "clip" in descriptor.gun.tags:
            return False
        return True

    def changeControlMode(self):
        input_handler = self.avatar.inputHandler
        if input_handler is not None and input_handler.ctrlModeName == CTRL_MODE_NAME.SNIPER:
            aiming_system = input_handler.ctrl.camera.aimingSystem
            input_handler.onControlModeChanged(CTRL_MODE_NAME.ARCADE, prevModeName=input_handler.ctrlModeName,
                                               preferredPos=aiming_system.getDesiredShotPoint(),
                                               turretYaw=aiming_system.turretYaw,
                                               gunPitch=aiming_system.gunPitch,
                                               aimingMode=input_handler.ctrl._aimingMode,
                                               closesDist=False,
                                               curVehicleID=self.avatar.playerVehicleID)


class CameraSettings(object):
    settingsCore = dependency.descriptor(ISettingsCore)
    settingsCache = dependency.descriptor(ISettingsCache)

    _CONTROL_MODE_NAME_TO_SEC = {
        CTRL_MODE_NAME.ARCADE: "gui/avatar_input_handler.xml/arcadeMode/camera/",
        CTRL_MODE_NAME.MAP_CASE_ARCADE_EPIC_MINEFIELD: "gui/avatar_input_handler.xml/arcadeEpicMinefieldMode/camera/",
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
        if input_handler is not None and control_mode_name in input_handler.ctrls:
            return input_handler.ctrls[control_mode_name].camera
        logError("{}, camera is not found in input_handler.ctrls {}", control_mode_name, input_handler.ctrls)
        return None

    @staticmethod
    def get_private_attr(obj, attr_name):
        for cls in obj.__class__.__mro__:
            mangled = "_%s%s" % (cls.__name__, attr_name)
            if hasattr(obj, mangled):
                return getattr(obj, mangled)
        return None

    def resetToDefault(self, control_mode_name):
        camera = self.getCamera(control_mode_name)
        if camera is not None:
            ResMgr.purge('gui/avatar_input_handler.xml')
            cameraSec = ResMgr.openSection(self._CONTROL_MODE_NAME_TO_SEC[control_mode_name])
            camera._reloadConfigs(cameraSec)
            if hasattr(camera, "_updateProperties"):
                state = None
                zoomStateSwitcher = self.get_private_attr(camera, "__zoomStateSwitcher")
                if zoomStateSwitcher is not None:
                    state = zoomStateSwitcher.getCurrentState()
                camera._updateProperties(state=state)
        self.reset = False

    def applySettings(self, params):
        if not self.settingsCore.isReady() or not self.settingsCache.settings.isSynced():
            addCallback(1.0, self.applySettings, params)
        elif any(self.settingsCore.applySetting(key, value) is not None for key, value in params.items()):
            self.settingsCore.applyStorages(False)
            self.settingsCore.clearStorages()


class Arcade(CameraSettings):

    def __init__(self):
        super(Arcade, self).__init__()

    @property
    def name(self):
        return ARCADE.NAME

    def update(self):
        if self.enabled != self.config[GLOBAL.ENABLED]:
            self.enabled = self.config[GLOBAL.ENABLED]
            toggleOverride(PostMortemControlMode, "enable", self.enablePostMortem, self.enabled)
        ctrl_mode_names = (CTRL_MODE_NAME.ARCADE, CTRL_MODE_NAME.MAP_CASE_ARCADE_EPIC_MINEFIELD)
        if self.enabled:
            self.reset = True
            for control_mode_name in ctrl_mode_names:
                camera = self.getCamera(control_mode_name)
                if camera is not None:
                    self.applySettings({GAME.COMMANDER_CAM: 0, GAME.PRE_COMMANDER_CAM: 0})
                    camera._cfg[ARCADE.DIST_RANGE] = MinMax(*self.config[ARCADE.DIST_RANGE])
                    camera._cfg[ARCADE.SCROLL_SENSITIVITY] = self.config[ARCADE.SCROLL_SENSITIVITY]
                    camera._cfg[ARCADE.START_DIST] = self.config[ARCADE.START_DEAD_DIST]
                    camera._cfg[ARCADE.START_ANGLE] = -0.18
                    camera._updateProperties()
        elif self.reset:
            for control_mode_name in ctrl_mode_names:
                self.resetToDefault(control_mode_name)

    def enablePostMortem(self, base, mode, **kwargs):
        if 'postmortemParams' in kwargs:
            kwargs['postmortemParams'] = (mode.camera.angles, self.config[ARCADE.START_DEAD_DIST])
            kwargs.setdefault('transitionDuration', 1.0)
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
            if _change_steps:
                self.reset = True
                steps = sorted(self.config[SNIPER.STEPS] or SNIPER.DEFAULT_STEPS)
                if steps != camera._cfg[self.ZOOMS]:
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
        try:
            saveZoom = True
            ownPosition = getOwnVehiclePosition()
            distance = (targetPos - ownPosition).length if ownPosition is not None else 0
            camera._cfg[self.ZOOM] = self.getZoom(camera._cfg[self.ZOOMS], distance)
        except Exception as e:
            logError("enableSniper: {}", repr(e))
        return base(camera, targetPos, saveZoom)


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
                    try:
                        mode.update()
                    except Exception as e:
                        logError("{}: {}", mode.name, repr(e))
                    mode.isChanged = False


camera_manager = CameraManager()


def fini():
    camera_manager.fini()

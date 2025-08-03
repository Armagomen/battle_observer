# coding=utf-8
import TriggersManager
from armagomen._constants import MAIN
from armagomen.battle_observer.i18n.save_shoot import LOCKED_MESSAGE
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import cancelOverride, overrideMethod
from armagomen.utils.keys_listener import g_keysListener
from Avatar import PlayerAvatar
from DestructibleEntity import DestructibleEntity
from frameworks.wulf import WindowLayer
from gui.Scaleform.genConsts.BATTLE_VIEW_ALIASES import BATTLE_VIEW_ALIASES
from gui.shared.personality import ServicesLocator
from helpers import dependency
from messenger.MessengerEntry import g_instance
from skeletons.gui.app_loader import GuiGlobalSpaceID, IAppLoader
from skeletons.gui.battle_session import IBattleSessionProvider
from Vehicle import Vehicle


class SaveShootLite(TriggersManager.ITriggerListener):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)
    appLoader = dependency.descriptor(IAppLoader)

    def __init__(self):
        user_settings.onModSettingsChanged += self.onModSettingsChanged
        ServicesLocator.appLoader.onGUISpaceEntered += self.onGUISpaceEntered
        ServicesLocator.appLoader.onGUISpaceLeft += self.onGUISpaceLeft
        self.enabled = user_settings.main[MAIN.SAVE_SHOT]
        self.unlock = False
        self.vehicleErrorComponent = None

    def shoot(self, base, avatar, isRepeat=False):
        target = avatar.target
        if target is None or isRepeat or self.unlock or self.checkTarget(target):
            return base(avatar, isRepeat=isRepeat)
        vehicle_info = self.sessionProvider.getArenaDP().getVehicleInfo(target.id)
        message = LOCKED_MESSAGE.format(vehicle_info.vehicleType.shortName)
        g_instance.gui.addClientMessage(message)
        if self.vehicleErrorComponent is not None:
            self.vehicleErrorComponent.as_showYellowMessageS(None, message)

    def onModSettingsChanged(self, config, blockID):
        if blockID == MAIN.NAME:
            self.enabled = config[MAIN.SAVE_SHOT]
            if self.enabled:
                overrideMethod(PlayerAvatar, "shoot")(self.shoot)
            else:
                cancelOverride(PlayerAvatar, "shoot", "shoot")

    def onGUISpaceEntered(self, spaceID):
        if self.enabled and spaceID == GuiGlobalSpaceID.BATTLE:
            g_keysListener.registerComponent(self.keyEvent)
            battlePage = self.appLoader.getApp().containerManager.getContainer(WindowLayer.VIEW).getView()
            if battlePage is not None:
                self.vehicleErrorComponent = battlePage.components.get(BATTLE_VIEW_ALIASES.VEHICLE_ERROR_MESSAGES)
            TriggersManager.g_manager.addListener(self)

    def onGUISpaceLeft(self, spaceID):
        if self.enabled and spaceID == GuiGlobalSpaceID.BATTLE:
            self.unlock = False
            self.vehicleErrorComponent = None
            TriggersManager.g_manager.delListener(self)

    def onTriggerActivated(self, params):
        if params.get('type') == TriggersManager.TRIGGER_TYPE.AUTO_AIM_AT_VEHICLE:
            self.unlock = True

    def onTriggerDeactivated(self, params):
        if params.get('type') == TriggersManager.TRIGGER_TYPE.AUTO_AIM_AT_VEHICLE:
            self.unlock = False

    @staticmethod
    def checkTarget(target):
        return isinstance(target, (Vehicle, DestructibleEntity)) and target.isAlive() and not target.isPlayerTeam()

    def keyEvent(self, isKeyDown):
        self.unlock = isKeyDown


save_shoot_lite = SaveShootLite()


def fini():
    user_settings.onModSettingsChanged -= save_shoot_lite.onModSettingsChanged
    ServicesLocator.appLoader.onGUISpaceLeft -= save_shoot_lite.onGUISpaceLeft
    ServicesLocator.appLoader.onGUISpaceEntered -= save_shoot_lite.onGUISpaceEntered

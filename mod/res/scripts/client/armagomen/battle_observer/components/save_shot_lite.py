# coding=utf-8
import TriggersManager
from armagomen._constants import MAIN
from armagomen.battle_observer.i18n.save_shoot import LOCKED_MESSAGE
from armagomen.utils.common import toggleOverride
from armagomen.utils.events import g_events
from armagomen.utils.keys_listener import g_keysListener
from armagomen.utils.logging import logError
from Avatar import PlayerAvatar
from DestructibleEntity import DestructibleEntity
from frameworks.wulf import WindowLayer
from gui.Scaleform.genConsts.BATTLE_VIEW_ALIASES import BATTLE_VIEW_ALIASES
from helpers import dependency
from messenger.MessengerEntry import g_instance
from skeletons.gui.app_loader import GuiGlobalSpaceID, IAppLoader
from Vehicle import Vehicle


class SaveShootLite(TriggersManager.ITriggerListener):
    appLoader = dependency.descriptor(IAppLoader)

    def __init__(self):
        g_events.onModSettingsChanged += self.onModSettingsChanged
        self.appLoader.onGUISpaceEntered += self.onGUISpaceEntered
        self.appLoader.onGUISpaceLeft += self.onGUISpaceLeft
        self.enabled = False
        self.unlock = False
        self.vehicleErrorComponent = None

    def fini(self):
        g_events.onModSettingsChanged -= self.onModSettingsChanged
        self.appLoader.onGUISpaceLeft -= self.onGUISpaceLeft
        self.appLoader.onGUISpaceEntered -= self.onGUISpaceEntered

    def _shoot(self, base, avatar, isRepeat=False):
        target = avatar.target
        if target is None or isRepeat or self.unlock or self.checkTarget(target):
            return base(avatar, isRepeat=isRepeat)
        shortName = "Undefined"
        try:
            if isinstance(target, Vehicle) and target.typeDescriptor:
                shortName = target.typeDescriptor.type.shortUserString
        except Exception as error:
            logError(repr(error))
        message = LOCKED_MESSAGE.format(shortName)
        g_instance.gui.addClientMessage(message)
        if self.vehicleErrorComponent is not None:
            self.vehicleErrorComponent.as_showYellowMessageS(None, message)

    def onModSettingsChanged(self, name, data):
        if name == MAIN.NAME:
            if self.enabled != data[MAIN.SAVE_SHOT]:
                self.enabled = data[MAIN.SAVE_SHOT]
                toggleOverride(PlayerAvatar, "shoot", self._shoot, self.enabled)

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
        return isinstance(target, (Vehicle, DestructibleEntity)) and target.isAlive() and not target.isPlayerTeam

    def keyEvent(self, isKeyDown):
        self.unlock = isKeyDown


save_shoot_lite = SaveShootLite()


def fini():
    save_shoot_lite.fini()

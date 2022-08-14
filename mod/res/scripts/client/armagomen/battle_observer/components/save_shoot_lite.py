from Avatar import PlayerAvatar
from PlayerEvents import g_playerEvents
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import GLOBAL, SAVE_SHOOT
from armagomen.utils.common import overrideMethod, isReplay
from armagomen.utils.keys_listener import g_keysListener
from frameworks.wulf import WindowLayer
from gui.Scaleform.genConsts.BATTLE_VIEW_ALIASES import BATTLE_VIEW_ALIASES
from gui.shared.personality import ServicesLocator
from messenger.MessengerEntry import g_instance

__all__ = ["save_shoot_lite"]


class SaveShootLite(object):

    def __init__(self):
        settings.onModSettingsChanged += self.onModSettingsChanged
        g_playerEvents.onAvatarReady += self.onEnterBattlePage
        g_playerEvents.onAvatarBecomeNonPlayer += self.onExitBattlePage
        self.enabled = False
        self.unlockShoot = False
        self.destroyedBlock = False
        self.msg = None
        self.vehicleErrorComponent = None
        overrideMethod(PlayerAvatar, "shoot")(self.shoot)

    def shoot(self, base, avatar, isRepeat=False):
        if not self.enabled or self.unlockShoot or not self.is_targetAllyOrDeath(avatar):
            return base(avatar, isRepeat=isRepeat)
        if isRepeat or not self.msg:
            return
        g_instance.gui.addClientMessage(self.msg)
        if self.vehicleErrorComponent is not None:
            self.vehicleErrorComponent.as_showYellowMessageS(None, self.msg)

    def onModSettingsChanged(self, config, blockID):
        if blockID == SAVE_SHOOT.NAME:
            self.enabled = config[GLOBAL.ENABLED] and not isReplay()
            self.destroyedBlock = config[SAVE_SHOOT.DESTROYED_BLOCK]
            self.msg = config[SAVE_SHOOT.MSG]

    def onEnterBattlePage(self):
        if self.enabled:
            g_keysListener.registerComponent(self.keyEvent)
            app = ServicesLocator.appLoader.getApp()
            if app is None:
                return
            battlePage = app.containerManager.getContainer(WindowLayer.VIEW).getView()
            if battlePage is None:
                return
            self.vehicleErrorComponent = battlePage.components.get(BATTLE_VIEW_ALIASES.VEHICLE_ERROR_MESSAGES)

    def onExitBattlePage(self):
        self.unlockShoot = False
        self.vehicleErrorComponent = None

    def is_targetAllyOrDeath(self, avatar):
        if avatar.target is not None and avatar.target.__class__.__name__ == SAVE_SHOOT.VEHICLE:
            if avatar.target.isAlive():
                return avatar.target.publicInfo[SAVE_SHOOT.TEAM] == avatar.team
            else:
                return self.destroyedBlock
        return False

    def keyEvent(self, isKeyDown):
        self.unlockShoot = isKeyDown


save_shoot_lite = SaveShootLite()

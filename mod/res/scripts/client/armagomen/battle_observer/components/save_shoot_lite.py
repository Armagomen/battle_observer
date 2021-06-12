from Avatar import PlayerAvatar
from PlayerEvents import g_playerEvents
from armagomen.battle_observer.core import settings, keysParser
from armagomen.constants import GLOBAL, SAVE_SHOOT, MAIN
from armagomen.utils.common import overrideMethod, isReplay
from bwobsolete_helpers.BWKeyBindings import KEY_ALIAS_ALT
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
        overrideMethod(PlayerAvatar, "shoot")(self.shoot)

    def shoot(self, base, avatar, isRepeat=False):
        if self.enabled and not self.unlockShoot and self.is_targetAllyOrDeath(avatar):
            if not isRepeat and self.msg:
                g_instance.gui.addClientMessage(self.msg)
            return
        return base(avatar, isRepeat=isRepeat)

    def onModSettingsChanged(self, config, blockID):
        if blockID == SAVE_SHOOT.NAME:
            self.enabled = config[GLOBAL.ENABLED] and not isReplay()
            self.destroyedBlock = config[SAVE_SHOOT.DESTROYED_BLOCK]
            self.msg = config[SAVE_SHOOT.MSG]

    @staticmethod
    def getHotKey():
        if settings.main[MAIN.USE_KEY_PAIRS]:
            return KEY_ALIAS_ALT
        else:
            return KEY_ALIAS_ALT[GLOBAL.FIRST],

    def onEnterBattlePage(self):
        if self.enabled:
            keysParser.registerComponent(SAVE_SHOOT.HOT_KEY, self.getHotKey())
            keysParser.onKeyPressed += self.keyEvent

    def onExitBattlePage(self):
        self.unlockShoot = False
        if self.enabled:
            keysParser.onKeyPressed -= self.keyEvent

    def is_targetAllyOrDeath(self, avatar):
        if avatar.target is not None and avatar.target.__class__.__name__ == SAVE_SHOOT.VEHICLE:
            if avatar.target.isAlive():
                return avatar.target.publicInfo[SAVE_SHOOT.TEAM] == avatar.team
            else:
                return self.destroyedBlock
        return False

    def keyEvent(self, keyName, isKeyDown):
        if keyName == SAVE_SHOOT.HOT_KEY:
            self.unlockShoot = isKeyDown


save_shoot_lite = SaveShootLite()

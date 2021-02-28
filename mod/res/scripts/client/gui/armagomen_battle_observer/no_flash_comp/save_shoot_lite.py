from Avatar import PlayerAvatar
from BattleReplay import g_replayCtrl
from PlayerEvents import g_playerEvents
from bwobsolete_helpers.BWKeyBindings import KEY_ALIAS_ALT
from messenger.MessengerEntry import g_instance
from ..core import cfg, cache, keysParser
from ..core.bo_constants import GLOBAL, SAVE_SHOOT, MAIN
from ..core.utils import overrideMethod

__all__ = ["save_shoot_lite"]


class SaveShootLite(object):

    def __init__(self):
        cache.onModSettingsChanged += self.onModSettingsChanged
        g_playerEvents.onAvatarReady += self.onEnterBattlePage
        g_playerEvents.onAvatarBecomeNonPlayer += self.onExitBattlePage
        self.enabled = False
        self.unlockShoot = False
        self.aliveOnly = False
        self.msg = None

        @overrideMethod(PlayerAvatar, "shoot")
        def shoot(base, avatar, isRepeat=False):
            if self.enabled and not self.unlockShoot and self.is_targetAllyOrDeath(avatar.target):
                if not isRepeat and self.msg:
                    g_instance.gui.addClientMessage(self.msg)
                return
            return base(avatar, isRepeat=isRepeat)

    def onModSettingsChanged(self, config, blockID):
        if blockID == SAVE_SHOOT.NAME:
            self.enabled = config[GLOBAL.ENABLED] and not g_replayCtrl.isPlaying
            self.aliveOnly = config[SAVE_SHOOT.ALIVE_ONLY]
            self.msg = config[SAVE_SHOOT.MSG]

    @staticmethod
    def getHotKey():
        if cfg.main[MAIN.USE_KEY_PAIRS]:
            return KEY_ALIAS_ALT
        else:
            return KEY_ALIAS_ALT[GLOBAL.FIRST],

    def onEnterBattlePage(self):
        keysParser.registerComponent(SAVE_SHOOT.HOT_KEY, self.getHotKey())
        if self.enabled:
            keysParser.onKeyPressed += self.keyEvent

    def onExitBattlePage(self):
        self.unlockShoot = False
        if self.enabled:
            keysParser.onKeyPressed -= self.keyEvent

    def is_targetAllyOrDeath(self, target):
        if target is not None and target.__class__.__name__ == SAVE_SHOOT.VEHICLE:
            death = not target.isAlive() and self.aliveOnly
            isAlly = target.publicInfo[SAVE_SHOOT.TEAM] == cache.allyTeam
            return death or isAlly
        return False

    def keyEvent(self, keyName, isKeyDown):
        if keyName == SAVE_SHOOT.HOT_KEY:
            self.unlockShoot = isKeyDown


save_shoot_lite = SaveShootLite()

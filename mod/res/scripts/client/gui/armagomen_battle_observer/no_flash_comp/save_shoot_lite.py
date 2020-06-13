from Avatar import PlayerAvatar
from BattleReplay import g_replayCtrl
from bwobsolete_helpers.BWKeyBindings import KEY_ALIAS_ALT
from messenger.MessengerEntry import g_instance

from ..core.battle_cache import cache
from ..core.bo_constants import GLOBAL, SAVE_SHOOT, MAIN
from ..core.config import cfg
from ..core.core import overrideMethod
from ..core.events import g_events
from ..core.keys_parser import g_keysParser


class SaveShootLite(object):

    def __init__(self):
        g_events.onSettingsChanged += self.onSettingsChanged
        g_events.onEnterBattlePage += self.onEnterBattlePage
        g_events.onExitBattlePage += self.onExitBattlePage
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

    def onSettingsChanged(self, config, blockID):
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
        g_keysParser.registerComponent(SAVE_SHOOT.HOT_KEY, self.getHotKey())
        if self.enabled:
            g_events.onKeyPressed += self.keyEvent

    def onExitBattlePage(self):
        self.unlockShoot = False
        if self.enabled:
            g_events.onKeyPressed -= self.keyEvent

    def is_targetAllyOrDeath(self, target):
        death = False
        isAlly = False
        if target is not None and target.__class__.__name__ == SAVE_SHOOT.VEHICLE:
            death = not target.isAlive() and self.aliveOnly
            isAlly = target.publicInfo[SAVE_SHOOT.TEAM] == cache.allyTeam
        return death or isAlly

    def keyEvent(self, keyName, isKeyDown):
        if keyName == SAVE_SHOOT.HOT_KEY:
            self.unlockShoot = isKeyDown


save_shoot_lite = SaveShootLite()

from gui.battle_control import avatar_getter

from armagomen.battle_observer.core import cfg, keysParser
from armagomen.battle_observer.core.constants import MINIMAP
from armagomen.battle_observer.meta.battle.minimap_meta import MinimapMeta


class Minimap(MinimapMeta):

    def __init__(self):
        super(Minimap, self).__init__()
        keysParser.registerComponent(MINIMAP.HOT_KEY, cfg.minimap[MINIMAP.ZOOM][MINIMAP.HOT_KEY])

    def onEnterBattlePage(self):
        super(Minimap, self).onEnterBattlePage()
        keysParser.onKeyPressed += self.keyEvent
        self.as_startUpdateS(cfg.minimap[MINIMAP.ZOOM][MINIMAP.INDENT])

    def onExitBattlePage(self):
        keysParser.onKeyPressed -= self.keyEvent
        super(Minimap, self).onExitBattlePage()

    def keyEvent(self, key, isKeyDown):
        if key == MINIMAP.HOT_KEY:
            self.as_MinimapCenteredS(isKeyDown)
            avatar_getter.setForcedGuiControlMode(isKeyDown, cursorVisible=isKeyDown)

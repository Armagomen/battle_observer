from gui.battle_control import avatar_getter
from ..core.bo_constants import MINIMAP
from ..core.config import cfg
from ..core.events import g_events
from ..core.keys_parser import g_keysParser
from ..meta.battle.minimap_meta import MinimapMeta


class Minimap(MinimapMeta):

    def __init__(self):
        super(Minimap, self).__init__()
        g_keysParser.registerComponent(MINIMAP.HOT_KEY, cfg.minimap[MINIMAP.ZOOM][MINIMAP.HOT_KEY])

    def onEnterBattlePage(self):
        super(Minimap, self).onEnterBattlePage()
        g_events.onKeyPressed += self.keyEvent
        self.as_startUpdateS(cfg.minimap[MINIMAP.ZOOM][MINIMAP.INDENT])

    def onExitBattlePage(self):
        g_events.onKeyPressed -= self.keyEvent
        super(Minimap, self).onExitBattlePage()

    def keyEvent(self, key, isKeyDown):
        if key == MINIMAP.HOT_KEY:
            self.as_MinimapCenteredS(isKeyDown)
            avatar_getter.setForcedGuiControlMode(isKeyDown, cursorVisible=isKeyDown)

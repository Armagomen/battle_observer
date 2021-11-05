from armagomen.battle_observer.core import keysParser
from armagomen.battle_observer.meta.battle.minimap_meta import MinimapMeta
from armagomen.constants import MINIMAP
from gui.battle_control import avatar_getter


class Minimap(MinimapMeta):

    def _populate(self):
        super(Minimap, self)._populate()
        keysParser.registerComponent(MINIMAP.HOT_KEY, self.settings[MINIMAP.ZOOM][MINIMAP.HOT_KEY])
        keysParser.onKeyPressed += self.onKeyPressed

    def _dispose(self):
        keysParser.onKeyPressed -= self.onKeyPressed
        super(Minimap, self)._dispose()

    def onKeyPressed(self, key, isKeyDown):
        if key == MINIMAP.HOT_KEY:
            self.as_MinimapCenteredS(isKeyDown)
            avatar_getter.setForcedGuiControlMode(isKeyDown, cursorVisible=isKeyDown)

    def onExitBattlePage(self):
        pass

    def onEnterBattlePage(self):
        self.as_startUpdateS(self.settings[MINIMAP.ZOOM][MINIMAP.INDENT])

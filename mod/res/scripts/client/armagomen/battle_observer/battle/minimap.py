from armagomen._constants import MINIMAP
from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta
from armagomen.utils.keys_listener import g_keysListener
from constants import ARENA_PERIOD
from gui.battle_control import avatar_getter


class MinimapZoomPlugin(BaseModMeta):

    def __init__(self):
        super(MinimapZoomPlugin, self).__init__()
        self.isComp7Battle = False

    def _populate(self):
        super(MinimapZoomPlugin, self)._populate()
        self.isComp7Battle = self.gui.isComp7Battle()
        g_keysListener.registerComponent(self.onKeyPressed, keyList=self.settings[MINIMAP.ZOOM_KEY])

    def onKeyPressed(self, isKeyDown):
        """hot key event"""
        if self._isDAAPIInited():
            if self.isComp7Battle and self._arenaVisitor.getArenaPeriod() != ARENA_PERIOD.BATTLE:
                return
            self.flashObject.minimapCentered(isKeyDown)
            avatar_getter.setForcedGuiControlMode(isKeyDown, enableAiming=False)

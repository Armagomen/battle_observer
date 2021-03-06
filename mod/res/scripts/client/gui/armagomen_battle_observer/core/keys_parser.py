from bwobsolete_helpers.BWKeyBindings import KEY_ALIAS_CONTROL, KEY_ALIAS_ALT, KEY_ALIAS_SHIFT
from gui import InputHandler
from gui.battle_control import avatar_getter
from .bo_constants import MAIN
from .config import cfg
from .events import g_events


class HotKeysParser(object):

    def __init__(self):
        self.keysMap = dict()
        self.pressedKeys = set()
        self.usableKeys = set()
        g_events.onEnterBattlePage += self.onEnterBattlePage
        g_events.onExitBattlePage += self.onExitBattlePage

    def registerComponent(self, keyName, keyList):
        normalizedKey = self.normalizeKey(keyList)
        self.keysMap[keyName] = normalizedKey
        self.usableKeys.update(normalizedKey)

    def clear(self):
        self.keysMap.clear()
        self.usableKeys.clear()
        self.pressedKeys.clear()

    def onEnterBattlePage(self):
        InputHandler.g_instance.onKeyDown += self.keyEvent
        InputHandler.g_instance.onKeyUp += self.keyEvent

    def onExitBattlePage(self):
        InputHandler.g_instance.onKeyDown -= self.keyEvent
        InputHandler.g_instance.onKeyUp -= self.keyEvent
        self.clear()

    def keyEvent(self, event):
        if event.key in self.usableKeys:
            key = event.key
            if not avatar_getter.isForcedGuiControlMode() or key in self.pressedKeys:
                isKeyDown = event.isKeyDown()
                if isKeyDown:
                    if cfg.main[MAIN.USE_KEY_PAIRS]:
                        if key in KEY_ALIAS_CONTROL:
                            self.pressedKeys.update(KEY_ALIAS_CONTROL)
                        elif key in KEY_ALIAS_ALT:
                            self.pressedKeys.update(KEY_ALIAS_ALT)
                        elif key in KEY_ALIAS_SHIFT:
                            self.pressedKeys.update(KEY_ALIAS_SHIFT)
                    self.pressedKeys.add(key)
                    for keyName, keys in self.keysMap.iteritems():
                        if self.pressedKeys.issuperset(keys):
                            g_events.onKeyPressed(keyName, isKeyDown)
                else:
                    for keyName, keys in self.keysMap.iteritems():
                        if self.pressedKeys.issuperset(keys):
                            g_events.onKeyPressed(keyName, isKeyDown)
                    if cfg.main[MAIN.USE_KEY_PAIRS]:
                        if key in KEY_ALIAS_CONTROL:
                            self.pressedKeys.difference_update(KEY_ALIAS_CONTROL)
                        elif key in KEY_ALIAS_ALT:
                            self.pressedKeys.difference_update(KEY_ALIAS_ALT)
                        elif key in KEY_ALIAS_SHIFT:
                            self.pressedKeys.difference_update(KEY_ALIAS_SHIFT)
                    self.pressedKeys.discard(key)

    @staticmethod
    def normalizeKey(keyList):
        keys = set()
        for key in keyList:
            if type(key) is list:
                keys.update(key)
            else:
                keys.add(key)
        return keys


g_keysParser = HotKeysParser()

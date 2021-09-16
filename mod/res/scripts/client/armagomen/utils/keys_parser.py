from Event import SafeEvent
from PlayerEvents import g_playerEvents
from bwobsolete_helpers.BWKeyBindings import KEY_ALIAS_CONTROL, KEY_ALIAS_ALT, KEY_ALIAS_SHIFT
from gui import InputHandler
from gui.battle_control import avatar_getter

USE_KEY_PAIRS = "useKeyPairs"


class HotKeysParser(object):

    def __init__(self, config):
        self.config = config
        self.keysMap = dict()
        self.pressedKeys = set()
        self.usableKeys = set()
        self.onKeyPressed = SafeEvent()
        g_playerEvents.onAvatarReady += self.onEnterBattlePage
        g_playerEvents.onAvatarBecomeNonPlayer += self.onExitBattlePage

    def registerComponent(self, keyName, keyList):
        normalizedKey = self.normalizeKey(keyList)
        self.keysMap[keyName] = normalizedKey
        self.usableKeys.update(normalizedKey)

    def clear(self):
        self.keysMap.clear()
        self.usableKeys.clear()
        self.pressedKeys.clear()

    def onEnterBattlePage(self):
        InputHandler.g_instance.onKeyDown += self.onKeyDown
        InputHandler.g_instance.onKeyUp += self.onKeyUp

    def onExitBattlePage(self):
        InputHandler.g_instance.onKeyDown -= self.onKeyDown
        InputHandler.g_instance.onKeyUp -= self.onKeyUp
        self.clear()

    def onKeyUp(self, event):
        if event.key not in self.usableKeys or avatar_getter.isForcedGuiControlMode():
            return
        for keyName, keys in self.keysMap.iteritems():
            if self.pressedKeys.issuperset(keys):
                self.onKeyPressed(keyName, False)
        if self.config.main[USE_KEY_PAIRS]:
            if event.key in KEY_ALIAS_CONTROL:
                self.pressedKeys.difference_update(KEY_ALIAS_CONTROL)
            elif event.key in KEY_ALIAS_ALT:
                self.pressedKeys.difference_update(KEY_ALIAS_ALT)
            elif event.key in KEY_ALIAS_SHIFT:
                self.pressedKeys.difference_update(KEY_ALIAS_SHIFT)
        self.pressedKeys.discard(event.key)

    def onKeyDown(self, event):
        if event.key not in self.usableKeys or avatar_getter.isForcedGuiControlMode():
            return
        if self.config.main[USE_KEY_PAIRS]:
            if event.key in KEY_ALIAS_CONTROL:
                self.pressedKeys.update(KEY_ALIAS_CONTROL)
            elif event.key in KEY_ALIAS_ALT:
                self.pressedKeys.update(KEY_ALIAS_ALT)
            elif event.key in KEY_ALIAS_SHIFT:
                self.pressedKeys.update(KEY_ALIAS_SHIFT)
        self.pressedKeys.add(event.key)
        for keyName, keys in self.keysMap.iteritems():
            if self.pressedKeys.issuperset(keys):
                self.onKeyPressed(keyName, True)

    @staticmethod
    def normalizeKey(keyList):
        keys = set()
        for key in keyList:
            if isinstance(key, (list, set, tuple)):
                keys.update(key)
            else:
                keys.add(key)
        return keys

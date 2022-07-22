from collections import namedtuple

from PlayerEvents import g_playerEvents
from armagomen.battle_observer.settings.default_settings import settings
from bwobsolete_helpers.BWKeyBindings import KEY_ALIAS_CONTROL, KEY_ALIAS_ALT, KEY_ALIAS_SHIFT
from gui import InputHandler

USE_KEY_PAIRS = "useKeyPairs"

KeysData = namedtuple("KeysData", ("keys", "keyFunction"))


class KeysListener(object):

    def __init__(self):
        self.keysMap = set()
        self.pressedKeys = set()
        self.usableKeys = set()
        g_playerEvents.onAvatarReady += self.onEnterBattlePage
        g_playerEvents.onAvatarBecomeNonPlayer += self.onExitBattlePage

    def registerComponent(self, keyList, keyFunction):
        normalizedKey = self.normalizeKey(keyList)
        self.keysMap.add(KeysData(normalizedKey, keyFunction))
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
        if event.key not in self.usableKeys or event.key not in self.pressedKeys:
            return
        for keysData in self.keysMap:
            if self.pressedKeys.issuperset(keysData.keys):
                keysData.keyFunction(False)
        if settings.main[USE_KEY_PAIRS]:
            if event.key in KEY_ALIAS_CONTROL:
                self.pressedKeys.difference_update(KEY_ALIAS_CONTROL)
            elif event.key in KEY_ALIAS_ALT:
                self.pressedKeys.difference_update(KEY_ALIAS_ALT)
            elif event.key in KEY_ALIAS_SHIFT:
                self.pressedKeys.difference_update(KEY_ALIAS_SHIFT)
        self.pressedKeys.discard(event.key)

    def onKeyDown(self, event):
        if event.isModifierDown() or event.key not in self.usableKeys or event.key in self.pressedKeys:
            return
        if settings.main[USE_KEY_PAIRS]:
            if event.key in KEY_ALIAS_CONTROL:
                self.pressedKeys.update(KEY_ALIAS_CONTROL)
            elif event.key in KEY_ALIAS_ALT:
                self.pressedKeys.update(KEY_ALIAS_ALT)
            elif event.key in KEY_ALIAS_SHIFT:
                self.pressedKeys.update(KEY_ALIAS_SHIFT)
        self.pressedKeys.add(event.key)
        for keysData in self.keysMap:
            if self.pressedKeys.issuperset(keysData.keys):
                keysData.keyFunction(True)

    @staticmethod
    def normalizeKey(keyList):
        keys = set()
        for key in keyList:
            if isinstance(key, (list, set, tuple)):
                keys.update(key)
            else:
                keys.add(key)
        return keys


g_keysListener = KeysListener()

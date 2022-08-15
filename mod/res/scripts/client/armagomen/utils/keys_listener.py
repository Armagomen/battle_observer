from collections import namedtuple

from Keys import KEY_LCONTROL, KEY_RCONTROL, KEY_RALT, KEY_LALT, KEY_LSHIFT, KEY_RSHIFT
from PlayerEvents import g_playerEvents
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import MAIN
from gui import InputHandler

KeysData = namedtuple("KeysData", ("keys", "keyFunction"))
KEY_ALIAS_CONTROL = {KEY_LCONTROL, KEY_RCONTROL}
KEY_ALIAS_ALT = {KEY_LALT, KEY_RALT}
KEY_ALIAS_SHIFT = {KEY_LSHIFT, KEY_RSHIFT}


class KeysListener(object):

    def __init__(self):
        self.keysMap = list()
        self.pressedKeys = set()
        self.usableKeys = set()
        self.useKeyPairs = False
        g_playerEvents.onAvatarReady += self.onEnterBattlePage
        g_playerEvents.onAvatarBecomeNonPlayer += self.onExitBattlePage

    def registerComponent(self, keyFunction, keyList=None):
        normalizedKey = KEY_ALIAS_ALT if not keyList else self.normalizeKey(keyList)
        self.keysMap.append(KeysData(normalizedKey, keyFunction))
        self.usableKeys.update(normalizedKey)

    def clear(self):
        self.keysMap = list()
        self.usableKeys.clear()
        self.pressedKeys.clear()

    def onEnterBattlePage(self):
        self.useKeyPairs = settings.main[MAIN.USE_KEY_PAIRS]
        InputHandler.g_instance.onKeyDown += self.onKeyDown
        InputHandler.g_instance.onKeyUp += self.onKeyUp

    def onExitBattlePage(self):
        InputHandler.g_instance.onKeyDown -= self.onKeyDown
        InputHandler.g_instance.onKeyUp -= self.onKeyUp
        self.clear()

    def onKeyUp(self, event):
        if event.key not in self.pressedKeys:
            return
        for keysData in self.keysMap:
            if self.pressedKeys.issuperset(keysData.keys):
                keysData.keyFunction(False)
        if self.useKeyPairs:
            if event.key in KEY_ALIAS_CONTROL:
                self.pressedKeys.difference_update(KEY_ALIAS_CONTROL)
            elif event.key in KEY_ALIAS_ALT:
                self.pressedKeys.difference_update(KEY_ALIAS_ALT)
            elif event.key in KEY_ALIAS_SHIFT:
                self.pressedKeys.difference_update(KEY_ALIAS_SHIFT)
        else:
            self.pressedKeys.discard(event.key)

    def onKeyDown(self, event):
        if event.isModifierDown() or event.key not in self.usableKeys or event.key in self.pressedKeys:
            return
        if self.useKeyPairs:
            if event.key in KEY_ALIAS_CONTROL:
                self.pressedKeys.update(KEY_ALIAS_CONTROL)
            elif event.key in KEY_ALIAS_ALT:
                self.pressedKeys.update(KEY_ALIAS_ALT)
            elif event.key in KEY_ALIAS_SHIFT:
                self.pressedKeys.update(KEY_ALIAS_SHIFT)
        else:
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

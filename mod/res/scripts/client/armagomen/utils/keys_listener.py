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
        g_playerEvents.onAvatarReady += self.onEnterBattlePage
        g_playerEvents.onAvatarBecomeNonPlayer += self.onExitBattlePage

    def registerComponent(self, keyFunction, keyList=None):
        self.keysMap.append(KeysData(self.normalizeKey(keyList) if keyList else KEY_ALIAS_ALT, keyFunction))

    def clear(self):
        self.keysMap = list()
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
        if event.key not in self.pressedKeys:
            return
        for keysData in self.keysMap:
            if event.key in keysData.keys:
                keysData.keyFunction(False)
        self.pressedKeys.discard(event.key)

    def onKeyDown(self, event):
        if event.isModifierDown() or event.key not in self.usableKeys or event.key in self.pressedKeys:
            return
        for keysData in self.keysMap:
            if event.key in keysData.keys:
                keysData.keyFunction(True)
        self.pressedKeys.add(event.key)

    def normalizeKey(self, keyList):
        keys = set()
        for key in keyList:
            if isinstance(key, (list, set, tuple)):
                keys.update(key)
            else:
                keys.add(key)
        if settings.main[MAIN.USE_KEY_PAIRS]:
            pairs = set()
            for key in keys:
                if key in KEY_ALIAS_CONTROL:
                    pairs.update(KEY_ALIAS_CONTROL)
                elif key in KEY_ALIAS_ALT:
                    pairs.update(KEY_ALIAS_ALT)
                elif key in KEY_ALIAS_SHIFT:
                    pairs.update(KEY_ALIAS_SHIFT)
            keys.update(pairs)
        self.usableKeys.update(keys)
        return keys


g_keysListener = KeysListener()

from collections import namedtuple

from armagomen._constants import MAIN
from gui import InputHandler
from Keys import KEY_LALT, KEY_LCONTROL, KEY_LSHIFT, KEY_RALT, KEY_RCONTROL, KEY_RSHIFT
from PlayerEvents import g_playerEvents

KeysData = namedtuple("KeysData", ("keys", "keyFunction"))
KEY_ALIAS_CONTROL = (KEY_LCONTROL, KEY_RCONTROL)
KEY_ALIAS_ALT = (KEY_LALT, KEY_RALT)
KEY_ALIAS_SHIFT = (KEY_LSHIFT, KEY_RSHIFT)


class KeysListener(object):

    def __init__(self):
        self.components = set()
        self.pressedKeys = set()
        self.usableKeys = set()
        self.mainSettings = {}

    def init(self, mainSettings):
        self.mainSettings = mainSettings
        g_playerEvents.onAvatarReady += self.onAvatarReady
        g_playerEvents.onAvatarBecomeNonPlayer += self.onAvatarBecomeNonPlayer

    def fini(self):
        g_playerEvents.onAvatarReady -= self.onAvatarReady
        g_playerEvents.onAvatarBecomeNonPlayer -= self.onAvatarBecomeNonPlayer

    def registerComponent(self, keyFunction, keyList=None):
        self.components.add(KeysData(self.normalizeKey(keyList) if keyList else KEY_ALIAS_ALT, keyFunction))

    def clear(self):
        self.components.clear()
        self.usableKeys.clear()
        self.pressedKeys.clear()

    def onAvatarReady(self):
        InputHandler.g_instance.onKeyDown += self.onKeyDown
        InputHandler.g_instance.onKeyUp += self.onKeyUp

    def onAvatarBecomeNonPlayer(self):
        InputHandler.g_instance.onKeyDown -= self.onKeyDown
        InputHandler.g_instance.onKeyUp -= self.onKeyUp
        self.clear()

    def onKeyUp(self, event):
        if event.key not in self.pressedKeys:
            return
        for component in self.components:
            if event.key in component.keys:
                component.keyFunction(False)
        self.pressedKeys.discard(event.key)

    def onKeyDown(self, event):
        if event.key not in self.usableKeys or event.key in self.pressedKeys:
            return
        for component in self.components:
            if event.key in component.keys:
                component.keyFunction(True)
        self.pressedKeys.add(event.key)

    def normalizeKey(self, keyList):
        keys = set()
        for key in keyList:
            if isinstance(key, (list, set, tuple)):
                keys.update(key)
            else:
                keys.add(key)
        if self.mainSettings[MAIN.USE_KEY_PAIRS]:
            for key in tuple(keys):
                if key in KEY_ALIAS_CONTROL:
                    keys.update(KEY_ALIAS_CONTROL)
                elif key in KEY_ALIAS_ALT:
                    keys.update(KEY_ALIAS_ALT)
                elif key in KEY_ALIAS_SHIFT:
                    keys.update(KEY_ALIAS_SHIFT)
        self.usableKeys.update(keys)
        return tuple(keys)


g_keysListener = KeysListener()

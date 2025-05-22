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
        self.components.add(KeysData(self.normalizeKey(keyList) if keyList else frozenset(KEY_ALIAS_ALT), keyFunction))

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

    def handleKey(self, key, is_pressed):
        if is_pressed and (key not in self.usableKeys or key in self.pressedKeys) or not is_pressed and key not in self.pressedKeys:
            return
        for component in self.components:
            if key in component.keys:
                component.keyFunction(is_pressed)
        if is_pressed:
            self.pressedKeys.add(key)
        else:
            self.pressedKeys.discard(key)

    def onKeyUp(self, event):
        self.handleKey(event.key, False)

    def onKeyDown(self, event):
        self.handleKey(event.key, True)

    def normalizeKey(self, keyList):
        keys = {item for key in keyList for item in (key if isinstance(key, (list, set, tuple)) else [key])}

        if self.mainSettings[MAIN.USE_KEY_PAIRS]:
            alias_sets = (KEY_ALIAS_CONTROL, KEY_ALIAS_ALT, KEY_ALIAS_SHIFT)
            for alias_set in alias_sets:
                if any(key in alias_set for key in keys):
                    keys.update(alias_set)

        self.usableKeys.update(keys)
        return frozenset(keys)


g_keysListener = KeysListener()

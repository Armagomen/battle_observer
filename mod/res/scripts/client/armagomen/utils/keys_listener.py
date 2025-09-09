from collections import namedtuple

from armagomen._constants import MAIN
from gui import InputHandler
from Keys import KEY_LALT, KEY_LCONTROL, KEY_LSHIFT, KEY_RALT, KEY_RCONTROL, KEY_RSHIFT

KeysData = namedtuple("KeysData", ("keys", "keyFunction"))
KEY_ALIAS_CONTROL = (KEY_LCONTROL, KEY_RCONTROL)
KEY_ALIAS_ALT = (KEY_LALT, KEY_RALT)
KEY_ALIAS_SHIFT = (KEY_LSHIFT, KEY_RSHIFT)


class KeysListener(object):

    def __init__(self):
        self.components = set()
        self.pressedKeys = set()
        self.usableKeys = set()
        self.settings = None

    def init(self, settings):
        self.settings = settings.main

    def fini(self):
        self.clear()
        self.settings = None

    def registerComponent(self, keyFunction, keyList=None):
        self.components.add(KeysData(self.normalizeKey(keyList) if keyList else frozenset(KEY_ALIAS_ALT), keyFunction))

    def clear(self):
        self.components.clear()
        self.usableKeys.clear()
        self.pressedKeys.clear()

    def start(self):
        InputHandler.g_instance.onKeyDown += self.onKeyDown
        InputHandler.g_instance.onKeyUp += self.onKeyUp

    def stop(self):
        InputHandler.g_instance.onKeyDown -= self.onKeyDown
        InputHandler.g_instance.onKeyUp -= self.onKeyUp
        self.clear()

    def handleKey(self, key, is_pressed):
        if is_pressed and (key not in self.usableKeys or key in self.pressedKeys) or not is_pressed and key not in self.pressedKeys:
            return
        for component in self.components:
            if key in component.keys:
                component.keyFunction(is_pressed)
        self.pressedKeys.add(key) if is_pressed else self.pressedKeys.discard(key)

    def onKeyUp(self, event):
        self.handleKey(event.key, False)

    def onKeyDown(self, event):
        self.handleKey(event.key, True)

    def normalizeKey(self, keyList):
        keys = {item for key in keyList for item in (key if isinstance(key, (list, set, tuple)) else [key])}

        if self.settings and self.settings.get(MAIN.USE_KEY_PAIRS):
            for alias_set in (KEY_ALIAS_CONTROL, KEY_ALIAS_ALT, KEY_ALIAS_SHIFT):
                if any(key in alias_set for key in keys):
                    keys.update(alias_set)

        self.usableKeys.update(keys)
        return frozenset(keys)


g_keysListener = KeysListener()

from collections import namedtuple

from armagomen._constants import MAIN, MOD_NAME
from armagomen.battle_observer.settings import user
from debug_utils import LOG_CURRENT_EXCEPTION
from gui import InputHandler
from Keys import KEY_LALT, KEY_LCONTROL, KEY_LSHIFT, KEY_RALT, KEY_RCONTROL, KEY_RSHIFT
from PlayerEvents import g_playerEvents

KeysData = namedtuple("KeysData", ("keys", "keyFunction"))
KEY_ALIAS_CONTROL = (KEY_LCONTROL, KEY_RCONTROL)
KEY_ALIAS_ALT = (KEY_LALT, KEY_RALT)
KEY_ALIAS_SHIFT = (KEY_LSHIFT, KEY_RSHIFT)


class KeysListener(object):

    def __init__(self):
        self.keysMap = set()
        self.pressedKeys = set()
        self.usableKeys = set()
        g_playerEvents.onAvatarReady += self.onEnterBattlePage
        g_playerEvents.onAvatarBecomeNonPlayer += self.onExitBattlePage

    def registerComponent(self, keyFunction, keyList=None):
        self.keysMap.add(KeysData(self.normalizeKey(keyList) if keyList else KEY_ALIAS_ALT, keyFunction))

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
        if event.key not in self.pressedKeys:
            return
        for keysData in self.keysMap:
            if event.key in keysData.keys:
                try:
                    keysData.keyFunction(False)
                except Exception:
                    LOG_CURRENT_EXCEPTION(MOD_NAME)
        self.pressedKeys.discard(event.key)

    def onKeyDown(self, event):
        if event.key not in self.usableKeys or event.key in self.pressedKeys:
            return
        for keysData in self.keysMap:
            if event.key in keysData.keys:
                try:
                    keysData.keyFunction(True)
                except Exception:
                    LOG_CURRENT_EXCEPTION(MOD_NAME)
        self.pressedKeys.add(event.key)

    def normalizeKey(self, keyList):
        keys = set()
        for key in keyList:
            if isinstance(key, (list, set, tuple)):
                keys.update(key)
            else:
                keys.add(key)
        if user.main[MAIN.USE_KEY_PAIRS]:
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

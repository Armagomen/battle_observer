from collections import namedtuple

from armagomen._constants import MAIN
from armagomen.battle_observer.settings import IBOSettingsLoader
from gui import InputHandler
from helpers import dependency
from Keys import KEY_LALT, KEY_LCONTROL, KEY_LSHIFT, KEY_RALT, KEY_RCONTROL, KEY_RSHIFT
from skeletons.gui.app_loader import GuiGlobalSpaceID, IAppLoader

KeysData = namedtuple("KeysData", ("keys", "keyFunction"))
KEY_ALIAS_CONTROL = (KEY_LCONTROL, KEY_RCONTROL)
KEY_ALIAS_ALT = (KEY_LALT, KEY_RALT)
KEY_ALIAS_SHIFT = (KEY_LSHIFT, KEY_RSHIFT)


class KeysListener(object):
    appLoader = dependency.descriptor(IAppLoader)
    settingsLoader = dependency.descriptor(IBOSettingsLoader)

    def __init__(self):
        self.components = set()
        self.pressedKeys = set()
        self.usableKeys = set()
        self.__prevSpaceID = GuiGlobalSpaceID.LOBBY

    def init(self):
        self.appLoader.onGUISpaceEntered += self.subscribe
        self.appLoader.onGUISpaceLeft += self.unsubscribe

    def fini(self):
        self.appLoader.onGUISpaceEntered -= self.subscribe
        self.appLoader.onGUISpaceLeft -= self.unsubscribe
        self.clear()

    def registerComponent(self, keyFunction, keyList=None):
        self.components.add(KeysData(self.normalizeKey(keyList) if keyList else frozenset(KEY_ALIAS_ALT), keyFunction))

    def clear(self):
        self.components.clear()
        self.usableKeys.clear()
        self.pressedKeys.clear()

    def subscribe(self, spaceID):
        if spaceID == GuiGlobalSpaceID.LOBBY and self.__prevSpaceID in (GuiGlobalSpaceID.BATTLE, GuiGlobalSpaceID.BATTLE_LOADING):
            self.clear()
        self.__prevSpaceID = spaceID
        if spaceID == GuiGlobalSpaceID.BATTLE:
            InputHandler.g_instance.onKeyDown += self.onKeyDown
            InputHandler.g_instance.onKeyUp += self.onKeyUp

    def unsubscribe(self, spaceID):
        if spaceID == GuiGlobalSpaceID.BATTLE:
            InputHandler.g_instance.onKeyDown -= self.onKeyDown
            InputHandler.g_instance.onKeyUp -= self.onKeyUp

    def handleKey(self, key, is_pressed):
        if key not in self.usableKeys or is_pressed == key in self.pressedKeys:
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
        if self.settingsLoader.settings.main.get(MAIN.USE_KEY_PAIRS):
            for alias_set in (KEY_ALIAS_CONTROL, KEY_ALIAS_ALT, KEY_ALIAS_SHIFT):
                if any(key in alias_set for key in keys):
                    keys.update(alias_set)

        self.usableKeys.update(keys)
        return frozenset(keys)

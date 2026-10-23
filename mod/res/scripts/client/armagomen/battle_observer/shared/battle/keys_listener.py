# coding=utf-8
from collections import namedtuple

from armagomen._logger import IALogger
from armagomen.battle_observer.shared.interface import IBOKeysListener
from gui import InputHandler
from helpers import dependency
from Keys import KEY_LALT, KEY_LCONTROL, KEY_LSHIFT, KEY_RALT, KEY_RCONTROL, KEY_RSHIFT
from skeletons.gui.app_loader import GuiGlobalSpaceID, IAppLoader

KeysData = namedtuple("KeysData", ("keys", "keyFunction"))
KEY_ALIAS_CONTROL = (KEY_LCONTROL, KEY_RCONTROL)
KEY_ALIAS_ALT = (KEY_LALT, KEY_RALT)
KEY_ALIAS_SHIFT = (KEY_LSHIFT, KEY_RSHIFT)


class KeysListener(IBOKeysListener):
    appLoader = dependency.descriptor(IAppLoader)
    logger = dependency.descriptor(IALogger)

    def __init__(self):
        self.logger.logInfo("Initializing KeysListener")
        self.components = set()
        self.pressedKeys = set()
        self.usableKeys = set()
        self.__prevSpaceID = GuiGlobalSpaceID.LOBBY
        self.appLoader.onGUISpaceEntered += self.subscribe
        self.appLoader.onGUISpaceLeft += self.unsubscribe

    def fini(self):
        self.appLoader.onGUISpaceEntered -= self.subscribe
        self.appLoader.onGUISpaceLeft -= self.unsubscribe
        self.clear()
        self.logger.logInfo("Finished KeysListener")

    def registerComponent(self, keyFunction, keyList=KEY_ALIAS_ALT):
        component = KeysData(self.normalizeKey(keyList), keyFunction)
        self.logger.logInfo("KeysListener registerComponent: {}", component)
        self.components.add(component)

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

    def onKeyDown(self, event):
        self.handleKey(event.key, True)

    def onKeyUp(self, event):
        self.handleKey(event.key, False)

    def handleKey(self, key, is_key_down):
        if not self.components or key not in self.usableKeys or is_key_down == (key in self.pressedKeys):
            return
        if is_key_down:
            self.pressedKeys.add(key)
        for component in self.components:
            if any(key in key_set and key_set.issubset(self.pressedKeys) for key_set in component.keys):
                component.keyFunction(is_key_down)
        if not is_key_down:
            self.pressedKeys.discard(key)

    def normalizeKey(self, keyList):
        import itertools
        alias_groups = (KEY_ALIAS_CONTROL, KEY_ALIAS_ALT, KEY_ALIAS_SHIFT)

        if isinstance(keyList, (int, long)):
            options = [[keyList]]
        elif isinstance(keyList, (list, tuple, set)):
            if all(isinstance(x, (int, long)) for x in keyList):
                if len(keyList) > 1 and any(all(k in group for k in keyList) for group in alias_groups):
                    options = [[k] for k in keyList]
                else:
                    options = [list(keyList)]
            elif len(keyList) == 1 and isinstance(keyList[0], (list, tuple, set)):
                options = [[k] for k in keyList[0]]
            else:
                options = [list(keyList)]
        else:
            options = []

        get_pool = lambda key: next((group for group in alias_groups if key in group), (key,))
        normalized_sets = set()
        for opt in options:
            pools = []
            for item in opt:
                if isinstance(item, (int, long)):
                    pools.append(get_pool(item))
                elif isinstance(item, (list, tuple, set)):
                    sub_pool = set()
                    for k in item:
                        sub_pool.update(get_pool(k))
                    pools.append(tuple(sub_pool))
                else:
                    pools.append((item,))

            for combination in itertools.product(*pools):
                key_set = frozenset(combination)
                normalized_sets.add(key_set)
                self.usableKeys.update(key_set)

        return frozenset(normalized_sets)

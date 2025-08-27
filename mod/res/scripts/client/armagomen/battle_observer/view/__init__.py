from armagomen._constants import BATTLE_ALIASES, LOBBY_ALIASES
from armagomen.battle_observer.components.controllers import damage_controller
from armagomen.battle_observer.view.view_settings import ViewSettings
from armagomen.utils.common import addCallback
from armagomen.utils.keys_listener import g_keysListener
from armagomen.utils.logging import logDebug, logInfo
from frameworks.wulf import WindowLayer
from gui.app_loader.settings import APP_NAME_SPACE
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.framework.package_layout import PackageBusinessHandler
from gui.shared import EVENT_BUS_SCOPE

ATTRIBUTE_NAME = 'as_BattleObserverCreate'
INFO_MSG = "loading view {}: alias={}"
DEFAULT_INTERVAL = 0.1

DEF_IGNORED_PAGES = (VIEW_ALIAS.DEV_BATTLE_PAGE, VIEW_ALIAS.EVENT_BATTLE_PAGE)


class TryLoadHandler(PackageBusinessHandler):

    def __init__(self, *args, **kwargs):
        super(TryLoadHandler, self).__init__(*args, **kwargs)
        self.__counter = 0

    def try_load(self):
        self.__counter += 1
        return self.__counter < 60


class ViewHandlerBattle(TryLoadHandler, ViewSettings):

    def __init__(self):
        BATTLE_PAGES = set(VIEW_ALIAS.BATTLE_PAGES + (VIEW_ALIAS.STRONGHOLD_BATTLE_PAGE, VIEW_ALIAS.EPIC_RANDOM_PAGE))
        listeners = tuple((alias, self.eventListener) for alias in BATTLE_PAGES.difference(DEF_IGNORED_PAGES))
        super(ViewHandlerBattle, self).__init__(listeners, appNS=APP_NAME_SPACE.SF_BATTLE, scope=EVENT_BUS_SCOPE.BATTLE)
        self.enable_controller = False

    def init(self):
        super(ViewHandlerBattle, self).init()
        self._invalidateComponents()
        self.enable_controller = bool({BATTLE_ALIASES.MAIN_GUN, BATTLE_ALIASES.PANELS}.intersection(self._components))
        if self.enable_controller:
            damage_controller.start()
        g_keysListener.start()

    def fini(self):
        self._clear()
        g_keysListener.stop()
        if self.enable_controller:
            damage_controller.stop()
        super(ViewHandlerBattle, self).fini()

    def eventListener(self, event):
        logDebug("{}:eventListener {}", self.__class__.__name__, repr(event))
        if self._components:
            self._registerViewComponents()
            addCallback(DEFAULT_INTERVAL, self._loadView, event.alias)

    def _loadView(self, alias):
        if not self.try_load():
            return
        page = self.findViewByAlias(WindowLayer.VIEW, alias)
        if page and hasattr(page.flashObject, ATTRIBUTE_NAME):
            logInfo(INFO_MSG, self.__class__.__name__, alias)
            page._blToggling.update(self._components)
            page.flashObject.as_BattleObserverCreate(self._components)
        else:
            logDebug("{}:_loadView - {} not found in {} or view is None", self.__class__.__name__, ATTRIBUTE_NAME, alias)
            addCallback(DEFAULT_INTERVAL, self._loadView, alias)


class ViewHandlerLobby(TryLoadHandler):

    def __init__(self):
        listeners = ((VIEW_ALIAS.LOBBY, self.eventListener),)
        super(ViewHandlerLobby, self).__init__(listeners, appNS=APP_NAME_SPACE.SF_LOBBY, scope=EVENT_BUS_SCOPE.LOBBY)

    def eventListener(self, event):
        logDebug("{}:eventListener {}", self.__class__.__name__, repr(event))
        addCallback(DEFAULT_INTERVAL, self._loadView, event.alias)

    def _loadView(self, alias):
        if not self.try_load():
            return
        hangar = self.findViewByAlias(WindowLayer.VIEW, alias)
        if hangar and hasattr(hangar.flashObject, ATTRIBUTE_NAME):
            logInfo(INFO_MSG, self.__class__.__name__, alias)
            hangar.flashObject.as_BattleObserverCreate(LOBBY_ALIASES)
        else:
            logDebug("{}:_loadView - {} not found in {} or view is None", self.__class__.__name__, ATTRIBUTE_NAME, alias)
            addCallback(DEFAULT_INTERVAL, self._loadView, alias)

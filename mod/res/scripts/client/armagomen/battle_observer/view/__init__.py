from armagomen._constants import BATTLE_ALIASES, LOBBY_ALIASES
from armagomen.battle_observer.components.controllers import damage_controller
from armagomen.battle_observer.view.view_settings import ViewSettings
from armagomen.utils.common import addCallback, IS_XVM_INSTALLED
from armagomen.utils.keys_listener import g_keysListener
from armagomen.utils.logging import logDebug, logError
from frameworks.wulf import WindowLayer
from gui.app_loader.settings import APP_NAME_SPACE
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.framework.package_layout import PackageBusinessHandler
from gui.shared import EVENT_BUS_SCOPE

ATTRIBUTE_NAME = 'as_BattleObserverCreate'
INFO_MSG = "loading view {}: alias={}"
DEFAULT_INTERVAL = 0.2

DEF_IGNORED_PAGES = (VIEW_ALIAS.DEV_BATTLE_PAGE, VIEW_ALIAS.EVENT_BATTLE_PAGE)


class ViewHandlerBattle(PackageBusinessHandler, ViewSettings):

    def __init__(self):
        BATTLE_PAGES = set(VIEW_ALIAS.BATTLE_PAGES + (VIEW_ALIAS.STRONGHOLD_BATTLE_PAGE, VIEW_ALIAS.EPIC_RANDOM_PAGE))
        listeners = tuple((alias, self.eventListener) for alias in BATTLE_PAGES.difference(DEF_IGNORED_PAGES))
        super(ViewHandlerBattle, self).__init__(listeners, APP_NAME_SPACE.SF_BATTLE, EVENT_BUS_SCOPE.BATTLE)
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
        logDebug("ViewHandlerBattle:eventListener {}", event.name)
        if self._components:
            self._registerViewComponents()
            addCallback(DEFAULT_INTERVAL, self._loadView, event.name)

    def _loadView(self, name):
        page = self.findViewByName(WindowLayer.VIEW, name)
        if page and hasattr(page.flashObject, ATTRIBUTE_NAME):
            logDebug("ViewHandlerBattle:_loadView {}", ATTRIBUTE_NAME)
            page._blToggling.update(self._components)
            page.flashObject.as_BattleObserverCreate(self._components)
        else:
            addCallback(DEFAULT_INTERVAL, self._loadView, name)


class ViewHandlerLobby(PackageBusinessHandler):

    def __init__(self):
        self.__subscribed = False
        listeners = ((VIEW_ALIAS.LOBBY_HANGAR, self.eventListener),)
        super(ViewHandlerLobby, self).__init__(listeners, APP_NAME_SPACE.SF_LOBBY, EVENT_BUS_SCOPE.LOBBY)

    def eventListener(self, event):
        if self.__subscribed:
            return
        self._app.loaderManager.onViewLoaded += self.__onViewLoaded
        self.__subscribed = True

    def __onViewLoaded(self, pyView, *args):
        alias = pyView.getAlias()
        if alias == VIEW_ALIAS.LOBBY_HANGAR:
            logDebug(INFO_MSG, self.__class__.__name__, alias)
            if hasattr(pyView.flashObject, ATTRIBUTE_NAME):
                addCallback(2.0 if IS_XVM_INSTALLED else DEFAULT_INTERVAL, pyView.flashObject.as_BattleObserverCreate, LOBBY_ALIASES)
                addCallback(2.0 if IS_XVM_INSTALLED else DEFAULT_INTERVAL, pyView.flashObject.as_BattleObserverShadow)
            else:
                logError("{}:flashObject, has ho attribute {}", alias, ATTRIBUTE_NAME)

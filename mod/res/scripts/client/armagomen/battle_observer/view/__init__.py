from armagomen._constants import BATTLE_ALIASES, LOBBY_ALIASES
from armagomen.battle_observer.components.controllers import cachedVehicleData, damage_controller
from armagomen.battle_observer.view.view_settings import ViewSettings
from armagomen.utils.common import addCallback
from armagomen.utils.events import g_events
from armagomen.utils.keys_listener import g_keysListener
from armagomen.utils.logging import logDebug
from frameworks.wulf import WindowLayer
from gui.app_loader.settings import APP_NAME_SPACE
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.framework.package_layout import PackageBusinessHandler
from gui.shared import EVENT_BUS_SCOPE

ATTRIBUTE_NAME = 'as_BattleObserverCreate'
DEFAULT_INTERVAL = 0.1
DEF_IGNORED_PAGES = (VIEW_ALIAS.DEV_BATTLE_PAGE, VIEW_ALIAS.EVENT_BATTLE_PAGE)


class TryLoadHandler(PackageBusinessHandler):

    def __init__(self, *args, **kwargs):
        super(TryLoadHandler, self).__init__(*args, **kwargs)
        self.__counter = 0

    def __try_load(self):
        self.__counter += 1
        return self.__counter < 60

    def _getView(self, alias, callback):
        if not self.__try_load():
            return
        view = self.findViewByAlias(WindowLayer.VIEW, alias)
        if view and hasattr(view.flashObject, ATTRIBUTE_NAME):
            callback(view)
        else:
            logDebug("_getView: {} not found in {} or view is None", ATTRIBUTE_NAME, repr(view))
            addCallback(DEFAULT_INTERVAL, self._getView, alias, callback)


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
        if self._components:
            self._registerViewComponents()
            self._getView(event.alias, self.onViewFounded)

    def onViewFounded(self, view):
        view._blToggling.update(self._components)
        view.flashObject.as_BattleObserverCreate(self._components)


class ViewHandlerLobby(TryLoadHandler):

    def __init__(self):
        listeners = ((VIEW_ALIAS.LOBBY, self.eventListener),)
        super(ViewHandlerLobby, self).__init__(listeners, appNS=APP_NAME_SPACE.SF_LOBBY, scope=EVENT_BUS_SCOPE.LOBBY)

    def init(self):
        super(ViewHandlerLobby, self).init()
        cachedVehicleData.subscribe()
        g_events.subscribe()

    def fini(self):
        super(ViewHandlerLobby, self).fini()
        cachedVehicleData.unsubscribe()
        g_events.unsubscribe()

    def eventListener(self, event):
        self._getView(event.alias, self.onViewFounded)

    @staticmethod
    def onViewFounded(view):
        view.flashObject.as_BattleObserverCreate(list(LOBBY_ALIASES))

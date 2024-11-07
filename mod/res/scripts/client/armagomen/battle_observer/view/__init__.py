import constants
from armagomen._constants import BATTLE_PAGES, LOBBY_ALIASES
from armagomen.battle_observer.components.controllers import damage_controller
from armagomen.battle_observer.components.minimap_plugins import MinimapZoomPlugin
from armagomen.battle_observer.components.statistics.statistic_data_loader import StatisticsDataLoader
from armagomen.battle_observer.view.view_settings import ViewSettings
from armagomen.utils.common import callback, xvmInstalled
from armagomen.utils.logging import logDebug, logError
from gui.app_loader.settings import APP_NAME_SPACE
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.framework.package_layout import PackageBusinessHandler
from gui.shared import EVENT_BUS_SCOPE

ATTRIBUTE_NAME = 'as_BattleObserverCreate'
DEBUG_MSG = "app.loaderManager.onViewLoaded: {}, alias={}"
INFO_MSG = "loading view {}: alias={}"


class ViewHandlerBattle(PackageBusinessHandler, ViewSettings):

    def __init__(self):
        listeners = tuple((alias, self.eventListener) for alias in BATTLE_PAGES)
        self.__subscribed = False
        self._icons = False
        self._minimap = None
        self._statistics = None
        super(ViewHandlerBattle, self).__init__(listeners, APP_NAME_SPACE.SF_BATTLE, EVENT_BUS_SCOPE.BATTLE)

    def init(self):
        super(ViewHandlerBattle, self).init()
        self.setComponents()
        damage_controller.start()

    def fini(self):
        if self._minimap is not None:
            self._minimap.fini()
            self._minimap = None
        self._statistics = None
        self._clear()
        damage_controller.stop()
        super(ViewHandlerBattle, self).fini()

    def eventListener(self, event):
        if self.__subscribed:
            return
        self._app.loaderManager.onViewLoaded += self.__onViewLoaded
        self.__subscribed = True
        if self.isWTREnabled():
            self._statistics = StatisticsDataLoader()
        self._icons = self.isIconsEnabled()
        if self.isMinimapEnabled():
            self._minimap = MinimapZoomPlugin()
        if any(self._components or self._statistics or self._icons or self._minimap):
            if self._components:
                self.registerComponents()

    def __onViewLoaded(self, pyView, *args):
        alias = pyView.getAlias()
        if alias not in BATTLE_PAGES:
            return
        self._app.loaderManager.onViewLoaded -= self.__onViewLoaded
        logDebug(INFO_MSG, self.__class__.__name__, alias)
        if not hasattr(pyView.flashObject, ATTRIBUTE_NAME):
            to_format_str = "{}:flashObject, has ho attribute {}"
            return logError(to_format_str, alias, ATTRIBUTE_NAME)
        pyView._blToggling.update(self._components)
        callback(2.0 if xvmInstalled else 0, self._loadView, pyView.flashObject)

    def _loadView(self, flashObject):
        flashObject.as_BattleObserverCreate(self._components)
        flashObject.as_BattleObserverHideWg(self._hiddenComponents)
        if self._minimap is not None:
            self._minimap.init(flashObject)
        if self._icons or self._statistics is not None:
            flashObject.as_BattleObserverCreateStatistic(self._icons, *self.getStatisticsSettings())
            if self._statistics is not None:
                if not self._statistics.enabled:
                    self._statistics.regionError()
                else:
                    self._statistics.setFeedback(flashObject.as_BattleObserverUpdateStatisticData)
                    self._statistics.getStatisticsDataFromServer()
        arena = self.sessionProvider.arenaVisitor.getArenaSubscription()
        if arena is None:
            return logError("_loadView: arena is None")

        def onPeriodChange(period, *args):
            if period != constants.ARENA_PERIOD.AFTERBATTLE:
                flashObject.as_BattleObserverUpdateLogsPosition()

        arena.onPeriodChange += onPeriodChange


class ViewHandlerLobby(PackageBusinessHandler):
    __slots__ = ('__subscribed', '_listeners', '_scope', '_app', '_appNS',)

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
        is_hangar = alias == VIEW_ALIAS.LOBBY_HANGAR
        if is_hangar:
            logDebug(INFO_MSG, self.__class__.__name__, alias)
            if not hasattr(pyView.flashObject, ATTRIBUTE_NAME):
                return logError("{}:flashObject, has ho attribute {}", alias, ATTRIBUTE_NAME)
            callback(2.0 if xvmInstalled else 0, pyView.flashObject.as_BattleObserverCreate, LOBBY_ALIASES)

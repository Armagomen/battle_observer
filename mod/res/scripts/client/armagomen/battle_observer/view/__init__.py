from armagomen._constants import BATTLE_PAGES, CURRENT_REALM, LOBBY_ALIASES
from armagomen.battle_observer.components.controllers.players_damage_controller import damage_controller
from armagomen.battle_observer.components.minimap_plugins import MinimapZoomPlugin
from armagomen.battle_observer.components.statistics.statistic_data_loader import StatisticsDataLoader
from armagomen.battle_observer.view.view_settings import ViewSettings
from armagomen.utils.common import callback, logDebug, logError, logInfo, xvmInstalled
from gui.app_loader.settings import APP_NAME_SPACE
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.framework.package_layout import PackageBusinessHandler
from gui.shared import EVENT_BUS_SCOPE

ATTRIBUTE_NAME = 'as_BattleObserverCreate'
DEBUG_MSG = "{}/__onViewLoaded: alias={}"
INFO_MSG = "{}: alias={}"


class ObserverViewHandlerBattle(PackageBusinessHandler, ViewSettings):

    def __init__(self):
        listeners = tuple((alias, self.eventListener) for alias in BATTLE_PAGES) if CURRENT_REALM != "RU" else tuple()
        super(ObserverViewHandlerBattle, self).__init__(listeners, APP_NAME_SPACE.SF_BATTLE, EVENT_BUS_SCOPE.BATTLE)
        self._minimap = None
        self._statistics = None
        self._icons = False

    def init(self):
        super(ObserverViewHandlerBattle, self).init()
        self.setComponents()
        damage_controller.start()

    def fini(self):
        if self._minimap is not None:
            self._minimap.fini()
            self._minimap = None
        self._statistics = None
        self._clear()
        damage_controller.stop()
        super(ObserverViewHandlerBattle, self).fini()

    def eventListener(self, event):
        if self.isWTREnabled():
            self._statistics = StatisticsDataLoader()
        self._icons = self.isIconsEnabled()
        if self.isMinimapEnabled():
            self._minimap = MinimapZoomPlugin()
        if self._components or self._statistics is not None or self._icons or self._minimap is not None:
            self._app.loaderManager.onViewLoaded += self.__onViewLoaded
            self.registerComponents()

    def __onViewLoaded(self, pyView, *args):
        alias = pyView.getAlias()
        logDebug(DEBUG_MSG, self.__class__.__name__, alias)
        if alias not in BATTLE_PAGES:
            return
        self._app.loaderManager.onViewLoaded -= self.__onViewLoaded
        logInfo(INFO_MSG.format(self.__class__.__name__, alias))
        if not hasattr(pyView.flashObject, ATTRIBUTE_NAME):
            to_format_str = "{}:flashObject, has ho attribute {}"
            return logError(to_format_str, alias, ATTRIBUTE_NAME)
        pyView._blToggling.update(self._components)
        callback(2.0 if xvmInstalled else 0, self._loadView, pyView.flashObject)
        callback(40.0, pyView.flashObject.as_BattleObserverUpdateDamageLogPosition)

    def _loadView(self, flashObject):
        flashObject.as_BattleObserverCreate(self._components, CURRENT_REALM)
        flashObject.as_BattleObserverHideWg(self._hiddenComponents, CURRENT_REALM)
        if self._minimap is not None:
            self._minimap.init(flashObject)
        if self._icons or self._statistics is not None:
            flashObject.as_BattleObserverCreateStatistic(self._icons, *self.getStatisticsSettings())
            if self._statistics is not None:
                self._statistics.setCallback(flashObject.as_BattleObserverUpdateStatisticData)
                self._statistics.getStatisticsDataFromServer()


class ObserverViewHandlerLobby(PackageBusinessHandler):
    __slots__ = ('_listeners', '_scope', '_app', '_appNS',)

    def __init__(self):
        listeners = ((VIEW_ALIAS.LOBBY_HANGAR, self.eventListener),) if CURRENT_REALM != "RU" else tuple()
        super(ObserverViewHandlerLobby, self).__init__(listeners, APP_NAME_SPACE.SF_LOBBY, EVENT_BUS_SCOPE.LOBBY)

    def eventListener(self, event):
        self._app.loaderManager.onViewLoaded += self.__onViewLoaded

    def __onViewLoaded(self, pyView, *args):
        alias = pyView.getAlias()
        logDebug(DEBUG_MSG, self.__class__.__name__, alias)
        if alias != VIEW_ALIAS.LOBBY_HANGAR:
            return
        self._app.loaderManager.onViewLoaded -= self.__onViewLoaded
        logInfo(INFO_MSG.format(self.__class__.__name__, alias))
        if not hasattr(pyView.flashObject, ATTRIBUTE_NAME):
            return logError("{}:flashObject, has ho attribute {}", alias, ATTRIBUTE_NAME)
        callback(2.0 if xvmInstalled else 0, pyView.flashObject.as_BattleObserverCreate, LOBBY_ALIASES)

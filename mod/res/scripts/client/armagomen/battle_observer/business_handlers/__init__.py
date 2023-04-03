from armagomen.battle_observer.components.controllers.players_damage_controller import damage_controller
from armagomen.battle_observer.components.minimap_plugins import MinimapZoomPlugin
from armagomen.battle_observer.components.statistics.statistic_data_loader import StatisticsDataLoader
from armagomen.battle_observer.core import viewSettings
from armagomen.constants import SWF, CURRENT_REALM, LOBBY_ALIASES
from armagomen.utils.common import logError, logInfo, logDebug, callback, xvmInstalled
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.framework.package_layout import PackageBusinessHandler
from gui.app_loader.settings import APP_NAME_SPACE
from gui.shared import EVENT_BUS_SCOPE


class ObserverBusinessHandlerBattle(PackageBusinessHandler):
    __slots__ = ('__icons', '_minimapPlugin', '_statistics')

    def __init__(self):
        aliases = (
            VIEW_ALIAS.CLASSIC_BATTLE_PAGE, VIEW_ALIAS.COMP7_BATTLE_PAGE, VIEW_ALIAS.EPIC_BATTLE_PAGE,
            VIEW_ALIAS.EPIC_RANDOM_PAGE, VIEW_ALIAS.RANKED_BATTLE_PAGE, VIEW_ALIAS.STRONGHOLD_BATTLE_PAGE,
        ) if CURRENT_REALM != "RU" else tuple()
        listeners = tuple((alias, self.eventListener) for alias in aliases)
        super(ObserverBusinessHandlerBattle, self).__init__(listeners, APP_NAME_SPACE.SF_BATTLE, EVENT_BUS_SCOPE.BATTLE)
        self._minimapPlugin = None
        self._statistics = None
        self.__icons = False

    def init(self):
        super(ObserverBusinessHandlerBattle, self).init()
        damage_controller.start()

    def fini(self):
        if self._minimapPlugin is not None:
            self._minimapPlugin.fini()
            self._minimapPlugin = None
        self._statistics = None
        viewSettings.clear()
        damage_controller.stop()
        super(ObserverBusinessHandlerBattle, self).fini()

    def eventListener(self, event):
        self._app.loaderManager.onViewLoaded += self.__onViewLoaded
        if viewSettings.isWTREnabled():
            self._statistics = StatisticsDataLoader()
        self.__icons = viewSettings.isIconsEnabled()
        if viewSettings.isMinimapEnabled():
            self._minimapPlugin = MinimapZoomPlugin()
        components = viewSettings.setComponents()
        if components or self._statistics is not None or self.__icons or self._minimapPlugin is not None:
            self._app.as_loadLibrariesS([SWF.BATTLE])
            logInfo("{}: loading libraries swf={}, alias={}".format(self.__class__.__name__, SWF.BATTLE, event.alias))

    def __onViewLoaded(self, pyView, *args):
        alias = pyView.getAlias()
        logDebug("ObserverBusinessHandler/onViewLoaded: {}", alias)
        self._app.loaderManager.onViewLoaded -= self.__onViewLoaded
        if not hasattr(pyView.flashObject, SWF.ATTRIBUTE_NAME):
            to_format_str = "{}:flashObject, has ho attribute {}"
            return logError(to_format_str, alias, SWF.ATTRIBUTE_NAME)
        callback(2.0 if xvmInstalled else 0, self._loadView, pyView)
        callback(40.0, pyView.flashObject.as_BattleObserverUpdateDamageLogPosition)

    def _loadView(self, pyView):
        pyView._blToggling.update(viewSettings.components)
        pyView.flashObject.as_BattleObserverCreate(viewSettings.components, CURRENT_REALM)
        pyView.flashObject.as_BattleObserverHideWg(viewSettings.hiddenComponents, CURRENT_REALM)
        if self._minimapPlugin is not None:
            self._minimapPlugin.init(pyView.flashObject)
        if self.__icons or self._statistics is not None:
            pyView.flashObject.as_BattleObserverCreateStatistic(self.__icons, *viewSettings.getStatisticsSettings())
            if self._statistics is not None:
                self._statistics.setCallback(pyView.flashObject.as_BattleObserverUpdateStatisticData)
                self._statistics.getStatisticsDataFromServer()


class ObserverBusinessHandlerLobby(PackageBusinessHandler):
    __slots__ = ('_listeners', '_scope', '_app', '_appNS',)

    def __init__(self):
        listeners = ((VIEW_ALIAS.LOBBY_HANGAR, self.eventListener),) if CURRENT_REALM != "RU" else tuple()
        super(ObserverBusinessHandlerLobby, self).__init__(listeners, APP_NAME_SPACE.SF_LOBBY, EVENT_BUS_SCOPE.LOBBY)

    def eventListener(self, event):
        self._app.loaderManager.onViewLoaded += self.__onViewLoaded
        self._app.as_loadLibrariesS([SWF.LOBBY])
        logInfo("{}: loading libraries swf={}, alias={}".format(self.__class__.__name__, SWF.LOBBY, event.alias))

    def __onViewLoaded(self, pyView, *args):
        if pyView.getAlias() != VIEW_ALIAS.LOBBY_HANGAR:
            return
        self._app.loaderManager.onViewLoaded -= self.__onViewLoaded
        if not hasattr(pyView.flashObject, SWF.ATTRIBUTE_NAME):
            return logError("{}:flashObject, has ho attribute {}", pyView.getAlias(), SWF.ATTRIBUTE_NAME)
        callback(2.0 if xvmInstalled else 0, pyView.flashObject.as_BattleObserverCreate, LOBBY_ALIASES)

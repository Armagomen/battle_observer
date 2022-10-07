from importlib import import_module

from armagomen.battle_observer.components.statistics.statistic_data_loader import StatisticsDataLoader
from armagomen.battle_observer.core import viewSettings
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import SWF, MAIN, STATISTICS, VEHICLE_TYPES, ALIASES, ALIAS_TO_PATH, MOD_NAME
from armagomen.utils.common import logError, logInfo, logDebug, callback
from armagomen.utils.events import g_events
from debug_utils import LOG_CURRENT_EXCEPTION
from gui.Scaleform.framework import ComponentSettings, ScopeTemplates
from gui.Scaleform.framework.package_layout import PackageBusinessHandler
from gui.app_loader.settings import APP_NAME_SPACE
from gui.shared import EVENT_BUS_SCOPE

__all__ = ()


def getViewSettings():
    view_settings = []
    for alias in ALIASES:
        try:
            file_path, class_name = ALIAS_TO_PATH[alias]
            module_class = getattr(import_module(file_path, package=__package__), class_name)
            view_settings.append(ComponentSettings(alias, module_class, ScopeTemplates.DEFAULT_SCOPE))
        except Exception as err:
            viewSettings.removeComponent(alias)
            logError("{}, {}, {}", __package__, alias, repr(err))
            LOG_CURRENT_EXCEPTION(tags=[MOD_NAME])
    logDebug("{}.getViewSettings: {}", __package__, view_settings)
    return tuple(view_settings)


def getBusinessHandlers():
    return ObserverBusinessHandlerBattle(),


def getContextMenuHandlers():
    return ()


class ObserverBusinessHandlerBattle(PackageBusinessHandler):
    __slots__ = ('_iconsEnabled', '_statLoadTry', '_statisticsEnabled', 'minimapPlugin', 'statistics', 'viewAliases')

    def __init__(self):
        from armagomen.battle_observer.components.minimap_plugins import MinimapZoomPlugin
        self.viewAliases = viewSettings.getViewAliases()
        listeners = [(alias, self.eventListener) for alias in self.viewAliases]
        super(ObserverBusinessHandlerBattle, self).__init__(listeners, APP_NAME_SPACE.SF_BATTLE, EVENT_BUS_SCOPE.BATTLE)
        self.minimapPlugin = MinimapZoomPlugin()
        self.statistics = None
        self._iconsEnabled = viewSettings.isIconsEnabled()
        self._statLoadTry = 0
        self._statisticsEnabled = False

    def init(self):
        super(ObserverBusinessHandlerBattle, self).init()
        if viewSettings.isWTREnabled():
            self.statistics = StatisticsDataLoader()
            self._statisticsEnabled = self.statistics.enabled

    def fini(self):
        self.minimapPlugin.fini()
        self.minimapPlugin = None
        self._statLoadTry = 0
        super(ObserverBusinessHandlerBattle, self).fini()

    def eventListener(self, event):
        if viewSettings.settingsAdded:
            self._app.as_loadLibrariesS([SWF.BATTLE])
            self._app.loaderManager.onViewLoaded += self.onViewLoaded
            logInfo("{}: loading libraries swf={}, alias={}".format(self.__class__.__name__, SWF.BATTLE, event.alias))

    def loadStatisticView(self, view):
        if self._statisticsEnabled:
            if not self.statistics.loaded and self._statLoadTry < 20:
                self._statLoadTry += 1
                return callback(0.5, self.loadStatisticView, view)
        statisticsItemsData = self.statistics.itemsWTRData if self._statisticsEnabled else {}
        cutWidth = settings.statistics[STATISTICS.PANELS_CUT_WIDTH]
        fullWidth = settings.statistics[STATISTICS.PANELS_FULL_WIDTH]
        typeColors = settings.vehicle_types[VEHICLE_TYPES.CLASS_COLORS]
        iconMultiplier = settings.statistics[STATISTICS.ICON_BLACKOUT]
        view.flashObject.as_createStatisticComponent(self._statisticsEnabled, self._iconsEnabled, statisticsItemsData,
                                                     cutWidth, fullWidth, typeColors, iconMultiplier)

    def onViewLoaded(self, view, *args):
        logDebug("ObserverBusinessHandler/onViewLoaded: {}", view.settings.alias)
        if view.settings is None or view.settings.alias not in self.viewAliases:
            return
        self._app.loaderManager.onViewLoaded -= self.onViewLoaded
        g_events.onBattlePageLoaded(view)
        if not hasattr(view.flashObject, SWF.ATTRIBUTE_NAME):
            to_format_str = "battle_page {}, has ho attribute {}"
            return logError(to_format_str, repr(view.flashObject), SWF.ATTRIBUTE_NAME)
        view.flashObject.as_observerCreateComponents(viewSettings.getComponents())
        view.flashObject.as_observerUpdatePrebattleTimer(settings.main[MAIN.REMOVE_SHADOW_IN_PREBATTLE])
        view.flashObject.as_observerHideWgComponents(viewSettings.getHiddenWGComponents())
        if self.minimapPlugin.enabled:
            self.minimapPlugin.init(view)
        if self._iconsEnabled or self._statisticsEnabled:
            self.loadStatisticView(view)

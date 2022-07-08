from collections import namedtuple
from importlib import import_module

from armagomen.battle_observer.components.minimap_plugins import MinimapZoomPlugin
from armagomen.battle_observer.components.statistics.statistic_data_loader import StatisticsDataLoader
from armagomen.battle_observer.components.statistics.wtr_data import WTRStatistics
from armagomen.battle_observer.core import view_settings
from armagomen.constants import SWF, ALIAS_TO_PATH, MAIN, STATISTICS, VEHICLE_TYPES
from armagomen.utils.common import logError, logWarning, logInfo
from armagomen.utils.events import g_events
from gui.Scaleform.framework import ComponentSettings, ScopeTemplates
from gui.Scaleform.framework.package_layout import PackageBusinessHandler, _addListener, _removeListener
from gui.app_loader.settings import APP_NAME_SPACE
from gui.shared import EVENT_BUS_SCOPE
from gui.shared.events import AppLifeCycleEvent
from helpers.func_utils import callback

Statistics = namedtuple('Statistics', ('wtr', 'icons', 'dataLoader', 'wtrData'))


def getViewSettings():
    settings = []
    isAllowed, aliases = view_settings.setIsAllowed()
    if isAllowed and aliases:
        for alias in aliases:
            try:
                file_path, class_name = ALIAS_TO_PATH[alias]
                module_class = getattr(import_module(file_path, package=__package__), class_name)
                settings.append(ComponentSettings(alias, module_class, ScopeTemplates.DEFAULT_SCOPE))
            except Exception as err:
                view_settings.removeComponent(alias)
                logWarning("{}, {}, {}".format(__package__, alias, repr(err)))
    return settings


def getBusinessHandlers():
    return ObserverBusinessHandler(),


def getContextMenuHandlers():
    return ()


class ObserverBusinessHandler(PackageBusinessHandler):
    __slots__ = ('_viewAliases', '_listeners', '_scope', '_app', '_appNS', 'minimapPlugin', '_arenaDP',
                 '_statLoadTry', 'statistics')

    def __init__(self):
        self._viewAliases = view_settings.getViewAliases()
        self._arenaDP = None
        self.minimapPlugin = MinimapZoomPlugin()
        self._statLoadTry = 0
        self.statistics = Statistics(view_settings.isWTREnabled(), view_settings.isIconsEnabled(),
                                     StatisticsDataLoader(), WTRStatistics())
        listeners = [(alias, self.eventListener) for alias in self._viewAliases]
        super(ObserverBusinessHandler, self).__init__(listeners, APP_NAME_SPACE.SF_BATTLE, EVENT_BUS_SCOPE.BATTLE)

    def init(self):
        super(ObserverBusinessHandler, self).init()
        self._arenaDP = view_settings.sessionProvider.getArenaDP()
        _addListener(AppLifeCycleEvent.INITIALIZING, self.onAppInitializing, EVENT_BUS_SCOPE.GLOBAL)

    def fini(self):
        _removeListener(AppLifeCycleEvent.INITIALIZING, self.onAppInitializing, EVENT_BUS_SCOPE.GLOBAL)
        self.minimapPlugin.fini()
        self.minimapPlugin = None
        self._arenaDP = None
        self._statLoadTry = 0
        super(ObserverBusinessHandler, self).fini()

    def eventListener(self, event):
        if view_settings.isAllowed:
            self._app.loaderManager.onViewLoaded += self.onViewLoaded

    def onAppInitializing(self, event):
        if event.ns == APP_NAME_SPACE.SF_BATTLE and view_settings.isAllowed:
            if self.statistics.wtr:
                self.statistics.dataLoader.setCachedStatisticData(self._arenaDP)
            self._app.as_loadLibrariesS([SWF.BATTLE])
            logInfo("loading flash libraries swf={}, appNS={}".format(SWF.BATTLE, event.ns))

    def loadStatisticView(self, view):
        if self.statistics.wtr and self.statistics.dataLoader.enabled:
            if not self.statistics.dataLoader.loaded and self._statLoadTry < 20:
                self._statLoadTry += 1
                return callback(0.5, self, "loadStatisticView", view)
            wtrData = self.statistics.wtrData.updateAllItems(self._arenaDP, self.statistics.dataLoader)
        else:
            wtrData = {}
        cutWidth = view_settings.cfg.statistics[STATISTICS.PANELS_CUT_WIDTH]
        fullWidth = view_settings.cfg.statistics[STATISTICS.PANELS_FULL_WIDTH]
        typeColors = view_settings.cfg.vehicle_types[VEHICLE_TYPES.CLASS_COLORS]
        iconMultiplier = view_settings.cfg.statistics[STATISTICS.ICON_BLACKOUT]
        view.flashObject.as_createStatisticComponent(self.statistics.wtr, self.statistics.icons, wtrData,
                                                     cutWidth, fullWidth, typeColors, iconMultiplier)

    def onViewLoaded(self, view, *args):
        if view.settings is None or view.settings.alias not in self._viewAliases:
            return
        self._app.loaderManager.onViewLoaded -= self.onViewLoaded
        g_events.onBattlePageLoaded(view)
        if not hasattr(view.flashObject, SWF.ATTRIBUTE_NAME):
            to_format_str = "battle_page {}, has ho attribute {}"
            return logError(to_format_str.format(repr(view.flashObject), SWF.ATTRIBUTE_NAME))
        view.flashObject.as_observerCreateComponents(view_settings.getComponents())
        view.flashObject.as_observerUpdatePrebattleTimer(view_settings.cfg.main[MAIN.REMOVE_SHADOW_IN_PREBATTLE])
        view.flashObject.as_observerHideWgComponents(view_settings.getHiddenWGComponents())
        if self.minimapPlugin.enabled:
            self.minimapPlugin.init(view)
        if self.statistics.icons or self.statistics.wtr:
            self.loadStatisticView(view)

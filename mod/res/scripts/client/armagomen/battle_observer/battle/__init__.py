from importlib import import_module

from armagomen.battle_observer.components.minimap_plugins import MinimapZoomPlugin
from armagomen.battle_observer.components.statistics.statistic_data_loader import StatisticsDataLoader
from armagomen.battle_observer.core import _view_settings
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import SWF, ALIAS_TO_PATH, MAIN, STATISTICS, VEHICLE_TYPES, MOD_NAME
from armagomen.utils.common import logError, logWarning, logInfo, logDebug, callback
from armagomen.utils.events import g_events
from debug_utils import LOG_CURRENT_EXCEPTION
from gui.Scaleform.framework import ComponentSettings, ScopeTemplates
from gui.Scaleform.framework.package_layout import PackageBusinessHandler
from gui.app_loader.settings import APP_NAME_SPACE
from gui.shared import EVENT_BUS_SCOPE


def getViewSettings():
    viewSettings = []
    for alias in _view_settings.setComponents():
        try:
            file_path, class_name = ALIAS_TO_PATH[alias]
            module_class = getattr(import_module(file_path, package=__package__), class_name)
            viewSettings.append(ComponentSettings(alias, module_class, ScopeTemplates.DEFAULT_SCOPE))
        except Exception as err:
            _view_settings.removeComponent(alias)
            logWarning("{}, {}, {}".format(__package__, alias, repr(err)))
            LOG_CURRENT_EXCEPTION(tags=[MOD_NAME])
    return viewSettings


def getBusinessHandlers():
    return (ObserverBusinessHandler(),)


def getContextMenuHandlers():
    return ()


class ObserverBusinessHandler(PackageBusinessHandler):
    __slots__ = ('minimapPlugin', '_statLoadTry', 'statistics', 'viewAliases')

    def __init__(self):
        self.viewAliases = _view_settings.getViewAliases()
        listeners = [(alias, self.eventListener) for alias in self.viewAliases]
        super(ObserverBusinessHandler, self).__init__(listeners, APP_NAME_SPACE.SF_BATTLE, EVENT_BUS_SCOPE.BATTLE)
        self.minimapPlugin = MinimapZoomPlugin()
        self._statLoadTry = 0
        self.statistics = StatisticsDataLoader(_view_settings.isWTREnabled())

    def fini(self):
        self.minimapPlugin.fini()
        self.minimapPlugin = None
        self._statLoadTry = 0
        super(ObserverBusinessHandler, self).fini()

    def eventListener(self, event):
        self._app.as_loadLibrariesS([SWF.BATTLE])
        self._app.loaderManager.onViewLoaded += self.onViewLoaded
        logInfo("ObserverBusinessHandler loading flash libraries swf={}, alias={}".format(SWF.BATTLE, event.alias))

    def loadStatisticView(self, view, icons):
        if self.statistics.enabled:
            if not self.statistics.loaded and self._statLoadTry < 20:
                self._statLoadTry += 1
                return callback(0.5, self.loadStatisticView, view, icons)
        cutWidth = settings.statistics[STATISTICS.PANELS_CUT_WIDTH]
        fullWidth = settings.statistics[STATISTICS.PANELS_FULL_WIDTH]
        typeColors = settings.vehicle_types[VEHICLE_TYPES.CLASS_COLORS]
        iconMultiplier = settings.statistics[STATISTICS.ICON_BLACKOUT]
        view.flashObject.as_createStatisticComponent(self.statistics.enabled, icons, self.statistics.itemsWTRData,
                                                     cutWidth, fullWidth, typeColors, iconMultiplier)

    def onViewLoaded(self, view, *args):
        logDebug("ObserverBusinessHandler/onViewLoaded: {}", view.settings.alias)
        if view.settings is None or view.settings.alias not in self.viewAliases:
            return
        self._app.loaderManager.onViewLoaded -= self.onViewLoaded
        g_events.onBattlePageLoaded(view)
        if not hasattr(view.flashObject, SWF.ATTRIBUTE_NAME):
            to_format_str = "battle_page {}, has ho attribute {}"
            return logError(to_format_str.format(repr(view.flashObject), SWF.ATTRIBUTE_NAME))
        view.flashObject.as_observerCreateComponents(_view_settings.getComponents())
        view.flashObject.as_observerUpdatePrebattleTimer(settings.main[MAIN.REMOVE_SHADOW_IN_PREBATTLE])
        view.flashObject.as_observerHideWgComponents(_view_settings.getHiddenWGComponents())
        if self.minimapPlugin.enabled:
            self.minimapPlugin.init(view)
        icons = _view_settings.isIconsEnabled()
        if icons or self.statistics.enabled:
            self.loadStatisticView(view, icons)


logInfo("package {} loaded".format(__package__))

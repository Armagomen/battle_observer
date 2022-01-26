from importlib import import_module

from armagomen.battle_observer.components.statistics.statistic_data_loader import statisticLoader
from armagomen.battle_observer.core import view_settings
from armagomen.constants import SWF, ALIAS_TO_PATH, MAIN, MINIMAP, GLOBAL
from armagomen.utils.common import logError, logWarning, logInfo
from armagomen.utils.events import g_events
from gui.Scaleform.framework import ComponentSettings, ScopeTemplates
from gui.Scaleform.framework.package_layout import PackageBusinessHandler, _addListener, _removeListener
from gui.app_loader.settings import APP_NAME_SPACE
from gui.shared import EVENT_BUS_SCOPE
from gui.shared.events import AppLifeCycleEvent
from helpers.func_utils import callback


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
    __slots__ = ('_viewAliases', '_statistics', '_icons', '_listeners', '_scope', '_app', '_appNS')

    def __init__(self):
        self._viewAliases = view_settings.getViewAliases()
        self._statistics = view_settings.isStatisticEnabled()
        self._icons = view_settings.isIconsEnabled()
        listeners = [(alias, self.eventListener) for alias in self._viewAliases]
        super(ObserverBusinessHandler, self).__init__(listeners, APP_NAME_SPACE.SF_BATTLE, EVENT_BUS_SCOPE.BATTLE)

    def init(self):
        super(ObserverBusinessHandler, self).init()
        _addListener(AppLifeCycleEvent.INITIALIZING, self.onAppInitializing, EVENT_BUS_SCOPE.GLOBAL)

    def fini(self):
        _removeListener(AppLifeCycleEvent.INITIALIZING, self.onAppInitializing, EVENT_BUS_SCOPE.GLOBAL)
        super(ObserverBusinessHandler, self).fini()

    def eventListener(self, event):
        if not view_settings.isAllowed:
            return
        self._app.loaderManager.onViewLoaded += self.onViewLoaded

    def onAppInitializing(self, event):
        if event.ns == APP_NAME_SPACE.SF_BATTLE and view_settings.isAllowed:
            if self._statistics:
                statisticLoader.setCachedStatisticData()
            self._app.as_loadLibrariesS([SWF.BATTLE])
            logInfo("loading flash libraries swf={}, appNS={}".format(SWF.BATTLE, event.ns))

    def onViewLoaded(self, view, *args):
        if view.settings is None or view.settings.alias not in self._viewAliases:
            return
        self._app.loaderManager.onViewLoaded -= self.onViewLoaded
        g_events.onBattlePageLoaded(view)
        if not hasattr(view.flashObject, SWF.ATTRIBUTE_NAME):
            to_format_str = "battle_page {}, has ho attribute {}"
            return logError(to_format_str.format(repr(view.flashObject), SWF.ATTRIBUTE_NAME))
        components = view_settings.getComponents()
        view._blToggling.update(components[1:])
        view.flashObject.as_observerCreateComponents(components, self._statistics, self._icons)
        view.flashObject.as_observerUpdatePrebattleTimer(view_settings.cfg.main[MAIN.REMOVE_SHADOW_IN_PREBATTLE])
        callback(2.0, view.flashObject, "as_observerHideWgComponents", view_settings.getHiddenWGComponents())
        minimapZoom = view_settings.cfg.minimap[GLOBAL.ENABLED] and view_settings.cfg.minimap[MINIMAP.ZOOM]
        if minimapZoom and not view_settings.cfg.xvmInstalled and view_settings.notEpicBattle:
            view.flashObject.as_createMimimapCentered()

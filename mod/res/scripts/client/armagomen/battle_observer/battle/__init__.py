from importlib import import_module

from armagomen.battle_observer.core import view_settings
from armagomen.battle_observer.statistics.statistic_data_loader import statisticLoader
from armagomen.constants import SWF, ALIAS_TO_PATH, MAIN
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
    __slots__ = ('_viewAliases', '_statistics', '_listeners', '_scope', '_app', '_appNS')

    def __init__(self):
        self._viewAliases = view_settings.getViewAliases()
        self._statistics = False
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
            if statisticLoader.enabled and view_settings.isStatisticEnabled:
                self._statistics = statisticLoader.setCachedStatisticData()
            self._app.as_loadLibrariesS([SWF.BATTLE])
            logInfo("loading flash libraries swf={}, appNS={}".format(SWF.BATTLE, event.ns))

    def load(self, flash):
        if not hasattr(flash, SWF.ATTRIBUTE_NAME):
            to_format_str = "battle_page {}, has ho attribute {}"
            return logError(to_format_str.format(repr(flash), SWF.ATTRIBUTE_NAME))
        flash.as_observerCreateComponents(view_settings.getComponents(), self._statistics, view_settings.isIconsEnabled)
        flash.as_observerUpdatePrebattleTimer(view_settings.cfg.main[MAIN.REMOVE_SHADOW_IN_PREBATTLE])
        # flash.as_observerHideWgComponents(view_settings.getHiddenWGComponents())
        callback(2.0, flash, "as_observerHideWgComponents", view_settings.getHiddenWGComponents())

    def onViewLoaded(self, view, *args):
        if view.settings is None or view.settings.alias not in self._viewAliases:
            return
        self._app.loaderManager.onViewLoaded -= self.onViewLoaded
        g_events.onBattlePageLoaded(view)
        callback(0.1, self, "load", view.flashObject)

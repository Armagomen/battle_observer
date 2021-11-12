from importlib import import_module

from armagomen.battle_observer.core import view_settings
from armagomen.battle_observer.statistics.statistic_data_loader import setCachedStatisticData
from armagomen.constants import GLOBAL, SWF, ALIAS_TO_PATH, SORTED_ALIASES, MAIN, ALIASES, STATISTICS_ALIASES
from armagomen.utils.common import logError, logWarning, logInfo
from armagomen.utils.events import g_events
from gui.Scaleform.daapi.view.battle.epic.page import _GAME_UI, _SPECTATOR_UI
from gui.Scaleform.framework import ComponentSettings, ScopeTemplates
from gui.Scaleform.framework.package_layout import PackageBusinessHandler, _addListener, _removeListener
from gui.app_loader.settings import APP_NAME_SPACE
from gui.shared import EVENT_BUS_SCOPE
from gui.shared.events import AppLifeCycleEvent


def getViewSettings():
    settings = []
    if view_settings.setIsAllowed():
        for alias in SORTED_ALIASES + STATISTICS_ALIASES:
            if not view_settings.getSetting(alias):
                _GAME_UI.discard(alias)
                _SPECTATOR_UI.discard(alias)
                continue
            try:
                class_name = alias.split("_")[GLOBAL.ONE]
                file_name = ALIAS_TO_PATH.get(alias)
                module_class = getattr(import_module(file_name, package=__package__), class_name)
                settings.append(ComponentSettings(alias, module_class, ScopeTemplates.DEFAULT_SCOPE))
                _GAME_UI.add(alias)
                _SPECTATOR_UI.add(alias)
            except Exception as err:
                logWarning("{}, {}, {}".format(__package__, alias, repr(err)))
    return settings


def getBusinessHandlers():
    return ObserverBusinessHandler(),


def getContextMenuHandlers():
    return ()


class ObserverBusinessHandler(PackageBusinessHandler):
    __slots__ = ('__viewAliases', '__statistics', '_listeners', '_scope', '_app', '_appNS')

    def __init__(self):
        self.__viewAliases = view_settings.getViewAliases()
        self.__statistics = False
        listeners = [(alias, self.eventListener) for alias in self.__viewAliases]
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
            if view_settings.isStatisticEnabled:
                self.__statistics = setCachedStatisticData()
            self._app.as_loadLibrariesS([SWF.BATTLE])
            logInfo("loading flash libraries swf={}, appNS={}".format(SWF.BATTLE, event.ns))

    def onViewLoaded(self, view, *args):
        if view.settings is None or view.settings.alias not in self.__viewAliases:
            return
        self._app.loaderManager.onViewLoaded -= self.onViewLoaded
        g_events.onBattlePageLoaded(view)
        flash = view.flashObject
        if not hasattr(flash, SWF.ATTRIBUTE_NAME):
            to_format_str = "battle_page {}, has ho attribute {}"
            return logError(to_format_str.format(repr(flash), SWF.ATTRIBUTE_NAME))
        iconsEnabled = view_settings.isIconsEnabled
        if self.__statistics or iconsEnabled:
            flash.as_observerStatisticComponents(self.__statistics, iconsEnabled)
        for alias in SORTED_ALIASES:
            if view_settings.getSetting(alias):
                flash.as_createBattleObserverComp(alias)
        flash.as_observerUpdatePrebattleTimer(view_settings.cfg.main[MAIN.REMOVE_SHADOW_IN_PREBATTLE])
        hiddenWGComponents = view_settings.getHiddenWGComponents()
        if hiddenWGComponents:
            flash.as_observerHideWgComponents(hiddenWGComponents)

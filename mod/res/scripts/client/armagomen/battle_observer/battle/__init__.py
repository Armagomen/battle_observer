from importlib import import_module

from PlayerEvents import g_playerEvents
from armagomen.battle_observer.core import view_settings
from armagomen.battle_observer.statistics.statistic_data_loader import setCachedStatisticData
from armagomen.constants import GLOBAL, SWF, ALIAS_TO_PATH, SORTED_ALIASES, MAIN, ALIASES
from armagomen.utils.common import logError, logWarning, logInfo
from armagomen.utils.events import g_events
from gui.Scaleform.daapi.view.battle.epic.page import _GAME_UI, _SPECTATOR_UI
from gui.Scaleform.framework import ComponentSettings, ScopeTemplates
from gui.Scaleform.framework.package_layout import PackageBusinessHandler
from gui.app_loader.settings import APP_NAME_SPACE
from gui.shared import EVENT_BUS_SCOPE
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider


def getViewSettings():
    view_settings.setIsAllowed()
    settings = []
    for alias in SORTED_ALIASES:
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
    __slots__ = ('flash', '__external', '__viewAliases', '_listeners', '_scope', '_app', '_appNS')
    sessionProvider = dependency.descriptor(IBattleSessionProvider)

    def __init__(self):
        self.flash = None
        self.__external = view_settings.getExternalComponents()
        self.__viewAliases = view_settings.getViewAliases()
        listeners = ((alias, self.eventListener) for alias in self.__viewAliases)
        super(ObserverBusinessHandler, self).__init__(listeners, APP_NAME_SPACE.SF_BATTLE, EVENT_BUS_SCOPE.BATTLE)

    def eventListener(self, event):
        if view_settings.getSetting(ALIASES.PANELS_STAT):
            arenaDP = self.sessionProvider.getArenaDP()
            setCachedStatisticData(vInfo.player.accountDBID for vInfo in arenaDP.getVehiclesInfoIterator())
        self._app.as_loadLibrariesS([SWF.BATTLE])
        self._app.loaderManager.onViewLoaded += self.onViewLoaded
        logInfo("loading flash libraries swf={}, alias={}".format(SWF.BATTLE, event.alias))

    def fini(self):
        self.flash = None
        super(ObserverBusinessHandler, self).fini()

    def onAvatarReady(self):
        g_playerEvents.onAvatarReady -= self.onAvatarReady
        if self.flash is None:
            return
        hiddenWGComponents = view_settings.getHiddenWGComponents()
        if hiddenWGComponents:
            self.flash.as_observerHideWgComponents(hiddenWGComponents)
        if self.__external:
            self.flash.as_observerRegisterExternalComponents(self.__external)

    def onViewLoaded(self, view, *args):
        if view.settings is None or view.settings.alias not in self.__viewAliases:
            return
        g_events.onBattlePageLoaded(view)
        self._app.loaderManager.onViewLoaded -= self.onViewLoaded
        g_playerEvents.onAvatarReady += self.onAvatarReady
        self.flash = view.flashObject
        if not hasattr(self.flash, SWF.ATTRIBUTE_NAME):
            to_format_str = "battle_page {}, has ho attribute {}"
            return logError(to_format_str.format(repr(self.flash), SWF.ATTRIBUTE_NAME))
        for alias in SORTED_ALIASES:
            if view_settings.getSetting(alias) and alias not in self.__external:
                self.flash.as_createBattleObserverComp(alias)
        self.flash.as_observerUpdateComponents(view_settings.cfg.main[MAIN.REMOVE_SHADOW_IN_PREBATTLE])

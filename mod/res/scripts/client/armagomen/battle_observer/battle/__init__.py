from importlib import import_module

from PlayerEvents import g_playerEvents
from armagomen.battle_observer.core import view_settings
from armagomen.constants import GLOBAL, SWF, ALIAS_TO_PATH, SORTED_ALIASES, MAIN
from armagomen.utils.common import logError, logWarning, logInfo
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.daapi.view.battle.epic.page import _GAME_UI, _SPECTATOR_UI
from gui.Scaleform.framework import ComponentSettings, ScopeTemplates
from gui.Scaleform.framework.package_layout import PackageBusinessHandler
from gui.app_loader.settings import APP_NAME_SPACE
from gui.shared import EVENT_BUS_SCOPE


def getViewSettings():
    settings = []
    for alias in SORTED_ALIASES:
        if not view_settings.getSetting(alias):
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


ALIASES_TO_LOAD = (VIEW_ALIAS.CLASSIC_BATTLE_PAGE, VIEW_ALIAS.RANKED_BATTLE_PAGE, VIEW_ALIAS.EPIC_RANDOM_PAGE)


class ObserverBusinessHandler(PackageBusinessHandler):
    __slots__ = ("flash", '_listeners', '_scope', '_app', '_appNS')

    def __init__(self):
        self.flash = None
        listeners = ((alias, self.eventListener) for alias in ALIASES_TO_LOAD)
        super(ObserverBusinessHandler, self).__init__(listeners, APP_NAME_SPACE.SF_BATTLE, EVENT_BUS_SCOPE.BATTLE)

    def eventListener(self, event):
        self._app.as_loadLibrariesS([SWF.BATTLE])
        self._app.loaderManager.onViewLoaded += self.onViewLoaded
        g_playerEvents.onAvatarReady += self.onAvatarReady
        logInfo("loading flash libraries " + SWF.BATTLE)
        
    def fini(self):
        self.flash = None
        super(ObserverBusinessHandler, self).fini()

    def onViewLoaded(self, view, *args):
        if view.settings is None or view.settings.alias not in ALIASES_TO_LOAD:
            return
        self._app.loaderManager.onViewLoaded -= self.onViewLoaded
        if view_settings.cfg.main[MAIN.DEBUG]:
            logInfo("__onViewLoaded " + view.settings.alias)
        flash = view.flashObject
        self.flash = flash
        if not hasattr(flash, SWF.ATTRIBUTE_NAME):
            to_format_str = "battle_page {}, has ho attribute {}"
            return logError(to_format_str.format(repr(flash), SWF.ATTRIBUTE_NAME))
        for comp in SORTED_ALIASES:
            if view_settings.getSetting(comp):
                flash.as_createBattleObserverComp(comp)
                if view_settings.cfg.main[MAIN.DEBUG]:
                    logInfo(comp + " loading flash")
        flash.as_updateBattleObserverChildIndexes()

    def onAvatarReady(self):
        g_playerEvents.onAvatarReady -= self.onAvatarReady
        if self.flash is not None:
            hiddenWGComponents = view_settings.getHiddenWGComponents()
            if hiddenWGComponents:
                self.flash.as_observerHideWgComponents(hiddenWGComponents)

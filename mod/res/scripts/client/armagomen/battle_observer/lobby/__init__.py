from importlib import import_module

from armagomen.battle_observer.core import settings
from armagomen.constants import GLOBAL, CLOCK, SWF, ALIASES
from armagomen.utils.common import logError, logWarning
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.framework import ComponentSettings, ScopeTemplates
from gui.Scaleform.framework.package_layout import PackageBusinessHandler
from gui.app_loader.settings import APP_NAME_SPACE
from gui.shared import EVENT_BUS_SCOPE


def checkSettings():
    return ALIASES.DATE_TIME, settings.clock[GLOBAL.ENABLED] and settings.clock[CLOCK.IN_LOBBY][GLOBAL.ENABLED]


def getViewSettings():
    alias, enable = checkSettings()
    view_settings = []
    if enable:
        try:
            class_name = alias.split("_")[GLOBAL.ONE]
            module_class = getattr(import_module(".date_times", package=__package__), class_name)
            view_settings.append(ComponentSettings(alias, module_class, ScopeTemplates.DEFAULT_SCOPE))
        except Exception as err:
            logWarning("{}, {}, {}".format(__package__, alias, repr(err)))
    return view_settings


def getBusinessHandlers():
    return ObserverBusinessHandler(),


def getContextMenuHandlers():
    return ()


class ObserverBusinessHandler(PackageBusinessHandler):
    __slots__ = ()

    def __init__(self):
        listeners = [(VIEW_ALIAS.LOBBY_HANGAR, self.eventListener)]
        super(ObserverBusinessHandler, self).__init__(listeners, APP_NAME_SPACE.SF_LOBBY, EVENT_BUS_SCOPE.LOBBY)

    def eventListener(self, event):
        self._app.as_loadLibrariesS([SWF.LOBBY])
        self._app.loaderManager.onViewLoaded += self.__onViewLoaded

    def __onViewLoaded(self, view, *args):
        if view.settings is None or view.settings.alias != VIEW_ALIAS.LOBBY_HANGAR:
            return
        self._app.loaderManager.onViewLoaded -= self.__onViewLoaded
        if not hasattr(view.flashObject, SWF.ATTRIBUTE_NAME):
            to_format_str = "hangar_page {}, has ho attribute {}"
            return logError(to_format_str.format(repr(view.flashObject), SWF.ATTRIBUTE_NAME))
        comp, enabled = checkSettings()
        if enabled:
            view.flashObject.as_createBattleObserverComp(comp)

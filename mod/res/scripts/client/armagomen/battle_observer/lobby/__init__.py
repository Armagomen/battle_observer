from importlib import import_module

from armagomen.battle_observer.core import settings
from armagomen.constants import GLOBAL, CLOCK, SWF, ALIASES
from armagomen.utils.common import logError, logWarning, callback, logInfo
from armagomen.utils.events import g_events
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
    __slots__ = ('_listeners', '_scope', '_app', '_appNS', "swfLoaded")

    def __init__(self):
        self.swfLoaded = False
        listeners = [(VIEW_ALIAS.LOBBY_HANGAR, self.eventListener), (VIEW_ALIAS.LOGIN, self.eventListener)]
        super(ObserverBusinessHandler, self).__init__(listeners, APP_NAME_SPACE.SF_LOBBY, EVENT_BUS_SCOPE.LOBBY)

    def eventListener(self, event):
        if not self.swfLoaded:
            self._app.as_loadLibrariesS([SWF.LOBBY])
            logInfo("loading flash libraries swf={}, alias={}".format(SWF.LOBBY, event.alias))
            self.swfLoaded = True
            self._app.loaderManager.onViewLoaded += self._onViewLoaded

    def fini(self):
        super(ObserverBusinessHandler, self).fini()
        self.swfLoaded = False

    @staticmethod
    def _onViewLoaded(view, *args):
        if view.settings is None:
            return
        if view.settings.alias == VIEW_ALIAS.LOGIN:
            callback(1.0, lambda: g_events.onLoginLoaded(view))
            # logInfo("onViewLoaded, alias {}".format(view.settings.alias))
        elif view.settings.alias == VIEW_ALIAS.LOBBY_HANGAR:
            callback(1.0, lambda: g_events.onHangarLoaded(view))
            # logInfo("onViewLoaded, alias {}".format(view.settings.alias))
            if not hasattr(view.flashObject, SWF.ATTRIBUTE_NAME):
                to_format_str = "hangar_page {}, has ho attribute {}"
                return logError(to_format_str.format(repr(view.flashObject), SWF.ATTRIBUTE_NAME))
            comp, enabled = checkSettings()
            if enabled:
                view.flashObject.as_createBattleObserverComp(comp)

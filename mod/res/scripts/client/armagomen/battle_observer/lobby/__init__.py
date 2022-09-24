from importlib import import_module

from armagomen.constants import SWF, ALIASES
from armagomen.utils.common import logError, logWarning, logDebug, callback
from armagomen.utils.events import g_events
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.framework import ComponentSettings, ScopeTemplates
from gui.Scaleform.framework.package_layout import PackageBusinessHandler
from gui.app_loader.settings import APP_NAME_SPACE
from gui.shared import EVENT_BUS_SCOPE


def getViewSettings():
    view_settings = []
    try:
        module_class = getattr(import_module(".date_times", package=__package__), "DateTimes")
        view_settings.append(ComponentSettings(ALIASES.DATE_TIME, module_class, ScopeTemplates.DEFAULT_SCOPE))
    except Exception as err:
        logWarning("{}, {}, {}".format(__package__, ALIASES.DATE_TIME, repr(err)))
    return view_settings


def getBusinessHandlers():
    return ObserverBusinessHandler(),


def getContextMenuHandlers():
    return ()


class ObserverBusinessHandler(PackageBusinessHandler):
    __slots__ = ('_listeners', '_scope', '_app', '_appNS')

    def __init__(self):
        listeners = [(VIEW_ALIAS.LOBBY_HANGAR, self.eventListener), (VIEW_ALIAS.LOGIN, self.eventListener)]
        super(ObserverBusinessHandler, self).__init__(listeners, APP_NAME_SPACE.SF_LOBBY, EVENT_BUS_SCOPE.LOBBY)

    def eventListener(self, event):
        self._app.loaderManager.onViewLoaded += self._onViewLoaded
        if event.alias == VIEW_ALIAS.LOBBY_HANGAR:
            self._app.as_loadLibrariesS([SWF.LOBBY])
            logDebug("loading flash libraries swf={}, alias={}", SWF.LOBBY, event.alias)

    @staticmethod
    def load(view):
        g_events.onHangarLoaded(view)
        if hasattr(view.flashObject, SWF.ATTRIBUTE_NAME):
            view.flashObject.as_observerCreateComponents([ALIASES.DATE_TIME])
        else:
            logError("hangar_page {}, has ho attribute {}", view.settings.alias, SWF.ATTRIBUTE_NAME)

    def _onViewLoaded(self, view, *args):
        if view.settings is None:
            return
        if view.settings.alias == VIEW_ALIAS.LOGIN:
            callback(1.0, g_events.onLoginLoaded, view)
            logDebug("onViewLoaded, alias={}", view.settings.alias)
        elif view.settings.alias == VIEW_ALIAS.LOBBY_HANGAR:
            callback(1.0, self.load, view)
            logDebug("onViewLoaded, alias={}", view.settings.alias)

from armagomen.constants import SWF, LOBBY_ALIASES
from armagomen.utils.common import logError, callback, logInfo, xvmInstalled
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.framework import ComponentSettings, ScopeTemplates
from gui.Scaleform.framework.package_layout import PackageBusinessHandler
from gui.app_loader.settings import APP_NAME_SPACE
from gui.shared import EVENT_BUS_SCOPE

__all__ = ()


def getViewSettings():
    from armagomen.battle_observer.lobby.date_times import DateTimes
    from armagomen.battle_observer.lobby.avg_data import AvgData
    return (ComponentSettings(LOBBY_ALIASES.DATE_TIME, DateTimes, ScopeTemplates.DEFAULT_SCOPE),
            ComponentSettings(LOBBY_ALIASES.AVG_DATA, AvgData, ScopeTemplates.DEFAULT_SCOPE),)


def getBusinessHandlers():
    return ObserverBusinessHandlerLobby(),


def getContextMenuHandlers():
    return ()


class ObserverBusinessHandlerLobby(PackageBusinessHandler):
    __slots__ = ('_listeners', '_scope', '_app', '_appNS',)

    def __init__(self):
        listeners = ((VIEW_ALIAS.LOBBY_HANGAR, self.eventListener),)
        super(ObserverBusinessHandlerLobby, self).__init__(listeners, APP_NAME_SPACE.SF_LOBBY, EVENT_BUS_SCOPE.LOBBY)

    def eventListener(self, event):
        self._app.loaderManager.onViewLoaded += self._onViewLoaded
        self._app.as_loadLibrariesS([SWF.LOBBY])
        logInfo("{}: loading libraries swf={}, alias={}".format(self.__class__.__name__, SWF.LOBBY, event.alias))

    def _onViewLoaded(self, pyView, *args):
        if pyView.getAlias() != VIEW_ALIAS.LOBBY_HANGAR:
            return
        self._app.loaderManager.onViewLoaded -= self._onViewLoaded
        if not hasattr(pyView.flashObject, SWF.ATTRIBUTE_NAME):
            return logError("{}:flashObject, has ho attribute {}", pyView.getAlias(), SWF.ATTRIBUTE_NAME)
        callback(1.0 if xvmInstalled else 0, pyView.flashObject.as_observerCreateComponents, LOBBY_ALIASES)

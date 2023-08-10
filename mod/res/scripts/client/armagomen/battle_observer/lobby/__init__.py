from armagomen._constants import LOBBY_ALIASES
from armagomen.battle_observer.lobby.date_times import DateTimes
from armagomen.battle_observer.view import ViewHandlerLobby
from gui.Scaleform.framework import ComponentSettings, ScopeTemplates

__all__ = ()

VIEW_SETTINGS = (
    ComponentSettings(LOBBY_ALIASES.DATE_TIME, DateTimes, ScopeTemplates.DEFAULT_SCOPE),
)


def getViewSettings():
    return VIEW_SETTINGS


def getBusinessHandlers():
    return ViewHandlerLobby(),


def getContextMenuHandlers():
    return ()

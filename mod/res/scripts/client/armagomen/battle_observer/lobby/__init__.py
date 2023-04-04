from armagomen.battle_observer.business_handlers import ObserverBusinessHandlerLobby
from armagomen.constants import LOBBY_ALIASES
from gui.Scaleform.framework import ComponentSettings, ScopeTemplates

__all__ = ()


def getViewSettings():
    from armagomen.battle_observer.lobby.date_times import DateTimes
    return (ComponentSettings(LOBBY_ALIASES.DATE_TIME, DateTimes, ScopeTemplates.DEFAULT_SCOPE),)


def getBusinessHandlers():
    return ObserverBusinessHandlerLobby(),


def getContextMenuHandlers():
    return ()

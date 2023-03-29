from armagomen.battle_observer.business_handlers import ObserverBusinessHandlerLobby
from armagomen.constants import LOBBY_ALIASES
from gui.Scaleform.framework import ComponentSettings, ScopeTemplates

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

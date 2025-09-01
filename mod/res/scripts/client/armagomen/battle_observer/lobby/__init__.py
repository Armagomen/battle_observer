from armagomen._constants import LOBBY_ALIASES
from armagomen.battle_observer.lobby.date_times import DateTimes
from armagomen.battle_observer.lobby.hangar_efficiency import HangarEfficiency
from armagomen.battle_observer.view import ViewHandlerLobby
from gui.Scaleform.framework import ComponentSettings, ScopeTemplates

__all__ = ()


def getViewSettings():
    return (ComponentSettings(LOBBY_ALIASES.DATE_TIME, DateTimes, ScopeTemplates.DEFAULT_SCOPE),
            ComponentSettings(LOBBY_ALIASES.EFFICIENCY, HangarEfficiency, ScopeTemplates.DEFAULT_SCOPE),)


def getBusinessHandlers():
    return ViewHandlerLobby(),


def getContextMenuHandlers():
    return ()

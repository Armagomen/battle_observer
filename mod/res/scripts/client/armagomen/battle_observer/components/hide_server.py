import constants
from armagomen.battle_observer.core import settings
from armagomen.constants import GLOBAL, MAIN
from armagomen.utils.common import overrideMethod
from gui.Scaleform.daapi.view.lobby.header.LobbyHeader import LobbyHeader


@overrideMethod(LobbyHeader, "as_setServerNameS")
def as_setServerNameS(base, header, data):
    if settings.main[MAIN.HIDE_SERVER_IN_HANGAR]:
        return base(header, "SERVER HIDDEN")
    return base(header, data)


def onModSettingsChanged(_settings, blockID):
    if blockID == MAIN.NAME:
        for name, setting in _settings.iteritems():
            if name == MAIN.HIDE_SERVER_IN_HANGAR:
                constants.IS_SHOW_SERVER_STATS = not setting


@overrideMethod(LobbyHeader, "as_setServerS")
def as_setServerS(base, header, serverShortName, const, _type):
    if settings.main[MAIN.HIDE_SERVER_IN_HANGAR]:
        return base(header, GLOBAL.EMPTY_LINE, GLOBAL.EMPTY_LINE, _type)
    return base(header, serverShortName, const, _type)


@overrideMethod(LobbyHeader, "as_updateOnlineCounterS")
def as_updateOnlineCounterS(base, header, clusterStats, regionStats, tooltip, isAvailable):
    if settings.main[MAIN.HIDE_SERVER_IN_HANGAR]:
        return base(header, "ONLINE", regionStats, GLOBAL.EMPTY_LINE, isAvailable)
    return base(header, clusterStats, regionStats, tooltip, isAvailable)


settings.onModSettingsChanged += onModSettingsChanged

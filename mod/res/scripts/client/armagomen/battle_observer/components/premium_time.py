from collections import defaultdict

from armagomen.battle_observer.core import settings
from armagomen.bo_constants import CLOCK
from armagomen.utils.common import overrideMethod, callback, cancelCallback
from gui.Scaleform.daapi.view.lobby.header.LobbyHeader import LobbyHeader
from helpers.time_utils import getTimeDeltaFromNow, makeLocalServerTime, ONE_DAY, ONE_HOUR, ONE_MINUTE


class PremiumTime(object):

    def __init__(self):
        self.callback = None

    def startCallback(self, base, header, data):
        if header.itemsCache.items.stats.isPremium:
            self.callback = callback(1.0, lambda: self.startCallback(base, header, data))
        else:
            self.stopCallback()
        data["doLabel"] = header._getPremiumLabelText(header.itemsCache.items.stats.activePremiumType)
        base(header, data)

    def stopCallback(self):
        if self.callback is not None:
            cancelCallback(self.callback)
            self.callback = None


handler = PremiumTime()
macros = defaultdict(int)


@overrideMethod(LobbyHeader, "_getPremiumLabelText")
def _getPremiumLabelText(base, header, premiumState):
    if settings.main[CLOCK.PREMIUM_TIME]:
        premiumExpiryTime = header.itemsCache.items.stats.activePremiumExpiryTime
        deltaInSeconds = float(getTimeDeltaFromNow(makeLocalServerTime(premiumExpiryTime)))
        macros["days"], delta = divmod(deltaInSeconds, ONE_DAY)
        macros["hours"], delta = divmod(delta, ONE_HOUR)
        macros["minutes"], macros["seconds"] = divmod(delta, ONE_MINUTE)
        if any(macros.itervalues()):
            return settings.main[CLOCK.PREMIUM_FORMAT] % macros
    return base(header, premiumState)


@overrideMethod(LobbyHeader, "as_setPremiumParamsS")
def as_setPremiumParamsS(base, header, data):
    if settings.main[CLOCK.PREMIUM_TIME]:
        handler.startCallback(base, header, data)
    else:
        base(header, data)


@overrideMethod(LobbyHeader, "_removeListeners")
def _removeListeners(base, header):
    base(header)
    handler.stopCallback()

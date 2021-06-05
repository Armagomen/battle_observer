from collections import defaultdict

from armagomen.battle_observer.core import settings
from armagomen.bo_constants import PREMIUM
from armagomen.utils.common import overrideMethod, callback, cancelCallback
from gui.Scaleform.daapi.view.lobby.header.LobbyHeader import LobbyHeader
from helpers.time_utils import getTimeDeltaFromNow, makeLocalServerTime, ONE_DAY, ONE_HOUR, ONE_MINUTE


class PremiumTime(object):

    def __init__(self):
        self.callback = None
        self.macros = defaultdict(int)
        overrideMethod(LobbyHeader, "as_setPremiumParamsS")(self.startCallback)
        overrideMethod(LobbyHeader, "_removeListeners")(self._removeListeners)

    def _getPremiumLabelText(self, timeDelta):
        if settings.main[PREMIUM.PREMIUM_TIME]:
            delta = float(getTimeDeltaFromNow(makeLocalServerTime(timeDelta)))
            self.macros["days"], delta = divmod(delta, ONE_DAY)
            self.macros["hours"], delta = divmod(delta, ONE_HOUR)
            self.macros["minutes"], self.macros["seconds"] = divmod(delta, ONE_MINUTE)
            return settings.main[PREMIUM.PREMIUM_FORMAT] % self.macros

    def startCallback(self, base, header, data):
        self.stopCallback()
        if settings.main[PREMIUM.PREMIUM_TIME] and header.itemsCache.items.stats.isPremium:
            self.callback = callback(1.0, lambda: self.startCallback(base, header, data))
            data["doLabel"] = self._getPremiumLabelText(header.itemsCache.items.stats.activePremiumExpiryTime)
        base(header, data)

    def stopCallback(self):
        if self.callback is not None:
            cancelCallback(self.callback)
            self.callback = None

    def _removeListeners(self, base, header):
        self.stopCallback()
        return base(header)


p_time = PremiumTime()

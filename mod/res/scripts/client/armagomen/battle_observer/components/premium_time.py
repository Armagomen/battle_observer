from armagomen._constants import MAIN
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import addCallback, cancelCallback, overrideMethod
from gui.impl import backport
from gui.impl.gen import R
from gui.Scaleform.daapi.view.lobby.header.LobbyHeader import LobbyHeader
from helpers.time_utils import getTimeDeltaFromNow, makeLocalServerTime, ONE_DAY, ONE_HOUR, ONE_MINUTE


class PremiumTime(object):

    def __init__(self):
        self.callback = None
        day = backport.text(R.strings.menu.header.account.premium.days()).replace(".", "")
        hour = backport.text(R.strings.menu.header.account.premium.hours()).replace(".", "")
        self.days = "<b><font color='#FAFAFA'>{0:d} %s. {2:02d}:{3:02d}:{4:02d}</font></b>" % day
        self.hours = "<b><font color='#FAFAFA'>{1:d} %s. {2:02d}:{3:02d}</font></b>" % hour
        overrideMethod(LobbyHeader, "as_setPremiumParamsS")(self.startCallback)
        overrideMethod(LobbyHeader, "_removeListeners")(self._removeListeners)

    @staticmethod
    def _getPremiumLabelText(template, delta):
        days, delta = divmod(delta, ONE_DAY)
        hours, delta = divmod(delta, ONE_HOUR)
        mins, secs = divmod(delta, ONE_MINUTE)
        return template.format(days, hours, mins, secs)

    def startCallback(self, base, header, data):
        self.stopCallback()
        if user_settings.main[MAIN.PREMIUM_TIME] and header.itemsCache.items.stats.isPremium:
            delta = int(getTimeDeltaFromNow(makeLocalServerTime(header.itemsCache.items.stats.activePremiumExpiryTime)))
            self.callback = addCallback(1.0, self.startCallback, base, header, data)
            data["doLabel"] = self._getPremiumLabelText(self.days if delta > ONE_DAY else self.hours, delta)
        base(header, data)

    def stopCallback(self):
        if self.callback is not None:
            cancelCallback(self.callback)
            self.callback = None

    def _removeListeners(self, base, header):
        self.stopCallback()
        return base(header)


p_time = PremiumTime()

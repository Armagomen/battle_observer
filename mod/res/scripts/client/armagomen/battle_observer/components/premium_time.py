from collections import namedtuple

from armagomen._constants import MAIN
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import addCallback, cancelCallback, overrideMethod
from gui.impl import backport
from gui.impl.gen import R
from gui.Scaleform.daapi.view.lobby.header.LobbyHeader import LobbyHeader
from helpers.time_utils import getTimeDeltaFromNow, makeLocalServerTime, ONE_DAY, ONE_HOUR, ONE_MINUTE

TEMPLATES = namedtuple("TEMPLATES", ("DAYS", "HOURS"))(
    "<b><font color='#FAFAFA'>%(days)d {0}. %(hours)02d:%(min)02d</font></b>".format(
        backport.text(R.strings.menu.header.account.premium.days()).replace(".", "")),
    "<b><font color='#FAFAFA'>%(hours)d {0}. %(min)02d:%(sec)02d</font></b>".format(
        backport.text(R.strings.menu.header.account.premium.hours()).replace(".", ""))
)


class PremiumTime(object):

    def __init__(self):
        self.callback = None
        self.macros = {}
        overrideMethod(LobbyHeader, "as_setPremiumParamsS")(self.startCallback)
        overrideMethod(LobbyHeader, "_removeListeners")(self._removeListeners)

    def _getPremiumLabelText(self, template, delta):
        self.macros["days"], delta = divmod(delta, ONE_DAY)
        self.macros["hours"], delta = divmod(delta, ONE_HOUR)
        self.macros["min"], self.macros["sec"] = divmod(delta, ONE_MINUTE)
        return template % self.macros

    def startCallback(self, base, header, data):
        self.stopCallback()
        if user_settings.main[MAIN.PREMIUM_TIME] and header.itemsCache.items.stats.isPremium:
            delta = int(getTimeDeltaFromNow(makeLocalServerTime(header.itemsCache.items.stats.activePremiumExpiryTime)))
            days = delta > ONE_DAY
            template = TEMPLATES.DAYS if days else TEMPLATES.HOURS
            self.callback = addCallback(30.0 if days else 1.0, self.startCallback, base, header, data)
            data["doLabel"] = self._getPremiumLabelText(template, delta)
        base(header, data)

    def stopCallback(self):
        if self.callback is not None:
            cancelCallback(self.callback)
            self.callback = None

    def _removeListeners(self, base, header):
        self.stopCallback()
        return base(header)


p_time = PremiumTime()

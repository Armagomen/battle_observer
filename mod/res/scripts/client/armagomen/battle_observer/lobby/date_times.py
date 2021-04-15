# coding=utf-8
from time import strftime

from armagomen.battle_observer.core import settings
from armagomen.battle_observer.core.bo_constants import CLOCK
from armagomen.battle_observer.meta.lobby.date_times_meta import DateTimesMeta
from armagomen.utils.common import checkDecoder
from armagomen.utils.timers import CyclicTimerEvent
from gui.shared.personality import ServicesLocator
from helpers.time_utils import getTimeDeltaFromNow, makeLocalServerTime, ONE_DAY, ONE_HOUR, ONE_MINUTE


class DateTimes(DateTimesMeta):

    def __init__(self):
        super(DateTimes, self).__init__()
        self.config = settings.clock[CLOCK.IN_LOBBY]
        self.coding = None
        self.timerEvent = CyclicTimerEvent(CLOCK.UPDATE_INTERVAL, self.updateTimeData)

    def _populate(self):
        super(DateTimes, self)._populate()
        self.updateDecoder()
        settings.onModSettingsChanged += self.onModSettingsChanged
        self.as_startUpdateS(self.config)
        self.timerEvent.start()

    def updateDecoder(self):
        self.coding = checkDecoder(strftime(self.config[CLOCK.FORMAT]))

    def onModSettingsChanged(self, config, blockID):
        if blockID == CLOCK.NAME:
            self.updateDecoder()

    def _dispose(self):
        self.timerEvent.stop()
        settings.onModSettingsChanged -= self.onModSettingsChanged
        super(DateTimes, self)._dispose()

    def updateTimeData(self):
        _time = strftime(self.config[CLOCK.FORMAT])
        if self.coding is not None:
            _time = _time.decode(self.coding)
        self.as_setDateTimeS(_time)
        self.setPremiumTimeLeft(self.config[CLOCK.PREMIUM_TIME])

    def setPremiumTimeLeft(self, enable):
        if enable and ServicesLocator.itemsCache.items.stats.isPremium:
            premiumExpiryTime = ServicesLocator.itemsCache.items.stats.activePremiumExpiryTime
            deltaInSeconds = float(getTimeDeltaFromNow(makeLocalServerTime(premiumExpiryTime)))
            days, delta = divmod(deltaInSeconds, ONE_DAY)
            hours, delta = divmod(delta, ONE_HOUR)
            minutes, seconds = divmod(delta, ONE_MINUTE)
            timedelta = {"days": days, "hours": hours, "minutes": minutes, "seconds": seconds}
            timeLeft = self.config[CLOCK.PREMIUM_FORMAT] % timedelta
            self.as_setPremiumLeftS(timeLeft)
        else:
            self.as_setPremiumLeftS()

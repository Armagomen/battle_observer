# coding=utf-8
from time import strftime

from armagomen._constants import CLOCK, GLOBAL
from armagomen.battle_observer.meta.lobby.date_times_meta import DateTimesMeta
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import ENCODING_ERRORS, ENCODING_LOCALE
from armagomen.utils.timers import CyclicTimerEvent


class DateTimes(DateTimesMeta):

    def __init__(self):
        super(DateTimes, self).__init__()
        self.config = user_settings.clock[CLOCK.IN_LOBBY]
        self.timerEvent = CyclicTimerEvent(CLOCK.UPDATE_INTERVAL, self.updateTimeData)

    def _populate(self):
        super(DateTimes, self)._populate()
        user_settings.onModSettingsChanged += self.onModSettingsChanged
        if self.config[GLOBAL.ENABLED] and user_settings.clock[GLOBAL.ENABLED]:
            self.timerEvent.start()

    def onModSettingsChanged(self, config, blockID):
        if blockID == CLOCK.NAME:
            self.timerEvent.stop()
            self.as_onSettingsChanged(config)
            if self.config[GLOBAL.ENABLED] and user_settings.clock[GLOBAL.ENABLED]:
                self.timerEvent.start()

    def _dispose(self):
        self.timerEvent.stop()
        user_settings.onModSettingsChanged -= self.onModSettingsChanged
        super(DateTimes, self)._dispose()

    def updateTimeData(self):
        self.as_setDateTimeS(unicode(strftime(self.config[CLOCK.FORMAT]), ENCODING_LOCALE, ENCODING_ERRORS))

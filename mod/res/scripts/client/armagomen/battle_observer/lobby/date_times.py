# coding=utf-8
from time import strftime

from armagomen._constants import CLOCK
from armagomen.battle_observer.meta.lobby.date_times_meta import DateTimesMeta
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import ENCODING_ERRORS, ENCODING_LOCALE


class DateTimes(DateTimesMeta):

    def __init__(self):
        super(DateTimes, self).__init__()
        self.config = user_settings.clock[CLOCK.IN_LOBBY]

    def _populate(self):
        super(DateTimes, self)._populate()
        user_settings.onModSettingsChanged += self.onModSettingsChanged

    def onModSettingsChanged(self, config, blockID):
        if blockID == CLOCK.NAME:
            self.as_onSettingsChanged(config)

    def _dispose(self):
        user_settings.onModSettingsChanged -= self.onModSettingsChanged
        super(DateTimes, self)._dispose()

    def getTimeString(self):
        return unicode(strftime(self.config[CLOCK.FORMAT]), ENCODING_LOCALE, ENCODING_ERRORS)

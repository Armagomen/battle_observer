# coding=utf-8
from time import strftime

from armagomen._constants import CLOCK
from armagomen.battle_observer.meta.lobby.date_times_meta import DateTimesMeta
from armagomen.utils.common import ENCODING_ERRORS, ENCODING_LOCALE
from armagomen.utils.events import g_events


class DateTimes(DateTimesMeta):

    def _populate(self):
        super(DateTimes, self)._populate()
        g_events.onModSettingsChanged += self.onModSettingsChanged

    def onModSettingsChanged(self, name, data):
        if name == CLOCK.NAME:
            self.as_onSettingsChanged(data)

    def _dispose(self):
        g_events.onModSettingsChanged -= self.onModSettingsChanged
        super(DateTimes, self)._dispose()

    def getTimeString(self):
        return unicode(strftime(self.settings[CLOCK.IN_LOBBY][CLOCK.FORMAT]), ENCODING_LOCALE, ENCODING_ERRORS)

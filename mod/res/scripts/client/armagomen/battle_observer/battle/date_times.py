# coding=utf-8
from time import strftime

from armagomen.battle_observer.meta.battle.date_times_meta import DateTimesMeta
from armagomen.constants import CLOCK
from armagomen.utils.common import ENCODING_LOCALE, ENCODING_ERRORS
from gui.battle_control.controllers.period_ctrl import IAbstractPeriodView


class DateTimes(DateTimesMeta, IAbstractPeriodView):

    def setTotalTime(self, totalTime):
        time_string = strftime(self.settings[CLOCK.IN_BATTLE][CLOCK.FORMAT])
        self.as_setDateTimeS(unicode(time_string, ENCODING_LOCALE, ENCODING_ERRORS))

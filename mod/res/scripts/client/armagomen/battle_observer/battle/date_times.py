from datetime import datetime

from armagomen.battle_observer.meta.battle.date_times_meta import DateTimesMeta
from armagomen.constants import CLOCK
from gui.battle_control.controllers.period_ctrl import IAbstractPeriodView


class DateTimes(DateTimesMeta, IAbstractPeriodView):

    def setTotalTime(self, totalTime):
        self.as_setDateTimeS(datetime.now().strftime(self.settings[CLOCK.IN_BATTLE][CLOCK.FORMAT]))

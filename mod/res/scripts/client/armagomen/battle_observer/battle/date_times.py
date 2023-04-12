from time import strftime

from armagomen.battle_observer.meta.battle.date_times_meta import DateTimesMeta
from armagomen.constants import CLOCK
from armagomen.utils.common import checkDecoder
from gui.battle_control.controllers.period_ctrl import IAbstractPeriodView


class DateTimes(DateTimesMeta, IAbstractPeriodView):

    def __init__(self):
        super(DateTimes, self).__init__()
        self.coding = None

    def _populate(self):
        super(DateTimes, self)._populate()
        self.coding = checkDecoder(strftime(self.settings[CLOCK.IN_BATTLE][CLOCK.FORMAT]))

    def setTotalTime(self, totalTime):
        _time = strftime(self.settings[CLOCK.IN_BATTLE][CLOCK.FORMAT])
        if self.coding is not None:
            _time = _time.encode(encoding=self.coding, errors="ignore").decode(errors="ignore")
        self.as_setDateTimeS(_time)

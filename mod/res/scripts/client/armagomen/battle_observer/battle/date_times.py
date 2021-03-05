from time import strftime

from armagomen.battle_observer.core import cfg
from armagomen.battle_observer.core.bo_constants import CLOCK
from armagomen.battle_observer.core.utils import CyclicTimerEvent
from armagomen.battle_observer.meta.battle.date_times_meta import DateTimesMeta
from armagomen.battle_observer.core.utils.common import checkDecoder

config = cfg.clock[CLOCK.IN_BATTLE]


class DateTimes(DateTimesMeta):

    def __init__(self):
        super(DateTimes, self).__init__()
        self.format = config[CLOCK.FORMAT]
        self.coding = checkDecoder(strftime(self.format))
        self.timerEvent = CyclicTimerEvent(CLOCK.UPDATE_INTERVAL, self.updateTimeData)

    def _populate(self):
        super(DateTimes, self)._populate()
        self.as_startUpdateS(config)
        self.timerEvent.start()

    def _dispose(self):
        self.timerEvent.stop()
        super(DateTimes, self)._dispose()

    def updateTimeData(self):
        _time = strftime(self.format)
        if self.coding is not None:
            _time = _time.decode(self.coding)
        self.as_setDateTimeS(_time)

from time import strftime

from ..core import cfg
from ..core.bo_constants import CLOCK
from ..core.utils import CyclicTimerEvent
from ..core.utils.common import checkDecoder
from ..meta.battle.date_times_meta import DateTimesMeta

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
        """stop and join time thread on destroy flash object"""
        self.timerEvent.stop()
        super(DateTimes, self)._dispose()

    def updateTimeData(self):
        _time = strftime(self.format)
        if self.coding is not None:
            _time = _time.decode(self.coding)
        self.as_setDateTimeS(_time)

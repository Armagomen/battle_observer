from time import strftime

from ..core import cfg, cache
from ..core.bo_constants import CLOCK
from ..core.utils import CyclicTimerEvent
from ..core.utils.common import checkDecoder
from ..meta.lobby.date_times_meta import DateTimesMeta


class DateTimes(DateTimesMeta):

    def __init__(self):
        super(DateTimes, self).__init__()
        self.config = cfg.clock[CLOCK.IN_LOBBY]
        self.coding = None
        self.timerEvent = CyclicTimerEvent(CLOCK.UPDATE_INTERVAL, self.updateTimeData)

    def _populate(self):
        super(DateTimes, self)._populate()
        self.updateDecoder()
        cache.onModSettingsChanged += self.onModSettingsChanged
        self.as_startUpdateS(self.config)
        self.timerEvent.start()

    def updateDecoder(self):
        self.coding = checkDecoder(strftime(self.config[CLOCK.FORMAT]))

    def onModSettingsChanged(self, config, blockID):
        if blockID == CLOCK.NAME:
            self.config = config[CLOCK.IN_LOBBY]
            self.updateDecoder()

    def _dispose(self):
        self.timerEvent.stop()
        cache.onModSettingsChanged -= self.onModSettingsChanged
        super(DateTimes, self)._dispose()

    def updateTimeData(self):
        _time = strftime(self.config[CLOCK.FORMAT])
        if self.coding is not None:
            _time = _time.decode(self.coding)
        self.as_setDateTimeS(_time)

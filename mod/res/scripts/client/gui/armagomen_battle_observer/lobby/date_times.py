from time import strftime

from ..core.bo_constants import CLOCK
from ..core.config import cfg
from ..core.core import m_core
from ..core.events import g_events
from ..core.timers import CyclicTimerEvent
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
        g_events.onSettingsChanged += self.onSettingsChanged
        self.as_startUpdateS(self.config)
        self.timerEvent.start()

    def updateDecoder(self):
        self.coding = m_core.checkDecoder(strftime(self.config[CLOCK.FORMAT]))

    def onSettingsChanged(self, config, blockID):
        if blockID == CLOCK.NAME:
            self.config = config[CLOCK.IN_LOBBY]
            self.updateDecoder()

    def _dispose(self):
        """stop and join time thread on destroy flash object"""
        self.timerEvent.stop()
        g_events.onSettingsChanged -= self.onSettingsChanged
        super(DateTimes, self)._dispose()

    def updateTimeData(self):
        _time = strftime(self.config[CLOCK.FORMAT])
        if self.coding is not None:
            _time = _time.decode(self.coding)
        self.as_setDateTimeS(_time)

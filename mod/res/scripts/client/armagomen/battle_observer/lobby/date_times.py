from time import strftime

from armagomen.battle_observer.core import config
from armagomen.battle_observer.core.constants import CLOCK
from armagomen.battle_observer.meta.lobby.date_times_meta import DateTimesMeta
from armagomen.utils.common import checkDecoder
from armagomen.utils.timers import CyclicTimerEvent


class DateTimes(DateTimesMeta):

    def __init__(self):
        super(DateTimes, self).__init__()
        self.config = config.clock[CLOCK.IN_LOBBY]
        self.coding = None
        self.timerEvent = CyclicTimerEvent(CLOCK.UPDATE_INTERVAL, self.updateTimeData)

    def _populate(self):
        super(DateTimes, self)._populate()
        self.updateDecoder()
        config.onModSettingsChanged += self.onModSettingsChanged
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
        config.onModSettingsChanged -= self.onModSettingsChanged
        super(DateTimes, self)._dispose()

    def updateTimeData(self):
        _time = strftime(self.config[CLOCK.FORMAT])
        if self.coding is not None:
            _time = _time.decode(self.coding)
        self.as_setDateTimeS(_time)

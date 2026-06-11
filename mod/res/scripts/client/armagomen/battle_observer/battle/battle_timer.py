from collections import defaultdict, namedtuple

from armagomen._constants import BATTLE_TIMER, COLORS, GLOBAL
from armagomen.battle_observer.meta.battle.battle_timer_meta import BattleTimerMeta
from constants import ARENA_PERIOD
from gui.battle_control.controllers.period_ctrl import IAbstractPeriodView
from helpers.time_utils import ONE_MINUTE

TimerColors = namedtuple("TimerColors", ("normal", "end"))


class BattleTimer(BattleTimerMeta, IAbstractPeriodView):

    def __init__(self):
        super(BattleTimer, self).__init__()
        self.timerColors = None
        self.isBattlePeriod = False
        self.timer = defaultdict(str, timerColor=COLORS.WHITE, timer=BATTLE_TIMER.START_STRING)

    def _populate(self):
        super(BattleTimer, self)._populate()
        self.timerColors = TimerColors(self.settings[BATTLE_TIMER.COLOR], self.settings[BATTLE_TIMER.END_COLOR])
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onPeriodChange += self.onArenaPeriodChange
            self.isBattlePeriod = arena.period == ARENA_PERIOD.BATTLE

    def _dispose(self):
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onPeriodChange -= self.onArenaPeriodChange

    def onArenaPeriodChange(self, period, *args):
        self.isBattlePeriod = period == ARENA_PERIOD.BATTLE

    def updateTimerColor(self, totalTime):
        color = self.timerColors.end if totalTime < BATTLE_TIMER.END_BATTLE_SEC else self.timerColors.normal
        if self.timer[BATTLE_TIMER.COLOR] != color:
            self.timer[BATTLE_TIMER.COLOR] = color

    def setTotalTime(self, totalTime):
        if self.isBattlePeriod:
            self.updateTimerColor(totalTime)
            self.timer[BATTLE_TIMER.M_TIMER] = BATTLE_TIMER.TIME_FORMAT % divmod(totalTime, ONE_MINUTE)
            self.as_timerS(self.settings[BATTLE_TIMER.TEMPLATE] % self.timer)
        else:
            self.as_timerS(GLOBAL.EMPTY_LINE)

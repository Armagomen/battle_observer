from collections import defaultdict, namedtuple

from armagomen.battle_observer.meta.battle.battle_timer_meta import BattleTimerMeta
from armagomen.constants import BATTLE_TIMER, COLORS, GLOBAL
from gui.battle_control.controllers.period_ctrl import IAbstractPeriodView
from helpers.time_utils import ONE_MINUTE

TimerColors = namedtuple("TimerColors", ("normal", "end"))


class BattleTimer(BattleTimerMeta, IAbstractPeriodView):

    def __init__(self):
        super(BattleTimer, self).__init__()
        self.timerColors = None
        self.timer = defaultdict(lambda: GLOBAL.CONFIG_ERROR, timerColor=COLORS.WHITE,
                                 timer=BATTLE_TIMER.START_STRING)

    def _populate(self):
        super(BattleTimer, self)._populate()
        self.timerColors = TimerColors(self.settings[BATTLE_TIMER.COLOR], self.settings[BATTLE_TIMER.END_COLOR])

    def updateTimerColor(self, totalTime):
        color = self.timerColors.end if totalTime < BATTLE_TIMER.END_BATTLE_SEC else self.timerColors.normal
        if self.timer[BATTLE_TIMER.COLOR] != color:
            self.timer[BATTLE_TIMER.COLOR] = color

    def setTotalTime(self, totalTime):
        self.updateTimerColor(totalTime)
        self.timer[BATTLE_TIMER.M_TIMER] = BATTLE_TIMER.TIME_FORMAT % divmod(totalTime, ONE_MINUTE)
        self.as_timerS(self.settings[BATTLE_TIMER.TEMPLATE] % self.timer)

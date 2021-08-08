from collections import defaultdict

from armagomen.constants import BATTLE_TIMER, COLORS, GLOBAL
from armagomen.battle_observer.meta.battle.battle_timer_meta import BattleTimerMeta
from gui.battle_control.controllers.period_ctrl import IAbstractPeriodView
from helpers.time_utils import ONE_MINUTE


class BattleTimer(BattleTimerMeta, IAbstractPeriodView):

    def __init__(self):
        super(BattleTimer, self).__init__()
        self.timer = defaultdict(lambda: GLOBAL.CONFIG_ERROR, timerColor=COLORS.NORMAL_TEXT,
                                 timer=BATTLE_TIMER.START_STRING)

    def setTotalTime(self, totalTime):
        self.timer[BATTLE_TIMER.COLOR] = self.settings[BATTLE_TIMER.END_COLOR] \
            if totalTime < BATTLE_TIMER.END_BATTLE_SEC else self.settings[BATTLE_TIMER.COLOR]
        self.timer[BATTLE_TIMER.M_TIMER] = BATTLE_TIMER.TIME_FORMAT % divmod(totalTime, ONE_MINUTE)
        self.as_timerS(self.settings[BATTLE_TIMER.TEMPLATE] % self.timer)

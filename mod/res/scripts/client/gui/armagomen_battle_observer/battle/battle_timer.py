from collections import defaultdict

from gui.battle_control.controllers.period_ctrl import IAbstractPeriodView
from helpers.time_utils import ONE_MINUTE
from ..core.bo_constants import BATTLE_TIMER, COLORS, GLOBAL
from ..core.config import cfg
from ..meta.battle.battle_timer_meta import BattleTimerMeta


class BattleTimer(BattleTimerMeta, IAbstractPeriodView):

    def __init__(self):
        super(BattleTimer, self).__init__()
        config = cfg.battle_timer
        default_timer = {BATTLE_TIMER.COLOR: COLORS.NORMAL_TEXT, BATTLE_TIMER.M_TIMER: BATTLE_TIMER.START_STRING}
        self.timer = defaultdict(GLOBAL.CONFIG_ERROR, default_timer)
        self.template = config[BATTLE_TIMER.TEMPLATE]
        self.color = {False: config[BATTLE_TIMER.COLOR], True: config[BATTLE_TIMER.END_COLOR]}

    def _populate(self):
        super(BattleTimer, self)._populate()
        self.as_startUpdateS()

    def setTotalTime(self, totalTime):
        self.timer[BATTLE_TIMER.COLOR] = self.color[totalTime < BATTLE_TIMER.END_BATTLE_SEC]
        self.timer[BATTLE_TIMER.M_TIMER] = BATTLE_TIMER.TIME_FORMAT % divmod(totalTime, ONE_MINUTE)
        self.as_timerS(self.template % self.timer)

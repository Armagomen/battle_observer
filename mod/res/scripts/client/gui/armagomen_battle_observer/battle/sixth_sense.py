from collections import defaultdict

from gui.Scaleform.daapi.view.battle.shared.indicators import SixthSenseIndicator
from ..core.bo_constants import GLOBAL, SIXTH_SENSE
from ..core.bw_utils import callback
from ..core.config import cfg
from ..core.events import g_events
from ..core.timers import SixthSenseTimer
from ..meta.battle.sixth_sense_meta import SixthSenseMeta

config = cfg.sixth_sense


class SixthSense(SixthSenseMeta):

    def __init__(self):
        super(SixthSense, self).__init__()
        self.macro = defaultdict(lambda: GLOBAL.CONFIG_ERROR)
        self.template = config[SIXTH_SENSE.TIMER][SIXTH_SENSE.TEMPLATE]
        self.showTimer = config[SIXTH_SENSE.SHOW_TIMER]
        self.macro[SIXTH_SENSE.M_TIME] = config[SIXTH_SENSE.TIME]
        self._timer = SixthSenseTimer(self.handleTimer, self.hide, config[SIXTH_SENSE.PLAY_TICK_SOUND])
        self.wg_as_show = None
        self.wg_as_hide = None

    def onEnterBattlePage(self):
        super(SixthSense, self).onEnterBattlePage()
        g_events.onPlayerVehicleDeath += self.hide
        if self.wg_as_show is None:
            self.wg_as_show = SixthSenseIndicator.as_showS
            SixthSenseIndicator.as_showS = lambda ssi: self.show()
        if self.wg_as_hide is None:
            self.wg_as_hide = SixthSenseIndicator.as_hideS
            SixthSenseIndicator.as_hideS = lambda ssi: None
        self.as_startUpdateS(config)

    def onExitBattlePage(self):
        self._timer.stop()
        g_events.onPlayerVehicleDeath -= self.hide
        if self.wg_as_show is not None:
            SixthSenseIndicator.as_showS = self.wg_as_show
            self.wg_as_show = None
        if self.wg_as_hide is not None:
            SixthSenseIndicator.as_hideS = self.wg_as_hide
            self.wg_as_hide = None
        super(SixthSense, self).onExitBattlePage()

    def handleTimer(self, timeLeft):
        self.macro[SIXTH_SENSE.M_TIME_LEFT] = timeLeft
        self.as_sixthSenseS(True, self.template % self.macro)

    def show(self):
        if self.showTimer:
            self._timer.setSeconds(config[SIXTH_SENSE.TIME])
            if self._timer.callback is None:
                self._timer.start()
        else:
            self.as_sixthSenseS(True, GLOBAL.EMPTY_LINE)
            callback(float(config[SIXTH_SENSE.TIME]), self.hide)

    def hide(self, *args):
        if args:
            self._timer.stop()
        self.as_sixthSenseS(False, GLOBAL.EMPTY_LINE)

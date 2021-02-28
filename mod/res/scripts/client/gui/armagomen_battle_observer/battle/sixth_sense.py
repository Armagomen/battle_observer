from collections import defaultdict

from gui.Scaleform.daapi.view.battle.shared.indicators import SixthSenseIndicator
from ..core import cfg, cache
from ..core.bo_constants import GLOBAL, SIXTH_SENSE
from ..core.utils import SixthSenseTimer
from ..core.utils.common import callback
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
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onVehicleKilled += self.onVehicleKilled
        if self.wg_as_show is None:
            self.wg_as_show = SixthSenseIndicator.as_showS
            SixthSenseIndicator.as_showS = lambda ssi: self.show()
        if self.wg_as_hide is None:
            self.wg_as_hide = SixthSenseIndicator.as_hideS
            SixthSenseIndicator.as_hideS = lambda ssi: None
        self.as_startUpdateS(config)

    def onExitBattlePage(self):
        self._timer.stop()
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onVehicleKilled -= self.onVehicleKilled
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
            if not self._timer.inProcess:
                self._timer.start()
        else:
            self.as_sixthSenseS(True, GLOBAL.EMPTY_LINE)
            callback(float(config[SIXTH_SENSE.TIME]), self.hide)

    def hide(self):
        self.as_sixthSenseS(False, GLOBAL.EMPTY_LINE)

    def onVehicleKilled(self, targetID, *args, **kwargs):
        if cache.player.playerVehicleID == targetID:
            if self.showTimer and self._timer.inProcess:
                self._timer.stop()
            else:
                self.hide()

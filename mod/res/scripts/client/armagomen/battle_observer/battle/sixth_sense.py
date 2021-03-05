from collections import defaultdict

from gui.battle_control.battle_constants import VEHICLE_VIEW_STATE

from armagomen.battle_observer.core import cfg
from armagomen.battle_observer.core.bo_constants import GLOBAL, SIXTH_SENSE
from armagomen.battle_observer.core.utils import SixthSenseTimer
from armagomen.battle_observer.core.utils.common import callback
from armagomen.battle_observer.meta.battle.sixth_sense_meta import SixthSenseMeta

config = cfg.sixth_sense


class SixthSense(SixthSenseMeta):

    def __init__(self):
        super(SixthSense, self).__init__()
        self.macro = defaultdict(lambda: GLOBAL.CONFIG_ERROR)
        self.template = config[SIXTH_SENSE.TIMER][SIXTH_SENSE.TEMPLATE]
        self.showTimer = config[SIXTH_SENSE.SHOW_TIMER]
        self.macro[SIXTH_SENSE.M_TIME] = config[SIXTH_SENSE.TIME]
        self._timer = SixthSenseTimer(self.handleTimer, self.as_hideS, config[SIXTH_SENSE.PLAY_TICK_SOUND])

    def onEnterBattlePage(self):
        super(SixthSense, self).onEnterBattlePage()
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onVehicleKilled += self.onVehicleKilled
        ctrl = self.sessionProvider.shared.vehicleState
        if ctrl is not None:
            ctrl.onVehicleStateUpdated += self.__onVehicleStateUpdated
        self.as_startUpdateS(config)

    def onExitBattlePage(self):
        self.stop()
        self._timer.destroy()
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onVehicleKilled -= self.onVehicleKilled
        ctrl = self.sessionProvider.shared.vehicleState
        if ctrl is not None:
            ctrl.onVehicleStateUpdated -= self.__onVehicleStateUpdated
        super(SixthSense, self).onExitBattlePage()

    def __onVehicleStateUpdated(self, state, value):
        if state == VEHICLE_VIEW_STATE.OBSERVED_BY_ENEMY:
            if value:
                self.show()
            else:
                self.stop()

    def handleTimer(self, timeLeft):
        self.macro[SIXTH_SENSE.M_TIME_LEFT] = timeLeft
        self.as_updateTimerS(self.template % self.macro)

    def show(self):
        self.as_showS()
        if self.showTimer:
            self._timer.start(config[SIXTH_SENSE.TIME])
        else:
            callback(float(config[SIXTH_SENSE.TIME]), self.as_hideS)

    def stop(self):
        if self.showTimer:
            self._timer.stop()
        else:
            self.as_hideS()

    def onVehicleKilled(self, targetID, *args, **kwargs):
        if self._player.playerVehicleID == targetID:
            self.stop()

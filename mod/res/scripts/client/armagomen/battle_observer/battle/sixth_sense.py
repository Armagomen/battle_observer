from collections import defaultdict

from PlayerEvents import g_playerEvents
from armagomen.battle_observer.meta.battle.sixth_sense_meta import SixthSenseMeta
from armagomen.constants import GLOBAL, SIXTH_SENSE
from armagomen.utils.common import callback
from armagomen.utils.timers import SixthSenseTimer
from constants import ARENA_PERIOD
from gui.battle_control.battle_constants import VEHICLE_VIEW_STATE

_STATES_TO_HIDE = {VEHICLE_VIEW_STATE.SWITCHING, VEHICLE_VIEW_STATE.RESPAWNING,
                   VEHICLE_VIEW_STATE.DESTROYED, VEHICLE_VIEW_STATE.CREW_DEACTIVATED}


class SixthSense(SixthSenseMeta):

    def __init__(self):
        super(SixthSense, self).__init__()
        self.macro = defaultdict(lambda: GLOBAL.CONFIG_ERROR, lampTime=GLOBAL.ZERO)
        self._timer = SixthSenseTimer(self.handleTimer, self.as_hideS, self._arenaVisitor.type.getCountdownTimerSound())

    def _populate(self):
        super(SixthSense, self)._populate()
        self.macro[SIXTH_SENSE.M_TIME] = self.settings[SIXTH_SENSE.TIME]

    def onEnterBattlePage(self):
        super(SixthSense, self).onEnterBattlePage()
        g_playerEvents.onArenaPeriodChange += self.__onRoundFinished
        ctrl = self.sessionProvider.shared.vehicleState
        if ctrl is not None:
            ctrl.onVehicleStateUpdated += self.__onVehicleStateUpdated

    def onExitBattlePage(self):
        self.stop()
        self._timer.destroy()
        g_playerEvents.onArenaPeriodChange -= self.__onRoundFinished
        ctrl = self.sessionProvider.shared.vehicleState
        if ctrl is not None:
            ctrl.onVehicleStateUpdated -= self.__onVehicleStateUpdated
        super(SixthSense, self).onExitBattlePage()

    def __onVehicleStateUpdated(self, state, value):
        if state == VEHICLE_VIEW_STATE.OBSERVED_BY_ENEMY:
            self.show() if value else self.stop()
        elif state in _STATES_TO_HIDE:
            self.stop()

    def __onRoundFinished(self, period, *args):
        if period == ARENA_PERIOD.AFTERBATTLE:
            self.stop()

    def handleTimer(self, timeLeft):
        self.macro[SIXTH_SENSE.M_TIME_LEFT] = timeLeft
        self.as_updateTimerS(self.settings[SIXTH_SENSE.TIMER][SIXTH_SENSE.TEMPLATE] % self.macro)

    def show(self):
        self.as_showS()
        if self.settings[SIXTH_SENSE.SHOW_TIMER]:
            self._timer.start(self.settings[SIXTH_SENSE.TIME], self.settings[SIXTH_SENSE.PLAY_TICK_SOUND])
        else:
            callback(float(self.settings[SIXTH_SENSE.TIME]), self.as_hideS)

    def stop(self):
        if self.settings[SIXTH_SENSE.SHOW_TIMER]:
            self._timer.stop()
        else:
            self.as_hideS()

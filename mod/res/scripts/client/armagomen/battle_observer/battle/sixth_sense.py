from collections import defaultdict

from PlayerEvents import g_playerEvents
from armagomen.battle_observer.meta.battle.sixth_sense_meta import SixthSenseMeta
from armagomen.constants import GLOBAL, SIXTH_SENSE
from armagomen.utils.common import callback
from armagomen.utils.timers import SixthSenseTimer
from gui.battle_control.battle_constants import VEHICLE_VIEW_STATE

_STATES_TO_HIDE = {VEHICLE_VIEW_STATE.SWITCHING, VEHICLE_VIEW_STATE.RESPAWNING,
                   VEHICLE_VIEW_STATE.DESTROYED, VEHICLE_VIEW_STATE.CREW_DEACTIVATED}


class SixthSense(SixthSenseMeta):

    def __init__(self):
        super(SixthSense, self).__init__()
        self.macro = defaultdict(lambda: GLOBAL.CONFIG_ERROR, lampTime=GLOBAL.ZERO)
        self._timer = None

    def _populate(self):
        super(SixthSense, self)._populate()
        self.macro[SIXTH_SENSE.M_TIME] = self.settings[SIXTH_SENSE.TIME]
        if self.settings[SIXTH_SENSE.SHOW_TIMER]:
            soundID = None
            if self.settings[SIXTH_SENSE.PLAY_TICK_SOUND]:
                soundID = self._arenaVisitor.type.getCountdownTimerSound()
            self._timer = SixthSenseTimer(self.handleTimer, self.hide, soundID=soundID)

    def onBattleSessionStart(self):
        super(SixthSense, self).onBattleSessionStart()
        g_playerEvents.onRoundFinished += self._onRoundFinished
        ctrl = self.sessionProvider.shared.vehicleState
        if ctrl is not None:
            ctrl.onVehicleStateUpdated += self._onVehicleStateUpdated

    def onBattleSessionStop(self):
        self.hide()
        if self._timer is not None:
            self._timer.destroy()
        g_playerEvents.onRoundFinished -= self._onRoundFinished
        ctrl = self.sessionProvider.shared.vehicleState
        if ctrl is not None:
            ctrl.onVehicleStateUpdated -= self._onVehicleStateUpdated
        super(SixthSense, self).onBattleSessionStop()

    def _onVehicleStateUpdated(self, state, value):
        if state == VEHICLE_VIEW_STATE.OBSERVED_BY_ENEMY:
            self.show() if value else self.hide()
        elif state in _STATES_TO_HIDE:
            self.hide()

    def _onRoundFinished(self, *args):
        self.hide()

    def handleTimer(self, timeLeft):
        self.macro[SIXTH_SENSE.M_TIME_LEFT] = timeLeft
        self.as_updateTimerS(self.settings[SIXTH_SENSE.TIMER][SIXTH_SENSE.TEMPLATE] % self.macro)

    def show(self):
        self.as_showS()
        if self._timer is not None:
            self._timer.start(self.settings[SIXTH_SENSE.TIME])
        else:
            callback(float(self.settings[SIXTH_SENSE.TIME]), self.hide)

    def hide(self):
        if self._timer is not None:
            self._timer.stop()
        self.as_hideS()

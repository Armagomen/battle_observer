import math
from collections import defaultdict

from PlayerEvents import g_playerEvents
from armagomen.battle_observer.meta.battle.own_health_meta import OwnHealthMeta
from armagomen.constants import GLOBAL, OWN_HEALTH, POSTMORTEM, VEHICLE
from armagomen.utils.common import percentToRGB
from constants import ARENA_PERIOD
from gui.Scaleform.daapi.view.battle.shared.formatters import normalizeHealth, getHealthPercent
from gui.battle_control import avatar_getter
from gui.battle_control.battle_constants import VEHICLE_VIEW_STATE
from gui.battle_control.controllers.prebattle_setups_ctrl import IPrebattleSetupsListener


class OwnHealth(OwnHealthMeta, IPrebattleSetupsListener):
    def __init__(self):
        super(OwnHealth, self).__init__()
        self.macrosDict = defaultdict(lambda: GLOBAL.CONFIG_ERROR, **{
            VEHICLE.CUR: GLOBAL.ZERO,
            VEHICLE.MAX: GLOBAL.ZERO,
            VEHICLE.PERCENT: GLOBAL.ZERO
        })
        self.isPostmortem = False
        self.__maxHealth = GLOBAL.ZERO

    def updateVehicleParams(self, vehicle, *args):
        if self.__maxHealth != vehicle.descriptor.maxHealth:
            self.__maxHealth = vehicle.descriptor.maxHealth
            self._updateHealth(self.__maxHealth)

    def _populate(self):
        super(OwnHealth, self)._populate()
        ctrl = self.sessionProvider.shared.crosshair
        if ctrl is not None:
            ctrl.onCrosshairPositionChanged += self.as_onCrosshairPositionChangedS
        handler = avatar_getter.getInputHandler()
        if handler is not None and hasattr(handler, "onCameraChanged"):
            handler.onCameraChanged += self.onCameraChanged
        g_playerEvents.onArenaPeriodChange += self.onArenaPeriod

    def onArenaPeriod(self, period, *args):
        self.as_setComponentVisible(period == ARENA_PERIOD.BATTLE)

    def _dispose(self):
        ctrl = self.sessionProvider.shared.crosshair
        if ctrl is not None:
            ctrl.onCrosshairPositionChanged -= self.as_onCrosshairPositionChangedS
        handler = avatar_getter.getInputHandler()
        if handler is not None and hasattr(handler, "onCameraChanged"):
            handler.onCameraChanged -= self.onCameraChanged
        g_playerEvents.onArenaPeriodChange -= self.onArenaPeriod
        super(OwnHealth, self)._dispose()

    def onEnterBattlePage(self):
        ctrl = self.sessionProvider.shared.vehicleState
        if ctrl is not None:
            ctrl.onVehicleControlling += self.__onVehicleControlling
            ctrl.onVehicleStateUpdated += self.__onVehicleStateUpdated

    def onExitBattlePage(self):
        ctrl = self.sessionProvider.shared.vehicleState
        if ctrl is not None:
            ctrl.onVehicleControlling -= self.__onVehicleControlling
            ctrl.onVehicleStateUpdated -= self.__onVehicleStateUpdated

    def __onVehicleControlling(self, vehicle):
        if self.isPostmortem:
            return self.as_setComponentVisible(False)
        if self.__maxHealth != vehicle.maxHealth:
            self.__maxHealth = vehicle.maxHealth
        self._updateHealth(vehicle.health)

    def __onVehicleStateUpdated(self, state, value):
        if state == VEHICLE_VIEW_STATE.HEALTH:
            self._updateHealth(value)

    def onCameraChanged(self, ctrlMode, *_, **__):
        self.isPostmortem = ctrlMode in POSTMORTEM.MODES
        self.as_setComponentVisible(not self.isPostmortem and self._player.arena.period == ARENA_PERIOD.BATTLE)

    def _updateHealth(self, health):
        if self.isPostmortem or health > self.__maxHealth or self.__maxHealth <= GLOBAL.ZERO:
            return
        health = normalizeHealth(health)
        if self.macrosDict[VEHICLE.CUR] == health and self.macrosDict[VEHICLE.MAX] == self.__maxHealth:
            return
        percent = getHealthPercent(health, self.__maxHealth)
        color = percentToRGB(percent, **self.settings[GLOBAL.AVG_COLOR])
        self.macrosDict[VEHICLE.CUR] = health
        self.macrosDict[VEHICLE.MAX] = self.__maxHealth
        self.macrosDict[VEHICLE.PERCENT] = int(math.ceil(percent * 100))
        self.as_setOwnHealthS(percent, self.settings[OWN_HEALTH.TEMPLATE] % self.macrosDict, color)

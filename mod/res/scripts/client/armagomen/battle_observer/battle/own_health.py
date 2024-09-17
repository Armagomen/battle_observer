# coding=utf-8

from armagomen._constants import GLOBAL, POSTMORTEM_MODES
from armagomen.battle_observer.meta.battle.own_health_meta import OwnHealthMeta
from armagomen.utils.common import percentToRGB
from constants import ARENA_PERIOD
from gui.battle_control import avatar_getter
from gui.battle_control.battle_constants import VEHICLE_VIEW_STATE
from gui.battle_control.controllers.prebattle_setups_ctrl import IPrebattleSetupsListener
from gui.Scaleform.daapi.view.battle.shared.formatters import getHealthPercent, normalizeHealth
from PlayerEvents import g_playerEvents


class OwnHealth(OwnHealthMeta, IPrebattleSetupsListener):
    def __init__(self):
        super(OwnHealth, self).__init__()
        self.isAliveMode = True
        self.isBattlePeriod = False
        self.__maxHealth = GLOBAL.ZERO
        self.__template = "{} • {:.2%}"

    def updateVehicleParams(self, vehicle, *args):
        if self.__maxHealth != vehicle.descriptor.maxHealth:
            self.__maxHealth = vehicle.descriptor.maxHealth
            self._updateHealth(self.__maxHealth)

    def _populate(self):
        super(OwnHealth, self)._populate()
        handler = avatar_getter.getInputHandler()
        if handler is not None and hasattr(handler, "onCameraChanged"):
            handler.onCameraChanged += self.onCameraChanged
        g_playerEvents.onArenaPeriodChange += self.onArenaPeriodChange
        ctrl = self.sessionProvider.shared.vehicleState
        if ctrl is not None:
            ctrl.onVehicleControlling += self.__onVehicleControlling
            ctrl.onVehicleStateUpdated += self.__onVehicleStateUpdated
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            self.isBattlePeriod = arena.period == ARENA_PERIOD.BATTLE
            self.isAliveMode = self.getVehicleInfo().isAlive()
            self.as_BarVisibleS(self.isBattlePeriod and self.isAliveMode)

    def onArenaPeriodChange(self, period, *args):
        self.isBattlePeriod = period == ARENA_PERIOD.BATTLE
        self.as_BarVisibleS(self.isBattlePeriod and self.isAliveMode)

    def _dispose(self):
        handler = avatar_getter.getInputHandler()
        if handler is not None and hasattr(handler, "onCameraChanged"):
            handler.onCameraChanged -= self.onCameraChanged
        g_playerEvents.onArenaPeriodChange -= self.onArenaPeriodChange
        ctrl = self.sessionProvider.shared.vehicleState
        if ctrl is not None:
            ctrl.onVehicleControlling -= self.__onVehicleControlling
            ctrl.onVehicleStateUpdated -= self.__onVehicleStateUpdated
        super(OwnHealth, self)._dispose()

    def __onVehicleControlling(self, vehicle):
        if self.__maxHealth != vehicle.maxHealth:
            self.__maxHealth = vehicle.maxHealth
        self._updateHealth(vehicle.health)

    def __onVehicleStateUpdated(self, state, value):
        if state == VEHICLE_VIEW_STATE.HEALTH:
            self._updateHealth(value)

    def onCameraChanged(self, ctrlMode, *_, **__):
        self.isAliveMode = ctrlMode not in POSTMORTEM_MODES
        self.as_BarVisibleS(self.isBattlePeriod and self.isAliveMode)

    def getAVGColor(self, percent=1.0):
        return percentToRGB(percent, **self.settings[GLOBAL.AVG_COLOR])

    def _updateHealth(self, health):
        if health > self.__maxHealth:
            self.__maxHealth = health
        if self.__maxHealth <= GLOBAL.ZERO:
            return
        percent = getHealthPercent(health, self.__maxHealth)
        text = self.__template.format(int(normalizeHealth(health)), percent)
        self.as_setOwnHealthS(percent, text, self.getAVGColor(percent))

from collections import defaultdict

from armagomen.battle_observer.meta.battle.own_health_meta import OwnHealthMeta
from armagomen.constants import GLOBAL, OWN_HEALTH, POSTMORTEM, VEHICLE
from armagomen.utils.common import percentToRGB
from armagomen.utils.events import g_events
from gui.Scaleform.daapi.view.battle.shared.formatters import normalizeHealth, normalizeHealthPercent
from gui.battle_control import avatar_getter
from gui.battle_control.battle_constants import VEHICLE_VIEW_STATE
from gui.battle_control.controllers.prebattle_setups_ctrl import IPrebattleSetupsListener


class OwnHealth(OwnHealthMeta, IPrebattleSetupsListener):
    def __init__(self):
        super(OwnHealth, self).__init__()
        self.macrosDict = defaultdict(lambda: GLOBAL.CONFIG_ERROR, **{
            VEHICLE.CUR: GLOBAL.ZERO,
            VEHICLE.MAX: GLOBAL.ZERO,
            VEHICLE.PERCENT: GLOBAL.ZERO,
            OWN_HEALTH.COLOR: percentToRGB(1.0)
        })
        self.isPostmortem = False
        self.__maxHealth = GLOBAL.ZERO

    def updateVehicleParams(self, vehicle, _):
        if self.__maxHealth != vehicle.descriptor.maxHealth:
            self.__maxHealth = vehicle.descriptor.maxHealth
            self._updateHealth(self.__maxHealth)

    def _populate(self):
        super(OwnHealth, self)._populate()
        g_events.onCrosshairPositionChanged -= self.as_onCrosshairPositionChanged
        self.as_startUpdateS(self.settings)

    def _dispose(self):
        g_events.onCrosshairPositionChanged -= self.as_onCrosshairPositionChanged
        super(OwnHealth, self)._dispose()

    def onEnterBattlePage(self):
        super(OwnHealth, self).onEnterBattlePage()
        ctrl = self.sessionProvider.shared.vehicleState
        if ctrl is not None:
            ctrl.onVehicleControlling += self.__onVehicleControlling
            ctrl.onVehicleStateUpdated += self.__onVehicleStateUpdated
            vehicle = ctrl.getControllingVehicle()
            if vehicle is not None:
                self.__onVehicleControlling(vehicle)
        handler = avatar_getter.getInputHandler()
        if handler is not None:
            handler.onCameraChanged += self.onCameraChanged

    def onExitBattlePage(self):
        handler = avatar_getter.getInputHandler()
        if handler is not None:
            handler.onCameraChanged -= self.onCameraChanged
        ctrl = self.sessionProvider.shared.vehicleState
        if ctrl is not None:
            ctrl.onVehicleControlling -= self.__onVehicleControlling
            ctrl.onVehicleStateUpdated -= self.__onVehicleStateUpdated
        super(OwnHealth, self).onExitBattlePage()

    def __onVehicleControlling(self, vehicle):
        if self.isPostmortem:
            return self.as_setOwnHealthS(GLOBAL.EMPTY_LINE)
        if self.__maxHealth != vehicle.maxHealth:
            self.__maxHealth = vehicle.maxHealth
        self._updateHealth(vehicle.health)

    def __onVehicleStateUpdated(self, state, value):
        if state == VEHICLE_VIEW_STATE.HEALTH:
            self._updateHealth(value)

    def onCameraChanged(self, ctrlMode, *_, **__):
        self.isPostmortem = ctrlMode in POSTMORTEM.MODES
        if self.isPostmortem:
            self.as_setOwnHealthS(GLOBAL.EMPTY_LINE)

    def _updateHealth(self, health):
        if self.isPostmortem or health > self.__maxHealth or self.__maxHealth <= GLOBAL.ZERO:
            return
        health = normalizeHealth(health)
        if self.macrosDict[VEHICLE.CUR] == health and self.macrosDict[VEHICLE.MAX] == self.__maxHealth:
            return
        self.macrosDict[VEHICLE.CUR] = health
        self.macrosDict[VEHICLE.MAX] = self.__maxHealth
        self.macrosDict[VEHICLE.PERCENT] = normalizeHealthPercent(health, self.__maxHealth)
        self.macrosDict[OWN_HEALTH.COLOR] = percentToRGB(self.macrosDict[VEHICLE.PERCENT] * 0.01)
        self.as_setOwnHealthS(self.settings[OWN_HEALTH.TEMPLATE] % self.macrosDict)

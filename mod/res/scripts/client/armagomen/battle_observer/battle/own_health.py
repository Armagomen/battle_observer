from collections import defaultdict

import BigWorld
from armagomen.battle_observer.meta.battle.own_health_meta import OwnHealthMeta
from armagomen.constants import GLOBAL, OWN_HEALTH, POSTMORTEM
from gui.Scaleform.daapi.view.battle.shared.formatters import normalizeHealth, normalizeHealthPercent
from gui.battle_control import avatar_getter
from gui.battle_control.battle_constants import VEHICLE_VIEW_STATE
# from gui.battle_control.controllers.prebattle_setups_ctrl import IPrebattleSetupsListener # 1.14


class OwnHealth(OwnHealthMeta):  # , IPrebattleSetupsListener): # 1.14
    def __init__(self):
        super(OwnHealth, self).__init__()
        self.macrosDict = defaultdict(lambda: GLOBAL.CONFIG_ERROR, **{
            OWN_HEALTH.CUR_HEALTH: GLOBAL.ZERO,
            OWN_HEALTH.MAX_HEALTH: GLOBAL.ZERO,
            OWN_HEALTH.PER_HEALTH: GLOBAL.ZERO,
        })
        self.isPostmortem = False
        self.__maxHealth = 0

    def setSetupsVehicle(self, vehicle):  # remove in 1.14
        pass

    def updateVehicleParams(self, vehicle, _):
        self.__maxHealth = vehicle.descriptor.maxHealth
        self._updateHealth(self.__maxHealth)

    def updateVehicleSetups(self, vehicle):  # remove in 1.14
        pass

    def stopSetupsSelection(self):  # remove in 1.14
        pass

    def _populate(self):
        super(OwnHealth, self)._populate()
        self.as_startUpdateS(self.settings)

    def _dispose(self):
        super(OwnHealth, self)._dispose()

    def onEnterBattlePage(self):
        super(OwnHealth, self).onEnterBattlePage()
        ctrl = self.sessionProvider.shared.vehicleState
        if ctrl is not None:
            ctrl.onVehicleControlling += self.__onVehicleControlling
            vehicle = ctrl.getControllingVehicle()
            if vehicle is not None:
                self.__onVehicleControlling(vehicle)
        handler = avatar_getter.getInputHandler()
        if handler is not None:
            handler.onCameraChanged += self.onCameraChanged
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onVehicleKilled += self.onVehicleKilled

    def onExitBattlePage(self):
        handler = avatar_getter.getInputHandler()
        if handler is not None:
            handler.onCameraChanged -= self.onCameraChanged
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onVehicleKilled -= self.onVehicleKilled
        ctrl = self.sessionProvider.shared.vehicleState
        if ctrl is not None:
            ctrl.onVehicleControlling -= self.__onVehicleControlling
            ctrl.onVehicleStateUpdated -= self.__onVehicleStateUpdated
        super(OwnHealth, self).onExitBattlePage()

    def __onVehicleControlling(self, vehicle):
        if self.isPostmortem:
            return self.as_setOwnHealthS(GLOBAL.EMPTY_LINE)
        self.__maxHealth = vehicle.maxHealth
        self._updateHealth(vehicle.health)
        ctrl = self.sessionProvider.shared.vehicleState
        if ctrl is None:
            return
        ctrl.onVehicleStateUpdated += self.__onVehicleStateUpdated
        value = ctrl.getStateValue(VEHICLE_VIEW_STATE.HEALTH)
        if value is not None:
            self.__onVehicleStateUpdated(VEHICLE_VIEW_STATE.HEALTH, value)

    def __onVehicleStateUpdated(self, state, value):
        if state == VEHICLE_VIEW_STATE.HEALTH:
            self._updateHealth(value)

    def onVehicleKilled(self, vehicleID, *_, **__):
        if vehicleID == BigWorld.player().playerVehicleID:
            self.as_setOwnHealthS(GLOBAL.EMPTY_LINE)

    def onCameraChanged(self, ctrlMode, *_, **__):
        self.as_onControlModeChangedS(ctrlMode)
        self.isPostmortem = ctrlMode in POSTMORTEM.MODES
        if self.isPostmortem:
            self.as_setOwnHealthS(GLOBAL.EMPTY_LINE)

    def _updateHealth(self, health):
        if self.isPostmortem or health > self.__maxHealth or self.__maxHealth <= 0:
            return
        health = normalizeHealth(health)
        if self.macrosDict[OWN_HEALTH.CUR_HEALTH] == health and self.macrosDict[OWN_HEALTH.MAX_HEALTH] == self.__maxHealth:
            return
        self.macrosDict[OWN_HEALTH.CUR_HEALTH] = health
        self.macrosDict[OWN_HEALTH.MAX_HEALTH] = self.__maxHealth
        self.macrosDict[OWN_HEALTH.PER_HEALTH] = normalizeHealthPercent(health, self.__maxHealth)
        self.as_setOwnHealthS(self.settings[OWN_HEALTH.TEMPLATE] % self.macrosDict)

from armagomen._constants import COLORS, PANELS, VEHICLE
from armagomen.battle_observer.components.controllers import damage_controller
from armagomen.battle_observer.meta.battle.players_panels_meta import PlayersPanelsMeta
from armagomen.utils.keys_listener import g_keysListener
from armagomen.utils.logging import logDebug
from gui.battle_control.controllers.battle_field_ctrl import IBattleFieldListener
from gui.Scaleform.daapi.view.battle.shared.formatters import normalizeHealthPercent


class PlayersPanels(PlayersPanelsMeta, IBattleFieldListener):

    def __init__(self):
        super(PlayersPanels, self).__init__()
        self.hpBarsEnable = False
        self.damagesEnable = False

    def _populate(self):
        super(PlayersPanels, self)._populate()
        self.hpBarsEnable = self.settings[PANELS.BARS_ENABLED]
        self.damagesEnable = self.settings[PANELS.DAMAGES_ENABLED]
        if self.hpBarsEnable:
            if self.settings[PANELS.ON_KEY_DOWN]:
                g_keysListener.registerComponent(self.as_setHealthBarsVisibleS, keyList=self.settings[PANELS.BAR_HOT_KEY])
            arena = self._arenaVisitor.getArenaSubscription()
            if arena is not None:
                arena.onPeriodChange += self.onPeriodChange
                arena.onVehicleKilled += self.onVehicleKilled
        if self.damagesEnable:
            damage_controller.onPlayerDamaged += self.onPlayerDamaged
            g_keysListener.registerComponent(self.as_setPlayersDamageVisibleS, keyList=self.settings[PANELS.DAMAGES_HOT_KEY])

    def _dispose(self):
        self.flashObject.as_clearStorage()
        if self.hpBarsEnable:
            arena = self._arenaVisitor.getArenaSubscription()
            if arena is not None:
                arena.onPeriodChange -= self.onPeriodChange
                arena.onVehicleKilled -= self.onVehicleKilled
        if self.damagesEnable:
            damage_controller.onPlayerDamaged -= self.onPlayerDamaged
        super(PlayersPanels, self)._dispose()

    def onColorblindUpdated(self, blind):
        barColor = self.getBarColor(True, blind)
        self.as_colorBlindBarsS(barColor)

    def getBarColor(self, isEnemy, isColorBlind=None):
        colors = self.getColors()[COLORS.GLOBAL]
        if isEnemy:
            if isColorBlind is None:
                isColorBlind = self._isColorBlind
            return colors[COLORS.ENEMY_BLIND_MAME if isColorBlind else COLORS.ENEMY_MAME]
        return colors[COLORS.ALLY_MAME]

    def createHealthBar(self, vehicleID, vInfoVO, isEnemy):
        max_health = vInfoVO.vehicleType.maxHealth or 0
        if self.settings[PANELS.BAR_CLASS_COLOR]:
            color = self.getVehicleClassColor(vInfoVO.vehicleType.classTag)
        else:
            color = self.getBarColor(isEnemy)
        visible = not self.settings[PANELS.ON_KEY_DOWN]
        vehicle_data = {VEHICLE.CUR: max_health, VEHICLE.MAX: max_health, VEHICLE.PERCENT: 100}
        self.as_addHealthBarS(vehicleID, color, visible)
        self.as_updateHealthBarS(vehicleID, 100, self.settings[PANELS.HP_TEMPLATE] % vehicle_data)

    def onAddedToStorage(self, vehicleID, isEnemy):
        """Called from flash after creation in AS"""
        vInfoVO = self.getVehicleInfo(vehicleID)
        if vInfoVO.isObserver():
            return
        if self.hpBarsEnable and vInfoVO.isAlive():
            self.createHealthBar(vehicleID, vInfoVO, isEnemy)
        if self.damagesEnable:
            self.as_addDamageS(vehicleID, self.settings[PANELS.DAMAGES_SETTINGS])
        logDebug("PlayersPanels onAddedToStorage: id={} enemy={}", vehicleID, isEnemy)

    def onVehicleKilled(self, targetID, *args):
        self.as_setVehicleDeadS(targetID)

    def updateVehicleHealth(self, vehicleID, newHealth, maxHealth):
        if self.hpBarsEnable:
            vInfoVO = self.getVehicleInfo(vehicleID)
            if vInfoVO.isObserver():
                return
            max_health = max(newHealth, maxHealth)
            health_percent = normalizeHealthPercent(newHealth, max_health)
            vehicle_data = {VEHICLE.CUR: max(0, newHealth), VEHICLE.MAX: max_health, VEHICLE.PERCENT: health_percent}
            self.as_updateHealthBarS(vehicleID, health_percent, self.settings[PANELS.HP_TEMPLATE] % vehicle_data)

    def onPlayerDamaged(self, attackerID, damage):
        damage_text = self.settings[PANELS.DAMAGES_TEMPLATE] % {PANELS.DAMAGE: damage}
        self.as_updateDamageS(attackerID, damage_text)

    def onPeriodChange(self, *args):
        self.updateDamageLogPosition()

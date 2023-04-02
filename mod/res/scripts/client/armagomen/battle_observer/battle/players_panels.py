from account_helpers.settings_core.settings_constants import GRAPHICS
from armagomen.battle_observer.components.controllers.players_damage_controller import damage_controller
from armagomen.battle_observer.meta.battle.players_panels_meta import PlayersPanelsMeta
from armagomen.constants import VEHICLE, PANELS, COLORS
from armagomen.utils.common import logDebug
from armagomen.utils.keys_listener import g_keysListener
from gui.Scaleform.daapi.view.battle.shared.formatters import normalizeHealthPercent
from gui.battle_control.controllers.battle_field_ctrl import IBattleFieldListener


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
            if not self.settings[PANELS.BAR_CLASS_COLOR]:
                self.settingsCore.onSettingsApplied += self.onSettingsApplied
            if self.settings[PANELS.ON_KEY_DOWN]:
                g_keysListener.registerComponent(self.as_setHealthBarsVisibleS,
                                                 keyList=self.settings[PANELS.BAR_HOT_KEY])
        if self.damagesEnable:
            damage_controller.onPlayerDamaged += self.onPlayerDamaged
            g_keysListener.registerComponent(self.as_setPlayersDamageVisibleS,
                                             keyList=self.settings[PANELS.DAMAGES_HOT_KEY])

    def _dispose(self):
        self.flashObject.as_clearStorage()
        if self.hpBarsEnable and not self.settings[PANELS.BAR_CLASS_COLOR]:
            self.settingsCore.onSettingsApplied -= self.onSettingsApplied
        if self.damagesEnable:
            damage_controller.onPlayerDamaged -= self.onPlayerDamaged
        super(PlayersPanels, self)._dispose()

    def onSettingsApplied(self, diff):
        if GRAPHICS.COLOR_BLIND in diff:
            barColor = self.getBarColor(True, diff[GRAPHICS.COLOR_BLIND])
            self.as_colorBlindBarsS(barColor)

    def getBarColor(self, isEnemy, isColorBlind=None):
        colors = self.getColors()[COLORS.GLOBAL]
        if isEnemy:
            if isColorBlind is None:
                isColorBlind = self.isColorBlind()
            return colors[COLORS.ENEMY_BLIND_MAME if isColorBlind else COLORS.ENEMY_MAME]
        return colors[COLORS.ALLY_MAME]

    def createHealthBar(self, vehicleID, vInfoVO, isEnemy):
        max_health = vInfoVO.vehicleType.maxHealth
        if self.settings[PANELS.BAR_CLASS_COLOR]:
            color = self.getVehicleClassColor(vInfoVO.vehicleType.classTag)
        else:
            color = self.getBarColor(isEnemy)
        visible = not self.settings[PANELS.ON_KEY_DOWN]
        vehicle_data = {VEHICLE.CUR: max_health, VEHICLE.MAX: max_health, VEHICLE.PERCENT: 100}
        self.as_addHealthBarS(vehicleID, color, self.settings[PANELS.BAR_SETTINGS], visible)
        self.as_updateHealthBarS(vehicleID, 100, self.settings[PANELS.HP_TEMPLATE] % vehicle_data)

    def onAddedToStorage(self, vehicleID, isEnemy):
        """Called from flash after creation in as_AddVehIdToListS"""
        vInfoVO = self.getVehicleInfo(vehicleID)
        if vInfoVO.isObserver():
            return
        if self.hpBarsEnable and vInfoVO.isAlive():
            self.createHealthBar(vehicleID, vInfoVO, isEnemy)
        if isEnemy and self.settings[PANELS.SPOTTED_FIX]:
            self.as_setSpottedPositionS(vehicleID)
        if self.damagesEnable:
            self.as_addDamageS(vehicleID, self.settings[PANELS.DAMAGES_SETTINGS])
        logDebug("PlayersPanels onAddedToStorage: id={} enemy={}", vehicleID, isEnemy)

    def updateDeadVehicles(self, aliveAllies, deadAllies, aliveEnemies, deadEnemies):
        for vehicleID in aliveAllies.union(aliveEnemies):
            self.as_AddVehIdToListS(vehicleID, vehicleID in aliveEnemies)
        for vehicleID in deadAllies.union(deadEnemies):
            self.as_setVehicleDeadS(vehicleID)

    def updateVehicleHealth(self, vehicleID, newHealth, maxHealth):
        if self.hpBarsEnable:
            if newHealth > maxHealth:
                maxHealth = newHealth
            health_percent = normalizeHealthPercent(newHealth, maxHealth)
            vehicle_data = {VEHICLE.CUR: max(0, newHealth), VEHICLE.MAX: maxHealth, VEHICLE.PERCENT: health_percent}
            self.as_updateHealthBarS(vehicleID, health_percent, self.settings[PANELS.HP_TEMPLATE] % vehicle_data)

    def onPlayerDamaged(self, attackerID, damage):
        damage_text = self.settings[PANELS.DAMAGES_TEMPLATE] % {PANELS.DAMAGE: damage}
        self.as_updateDamageS(attackerID, damage_text)

from collections import defaultdict

from account_helpers.settings_core.settings_constants import GRAPHICS
from armagomen.battle_observer.core import keysParser
from armagomen.battle_observer.meta.battle.players_panels_meta import PlayersPanelsMeta
from armagomen.constants import VEHICLE, PANELS, COLORS, VEHICLE_TYPES
from armagomen.utils.common import getEntity
from gui.Scaleform.daapi.view.battle.shared.formatters import getHealthPercent
from gui.battle_control.controllers.battle_field_ctrl import IBattleFieldListener


class PlayersPanels(PlayersPanelsMeta, IBattleFieldListener):

    def __init__(self):
        super(PlayersPanels, self).__init__()
        self.hpBarsEnable = False
        self.damagesEnable = False
        self.damagesText = None
        self.playersDamage = defaultdict(int)

    def _populate(self):
        super(PlayersPanels, self)._populate()
        self.hpBarsEnable = self.settings[PANELS.BARS_ENABLED]
        self.damagesEnable = self.settings[PANELS.DAMAGES_ENABLED]
        self.damagesText = self.settings[PANELS.DAMAGES_TEMPLATE]
        keysParser.onKeyPressed += self.onKeyPressed
        if self.hpBarsEnable:
            if not self.settings[PANELS.BAR_CLASS_COLOR]:
                self.settingsCore.onSettingsApplied += self.onSettingsApplied
            if self.settings[PANELS.ON_KEY_DOWN]:
                keysParser.registerComponent(PANELS.BAR_HOT_KEY, self.settings[PANELS.BAR_HOT_KEY])
        if not self.damagesEnable:
            return
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onVehicleHealthChanged += self.onPlayersDamaged
            keysParser.registerComponent(PANELS.DAMAGES_HOT_KEY, self.settings[PANELS.DAMAGES_HOT_KEY])

    def onExitBattlePage(self):
        pass

    def onEnterBattlePage(self):
        pass

    def _dispose(self):
        self.flashObject.as_clearStorage()
        keysParser.onKeyPressed -= self.onKeyPressed
        if self.hpBarsEnable and not self.settings[PANELS.BAR_CLASS_COLOR]:
            self.settingsCore.onSettingsApplied -= self.onSettingsApplied
        if self.damagesEnable:
            arena = self._arenaVisitor.getArenaSubscription()
            if arena is not None:
                arena.onVehicleHealthChanged -= self.onPlayersDamaged
        super(PlayersPanels, self)._dispose()

    def clear(self):
        self.playersDamage.clear()

    def onKeyPressed(self, name, isKeyDown):
        if name is PANELS.BAR_HOT_KEY and self.hpBarsEnable:
            self.as_setHealthBarsVisibleS(isKeyDown)
        elif name is PANELS.DAMAGES_HOT_KEY and self.damagesEnable:
            self.as_setPlayersDamageVisibleS(isKeyDown)

    def onSettingsApplied(self, diff):
        if GRAPHICS.COLOR_BLIND in diff:
            barColor = self.getBarColor(True, diff[GRAPHICS.COLOR_BLIND])
            self.as_colorBlindBarsS(barColor)

    def getBarColor(self, isEnemy, isColorBlind=None):
        if isEnemy:
            if isColorBlind is None:
                isColorBlind = self.isColorBlind()
            return self.colors[COLORS.GLOBAL][COLORS.ENEMY_BLIND_MAME if isColorBlind else COLORS.ENEMY_MAME]
        return self.colors[COLORS.GLOBAL][COLORS.ALLY_MAME]

    def createHealthBar(self, vehicleID, vInfoVO, isEnemy):
        maxHealth = vInfoVO.vehicleType.maxHealth
        newHealth = getattr(getEntity(vehicleID), VEHICLE.CUR, maxHealth)
        if self.settings[PANELS.BAR_CLASS_COLOR]:
            color = self.vehicle_types[VEHICLE_TYPES.CLASS_COLORS][vInfoVO.vehicleType.classTag]
        else:
            color = self.getBarColor(isEnemy)
        self.as_addHealthBarS(vehicleID, color, self.colors[COLORS.GLOBAL],
                              self.settings[PANELS.BAR_SETTINGS], not self.settings[PANELS.ON_KEY_DOWN])
        scale = round(getHealthPercent(newHealth, maxHealth), 3)
        self.as_updateHealthBarS(vehicleID, scale,
                                 self.settings[PANELS.HP_TEMPLATE] % {
                                     VEHICLE.CUR: newHealth,
                                     VEHICLE.MAX: maxHealth,
                                     VEHICLE.PERCENT: scale * 100
                                 })

    def onAddedToStorage(self, vehicleID, isEnemy):
        """called from flash after creation in as_AddVehIdToListS"""
        vInfoVO = self._arenaDP.getVehicleInfo(vehicleID)
        if vInfoVO.isObserver():
            return
        if self.hpBarsEnable and vInfoVO.isAlive():
            self.createHealthBar(vehicleID, vInfoVO, isEnemy)
        if isEnemy and self.settings[PANELS.SPOTTED_FIX]:
            self.as_setSpottedPositionS(vehicleID)
        if self.damagesEnable:
            self.as_addDamageS(vehicleID, self.settings[PANELS.DAMAGES_SETTINGS])

    def updateDeadVehicles(self, aliveAllies, deadAllies, aliveEnemies, deadEnemies):
        for vehicleID in aliveAllies.union(aliveEnemies):
            self.as_AddVehIdToListS(vehicleID, vehicleID in aliveEnemies)
        for vehicleID in deadAllies.union(deadEnemies):
            self.as_setVehicleDeadS(vehicleID)

    def updateVehicleHealth(self, vehicleID, newHealth, maxHealth):
        if self.hpBarsEnable:
            scale = round(getHealthPercent(newHealth, maxHealth), 3)
            self.as_updateHealthBarS(vehicleID, scale,
                                     self.settings[PANELS.HP_TEMPLATE] % {
                                         VEHICLE.CUR: newHealth,
                                         VEHICLE.MAX: maxHealth,
                                         VEHICLE.PERCENT: scale * 100
                                     })

    def onPlayersDamaged(self, targetID, attackerID, damage):
        self.playersDamage[attackerID] += damage
        self.as_updateDamageS(attackerID, self.settings[PANELS.DAMAGES_TEMPLATE] % {
            PANELS.DAMAGE: self.playersDamage[attackerID]
        })

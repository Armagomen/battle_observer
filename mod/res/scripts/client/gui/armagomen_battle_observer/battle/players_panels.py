from account_helpers.settings_core.settings_constants import GRAPHICS
from gui.battle_control.controllers.battle_field_ctrl import IBattleFieldListener
from gui.shared.personality import ServicesLocator
from ..core import cfg, cache, keysParser
from ..core.bo_constants import VEHICLE, GLOBAL, PANELS, COLORS, VEHICLE_TYPES
from ..core.utils.common import getEntity
from ..meta.battle.players_panels_meta import PlayersPanelsMeta

config = cfg.players_panels


class PlayersPanels(PlayersPanelsMeta, IBattleFieldListener):
    settingsCore = ServicesLocator.settingsCore

    def __init__(self):
        super(PlayersPanels, self).__init__()
        isColorBlind = self.settingsCore.getSetting(GRAPHICS.COLOR_BLIND)
        self.barColors = config[PANELS.BAR_SETTINGS][PANELS.BAR][COLORS.NAME]
        self.COLORS = (self.barColors[PANELS.ALLY],
                       self.barColors[PANELS.BLIND if isColorBlind else PANELS.ENEMY])
        self.hp_text = config[PANELS.HP_TEMPLATE]
        self.vClassColors = cfg.vehicle_types[VEHICLE_TYPES.CLASS_COLORS]
        self.hpBarsEnable = config[PANELS.BARS_ENABLED]
        self.barsOnKey = config[PANELS.ON_KEY_DOWN]
        self.damagesEnable = config[PANELS.DAMAGES_ENABLED]
        self.damagesText = config[PANELS.DAMAGES_TEMPLATE]
        self.damagesSettings = config[PANELS.DAMAGES_SETTINGS]
        self.gui = self._arenaVisitor.gui
        self.battle_ctx = self.sessionProvider.getCtx()
        self._vehicles = set()

    def onEnterBattlePage(self):
        super(PlayersPanels, self).onEnterBattlePage()
        isInEpicRange = self.gui.isInEpicRange()
        isEpicRandomBattle = self.gui.isEpicRandomBattle()
        if not isInEpicRange and not isEpicRandomBattle:
            keysParser.onKeyPressed += self.onKeyPressed
            if self.hpBarsEnable:
                self.settingsCore.onSettingsApplied += self.onSettingsApplied
                if self.barsOnKey:
                    keysParser.registerComponent(PANELS.BAR_HOT_KEY, config[PANELS.BAR_HOT_KEY])
            if self.damagesEnable:
                arena = self.sessionProvider.arenaVisitor.getArenaSubscription()
                if arena is not None:
                    arena.onVehicleHealthChanged += self.onPlayersDamaged
                    keysParser.registerComponent(PANELS.DAMAGES_HOT_KEY, config[PANELS.DAMAGES_HOT_KEY])

    def onExitBattlePage(self):
        isInEpicRange = self.gui.isInEpicRange()
        isEpicRandomBattle = self.gui.isEpicRandomBattle()
        if not isInEpicRange and not isEpicRandomBattle:
            keysParser.onKeyPressed -= self.onKeyPressed
            if self.hpBarsEnable:
                self.settingsCore.onSettingsApplied -= self.onSettingsApplied
            if self.damagesEnable:
                arena = self.sessionProvider.arenaVisitor.getArenaSubscription()
                if arena is not None:
                    arena.onVehicleHealthChanged -= self.onPlayersDamaged
        super(PlayersPanels, self).onExitBattlePage()

    def onKeyPressed(self, name, show):
        if name == PANELS.BAR_HOT_KEY:
            self.healthOnAlt(show)
        elif name == PANELS.DAMAGES_HOT_KEY:
            self.as_setPlayersDamageVisibleS(show)

    def onSettingsApplied(self, diff):
        if GRAPHICS.COLOR_BLIND in diff:
            if config[PANELS.BAR_CLASS_COLOR]:
                return
            self.COLORS = (self.barColors[PANELS.ALLY],
                           self.barColors[PANELS.BLIND if diff[GRAPHICS.COLOR_BLIND] else PANELS.ENEMY])
            for vehicleID in self._vehicles:
                self.as_colorBlindPPbarsS(vehicleID, self.COLORS[self.battle_ctx.isEnemy(vehicleID)])

    def addVehicleToStorage(self, vehicleID):
        vInfoVO = self._arenaDP.getVehicleInfo(vehicleID)
        if vInfoVO.isObserver():
            return
        self._vehicles.add(vehicleID)
        is_enemy = self.battle_ctx.isEnemy(vehicleID)
        classTag = vInfoVO.vehicleType.classTag
        self.as_AddVehIdToListS(vehicleID)
        if config[PANELS.ICONS_ENABLED]:
            self.replaceIconColor(vehicleID, classTag, is_enemy)
        if self.hpBarsEnable and vInfoVO.isAlive():
            maxHealth = vInfoVO.vehicleType.maxHealth
            newHealth = getattr(getEntity(vehicleID), 'health', maxHealth)
            color = self.vClassColors[classTag] if config[PANELS.BAR_CLASS_COLOR] else self.COLORS[is_enemy]
            self.as_AddPPanelBarS(vehicleID, color, config[PANELS.BAR_SETTINGS], PANELS.TEAM[is_enemy],
                                  not self.barsOnKey)
            self.as_updatePPanelBarS(vehicleID, newHealth, maxHealth, self.hp_text % {
                VEHICLE.CUR: newHealth,
                VEHICLE.MAX: maxHealth,
                VEHICLE.PERCENT: self.getPercent(newHealth, maxHealth)
            })
        if self.damagesEnable:
            self.as_AddTextFieldS(vehicleID, PANELS.DAMAGES_TF, self.damagesSettings, PANELS.TEAM[is_enemy])

    def updateDeadVehicles(self, aliveAllies, deadAllies, aliveEnemies, deadEnemies):
        for vehicleID in aliveAllies:
            if vehicleID not in self._vehicles:
                self.addVehicleToStorage(vehicleID)
        for vehicleID in aliveEnemies:
            if vehicleID not in self._vehicles:
                self.addVehicleToStorage(vehicleID)
        if self.hpBarsEnable:
            for vehicleID in deadAllies:
                self.onVehicleKilled(vehicleID)
            for vehicleID in deadEnemies:
                self.onVehicleKilled(vehicleID)

    def onVehicleKilled(self, targetID):
        if targetID in self._vehicles:
            self._vehicles.remove(targetID)
            self.as_updatePPanelBarS(targetID, GLOBAL.ZERO, GLOBAL.ZERO, GLOBAL.EMPTY_LINE)

    @staticmethod
    def getPercent(current, maximum):
        if current > GLOBAL.ZERO:
            return float(current) / maximum * 100
        else:
            return GLOBAL.F_ZERO

    def replaceIconColor(self, vehicleID, classTag, enemy):
        self.as_setVehicleIconColorS(vehicleID, self.vClassColors[classTag], config[PANELS.BLACKOUT], enemy)

    def healthOnAlt(self, enable):
        if self.hpBarsEnable:
            for vehicleID in self._vehicles:
                self.as_setHPbarsVisibleS(vehicleID, enable)

    def updateVehicleHealth(self, vehicleID, newHealth, maxHealth):
        if self.hpBarsEnable:
            if vehicleID not in self._vehicles:
                self.addVehicleToStorage(vehicleID)
            else:
                self.as_updatePPanelBarS(vehicleID, newHealth, maxHealth, self.hp_text % {
                    VEHICLE.CUR: newHealth,
                    VEHICLE.MAX: maxHealth,
                    VEHICLE.PERCENT: self.getPercent(newHealth, maxHealth)
                })

    def onPlayersDamaged(self, vehicleID, attackerID, damage):
        cache.playersDamage[attackerID] += damage
        self.as_updateTextFieldS(attackerID, PANELS.DAMAGES_TF,
                                 self.damagesText % {PANELS.DAMAGE: cache.playersDamage[attackerID]})

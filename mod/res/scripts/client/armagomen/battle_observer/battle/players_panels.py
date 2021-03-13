from collections import defaultdict

from account_helpers.settings_core.settings_constants import GRAPHICS
from armagomen.battle_observer.core import config, keysParser
from armagomen.battle_observer.core.bo_constants import VEHICLE, GLOBAL, PANELS, COLORS, VEHICLE_TYPES
from armagomen.battle_observer.meta.battle.players_panels_meta import PlayersPanelsMeta
from armagomen.utils.common import getEntity
from gui.battle_control.controllers.battle_field_ctrl import IBattleFieldListener
from gui.shared.personality import ServicesLocator



class PlayersPanels(PlayersPanelsMeta, IBattleFieldListener):
    settingsCore = ServicesLocator.settingsCore

    def __init__(self):
        super(PlayersPanels, self).__init__()
        isColorBlind = self.settingsCore.getSetting(GRAPHICS.COLOR_BLIND)
        self.barColors = config.colors[COLORS.GLOBAL]
        self.COLORS = (self.barColors[COLORS.ALLY_MAME],
                       self.barColors[COLORS.ENEMY_BLIND_MAME if isColorBlind else COLORS.ENEMY_MAME])
        self.vClassColors = config.vehicle_types[VEHICLE_TYPES.CLASS_COLORS]
        self.hpBarsEnable = config.players_panels[PANELS.BARS_ENABLED]
        self.damagesEnable = config.players_panels[PANELS.DAMAGES_ENABLED]
        self.damagesText = config.players_panels[PANELS.DAMAGES_TEMPLATE]
        self.damagesSettings = config.players_panels[PANELS.DAMAGES_SETTINGS]
        self.battle_ctx = self.sessionProvider.getCtx()
        self._vehicles = set()
        self.playersDamage = defaultdict(int)

    def onEnterBattlePage(self):
        super(PlayersPanels, self).onEnterBattlePage()
        isInEpicRange = self._arenaVisitor.gui.isInEpicRange()
        isEpicRandomBattle = self._arenaVisitor.gui.isEpicRandomBattle()
        if not isInEpicRange and not isEpicRandomBattle:
            keysParser.onKeyPressed += self.onKeyPressed
            if self.hpBarsEnable:
                self.settingsCore.onSettingsApplied += self.onSettingsApplied
                if config.players_panels[PANELS.ON_KEY_DOWN]:
                    keysParser.registerComponent(PANELS.BAR_HOT_KEY, config.players_panels[PANELS.BAR_HOT_KEY])
            if self.damagesEnable:
                arena = self._arenaVisitor.getArenaSubscription()
                if arena is not None:
                    arena.onVehicleHealthChanged += self.onPlayersDamaged
                    keysParser.registerComponent(PANELS.DAMAGES_HOT_KEY, config.players_panels[PANELS.DAMAGES_HOT_KEY])

    def onExitBattlePage(self):
        isInEpicRange = self._arenaVisitor.gui.isInEpicRange()
        isEpicRandomBattle = self._arenaVisitor.gui.isEpicRandomBattle()
        if not isInEpicRange and not isEpicRandomBattle:
            keysParser.onKeyPressed -= self.onKeyPressed
            if self.hpBarsEnable:
                self.settingsCore.onSettingsApplied -= self.onSettingsApplied
            if self.damagesEnable:
                self.playersDamage.clear()
                arena = self._arenaVisitor.getArenaSubscription()
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
            if config.players_panels[PANELS.BAR_CLASS_COLOR]:
                return
            self.COLORS = (self.barColors[COLORS.ALLY_MAME],
                           self.barColors[COLORS.ENEMY_BLIND_MAME if diff[GRAPHICS.COLOR_BLIND] else COLORS.ENEMY_MAME])
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
        if config.players_panels[PANELS.ICONS_ENABLED]:
            self.replaceIconColor(vehicleID, classTag, is_enemy)
        if self.hpBarsEnable and vInfoVO.isAlive():
            maxHealth = vInfoVO.vehicleType.maxHealth
            newHealth = getattr(getEntity(vehicleID), 'health', maxHealth)
            if config.players_panels[PANELS.BAR_CLASS_COLOR]:
                color = self.vClassColors[classTag]
            else:
                color = self.COLORS[is_enemy]
            self.as_AddPPanelBarS(vehicleID, color, config.colors[COLORS.GLOBAL],
                                  config.players_panels[PANELS.BAR_SETTINGS], PANELS.TEAM[is_enemy],
                                  not config.players_panels[PANELS.ON_KEY_DOWN])
            self.as_updatePPanelBarS(vehicleID, newHealth, maxHealth, config.players_panels[PANELS.HP_TEMPLATE] % {
                VEHICLE.CUR: newHealth,
                VEHICLE.MAX: maxHealth,
                VEHICLE.PERCENT: self.getPercent(newHealth, maxHealth)
            })
        if is_enemy and config.players_panels[PANELS.SPOTTED_FIX]:
            self.as_setSpottedPositionS(vehicleID)
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
        self.as_setVehicleIconColorS(vehicleID, self.vClassColors[classTag],
                                     config.players_panels[PANELS.ICONS_BLACKOUT], enemy)

    def healthOnAlt(self, enable):
        if self.hpBarsEnable:
            for vehicleID in self._vehicles:
                self.as_setHPbarsVisibleS(vehicleID, enable)

    def updateVehicleHealth(self, vehicleID, newHealth, maxHealth):
        if self.hpBarsEnable:
            if vehicleID not in self._vehicles:
                self.addVehicleToStorage(vehicleID)
            else:
                self.as_updatePPanelBarS(vehicleID, newHealth, maxHealth, config.players_panels[PANELS.HP_TEMPLATE] % {
                    VEHICLE.CUR: newHealth,
                    VEHICLE.MAX: maxHealth,
                    VEHICLE.PERCENT: self.getPercent(newHealth, maxHealth)
                })

    def onPlayersDamaged(self, vehicleID, attackerID, damage):
        self.playersDamage[attackerID] += damage
        self.as_updateTextFieldS(attackerID, PANELS.DAMAGES_TF,
                                 self.damagesText % {PANELS.DAMAGE: self.playersDamage[attackerID]})

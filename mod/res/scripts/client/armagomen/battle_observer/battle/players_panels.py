from collections import defaultdict

from account_helpers.settings_core.settings_constants import GRAPHICS
from armagomen.battle_observer.core import keysParser
from armagomen.battle_observer.meta.battle.players_panels_meta import PlayersPanelsMeta
from armagomen.battle_observer.statistics.statistic_data_loader import getWTRRating
from armagomen.battle_observer.statistics.statistic_wtr import getStatisticString
from armagomen.constants import VEHICLE, GLOBAL, PANELS, COLORS, VEHICLE_TYPES
from armagomen.utils.common import getEntity
from gui.Scaleform.daapi.view.battle.shared.formatters import getHealthPercent
from gui.battle_control.controllers.battle_field_ctrl import IBattleFieldListener


class PlayersPanels(PlayersPanelsMeta, IBattleFieldListener):

    def __init__(self):
        super(PlayersPanels, self).__init__()
        self.barColors = None
        self.COLORS = None
        self.vehicleColor = None
        self.hpBarsEnable = False
        self.damagesEnable = False
        self.damagesText = None
        self.damagesSettings = None
        self.ratings = None
        self.battle_ctx = self.sessionProvider.getCtx()
        self.isEpicRandomBattle = self._arenaVisitor.gui.isEpicRandomBattle()
        self._vehicles = set()
        self.playersDamage = defaultdict(int)

    def _populate(self):
        super(PlayersPanels, self)._populate()
        isColorBlind = self.settingsCore.getSetting(GRAPHICS.COLOR_BLIND)
        self.hpBarsEnable = self.settings[PANELS.BARS_ENABLED] and not self.isEpicRandomBattle
        self.damagesEnable = self.settings[PANELS.DAMAGES_ENABLED]
        self.damagesText = self.settings[PANELS.DAMAGES_TEMPLATE]
        self.damagesSettings = self.settings[PANELS.DAMAGES_SETTINGS]
        self.statisticSettings = self.settings[PANELS.STATISTIC_SETTINGS]
        self.barColors = self.colors[COLORS.GLOBAL]
        self.COLORS = (self.barColors[COLORS.ALLY_MAME],
                       self.barColors[COLORS.ENEMY_BLIND_MAME if isColorBlind else COLORS.ENEMY_MAME])
        self.vehicleColor = self.vehicle_types[VEHICLE_TYPES.CLASS_COLORS]
        isInEpicRange = self._arenaVisitor.gui.isInEpicRange()
        if isInEpicRange or self.isEpicRandomBattle:
            return
        keysParser.onKeyPressed += self.onKeyPressed
        if self.hpBarsEnable:
            self.settingsCore.onSettingsApplied += self.onSettingsApplied
            if self.settings[PANELS.ON_KEY_DOWN]:
                keysParser.registerComponent(PANELS.BAR_HOT_KEY, self.settings[PANELS.BAR_HOT_KEY])
        if self.settings[PANELS.STATISTIC_ENABLE]:
            self.ratings = getWTRRating(vInfo.player.accountDBID for vInfo in self._arenaDP.getVehiclesInfoIterator())
        if not self.damagesEnable:
            return
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onVehicleHealthChanged += self.onPlayersDamaged
            keysParser.registerComponent(PANELS.DAMAGES_HOT_KEY,
                                         self.settings[PANELS.DAMAGES_HOT_KEY])

    def _dispose(self):
        self._vehicles.clear()
        self.flashObject.as_clearStorage()
        isInEpicRange = self._arenaVisitor.gui.isInEpicRange()
        if not isInEpicRange and not self.isEpicRandomBattle:
            keysParser.onKeyPressed -= self.onKeyPressed
            if self.hpBarsEnable:
                self.settingsCore.onSettingsApplied -= self.onSettingsApplied
            if self.damagesEnable:
                self.playersDamage.clear()
                arena = self._arenaVisitor.getArenaSubscription()
                if arena is not None:
                    arena.onVehicleHealthChanged -= self.onPlayersDamaged
        super(PlayersPanels, self)._dispose()

    def onKeyPressed(self, name, isKeyDown):
        if name == PANELS.BAR_HOT_KEY:
            self.healthOnAlt(isKeyDown)
        elif name == PANELS.DAMAGES_HOT_KEY:
            self.as_setPlayersDamageVisibleS(isKeyDown)

    def onSettingsApplied(self, diff):
        if GRAPHICS.COLOR_BLIND in diff:
            if self.settings[PANELS.BAR_CLASS_COLOR]:
                return
            self.COLORS = (self.barColors[COLORS.ALLY_MAME],
                           self.barColors[COLORS.ENEMY_BLIND_MAME if diff[GRAPHICS.COLOR_BLIND] else COLORS.ENEMY_MAME])
            for vehicleID in self._vehicles:
                self.as_colorBlindPPbarsS(vehicleID, self.COLORS[self.battle_ctx.isEnemy(vehicleID)])

    def onAddedToStorage(self, vehicleID, isEnemy):
        """called from flash after creation in as_AddVehIdToListS"""
        if vehicleID in self._vehicles:
            return
        vInfoVO = self._arenaDP.getVehicleInfo(vehicleID)
        if vInfoVO.isObserver():
            return
        self._vehicles.add(vehicleID)
        classTag = vInfoVO.vehicleType.classTag
        if self.settings[PANELS.ICONS_ENABLED]:
            self.replaceIconColor(vehicleID, classTag, isEnemy)
        if self.hpBarsEnable and vInfoVO.isAlive():
            maxHealth = vInfoVO.vehicleType.maxHealth
            newHealth = getattr(getEntity(vehicleID), 'health', maxHealth)
            if self.settings[PANELS.BAR_CLASS_COLOR]:
                color = self.vehicleColor[classTag]
            else:
                color = self.COLORS[isEnemy]
            self.as_AddPPanelBarS(vehicleID, color, self.colors[COLORS.GLOBAL],
                                  self.settings[PANELS.BAR_SETTINGS], PANELS.TEAM[isEnemy],
                                  not self.settings[PANELS.ON_KEY_DOWN])
            scale = round(getHealthPercent(newHealth, maxHealth), 3)
            self.as_updatePPanelBarS(vehicleID, scale,
                                     self.settings[PANELS.HP_TEMPLATE] % {
                                         VEHICLE.CUR: newHealth,
                                         VEHICLE.MAX: maxHealth,
                                         VEHICLE.PERCENT: scale * 100
                                     })
        if isEnemy and self.settings[PANELS.SPOTTED_FIX]:
            self.as_setSpottedPositionS(vehicleID)
        if self.damagesEnable:
            self.as_AddTextFieldS(vehicleID, PANELS.DAMAGES_TF, self.damagesSettings, PANELS.TEAM[isEnemy])
        if self.ratings and vInfoVO.player.accountDBID:
            self.as_AddTextFieldS(vehicleID, "WTR", self.statisticSettings, PANELS.TEAM[isEnemy])
            self.as_updateTextFieldS(vehicleID, "WTR", getStatisticString(self.ratings[vInfoVO.player.accountDBID]))

    def updateDeadVehicles(self, aliveAllies, deadAllies, aliveEnemies, deadEnemies):
        for vehicleID in aliveAllies.union(aliveEnemies).difference(self._vehicles):
            self.as_AddVehIdToListS(vehicleID, vehicleID in aliveEnemies)
        if self.hpBarsEnable:
            for vehicleID in deadAllies.union(deadEnemies):
                self.onVehicleKilled(vehicleID)

    def onVehicleKilled(self, targetID):
        if targetID in self._vehicles:
            self.as_updatePPanelBarS(targetID, GLOBAL.ZERO, GLOBAL.EMPTY_LINE)

    def replaceIconColor(self, vehicleID, classTag, enemy):
        self.as_setVehicleIconColorS(vehicleID, self.vehicleColor[classTag],
                                     self.settings[PANELS.ICONS_BLACKOUT], enemy)

    def healthOnAlt(self, enable):
        if self.hpBarsEnable:
            for vehicleID in self._vehicles:
                self.as_setHPbarsVisibleS(vehicleID, enable)

    def updateVehicleHealth(self, vehicleID, newHealth, maxHealth):
        if vehicleID not in self._vehicles:
            self.as_AddVehIdToListS(vehicleID, self.battle_ctx.isEnemy(vehicleID))
        elif self.hpBarsEnable:
            scale = round(getHealthPercent(newHealth, maxHealth), 3)
            self.as_updatePPanelBarS(vehicleID, scale,
                                     self.settings[PANELS.HP_TEMPLATE] % {
                                         VEHICLE.CUR: newHealth,
                                         VEHICLE.MAX: maxHealth,
                                         VEHICLE.PERCENT: scale * 100
                                     })

    def onPlayersDamaged(self, targetID, attackerID, damage):
        self.playersDamage[attackerID] += damage
        self.as_updateTextFieldS(attackerID, PANELS.DAMAGES_TF,
                                 self.damagesText % {PANELS.DAMAGE: self.playersDamage[attackerID]})

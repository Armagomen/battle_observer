from account_helpers.settings_core.settings_constants import GRAPHICS
from gui.battle_control.controllers.battle_field_ctrl import IBattleFieldListener
from gui.shared.personality import ServicesLocator
from ..core.battle_cache import cache
from ..core.bo_constants import VEHICLE, GLOBAL, PANELS, COLORS, VEHICLE_TYPES
from ..core.config import cfg
from ..core.events import g_events
from ..core.keys_parser import g_keysParser
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
        self.gui = self.sessionProvider.arenaVisitor.gui
        self.battle_ctx = self.sessionProvider.getCtx()
        self.observers = set()
        self._vehicles = dict()

    def onEnterBattlePage(self):
        super(PlayersPanels, self).onEnterBattlePage()
        isInEpicRange = self.gui.isInEpicRange()
        isEpicRandomBattle = self.gui.isEpicRandomBattle()
        if not isInEpicRange and not isEpicRandomBattle:
            arena = self.sessionProvider.arenaVisitor.getArenaSubscription()
            if self.hpBarsEnable:
                if arena is not None:
                    arena.onVehicleKilled += self.onVehicleKilled
                if self.barsOnKey:
                    g_keysParser.registerComponent(PANELS.BAR_HOT_KEY, config[PANELS.BAR_HOT_KEY])
            g_events.onKeyPressed += self.onKeyPressed
            self.settingsCore.onSettingsApplied += self.onSettingsApplied
            g_events.onVehicleAddUpdate += self.onVehicleAdd
            if self.damagesEnable:
                if arena is not None:
                    arena.onVehicleHealthChanged += self.onPlayersDamaged
                    g_keysParser.registerComponent(PANELS.DAMAGES_HOT_KEY, config[PANELS.DAMAGES_HOT_KEY])
            g_events.updateStatus += self.updateStatus
            self.updateLinks()

    def onExitBattlePage(self):
        isInEpicRange = self.gui.isInEpicRange()
        isEpicRandomBattle = self.gui.isEpicRandomBattle()
        if not isInEpicRange and not isEpicRandomBattle:
            arena = self.sessionProvider.arenaVisitor.getArenaSubscription()
            g_events.updateStatus -= self.updateStatus
            if self.hpBarsEnable:
                if arena is not None:
                    arena.onVehicleKilled -= self.onVehicleKilled
            g_events.onKeyPressed -= self.onKeyPressed
            self.settingsCore.onSettingsApplied -= self.onSettingsApplied
            g_events.onVehicleAddUpdate -= self.onVehicleAdd
            if self.damagesEnable:
                if arena is not None:
                    arena.onVehicleHealthChanged -= self.onPlayersDamaged
        super(PlayersPanels, self).onExitBattlePage()

    def onKeyPressed(self, name, show):
        if name == PANELS.BAR_HOT_KEY:
            self.healthOnAlt(show)
        elif name == PANELS.DAMAGES_HOT_KEY:
            self.as_setPlayersDamageVisibleS(show)

    def onSettingsApplied(self, diff):
        if self.hpBarsEnable:
            if GRAPHICS.COLOR_BLIND in diff:
                if config[PANELS.BAR_CLASS_COLOR]:
                    return
                self.COLORS = (self.barColors[PANELS.ALLY],
                               self.barColors[PANELS.BLIND if diff[GRAPHICS.COLOR_BLIND] else PANELS.ENEMY])
                for vehicleID in self._vehicles:
                    self.as_colorBlindPPbarsS(vehicleID, self.COLORS[self.battle_ctx.isEnemy(vehicleID)])

    def onVehicleAdd(self, vehicleID, vehicleType):
        if vehicleID in self.observers or vehicleID in self._vehicles:
            return
        self.as_AddVehIdToListS(vehicleID)
        is_enemy = self.battle_ctx.isEnemy(vehicleID)
        if config[PANELS.ICONS_ENABLED]:
            self.replaceIconColor(vehicleID, vehicleType.classTag, is_enemy)
        if self.hpBarsEnable:
            self.createHPBar(vehicleID, vehicleType, is_enemy)
        if self.damagesEnable:
            self.as_AddTextFieldS(vehicleID, PANELS.DAMAGES_TF, self.damagesSettings, PANELS.TEAM[is_enemy])

    def onVehicleKilled(self, targetID, *args, **kwargs):
        vehicle = self._vehicles.get(targetID)
        if vehicle is not None:
            vehicle[VEHICLE.CUR] = GLOBAL.ZERO
            self.as_updatePPanelBarS(targetID, GLOBAL.ZERO, vehicle[VEHICLE.MAX], self.hp_text % vehicle)

    @staticmethod
    def getPercent(current, maximum):
        if current > GLOBAL.ZERO:
            return float(current) / maximum * 100
        else:
            return GLOBAL.F_ZERO

    def createHPBar(self, vehicleID, vehicleType, enemy):
        maxHealth = vehicleType.maxHealth
        vehicle = self._vehicles.setdefault(vehicleID, {})
        if not vehicle:
            vehicle[VEHICLE.MAX] = maxHealth
            vehicle[VEHICLE.PERCENT] = 100.0
            vehicle[VEHICLE.CUR] = maxHealth
        color = self.vClassColors[vehicleType.classTag] if config[PANELS.BAR_CLASS_COLOR] else self.COLORS[enemy]
        self.as_AddPPanelBarS(vehicleID, color, config[PANELS.BAR_SETTINGS], PANELS.TEAM[enemy], not self.barsOnKey)
        self.as_updatePPanelBarS(vehicleID, maxHealth, maxHealth, self.hp_text % self._vehicles[vehicleID])

    def replaceIconColor(self, vehicleID, classTag, enemy):
        self.as_setVehicleIconColorS(vehicleID, self.vClassColors[classTag], config[PANELS.BLACKOUT], enemy)

    def updateLinks(self):
        for vInfoVO in cache.arenaDP.getVehiclesInfoIterator():
            if vInfoVO.isObserver():
                self.observers.add(vInfoVO.vehicleID)
            else:
                self.onVehicleAdd(vInfoVO.vehicleID, vInfoVO.vehicleType)

    def healthOnAlt(self, enable):
        for vehicleID, vehicle in self._vehicles.iteritems():
            self.as_setHPbarsVisibleS(vehicleID, enable and vehicle[VEHICLE.CUR])

    def updateVehicleHealth(self, vehicleID, newHealth, maxHealth):
        vehicle = self._vehicles.get(vehicleID)
        if vehicle is None:
            return
        vehicle[VEHICLE.PERCENT] = self.getPercent(newHealth, maxHealth)
        vehicle[VEHICLE.CUR] = newHealth
        self.as_updatePPanelBarS(vehicleID, newHealth, maxHealth, self.hp_text % vehicle)

    def updateStatus(self, controller, info):
        vehicleID = info[PANELS.VEHICLE_ID]
        if config[PANELS.ICONS_ENABLED]:
            if vehicleID in self.observers:
                return
            class_tag = cache.arenaDP.getVehicleInfo(vehicleID).vehicleType.classTag
            self.replaceIconColor(vehicleID, class_tag, info[PANELS.IS_ENEMY])

    def onPlayersDamaged(self, vehicleID, attackerID, damage):
        cache.playersDamage[attackerID] += damage
        self.as_updateTextFieldS(attackerID, PANELS.DAMAGES_TF,
                                 self.damagesText % {PANELS.DAMAGE: cache.playersDamage[attackerID]})

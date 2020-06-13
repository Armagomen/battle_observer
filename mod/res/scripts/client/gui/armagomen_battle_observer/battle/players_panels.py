from account_helpers.settings_core.settings_constants import GRAPHICS
from gui.shared.personality import ServicesLocator

from ..core.battle_cache import cache, g_health
from ..core.bo_constants import VEHICLE, GLOBAL, PANELS, COLORS, VEHICLE_TYPES
from ..core.config import cfg
from ..core.events import g_events
from ..core.keys_parser import g_keysParser
from ..meta.battle.players_panels_meta import PlayersPanelsMeta

spotted = cfg.players_spotted
bars = cfg.players_bars
damages = cfg.players_damages
icon = cfg.panels_icon


class PlayersPanels(PlayersPanelsMeta):
    settingsCore = ServicesLocator.settingsCore

    def __init__(self):
        super(PlayersPanels, self).__init__()
        isColorBlind = self.settingsCore.getSetting(GRAPHICS.COLOR_BLIND)
        self.isInAoIEnabled = spotted[GLOBAL.ENABLED]
        self.isInAoISettings = spotted[GLOBAL.SETTINGS]
        self.barColors = bars[PANELS.BAR_SETTINGS][PANELS.BAR][COLORS.NAME]
        self.COLORS = (self.barColors[PANELS.ALLY],
                       self.barColors[PANELS.BLIND if isColorBlind else PANELS.ENEMY])
        self.SPOTTED_STATUS = (spotted[PANELS.STATUS][PANELS.NOT_LIGHT], spotted[PANELS.STATUS][PANELS.LIGHTS])
        self.hp_text = bars[PANELS.HP_TEMPLATE]
        self.vClassColors = cfg.vehicle_types[VEHICLE_TYPES.CLASS_COLORS]
        self.hpBarsEnable = bars[GLOBAL.ENABLED]
        self.barsOnKey = bars[PANELS.ON_KEY_DOWN]
        self.damagesEnable = damages[GLOBAL.ENABLED]
        self.damagesText = damages[PANELS.DAMAGES_TEMPLATE]
        self.damagesSettings = damages[PANELS.DAMAGES_SETTINGS]
        self.gui = self.sessionProvider.arenaVisitor.gui
        self.battle_ctx = self.sessionProvider.getCtx()
        self.storage = set()

    def onEnterBattlePage(self):
        super(PlayersPanels, self).onEnterBattlePage()
        isInEpicRange = self.gui.isInEpicRange()
        isEpicRandomBattle = self.gui.isEpicRandomBattle()
        if not isInEpicRange and not isEpicRandomBattle:
            if self.hpBarsEnable:
                g_events.updateHealthPoints += self.updateHealthPoints
                if self.barsOnKey:
                    g_keysParser.registerComponent(PANELS.BAR_HOT_KEY, bars[PANELS.BAR_HOT_KEY])
            g_events.onKeyPressed += self.onKeyPressed
            self.settingsCore.onSettingsApplied += self.onSettingsApplied
            g_events.onVehicleAddPanels += self.onVehicleAdd
            if self.damagesEnable:
                g_events.onPlayersDamaged += self.onPlayersDamaged
                g_keysParser.registerComponent(PANELS.DAMAGES_HOT_KEY, damages[PANELS.DAMAGES_HOT_KEY])
            if self.isInAoIEnabled:
                g_events.setInAoI += self.setInAoI
            g_events.updateStatus += self.updateStatus
            self.updateLinks()

    def onExitBattlePage(self):
        isInEpicRange = self.gui.isInEpicRange()
        isEpicRandomBattle = self.gui.isEpicRandomBattle()
        if not isInEpicRange and not isEpicRandomBattle:
            if self.isInAoIEnabled:
                g_events.setInAoI -= self.setInAoI
            g_events.updateStatus -= self.updateStatus
            if self.hpBarsEnable:
                g_events.updateHealthPoints -= self.updateHealthPoints
            g_events.onKeyPressed -= self.onKeyPressed
            self.settingsCore.onSettingsApplied -= self.onSettingsApplied
            g_events.onVehicleAddPanels -= self.onVehicleAdd
            if self.damagesEnable:
                g_events.onPlayersDamaged -= self.onPlayersDamaged
        self.storage.clear()
        super(PlayersPanels, self).onExitBattlePage()

    def onKeyPressed(self, name, show):
        if name == PANELS.BAR_HOT_KEY:
            self.healthOnAlt(show)
        elif name == PANELS.DAMAGES_HOT_KEY:
            self.as_setPlayersDamageVisibleS(show)

    def onVehicleKilled(self, targetID):
        if self.isInAoIEnabled:
            self.as_updateTextFieldS(targetID, PANELS.IN_AOI, GLOBAL.EMPTY_LINE)

    def onSettingsApplied(self, diff):
        if self.hpBarsEnable:
            if GRAPHICS.COLOR_BLIND in diff:
                if bars[PANELS.BAR_CLASS_COLOR]:
                    return
                self.COLORS = (self.barColors[PANELS.ALLY],
                               self.barColors[PANELS.BLIND if diff[GRAPHICS.COLOR_BLIND] else PANELS.ENEMY])
                for vehicleID in g_health.cache:
                    self.as_colorBlindPPbarsS(vehicleID, self.COLORS[self.battle_ctx.isEnemy(vehicleID)])

    def setInAoI(self, plugin, entry, isInAoI):
        if entry._isEnemy and entry._isAlive:
            for vehicleID, vehicle in plugin._entries.iteritems():
                if entry._entryID == vehicle._entryID:
                    self.as_updateTextFieldS(vehicleID, PANELS.IN_AOI, self.SPOTTED_STATUS[isInAoI])
                    break

    def onVehicleAdd(self, vehicleID, vehicleType):
        if vehicleID in cache.observers or vehicleID in self.storage:
            return
        self.storage.add(vehicleID)
        self.as_AddVehIdToListS(vehicleID)
        is_enemy = self.battle_ctx.isEnemy(vehicleID)
        if self.isInAoIEnabled:
            self.createInAoIField(vehicleID, is_enemy)
        if self.hpBarsEnable or icon[GLOBAL.ENABLED]:
            if icon[GLOBAL.ENABLED]:
                self.paintingIcon(vehicleID, vehicleType.classTag, is_enemy)
            if self.hpBarsEnable:
                self.createHPBar(vehicleID, vehicleType.classTag, is_enemy)
        if self.damagesEnable:
            self.as_AddTextFieldS(vehicleID, PANELS.DAMAGES_TF, self.damagesSettings, PANELS.TEAM[is_enemy])

    def createInAoIField(self, vehicleID, enemy):
        self.as_AddTextFieldS(vehicleID, PANELS.IN_AOI, self.isInAoISettings, PANELS.TEAM[enemy])

    @staticmethod
    def getPercent(current, maximum):
        return float(current) / maximum * 100

    def createHPBar(self, vehicleID, classTag, enemy):
        vehicle = g_health.getVehicle(vehicleID)
        _max = vehicle[VEHICLE.MAX]
        curr = vehicle[VEHICLE.CUR]
        vehicle[VEHICLE.PERCENT] = self.getPercent(curr, _max)
        color = self.vClassColors[classTag] if bars[PANELS.BAR_CLASS_COLOR] else self.COLORS[enemy]
        self.as_AddPPanelBarS(vehicleID, color, bars[PANELS.BAR_SETTINGS], PANELS.TEAM[enemy], not self.barsOnKey)
        self.as_updatePPanelBarS(vehicleID, curr, _max, self.hp_text % vehicle)

    def paintingIcon(self, vehicleID, classTag, enemy):
        self.as_setVehicleIconColorS(vehicleID, self.vClassColors[classTag], icon[PANELS.BLACKOUT], enemy)

    def updateLinks(self):
        for vInfoVO in cache.arenaDP.getVehiclesInfoIterator():
            if vInfoVO.vehicleID in cache.observers:
                continue
            self.onVehicleAdd(vInfoVO.vehicleID, vInfoVO.vehicleType)

    def healthOnAlt(self, enable):
        for vehicleID, vehicle in g_health.cache.iteritems():
            self.as_setHPbarsVisibleS(vehicleID, enable and vehicle[VEHICLE.CUR])

    def updateHealthPoints(self, team, team_current, team_maximum, vehicle_id, vehicle):
        curr, _max = vehicle[VEHICLE.CUR], vehicle[VEHICLE.MAX]
        vehicle[VEHICLE.PERCENT] = self.getPercent(curr, _max)
        self.as_updatePPanelBarS(vehicle_id, curr, _max, self.hp_text % vehicle)

    def updateStatus(self, controller, info):
        vehicle_id = info[PANELS.VEHICLE_ID]
        if icon[GLOBAL.ENABLED]:
            if vehicle_id in cache.observers:
                return
            class_tag = cache.arenaDP.getVehicleInfo(vehicle_id).vehicleType.classTag
            self.paintingIcon(vehicle_id, class_tag, info[PANELS.IS_ENEMY])
        if info[PANELS.STATUS] == PANELS.KILLED_STATUS:
            self.onVehicleKilled(vehicle_id)

    def onPlayersDamaged(self, attackerID):
        self.as_updateTextFieldS(attackerID, PANELS.DAMAGES_TF,
                                 self.damagesText % {PANELS.DAMAGE: cache.playersDamage[attackerID]})

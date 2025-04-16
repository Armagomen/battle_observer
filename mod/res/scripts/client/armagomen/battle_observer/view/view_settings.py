from armagomen._constants import BATTLE_ALIASES, BATTLES_RANGE, CLOCK, FLIGHT_TIME, GLOBAL, IS_WG_CLIENT, MINIMAP, STATISTICS
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import xvmInstalled
from armagomen.utils.logging import logDebug, logInfo

if IS_WG_CLIENT:
    from frontline.gui.Scaleform.daapi.view.battle.frontline_battle_page import _NEVER_HIDE, _STATE_TO_UI, PageStates
else:
    from gui.Scaleform.daapi.view.battle.epic.page import _NEVER_HIDE, _STATE_TO_UI, PageStates
from gui.battle_control.battle_constants import BATTLE_CTRL_ID
from gui.Scaleform.daapi.view.battle.shared.page import ComponentsConfig
from gui.Scaleform.genConsts.BATTLE_VIEW_ALIASES import BATTLE_VIEW_ALIASES
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider

ALIASES_TO_HIDE = (
    (BATTLE_ALIASES.DEBUG, BATTLE_VIEW_ALIASES.DEBUG_PANEL),
    (BATTLE_ALIASES.SIXTH_SENSE, BATTLE_VIEW_ALIASES.SIXTH_SENSE),
    (BATTLE_ALIASES.TEAM_BASES, BATTLE_VIEW_ALIASES.TEAM_BASES_PANEL),
    (BATTLE_ALIASES.TIMER, BATTLE_VIEW_ALIASES.BATTLE_TIMER)
)

ALIAS_TO_CTRL = {
    BATTLE_ALIASES.DATE_TIME: BATTLE_CTRL_ID.ARENA_PERIOD,
    BATTLE_ALIASES.DEBUG: BATTLE_CTRL_ID.DEBUG,
    BATTLE_ALIASES.HP_BARS: BATTLE_CTRL_ID.BATTLE_FIELD_CTRL,
    BATTLE_ALIASES.MAIN_GUN: BATTLE_CTRL_ID.BATTLE_FIELD_CTRL,
    BATTLE_ALIASES.OWN_HEALTH: BATTLE_CTRL_ID.PREBATTLE_SETUPS_CTRL,
    BATTLE_ALIASES.PANELS: BATTLE_CTRL_ID.BATTLE_FIELD_CTRL,
    BATTLE_ALIASES.TEAM_BASES: BATTLE_CTRL_ID.TEAM_BASES,
    BATTLE_ALIASES.TIMER: BATTLE_CTRL_ID.ARENA_PERIOD
}

NEVER_HIDE_FL = (BATTLE_ALIASES.DEBUG, BATTLE_ALIASES.TIMER, BATTLE_ALIASES.DATE_TIME, BATTLE_ALIASES.SIXTH_SENSE)


class ViewSettings(object):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)

    def __init__(self):
        self._components = None
        self._hiddenComponents = set()

    @property
    def gui(self):
        return self.sessionProvider.arenaVisitor.gui

    def isSPG(self):
        return self.sessionProvider.getArenaDP().getVehicleInfo().isSPG()

    def isRandomBattle(self):
        return self.gui.isRandomBattle() or self.gui.isMapbox()

    def isStatisticsModuleEnabled(self):
        if self.gui.isEpicRandomBattle() or self.gui.isInEpicRange():
            return False
        return user_settings.statistics[GLOBAL.ENABLED]

    @staticmethod
    def xvmInstalled(module):
        if xvmInstalled:
            logInfo("{} module is disabled, XVM is installed", module)
        return xvmInstalled

    def isMinimapEnabled(self):
        if self.xvmInstalled("Minimap") or self.gui.isEpicBattle():
            return False
        return user_settings.minimap[GLOBAL.ENABLED] and user_settings.minimap[MINIMAP.ZOOM]

    def isWGREnabled(self):
        if self.xvmInstalled("Statistics"):
            return False
        return self.isStatisticsModuleEnabled() and user_settings.statistics[STATISTICS.STATISTIC_ENABLED]

    def isIconsEnabled(self):
        if self.xvmInstalled("Icons"):
            return False
        return self.isStatisticsModuleEnabled() and user_settings.statistics[STATISTICS.ICON_ENABLED]

    def isPlayersPanelsEnabled(self):
        if self.xvmInstalled("PlayersPanels") or self.gui.isInEpicRange() or self.gui.isEpicRandomBattle():
            return False
        return user_settings.players_panels[GLOBAL.ENABLED]

    def isFlightTimeEnabled(self):
        enabled = user_settings.flight_time[GLOBAL.ENABLED]
        if user_settings.flight_time[FLIGHT_TIME.SPG_ONLY]:
            return enabled and self.isSPG()
        return enabled

    def isDistanceToEnemyEnabled(self):
        if self.isSPG() or self.gui.isInEpicRange():
            return False
        return user_settings.distance_to_enemy[GLOBAL.ENABLED]

    def getSetting(self, alias):
        if alias is BATTLE_ALIASES.HP_BARS and not self.gui.isInEpicRange():
            return user_settings.hp_bars[GLOBAL.ENABLED]
        elif alias is BATTLE_ALIASES.DAMAGE_LOG:
            return user_settings.log_total[GLOBAL.ENABLED]
        elif alias is BATTLE_ALIASES.DAMAGE_LOG_EXT:
            return user_settings.log_extended[GLOBAL.ENABLED] and not self.gui.isEpicBattle()
        elif alias is BATTLE_ALIASES.MAIN_GUN and self.isRandomBattle():
            return user_settings.main_gun[GLOBAL.ENABLED]
        elif alias is BATTLE_ALIASES.DEBUG:
            return user_settings.debug_panel[GLOBAL.ENABLED]
        elif alias is BATTLE_ALIASES.TIMER:
            return user_settings.battle_timer[GLOBAL.ENABLED]
        elif alias is BATTLE_ALIASES.SIXTH_SENSE:
            return user_settings.sixth_sense[GLOBAL.ENABLED]
        elif alias is BATTLE_ALIASES.TEAM_BASES and not self.gui.isInEpicRange():
            return user_settings.team_bases_panel[GLOBAL.ENABLED]
        elif alias is BATTLE_ALIASES.ARMOR_CALC:
            return user_settings.armor_calculator[GLOBAL.ENABLED]
        elif alias is BATTLE_ALIASES.FLIGHT_TIME:
            return self.isFlightTimeEnabled()
        elif alias is BATTLE_ALIASES.DISPERSION_TIMER:
            return user_settings.dispersion_timer[GLOBAL.ENABLED]
        elif alias is BATTLE_ALIASES.PANELS:
            return self.isPlayersPanelsEnabled()
        elif alias is BATTLE_ALIASES.DATE_TIME:
            return user_settings.clock[GLOBAL.ENABLED] and user_settings.clock[CLOCK.IN_BATTLE][GLOBAL.ENABLED]
        elif alias is BATTLE_ALIASES.DISTANCE:
            return self.isDistanceToEnemyEnabled()
        elif alias is BATTLE_ALIASES.OWN_HEALTH:
            return user_settings.own_health[GLOBAL.ENABLED]
        elif alias is BATTLE_ALIASES.WGR_ICONS:
            return self.isWGREnabled() or self.isIconsEnabled()
        elif alias is BATTLE_ALIASES.MAP:
            return self.isMinimapEnabled()
        return False

    def setComponents(self):
        if self.gui.guiType in BATTLES_RANGE:
            self._components = [alias for alias in BATTLE_ALIASES if self.getSetting(alias)]
            if self.gui.isEpicBattle():
                self.addInToEpicUI(True)
            self._hiddenComponents.update(wgAlias for alias, wgAlias in ALIASES_TO_HIDE if alias in self._components)
        logDebug("viewSettings setComponents: components={}", self._components)

    def _clear(self):
        if self.gui.isEpicBattle():
            self.addInToEpicUI(False)
        self._components = None
        self._hiddenComponents.clear()
        logDebug("clear viewSettings components")

    def addInToEpicUI(self, add):
        for alias in self._components:
            if not add:
                _NEVER_HIDE.discard(alias)
                _STATE_TO_UI[PageStates.COUNTDOWN].discard(alias)
                _STATE_TO_UI[PageStates.RESPAWN].discard(alias)
                _STATE_TO_UI[PageStates.GAME].discard(alias)
                _STATE_TO_UI[PageStates.SPECTATOR_FREE].discard(alias)
                _STATE_TO_UI[PageStates.SPECTATOR_DEATHCAM].discard(alias)
                _STATE_TO_UI[PageStates.SPECTATOR_FOLLOW].discard(alias)
            else:
                _STATE_TO_UI[PageStates.COUNTDOWN].add(alias)
                _STATE_TO_UI[PageStates.RESPAWN].add(alias)
                _STATE_TO_UI[PageStates.GAME].add(alias)
                _STATE_TO_UI[PageStates.SPECTATOR_FREE].add(alias)
                _STATE_TO_UI[PageStates.SPECTATOR_DEATHCAM].add(alias)
                _STATE_TO_UI[PageStates.SPECTATOR_FOLLOW].add(alias)
                if alias in NEVER_HIDE_FL:
                    _NEVER_HIDE.add(alias)

    def registerComponents(self):
        if not self._components:
            return logDebug("viewSettings, registerComponents: _components is empty")
        config = ComponentsConfig()
        for alias in ALIAS_TO_CTRL:
            if alias in self._components:
                config += ComponentsConfig(((ALIAS_TO_CTRL[alias], (alias,)),))
        config = config.getConfig()
        logDebug("viewSettings, registerComponents: {}", config)
        self.sessionProvider.registerViewComponents(*config)

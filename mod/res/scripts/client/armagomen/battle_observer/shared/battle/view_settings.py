from collections import defaultdict

from armagomen._constants import ARMOR_CALC_PARAMS, BATTLE_ALIASES, CLOCK, DAMAGE_LOG, FLIGHT_TIME, GLOBAL, MINIMAP, STATISTICS
from armagomen.battle_observer.settings import IBOSettingsLoader
from armagomen import IALogger
from armagomen.utils.common import IS_XVM_INSTALLED
from constants import ARENA_GUI_TYPE
from frontline.gui.Scaleform.daapi.view.battle.frontline_battle_page import _NEVER_HIDE, _STATE_TO_UI, PageStates
from gui.battle_control.battle_constants import BATTLE_CTRL_ID
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider

ALIAS_TO_CTRL = {
    BATTLE_ALIASES.DATE_TIME: BATTLE_CTRL_ID.ARENA_PERIOD,
    BATTLE_ALIASES.HP_BARS: BATTLE_CTRL_ID.BATTLE_FIELD_CTRL,
    BATTLE_ALIASES.MAIN_GUN: BATTLE_CTRL_ID.BATTLE_FIELD_CTRL,
    BATTLE_ALIASES.OWN_HEALTH: BATTLE_CTRL_ID.PREBATTLE_SETUPS_CTRL,
    BATTLE_ALIASES.PANELS: BATTLE_CTRL_ID.BATTLE_FIELD_CTRL,
    BATTLE_ALIASES.TEAM_BASES: BATTLE_CTRL_ID.TEAM_BASES,
    BATTLE_ALIASES.TIMER: BATTLE_CTRL_ID.ARENA_PERIOD
}

NEVER_HIDE_FL = (BATTLE_ALIASES.DEBUG, BATTLE_ALIASES.TIMER, BATTLE_ALIASES.DATE_TIME)


class IViewSettings(object):

    def fini(self):
        pass

    def invalidateComponents(self):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def registerViewComponents(self):
        raise NotImplementedError

    @property
    def battlePages(self):
        raise NotImplementedError


class ViewSettingsAS(IViewSettings):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)
    settingsLoader = dependency.descriptor(IBOSettingsLoader)
    logger = dependency.descriptor(IALogger)

    AS_ATTRIBUTE_NAME = 'as_BattleObserverCreate'

    def __init__(self):
        self.components = None

    @property
    def gui(self):
        return self.sessionProvider.arenaVisitor.gui

    def isSPG(self):
        return self.sessionProvider.getArenaDP().getVehicleInfo().isSPG()

    def isRandomBattle(self):
        return self.gui.isRandomBattle() or self.gui.isMapbox()

    def isLastStand(self):
        return self.gui.guiType == getattr(ARENA_GUI_TYPE, "LAST_STAND", -1)

    def isHalloween(self):
        return self.gui.guiType == getattr(ARENA_GUI_TYPE, "HALLOWEEN", -1)

    def xvm_installed(self, module):
        if IS_XVM_INSTALLED:
            self.logger.logInfo("{} module is disabled, XVM is installed", module)
        return IS_XVM_INSTALLED

    def isSpecialBattle(self):
        return self.gui.isInEpicRange() or self.isLastStand() or self.gui.isBattleRoyale() or self.isHalloween()

    def spacialOrEpicRandom(self):
        return self.isSpecialBattle() or self.gui.isEpicRandomBattle()

    def isFlightTimeEnabled(self):
        flight_time = self.settingsLoader.settings.flight_time
        if flight_time[FLIGHT_TIME.SPG_ONLY]:
            return flight_time[GLOBAL.ENABLED] and self.isSPG()
        return flight_time[GLOBAL.ENABLED]

    def isDistanceToEnemyEnabled(self):
        if self.isSPG() or self.isSpecialBattle():
            return False
        return self.settingsLoader.settings.distance_to_enemy[GLOBAL.ENABLED]

    def isHealthEnabled(self):
        return self.settingsLoader.settings.hp_bars[GLOBAL.ENABLED] and not self.isSpecialBattle()

    def isMainGunEnabled(self):
        return self.settingsLoader.settings.main_gun[GLOBAL.ENABLED] and self.isRandomBattle()

    def isExtendedLogEnabled(self):
        extended = self.settingsLoader.settings.log_extended
        return extended[GLOBAL.ENABLED] and not self.isSpecialBattle() and (
                extended[DAMAGE_LOG.D_DONE_ENABLED] or extended[DAMAGE_LOG.D_RECEIVED_ENABLED])

    def isMinimapEnabled(self):
        if self.xvm_installed(BATTLE_ALIASES.MAP) or self.spacialOrEpicRandom():
            return False
        minimap = self.settingsLoader.settings.minimap
        return minimap[GLOBAL.ENABLED] and minimap[MINIMAP.ZOOM]

    def isStatisticsAndIconsEnabled(self):
        if self.xvm_installed(BATTLE_ALIASES.WGR_ICONS) or self.spacialOrEpicRandom():
            return False
        statistics = self.settingsLoader.settings.statistics
        return statistics[GLOBAL.ENABLED] and (
                statistics[STATISTICS.STATISTIC_ENABLED] or statistics[STATISTICS.ICON_ENABLED])

    def isPlayersPanelsEnabled(self):
        if self.xvm_installed(BATTLE_ALIASES.PANELS) or self.spacialOrEpicRandom():
            return False
        return self.settingsLoader.settings.players_panels[GLOBAL.ENABLED]

    def isTeamBasesEnabled(self):
        return self.settingsLoader.settings.team_bases_panel[GLOBAL.ENABLED] and not self.isSpecialBattle()

    def isClockEnabled(self):
        clock = self.settingsLoader.settings.clock
        return clock[GLOBAL.ENABLED] and clock[CLOCK.IN_BATTLE][GLOBAL.ENABLED] and not self.isLastStand()

    def isArmorCalculatorUIEnabled(self):
        if self.settingsLoader.settings.armor_calculator[GLOBAL.ENABLED]:
            return any(self.settingsLoader.settings.armor_calculator.get(key, False) for key in ARMOR_CALC_PARAMS)
        return False

    def invalidateComponents(self):
        self.components = tuple(alias for alias, enabled in (
            (BATTLE_ALIASES.WGR_ICONS, self.isStatisticsAndIconsEnabled()),
            (BATTLE_ALIASES.HP_BARS, self.isHealthEnabled()),
            (BATTLE_ALIASES.MAIN_GUN, self.isMainGunEnabled()),
            (BATTLE_ALIASES.DAMAGE_LOG, self.settingsLoader.settings.log_total[GLOBAL.ENABLED]),
            (BATTLE_ALIASES.DAMAGE_LOG_EXT, self.isExtendedLogEnabled()),
            (BATTLE_ALIASES.DEBUG, self.settingsLoader.settings.debug_panel[GLOBAL.ENABLED]),
            (BATTLE_ALIASES.TIMER, self.settingsLoader.settings.battle_timer[GLOBAL.ENABLED] and not self.isLastStand()),
            (BATTLE_ALIASES.TEAM_BASES, self.isTeamBasesEnabled()),
            (BATTLE_ALIASES.SIXTH_SENSE, self.settingsLoader.settings.sixth_sense[GLOBAL.ENABLED]),
            (BATTLE_ALIASES.ARMOR_CALC, self.isArmorCalculatorUIEnabled()),
            (BATTLE_ALIASES.FLIGHT_TIME, self.isFlightTimeEnabled()),
            (BATTLE_ALIASES.DISPERSION_TIMER, self.settingsLoader.settings.dispersion_timer[GLOBAL.ENABLED]),
            (BATTLE_ALIASES.PANELS, self.isPlayersPanelsEnabled()),
            (BATTLE_ALIASES.DATE_TIME, self.isClockEnabled()),
            (BATTLE_ALIASES.DISTANCE, self.isDistanceToEnemyEnabled()),
            (BATTLE_ALIASES.OWN_HEALTH, self.settingsLoader.settings.own_health[GLOBAL.ENABLED]),
            (BATTLE_ALIASES.MAP, self.isMinimapEnabled())
        ) if enabled)

        if self.gui.isInEpicRange() and self.components:
            self.addInToEpicUI(True)
        self.logger.logDebug("viewSettings _invalidateComponents: components={}", self.components)

    def clear(self):
        if self.gui.isInEpicRange() and self.components:
            self.addInToEpicUI(False)
        self.components = None
        self.logger.logDebug("clear viewSettings components")

    def addInToEpicUI(self, add):
        states = (
            PageStates.COUNTDOWN,
            PageStates.RESPAWN,
            PageStates.GAME,
            PageStates.SPECTATOR_FREE,
            PageStates.SPECTATOR_DEATHCAM,
            PageStates.SPECTATOR_FOLLOW,
        )
        action_ui = lambda s, a: s.add(a) if add else s.discard(a)
        action_never = _NEVER_HIDE.add if add else _NEVER_HIDE.discard

        for alias in self.components:
            for state in states:
                action_ui(_STATE_TO_UI[state], alias)
            if alias in NEVER_HIDE_FL:
                action_never(alias)

    def registerViewComponents(self):
        components = set(ALIAS_TO_CTRL.keys()).intersection(self.components)
        if components:
            grouped_aliases = defaultdict(list)
            for alias in components:
                grouped_aliases[ALIAS_TO_CTRL[alias]].append(alias)
            self.sessionProvider.registerViewComponents(*grouped_aliases.items())
            self.logger.logDebug("viewSettings, _registerViewComponents: {}", grouped_aliases)

    @property
    def battlePages(self):
        base = set(VIEW_ALIAS.BATTLE_PAGES)
        extra = {
            VIEW_ALIAS.STRONGHOLD_BATTLE_PAGE,
            VIEW_ALIAS.EPIC_RANDOM_PAGE,
            VIEW_ALIAS.COMP7_BATTLE_PAGE,
            VIEW_ALIAS.COMP7_LIGHT_BATTLE_PAGE,
        }
        ignore = {
            VIEW_ALIAS.DEV_BATTLE_PAGE,
            VIEW_ALIAS.EVENT_BATTLE_PAGE,
        }
        return (base | extra) - ignore

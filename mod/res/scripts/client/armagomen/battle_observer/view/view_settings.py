from collections import defaultdict

from armagomen._constants import BATTLE_ALIASES, CLOCK, DAMAGE_LOG, FLIGHT_TIME, GLOBAL, IS_WG_CLIENT, MINIMAP, STATISTICS
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import IS_XVM_INSTALLED
from armagomen.utils.logging import logDebug, logInfo
from constants import ARENA_GUI_TYPE

if IS_WG_CLIENT:
    from frontline.gui.Scaleform.daapi.view.battle.frontline_battle_page import _NEVER_HIDE, _STATE_TO_UI, PageStates
else:
    from gui.Scaleform.daapi.view.battle.epic.page import _NEVER_HIDE, _STATE_TO_UI, PageStates
from gui.battle_control.battle_constants import BATTLE_CTRL_ID
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


class ViewSettings(object):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)

    def __init__(self):
        self._components = None

    @property
    def gui(self):
        return self.sessionProvider.arenaVisitor.gui

    def isSPG(self):
        return self.sessionProvider.getArenaDP().getVehicleInfo().isSPG()

    def isRandomBattle(self):
        return self.gui.isRandomBattle() or self.gui.isMapbox()

    def isLastStand(self):
        return self.gui.guiType == getattr(ARENA_GUI_TYPE, "LAST_STAND", -1)

    @staticmethod
    def xvm_installed(module):
        if IS_XVM_INSTALLED:
            logInfo("{} module is disabled, XVM is installed", module)
        return IS_XVM_INSTALLED

    def isSpecialBattle(self):
        return self.gui.isInEpicRange() or self.isLastStand() or self.gui.isBattleRoyale()

    def spacialOrEpicRandom(self):
        return self.isSpecialBattle() or self.gui.isEpicRandomBattle()

    def isFlightTimeEnabled(self):
        enabled = user_settings.flight_time[GLOBAL.ENABLED]
        if user_settings.flight_time[FLIGHT_TIME.SPG_ONLY]:
            return enabled and self.isSPG()
        return enabled

    def isDistanceToEnemyEnabled(self):
        if self.isSPG() or self.isSpecialBattle():
            return False
        return user_settings.distance_to_enemy[GLOBAL.ENABLED]

    def isHealthEnabled(self):
        return user_settings.hp_bars[GLOBAL.ENABLED] and not self.isSpecialBattle()

    def isMainGunEnabled(self):
        return user_settings.main_gun[GLOBAL.ENABLED] and self.isRandomBattle()

    def isExtendedLogEnabled(self):
        return user_settings.log_extended[GLOBAL.ENABLED] and not self.isSpecialBattle() and (
                user_settings.log_extended[DAMAGE_LOG.D_DONE_ENABLED] or user_settings.log_extended[DAMAGE_LOG.D_RECEIVED_ENABLED])

    def isMinimapEnabled(self):
        if self.xvm_installed("Minimap") or self.spacialOrEpicRandom():
            return False
        return user_settings.minimap[GLOBAL.ENABLED] and user_settings.minimap[MINIMAP.ZOOM]

    def isStatisticsAndIconsEnabled(self):
        if self.xvm_installed("Statistics and Icons") or self.spacialOrEpicRandom():
            return False
        return user_settings.statistics[GLOBAL.ENABLED] and (
                user_settings.statistics[STATISTICS.STATISTIC_ENABLED] or user_settings.statistics[STATISTICS.ICON_ENABLED])

    def isPlayersPanelsEnabled(self):
        if self.xvm_installed("PlayersPanels") or self.spacialOrEpicRandom():
            return False
        return user_settings.players_panels[GLOBAL.ENABLED]

    def isTeamBasesEnabled(self):
        return user_settings.team_bases_panel[GLOBAL.ENABLED] and not self.isSpecialBattle()

    @staticmethod
    def isClockEnabled():
        return user_settings.clock[GLOBAL.ENABLED] and user_settings.clock[CLOCK.IN_BATTLE][GLOBAL.ENABLED]

    def _invalidateComponents(self):
        self._components = tuple(alias for alias, enabled in (
            (BATTLE_ALIASES.WGR_ICONS, self.isStatisticsAndIconsEnabled()),
            (BATTLE_ALIASES.HP_BARS, self.isHealthEnabled()),
            (BATTLE_ALIASES.MAIN_GUN, self.isMainGunEnabled()),
            (BATTLE_ALIASES.DAMAGE_LOG, user_settings.log_total[GLOBAL.ENABLED]),
            (BATTLE_ALIASES.DAMAGE_LOG_EXT, self.isExtendedLogEnabled()),
            (BATTLE_ALIASES.DEBUG, user_settings.debug_panel[GLOBAL.ENABLED]),
            (BATTLE_ALIASES.TIMER, user_settings.battle_timer[GLOBAL.ENABLED]),
            (BATTLE_ALIASES.TEAM_BASES, self.isTeamBasesEnabled()),
            (BATTLE_ALIASES.SIXTH_SENSE, user_settings.sixth_sense[GLOBAL.ENABLED]),
            (BATTLE_ALIASES.ARMOR_CALC, user_settings.armor_calculator[GLOBAL.ENABLED]),
            (BATTLE_ALIASES.FLIGHT_TIME, self.isFlightTimeEnabled()),
            (BATTLE_ALIASES.DISPERSION_TIMER, user_settings.dispersion_timer[GLOBAL.ENABLED]),
            (BATTLE_ALIASES.PANELS, self.isPlayersPanelsEnabled()),
            (BATTLE_ALIASES.DATE_TIME, self.isClockEnabled()),
            (BATTLE_ALIASES.DISTANCE, self.isDistanceToEnemyEnabled()),
            (BATTLE_ALIASES.OWN_HEALTH, user_settings.own_health[GLOBAL.ENABLED]),
            (BATTLE_ALIASES.MAP, self.isMinimapEnabled())
        ) if enabled)

        if self.gui.isInEpicRange() and self._components:
            self.addInToEpicUI(True)
        logDebug("viewSettings _invalidateComponents: components={}", self._components)

    def _clear(self):
        if self.gui.isInEpicRange() and self._components:
            self.addInToEpicUI(False)
        self._components = None
        logDebug("clear viewSettings components")

    def addInToEpicUI(self, add):
        for alias in self._components:
            if not add:
                if alias in NEVER_HIDE_FL:
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

    def _registerViewComponents(self):
        components = set(ALIAS_TO_CTRL.keys()).intersection(self._components)
        if components:
            grouped_aliases = defaultdict(list)
            for alias in components:
                grouped_aliases[ALIAS_TO_CTRL[alias]].append(alias)
            self.sessionProvider.registerViewComponents(*grouped_aliases.items())
            logDebug("viewSettings, _registerViewComponents: {}", grouped_aliases)

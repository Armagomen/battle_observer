import math
from collections import namedtuple

from CurrentVehicle import g_currentVehicle
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import GLOBAL, CLOCK, ALIASES, DISPERSION, STATISTICS, FLIGHT_TIME, SWF
from armagomen.utils.common import xvmInstalled, logInfo, getPlayer, logDebug, logError
from constants import ARENA_GUI_TYPE, ROLE_TYPE
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.daapi.view.battle.epic.page import _GAME_UI, _SPECTATOR_UI, _NEVER_HIDE
from gui.Scaleform.genConsts.BATTLE_VIEW_ALIASES import BATTLE_VIEW_ALIASES
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider

BATTLES_RANGE = (
    ARENA_GUI_TYPE.COMP7,
    ARENA_GUI_TYPE.EPIC_BATTLE,
    ARENA_GUI_TYPE.EPIC_RANDOM,
    ARENA_GUI_TYPE.EPIC_RANDOM_TRAINING,
    ARENA_GUI_TYPE.FORT_BATTLE_2,
    ARENA_GUI_TYPE.MAPBOX,
    ARENA_GUI_TYPE.RANDOM,
    ARENA_GUI_TYPE.RANKED,
    ARENA_GUI_TYPE.SORTIE_2,
    ARENA_GUI_TYPE.TRAINING,
    ARENA_GUI_TYPE.UNKNOWN,
)

ALIASES_TO_HIDE = (
    (ALIASES.HP_BARS, BATTLE_VIEW_ALIASES.FRAG_CORRELATION_BAR),
    (ALIASES.SIXTH_SENSE, BATTLE_VIEW_ALIASES.SIXTH_SENSE),
    (ALIASES.DEBUG, BATTLE_VIEW_ALIASES.DEBUG_PANEL),
    (ALIASES.TIMER, BATTLE_VIEW_ALIASES.BATTLE_TIMER)
)


def registerBattleObserverPackages():
    from gui.override_scaleform_views_manager import g_overrideScaleFormViewsConfig
    from gui.shared.system_factory import collectScaleformBattlePackages, registerScaleformBattlePackages, \
        registerScaleformLobbyPackages
    registerScaleformLobbyPackages(SWF.LOBBY_PACKAGES)
    for guiType in BATTLES_RANGE:
        if collectScaleformBattlePackages(guiType):
            registerScaleformBattlePackages(guiType, SWF.BATTLE_PACKAGES)
        g_overrideScaleFormViewsConfig.battlePackages[guiType].extend(SWF.BATTLE_PACKAGES)


TopLogAVG = namedtuple("TopLogAVG", ("damage", "assist"))


class ViewSettings(object):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)

    def __init__(self):
        self.isSPG = False
        self.__components = set()
        self.__hiddenComponents = set()
        self.__logsAVGData = TopLogAVG(GLOBAL.ZERO, GLOBAL.ZERO)
        g_currentVehicle.onChanged += self.onVehicleChanged

    def onVehicleChanged(self):
        self.isSPG = g_currentVehicle.item.role == ROLE_TYPE.SPG
        damage = 0
        assist = 0
        try:
            dossier = g_currentVehicle.getDossier()
            if dossier:
                d_damage = dossier.getRandomStats().getAvgDamage()
                d_assist = dossier.getRandomStats().getDamageAssistedEfficiencyWithStan()
                if d_damage is not None:
                    damage = int(math.floor(d_damage))
                if d_assist is not None:
                    assist = int(math.floor(d_assist))
                logDebug("set vehicle efficiency (avgDamage: {}, avgAssist: {})", damage, assist)
        except Exception as error:
            logError(repr(error))
        finally:
            self.__logsAVGData = TopLogAVG(damage, assist)

    @property
    def logAvgData(self):
        return self.__logsAVGData

    @property
    def gui(self):
        return self.sessionProvider.arenaVisitor.gui

    def isRandomBattle(self):
        return self.gui.isRandomBattle() or self.gui.isMapbox()

    def notEpicRandomBattle(self):
        return not self.gui.isEpicRandomBattle()

    def isStatisticsModuleEnabled(self):
        if self.gui.isComp7Battle() or self.gui.isEpicRandomBattle() or self.gui.isInEpicRange():
            return False
        return settings.statistics[GLOBAL.ENABLED]

    def isWTREnabled(self):
        if xvmInstalled:
            logInfo("Statistics module is disabled, XVM is installed")
            return False
        return self.isStatisticsModuleEnabled() and settings.statistics[STATISTICS.STATISTIC_ENABLED]

    def isIconsEnabled(self):
        if xvmInstalled:
            logInfo("Icons module is disabled, XVM is installed")
            return False
        return self.isStatisticsModuleEnabled() and settings.statistics[STATISTICS.ICON_ENABLED]

    def isPlayersPanelsLoading(self):
        if xvmInstalled or self.gui.isInEpicRange() or self.gui.isEpicRandomBattle():
            if xvmInstalled:
                logInfo("PlayersPanels module is disabled, XVM is installed")
            return False
        return settings.players_panels[GLOBAL.ENABLED]

    def isFlightTimeLoading(self):
        if settings.flight_time[FLIGHT_TIME.SPG_ONLY]:
            return settings.flight_time[GLOBAL.ENABLED] and self.isSPG
        return settings.flight_time[GLOBAL.ENABLED]

    def isDistanceToEnemyLoading(self):
        if self.isSPG or self.gui.isInEpicRange():
            return False
        return settings.distance_to_enemy[GLOBAL.ENABLED]

    def getSetting(self, alias):
        if alias is ALIASES.HP_BARS and not self.gui.isInEpicRange():
            return settings.hp_bars[GLOBAL.ENABLED]
        elif alias is ALIASES.DAMAGE_LOG:
            return settings.log_total[GLOBAL.ENABLED] or settings.log_extended[GLOBAL.ENABLED]
        elif alias is ALIASES.MAIN_GUN and self.isRandomBattle():
            return settings.main_gun[GLOBAL.ENABLED]
        elif alias is ALIASES.DEBUG:
            return settings.debug_panel[GLOBAL.ENABLED]
        elif alias is ALIASES.TIMER:
            return settings.battle_timer[GLOBAL.ENABLED]
        elif alias is ALIASES.SIXTH_SENSE:
            return settings.sixth_sense[GLOBAL.ENABLED]
        elif alias is ALIASES.TEAM_BASES:
            return settings.team_bases_panel[GLOBAL.ENABLED]
        elif alias is ALIASES.ARMOR_CALC:
            return settings.armor_calculator[GLOBAL.ENABLED]
        elif alias is ALIASES.FLIGHT_TIME:
            return self.isFlightTimeLoading()
        elif alias is ALIASES.DISPERSION_TIMER:
            return settings.dispersion_circle[GLOBAL.ENABLED] and settings.dispersion_circle[DISPERSION.TIMER_ENABLED]
        elif alias is ALIASES.PANELS:
            return self.isPlayersPanelsLoading()
        elif alias is ALIASES.DATE_TIME:
            return settings.clock[GLOBAL.ENABLED] and settings.clock[CLOCK.IN_BATTLE][GLOBAL.ENABLED]
        elif alias is ALIASES.DISTANCE:
            return self.isDistanceToEnemyLoading()
        elif alias is ALIASES.OWN_HEALTH:
            return settings.own_health[GLOBAL.ENABLED]
        return False

    def setComponents(self):
        if getattr(getPlayer(), "arenaGuiType", None) in BATTLES_RANGE:
            self.checkComponents()
            self.setHiddenComponents()
        logDebug("viewSettings setComponents: components={}", self.__components)
        return self.__components

    def clear(self):
        self.__components.clear()
        self.__hiddenComponents.clear()
        logDebug("clear viewSettings components")

    def checkComponents(self):
        for alias in ALIASES:
            if self.getSetting(alias):
                self.__components.add(alias)
                _GAME_UI.add(alias)
                _SPECTATOR_UI.add(alias)
                if alias is ALIASES.SIXTH_SENSE:
                    _NEVER_HIDE.add(alias)
            else:
                _GAME_UI.discard(alias)
                _SPECTATOR_UI.discard(alias)
                self.__components.discard(alias)
                if alias is ALIASES.SIXTH_SENSE:
                    _NEVER_HIDE.discard(alias)

    def setHiddenComponents(self):
        for alias, wg_alias in ALIASES_TO_HIDE:
            if alias in self.__components:
                self.__hiddenComponents.add(wg_alias)
            else:
                self.__hiddenComponents.discard(wg_alias)

    def addReplaceAlias(self, aliases):
        new_aliases = list(aliases)
        if ALIASES.TEAM_BASES in self.__components and BATTLE_VIEW_ALIASES.TEAM_BASES_PANEL in new_aliases:
            new_aliases.remove(BATTLE_VIEW_ALIASES.TEAM_BASES_PANEL)
            new_aliases.append(ALIASES.TEAM_BASES)
        elif ALIASES.TIMER in self.__components and BATTLE_VIEW_ALIASES.BATTLE_TIMER in new_aliases:
            new_aliases.append(ALIASES.TIMER)
        elif BATTLE_VIEW_ALIASES.DAMAGE_PANEL in new_aliases:
            if ALIASES.OWN_HEALTH in self.__components:
                new_aliases.append(ALIASES.OWN_HEALTH)
            if ALIASES.DAMAGE_LOG in self.__components:
                new_aliases.append(ALIASES.DAMAGE_LOG)
        elif ALIASES.DEBUG in self.__components and BATTLE_VIEW_ALIASES.DEBUG_PANEL in new_aliases:
            new_aliases.remove(BATTLE_VIEW_ALIASES.DEBUG_PANEL)
            new_aliases.append(ALIASES.DEBUG)
        elif BATTLE_VIEW_ALIASES.FRAG_CORRELATION_BAR in new_aliases:
            if ALIASES.HP_BARS in self.__components:
                new_aliases.remove(BATTLE_VIEW_ALIASES.FRAG_CORRELATION_BAR)
                new_aliases.append(ALIASES.HP_BARS)
            if ALIASES.PANELS in self.__components:
                new_aliases.append(ALIASES.PANELS)
            if ALIASES.MAIN_GUN in self.__components:
                new_aliases.append(ALIASES.MAIN_GUN)
        elif ALIASES.SIXTH_SENSE in self.__components and BATTLE_VIEW_ALIASES.SIXTH_SENSE in new_aliases:
            new_aliases.remove(BATTLE_VIEW_ALIASES.SIXTH_SENSE)
        result = tuple(new_aliases)
        logDebug("viewSettings, replace aliases: old={} new={}", aliases, result)
        return result

    def getHiddenWGComponents(self):
        return self.__hiddenComponents

    @staticmethod
    def getViewAliases():
        return {VIEW_ALIAS.CLASSIC_BATTLE_PAGE, VIEW_ALIAS.RANKED_BATTLE_PAGE,
                VIEW_ALIAS.EPIC_RANDOM_PAGE, VIEW_ALIAS.EPIC_BATTLE_PAGE,
                VIEW_ALIAS.STRONGHOLD_BATTLE_PAGE, VIEW_ALIAS.COMP7_BATTLE_PAGE}

    def getComponents(self):
        return self.__components

    def removeComponent(self, alias):
        self.__components.discard(alias)
        for bo_alias, wg_alias in ALIASES_TO_HIDE:
            if alias == bo_alias:
                self.__hiddenComponents.discard(wg_alias)

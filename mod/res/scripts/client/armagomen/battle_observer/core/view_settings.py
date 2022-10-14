from CurrentVehicle import g_currentVehicle
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import GLOBAL, CLOCK, ALIASES, DISPERSION, STATISTICS, FLIGHT_TIME, SWF
from armagomen.utils.common import overrideMethod, xvmInstalled, logInfo, getPlayer
from constants import ARENA_GUI_TYPE, ROLE_TYPE
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.daapi.view.battle.epic.page import _GAME_UI, _SPECTATOR_UI, _NEVER_HIDE
from gui.Scaleform.daapi.view.battle.shared.page import SharedPage
from gui.Scaleform.genConsts.BATTLE_VIEW_ALIASES import BATTLE_VIEW_ALIASES
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider

BATTLES_RANGE = {
    ARENA_GUI_TYPE.EPIC_BATTLE,
    ARENA_GUI_TYPE.EPIC_RANDOM,
    ARENA_GUI_TYPE.EPIC_RANDOM_TRAINING,
    ARENA_GUI_TYPE.FORT_BATTLE_2,
    ARENA_GUI_TYPE.FUN_RANDOM,
    ARENA_GUI_TYPE.MAPBOX,
    ARENA_GUI_TYPE.RANDOM,
    ARENA_GUI_TYPE.RANKED,
    ARENA_GUI_TYPE.SORTIE_2,
    ARENA_GUI_TYPE.TRAINING,
    ARENA_GUI_TYPE.UNKNOWN,
    ARENA_GUI_TYPE.COMP7
}

ALIASES_TO_HIDE = (
    (ALIASES.HP_BARS, BATTLE_VIEW_ALIASES.FRAG_CORRELATION_BAR),
    (ALIASES.SIXTH_SENSE, BATTLE_VIEW_ALIASES.SIXTH_SENSE),
    (ALIASES.DEBUG, BATTLE_VIEW_ALIASES.DEBUG_PANEL),
    (ALIASES.TIMER, BATTLE_VIEW_ALIASES.BATTLE_TIMER)
)


def registerBattleObserverPackages():
    from gui.Scaleform.daapi.settings import config
    from gui.shared.system_factory import collectScaleformBattlePackages
    config.registerScaleformLobbyPackages(SWF.LOBBY_PACKAGES)
    config.BATTLE_PACKAGES_BY_DEFAULT += SWF.BATTLE_PACKAGES
    for guiType in BATTLES_RANGE:
        if collectScaleformBattlePackages(guiType):
            config.registerScaleformBattlePackages(guiType, SWF.BATTLE_PACKAGES)


class ViewSettings(object):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)

    def __init__(self):
        self.isSPG = False
        self.__components = set()
        self.__hiddenComponents = set()
        self.settingsAdded = False
        registerBattleObserverPackages()
        g_currentVehicle.onChanged += self.onVehicleChanged
        overrideMethod(SharedPage)(self.new_SharedPage_init)

    def onVehicleChanged(self):
        self.isSPG = g_currentVehicle.item.role == ROLE_TYPE.SPG

    def isRandomBattle(self):
        return (self.sessionProvider.arenaVisitor.gui.isRandomBattle() or
                self.sessionProvider.arenaVisitor.gui.isMapbox())

    def notEpicBattle(self):
        return not self.sessionProvider.arenaVisitor.gui.isInEpicRange()

    def notEpicRandomBattle(self):
        return not self.sessionProvider.arenaVisitor.gui.isEpicRandomBattle()

    def isStatisticsModuleEnabled(self):
        return settings.statistics[GLOBAL.ENABLED] and self.notEpicBattle() and self.notEpicRandomBattle() and \
               not self.sessionProvider.arenaVisitor.gui.isComp7Battle()

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

    def getSetting(self, alias):
        if alias is ALIASES.HP_BARS:
            return settings.hp_bars[GLOBAL.ENABLED] and self.notEpicBattle()
        elif alias is ALIASES.DAMAGE_LOG:
            return (settings.log_total[GLOBAL.ENABLED] or
                    settings.log_damage_extended[GLOBAL.ENABLED] or
                    settings.log_input_extended[GLOBAL.ENABLED])
        elif alias is ALIASES.MAIN_GUN:
            return settings.main_gun[GLOBAL.ENABLED] and self.isRandomBattle()
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
            if settings.flight_time[FLIGHT_TIME.SPG_ONLY]:
                return settings.flight_time[GLOBAL.ENABLED] and self.isSPG
            return settings.flight_time[GLOBAL.ENABLED]
        elif alias is ALIASES.DISPERSION_TIMER:
            return (settings.dispersion_circle[GLOBAL.ENABLED] and
                    settings.dispersion_circle[DISPERSION.TIMER_ENABLED])
        elif alias is ALIASES.PANELS:
            return not xvmInstalled and settings.players_panels[
                GLOBAL.ENABLED] and self.notEpicBattle() and self.notEpicRandomBattle()
        elif alias is ALIASES.DATE_TIME:
            return settings.clock[GLOBAL.ENABLED] and settings.clock[CLOCK.IN_BATTLE][GLOBAL.ENABLED]
        elif alias is ALIASES.DISTANCE:
            return not self.isSPG and settings.distance_to_enemy[GLOBAL.ENABLED] and self.notEpicBattle()
        elif alias is ALIASES.OWN_HEALTH:
            return settings.own_health[GLOBAL.ENABLED]
        else:
            return False

    def setComponents(self):
        if getattr(getPlayer(), "arenaGuiType", None) in BATTLES_RANGE:
            self.checkComponents()
            self.setHiddenComponents()

    def clear(self):
        self.settingsAdded = False
        self.__components.clear()
        self.__hiddenComponents.clear()

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

    @staticmethod
    def checkPageName(page):
        return page.__class__.__name__ in ("StrongholdPage", "EpicBattlePage", "EpicRandomPage", "ClassicPage",
                                           "Comp7BattlePage")

    def new_SharedPage_init(self, base, page, *args, **kwargs):
        self.clear()
        base(page, *args, **kwargs)
        if self.checkPageName(page):
            self.setComponents()
            if not self.__components:
                self.__hiddenComponents.clear()
                return
            componentsConfig = page._SharedPage__componentsConfig
            newConfig = tuple((i, self.addReplaceAlias(aliases)) for i, aliases in componentsConfig.getConfig())
            componentsConfig._ComponentsConfig__config = newConfig
            self.settingsAdded = True

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
        return tuple(new_aliases)

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

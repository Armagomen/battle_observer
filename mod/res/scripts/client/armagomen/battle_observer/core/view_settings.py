from CurrentVehicle import g_currentVehicle
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import GLOBAL, CLOCK, ALIASES, DISPERSION, STATISTICS, FLIGHT_TIME, SWF
from armagomen.utils.common import overrideMethod, xvmInstalled
from armagomen.utils.events import g_events
from constants import ARENA_GUI_TYPE, ROLE_TYPE
from gui.Scaleform.daapi.settings import config as packages
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.daapi.view.battle.epic.page import _GAME_UI, _SPECTATOR_UI
from gui.Scaleform.daapi.view.battle.shared.page import SharedPage
from gui.Scaleform.genConsts.BATTLE_VIEW_ALIASES import BATTLE_VIEW_ALIASES
from gui.shared.system_factory import registerScaleformBattlePackages
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider

BATTLES_RANGE = {ARENA_GUI_TYPE.RANDOM,
                 ARENA_GUI_TYPE.FUN_RANDOM,
                 ARENA_GUI_TYPE.UNKNOWN,
                 ARENA_GUI_TYPE.TRAINING,
                 ARENA_GUI_TYPE.RANKED,
                 ARENA_GUI_TYPE.EPIC_RANDOM,
                 ARENA_GUI_TYPE.EPIC_RANDOM_TRAINING,
                 ARENA_GUI_TYPE.SORTIE_2,
                 ARENA_GUI_TYPE.FORT_BATTLE_2,
                 ARENA_GUI_TYPE.TUTORIAL,
                 ARENA_GUI_TYPE.EPIC_BATTLE,
                 ARENA_GUI_TYPE.MAPBOX}

BATTLE_TYPES_TO_INJECT_PACKAGES = {ARENA_GUI_TYPE.RANKED,
                                   ARENA_GUI_TYPE.EPIC_RANDOM,
                                   ARENA_GUI_TYPE.EPIC_RANDOM_TRAINING,
                                   ARENA_GUI_TYPE.SORTIE_2,
                                   ARENA_GUI_TYPE.FORT_BATTLE_2,
                                   ARENA_GUI_TYPE.TUTORIAL,
                                   ARENA_GUI_TYPE.EPIC_BATTLE}

class ViewSettings(object):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)

    def __init__(self):
        self.isAllowed = False
        self.isSPG = False
        self.__viewAliases = {VIEW_ALIAS.CLASSIC_BATTLE_PAGE, VIEW_ALIAS.RANKED_BATTLE_PAGE,
                              VIEW_ALIAS.EPIC_RANDOM_PAGE, VIEW_ALIAS.EPIC_BATTLE_PAGE,
                              VIEW_ALIAS.STRONGHOLD_BATTLE_PAGE}
        self.__components = []
        self.__hiddenComponents = []
        g_events.onHangarVehicleChanged += self.onVehicleChanged
        overrideMethod(SharedPage)(self.new_SharedPage_init)
        for guiType in BATTLE_TYPES_TO_INJECT_PACKAGES:
            registerScaleformBattlePackages(guiType, SWF.BATTLE_PACKAGES)
        packages.BATTLE_PACKAGES_BY_DEFAULT += SWF.BATTLE_PACKAGES
        packages.LOBBY_PACKAGES += SWF.LOBBY_PACKAGES

    def onVehicleChanged(self):
        self.isSPG = g_currentVehicle.item.role == ROLE_TYPE.SPG

    @property
    def isRandomBattle(self):
        return (self.sessionProvider.arenaVisitor.gui.isRandomBattle() or
                self.sessionProvider.arenaVisitor.gui.isMapbox())

    @property
    def notEpicBattle(self):
        return not self.sessionProvider.arenaVisitor.gui.isInEpicRange()

    @property
    def notEpicRandomBattle(self):
        return not self.sessionProvider.arenaVisitor.gui.isEpicRandomBattle()

    @property
    def statsMain(self):
        return settings.statistics[GLOBAL.ENABLED] and self.notEpicBattle and self.notEpicRandomBattle

    def isWTREnabled(self):
        if xvmInstalled:
            return False
        return self.statsMain and settings.statistics[STATISTICS.STATISTIC_ENABLED]

    def isIconsEnabled(self):
        if xvmInstalled:
            return False
        return self.statsMain and settings.statistics[STATISTICS.ICON_ENABLED]

    def getSetting(self, alias):
        if alias is ALIASES.HP_BARS:
            return settings.hp_bars[GLOBAL.ENABLED] and self.notEpicBattle
        elif alias is ALIASES.DAMAGE_LOG:
            return (settings.log_total[GLOBAL.ENABLED] or
                    settings.log_damage_extended[GLOBAL.ENABLED] or
                    settings.log_input_extended[GLOBAL.ENABLED])
        elif alias is ALIASES.MAIN_GUN:
            return settings.main_gun[GLOBAL.ENABLED] and self.isRandomBattle
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
                GLOBAL.ENABLED] and self.notEpicBattle and self.notEpicRandomBattle
        elif alias is ALIASES.USER_BACKGROUND:
            return settings.user_background[GLOBAL.ENABLED] and self.notEpicBattle
        elif alias is ALIASES.DATE_TIME:
            return settings.clock[GLOBAL.ENABLED] and settings.clock[CLOCK.IN_BATTLE][GLOBAL.ENABLED]
        elif alias is ALIASES.DISTANCE:
            return (not self.isSPG and settings.distance_to_enemy[GLOBAL.ENABLED] and
                    self.notEpicBattle and self.notEpicRandomBattle)
        elif alias is ALIASES.OWN_HEALTH:
            return settings.own_health[GLOBAL.ENABLED]
        else:
            return False

    def setIsAllowed(self):
        self.__components = []
        self.__hiddenComponents = []
        arenaVisitor = self.sessionProvider.arenaVisitor
        if arenaVisitor is None:
            self.isAllowed = False
        else:
            self.isAllowed = arenaVisitor.getArenaGuiType() in BATTLES_RANGE
            if self.isAllowed:
                self.setComponents()
            self.setHiddenComponents()
        return self.isAllowed, self.__components

    def setComponents(self):
        for alias in ALIASES:
            if self.getSetting(alias):
                self.__components.append(alias)
                _GAME_UI.add(alias)
                _SPECTATOR_UI.add(alias)
            else:
                _GAME_UI.discard(alias)
                _SPECTATOR_UI.discard(alias)

    def setHiddenComponents(self):
        if ALIASES.HP_BARS in self.__components:
            self.__hiddenComponents.append(BATTLE_VIEW_ALIASES.FRAG_CORRELATION_BAR)
        if ALIASES.SIXTH_SENSE in self.__components:
            self.__hiddenComponents.append(BATTLE_VIEW_ALIASES.SIXTH_SENSE)
        if ALIASES.DEBUG in self.__components:
            self.__hiddenComponents.append(BATTLE_VIEW_ALIASES.DEBUG_PANEL)
        if ALIASES.TIMER in self.__components:
            self.__hiddenComponents.append(BATTLE_VIEW_ALIASES.BATTLE_TIMER)

    def new_SharedPage_init(self, base, page, *args, **kwargs):
        base(page, *args, **kwargs)
        if not self.isAllowed:
            return
        componentsConfig = page._SharedPage__componentsConfig
        newConfig = tuple((i, self.addReplaceAlias(aliases)) for i, aliases in componentsConfig.getConfig())
        componentsConfig._ComponentsConfig__config = newConfig

    def addReplaceAlias(self, aliases):
        new_aliases = list(aliases)
        if ALIASES.TEAM_BASES in self.__components and BATTLE_VIEW_ALIASES.TEAM_BASES_PANEL in new_aliases:
            new_aliases.remove(BATTLE_VIEW_ALIASES.TEAM_BASES_PANEL)
            new_aliases.append(ALIASES.TEAM_BASES)
        elif ALIASES.TIMER in self.__components and BATTLE_VIEW_ALIASES.BATTLE_TIMER in new_aliases:
            new_aliases.append(ALIASES.TIMER)
        elif ALIASES.OWN_HEALTH in self.__components and BATTLE_VIEW_ALIASES.DAMAGE_PANEL in new_aliases:
            new_aliases.append(ALIASES.OWN_HEALTH)
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
        return tuple(new_aliases)

    def getHiddenWGComponents(self):
        return self.__hiddenComponents

    def getViewAliases(self):
        return self.__viewAliases

    def getComponents(self):
        return self.__components

    def removeComponent(self, alias):
        if alias in self.__components:
            self.__components.remove(alias)

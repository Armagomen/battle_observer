from collections import defaultdict

from PlayerEvents import g_playerEvents
from armagomen.battle_observer.core.constants import GLOBAL, MAIN, MINIMAP, HP_BARS, CLOCK, ALIASES, \
    DISPERSION_CIRCLE
from armagomen.utils.common import overrideMethod
from constants import ARENA_GUI_TYPE
from gui.Scaleform.daapi.view.battle.shared.page import SharedPage
from gui.Scaleform.genConsts.BATTLE_VIEW_ALIASES import BATTLE_VIEW_ALIASES
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider


class ViewSettings(object):
    @property
    def sessionProvider(self):
        if self.__sessionProvider is None:
            self.__sessionProvider = dependency.instance(IBattleSessionProvider)
        return self.__sessionProvider

    @property
    def isRandomBattle(self):
        return self.sessionProvider.arenaVisitor.gui.isRandomBattle()

    @property
    def isAllowed(self):
        if self.__isAllowed is None:
            enabled = False
            arenaVisitor = self.sessionProvider.arenaVisitor
            if arenaVisitor is not None:
                enabled = self.isRandomBattle or arenaVisitor.gui.isTrainingBattle() or \
                          arenaVisitor.gui.isRankedBattle() or \
                          arenaVisitor.getArenaGuiType() in (ARENA_GUI_TYPE.UNKNOWN,
                                                             ARENA_GUI_TYPE.FORT_BATTLE_2,
                                                             ARENA_GUI_TYPE.SORTIE_2)
            self.__isAllowed = enabled
        return self.__isAllowed

    def __init__(self, cfg):
        g_playerEvents.onAvatarBecomeNonPlayer += self.clear
        self.__sessionProvider = None
        self.__isAllowed = None
        self.__cache = defaultdict(bool)
        self.__alias_to_bool = {
            ALIASES.HP_BARS: lambda: cfg.hp_bars[GLOBAL.ENABLED] and self.isAllowed,
            ALIASES.DAMAGE_LOG: lambda: cfg.log_total[GLOBAL.ENABLED] or cfg.log_damage_extended[GLOBAL.ENABLED] or
                                        cfg.log_input_extended[GLOBAL.ENABLED],
            ALIASES.MAIN_GUN: lambda: cfg.main_gun[GLOBAL.ENABLED] and self.isRandomBattle,
            ALIASES.DEBUG: lambda: cfg.debug_panel[GLOBAL.ENABLED],
            ALIASES.TIMER: lambda: cfg.battle_timer[GLOBAL.ENABLED],
            ALIASES.SIXTH_SENSE: lambda: cfg.sixth_sense[GLOBAL.ENABLED],
            ALIASES.TEAM_BASES: lambda: cfg.team_bases_panel[GLOBAL.ENABLED],
            ALIASES.ARMOR_CALC: lambda: cfg.armor_calculator[GLOBAL.ENABLED],
            ALIASES.FLIGHT_TIME: lambda: cfg.flight_time[GLOBAL.ENABLED],
            ALIASES.DISPERSION_TIMER: lambda: cfg.dispersion_circle[GLOBAL.ENABLED] and
                                              cfg.dispersion_circle[DISPERSION_CIRCLE.TIMER_ENABLED],
            ALIASES.PANELS: lambda: cfg.players_panels[GLOBAL.ENABLED] and self.isAllowed,
            ALIASES.MINIMAP: lambda: cfg.minimap[MINIMAP.ZOOM][GLOBAL.ENABLED] and cfg.minimap[GLOBAL.ENABLED],
            ALIASES.USER_BACKGROUND: lambda: cfg.user_background[GLOBAL.ENABLED] or cfg.main[MAIN.BG] and
                                             cfg.hp_bars[HP_BARS.STYLE] == HP_BARS.NORMAL_STYLE,
            ALIASES.WG_COMP: lambda: True,
            ALIASES.DATE_TIME: lambda: cfg.clock[GLOBAL.ENABLED] and cfg.clock[CLOCK.IN_BATTLE][GLOBAL.ENABLED]
        }

        @overrideMethod(SharedPage)
        def new_SharedPage_init(base, page, *args, **kwargs):
            base(page, *args, **kwargs)
            config = page._SharedPage__componentsConfig._ComponentsConfig__config
            newConfig = tuple((i, self.checkAndReplaceAlias(aliases)) for i, aliases in config)
            page._SharedPage__componentsConfig._ComponentsConfig__config = newConfig

    def getSetting(self, alias):
        if alias not in self.__cache:
            check = self.__alias_to_bool.get(alias)
            if check is not None and callable(check):
                self.__cache[alias] = check()
        return self.__cache[alias]

    def clear(self):
        self.__cache.clear()
        self.__isAllowed = None
        self.__sessionProvider = None

    def checkAndReplaceAlias(self, aliases):
        new_aliases = list(aliases)
        if self.getSetting(ALIASES.TEAM_BASES) and BATTLE_VIEW_ALIASES.TEAM_BASES_PANEL in new_aliases:
            del new_aliases[new_aliases.index(BATTLE_VIEW_ALIASES.TEAM_BASES_PANEL)]
            new_aliases.append(ALIASES.TEAM_BASES)
        elif self.getSetting(ALIASES.TIMER) and BATTLE_VIEW_ALIASES.BATTLE_TIMER in new_aliases:
            new_aliases.append(ALIASES.TIMER)
        elif self.getSetting(ALIASES.DEBUG) and BATTLE_VIEW_ALIASES.DEBUG_PANEL in new_aliases:
            del new_aliases[new_aliases.index(BATTLE_VIEW_ALIASES.DEBUG_PANEL)]
            new_aliases.append(ALIASES.DEBUG)
        elif BATTLE_VIEW_ALIASES.FRAG_CORRELATION_BAR in new_aliases:
            if self.getSetting(ALIASES.HP_BARS):
                new_aliases.append(ALIASES.HP_BARS)
            if self.getSetting(ALIASES.PANELS):
                new_aliases.append(ALIASES.PANELS)
            if self.getSetting(ALIASES.MAIN_GUN):
                new_aliases.append(ALIASES.MAIN_GUN)
        return tuple(new_aliases)

from collections import defaultdict

from PlayerEvents import g_playerEvents
from gui.Scaleform.daapi.view.battle.shared.page import SharedPage
from gui.Scaleform.genConsts.BATTLE_VIEW_ALIASES import BATTLE_VIEW_ALIASES
from .battle_core import b_core
from .bo_constants import GLOBAL, MAIN, MINIMAP, HP_BARS, CLOCK, ALIASES
from .config import cfg
from .core import overrideMethod


class ElementsSettingsGetter(object):

    def __init__(self):
        g_playerEvents.onAvatarBecomeNonPlayer += self.clear
        self.sorted_aliases = (
            ALIASES.HP_BARS, ALIASES.SCORE_PANEL, ALIASES.DAMAGE_LOG, ALIASES.MAIN_GUN, ALIASES.DEBUG, ALIASES.TIMER,
            ALIASES.SIXTH_SENSE, ALIASES.TEAM_BASES, ALIASES.ARMOR_CALC, ALIASES.FLIGHT_TIME, ALIASES.PANELS,
            ALIASES.MINIMAP, ALIASES.USER_BACKGROUND, ALIASES.WG_COMP, ALIASES.DATE_TIME
        )
        self.alias_to_path = {
            ALIASES.HP_BARS: ".teams_hp",
            ALIASES.SCORE_PANEL: ".score_panel",
            ALIASES.DAMAGE_LOG: ".damage_log",
            ALIASES.MAIN_GUN: ".main_gun",
            ALIASES.DEBUG: ".debug_panel",
            ALIASES.TIMER: ".battle_timer",
            ALIASES.SIXTH_SENSE: ".sixth_sense",
            ALIASES.TEAM_BASES: ".team_bases",
            ALIASES.ARMOR_CALC: ".armor_calculator",
            ALIASES.FLIGHT_TIME: ".flight_time",
            ALIASES.PANELS: ".players_panels",
            ALIASES.MINIMAP: ".minimap",
            ALIASES.USER_BACKGROUND: ".user_background",
            ALIASES.WG_COMP: ".wg_comp_settings",
            ALIASES.DATE_TIME: ".date_times"
        }
        self.__cache = defaultdict(bool)
        self.alias_to_bool = {
            ALIASES.HP_BARS: lambda: cfg.hp_bars[GLOBAL.ENABLED],
            ALIASES.SCORE_PANEL: lambda: cfg.hp_bars[GLOBAL.ENABLED],
            ALIASES.DAMAGE_LOG: lambda: cfg.log_total[GLOBAL.ENABLED] or cfg.log_damage_extended[GLOBAL.ENABLED] or
                                        cfg.log_input_extended[GLOBAL.ENABLED],
            ALIASES.MAIN_GUN: lambda: cfg.main_gun[GLOBAL.ENABLED],
            ALIASES.DEBUG: lambda: cfg.debug_panel[GLOBAL.ENABLED],
            ALIASES.TIMER: lambda: cfg.battle_timer[GLOBAL.ENABLED],
            ALIASES.SIXTH_SENSE: lambda: cfg.sixth_sense[GLOBAL.ENABLED],
            ALIASES.TEAM_BASES: lambda: cfg.team_bases_panel[GLOBAL.ENABLED],
            ALIASES.ARMOR_CALC: lambda: cfg.armor_calculator[GLOBAL.ENABLED],
            ALIASES.FLIGHT_TIME: lambda: cfg.flight_time[GLOBAL.ENABLED],
            ALIASES.PANELS: lambda: cfg.panels_icon[GLOBAL.ENABLED] or cfg.players_spotted[GLOBAL.ENABLED] or
                                    cfg.players_damages[GLOBAL.ENABLED] or cfg.players_bars[GLOBAL.ENABLED],
            ALIASES.MINIMAP: lambda: cfg.minimap[MINIMAP.ZOOM][GLOBAL.ENABLED] and cfg.minimap[GLOBAL.ENABLED],
            ALIASES.USER_BACKGROUND: lambda: cfg.user_background[GLOBAL.ENABLED] or cfg.main[MAIN.BG] and
                                             cfg.hp_bars[HP_BARS.STYLE] == HP_BARS.NORMAL_STYLE,
            ALIASES.WG_COMP: lambda: True,
            ALIASES.DATE_TIME: lambda: cfg.clock[GLOBAL.ENABLED] and cfg.clock[CLOCK.IN_BATTLE][GLOBAL.ENABLED]
        }

    def getSetting(self, alias):
        if alias not in self.__cache:
            check = self.alias_to_bool.get(alias)
            if check is not None and callable(check):
                self.__cache[alias] = check()
        return self.__cache[alias]

    def clear(self):
        self.__cache.clear()


g_settingsGetter = ElementsSettingsGetter()


def checkAndReplaceAlias(alias):
    if g_settingsGetter.getSetting(ALIASES.TEAM_BASES) and alias == BATTLE_VIEW_ALIASES.TEAM_BASES_PANEL:
        return ALIASES.TEAM_BASES
    elif g_settingsGetter.getSetting(ALIASES.TIMER) and alias == BATTLE_VIEW_ALIASES.BATTLE_TIMER:
        return ALIASES.TIMER
    elif g_settingsGetter.getSetting(ALIASES.DEBUG) and alias == BATTLE_VIEW_ALIASES.DEBUG_PANEL:
        return ALIASES.DEBUG
    return alias


@overrideMethod(SharedPage)
def new_SharedPage_init(base, page, *args, **kwargs):
    base(page, *args, **kwargs)
    enabled = (
        g_settingsGetter.getSetting(ALIASES.TIMER),
        g_settingsGetter.getSetting(ALIASES.TEAM_BASES),
        g_settingsGetter.getSetting(ALIASES.DEBUG)
    )
    if any(enabled) and b_core.randomOrRanked()[0]:
        config = page._SharedPage__componentsConfig._ComponentsConfig__config
        newConfig = tuple((i, tuple(checkAndReplaceAlias(alias)
                                    for alias in aliases)) for i, aliases in config)
        page._SharedPage__componentsConfig._ComponentsConfig__config = newConfig

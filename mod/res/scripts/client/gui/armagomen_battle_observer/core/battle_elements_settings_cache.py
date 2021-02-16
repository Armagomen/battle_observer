from collections import defaultdict

from PlayerEvents import g_playerEvents
from gui.Scaleform.daapi.view.battle.shared.page import SharedPage
from gui.Scaleform.genConsts.BATTLE_VIEW_ALIASES import BATTLE_VIEW_ALIASES
from .battle_core import b_core
from .bo_constants import GLOBAL, MAIN, MINIMAP, HP_BARS, CLOCK, ALIASES, DISPERSION_CIRCLE
from .config import cfg
from .core import overrideMethod


class ElementsSettingsGetter(object):

    def __init__(self):
        g_playerEvents.onAvatarBecomeNonPlayer += self.clear
        self.__cache = defaultdict(bool)
        self.__alias_to_bool = {
            ALIASES.HP_BARS: lambda: cfg.hp_bars[GLOBAL.ENABLED],
            ALIASES.DAMAGE_LOG: lambda: cfg.log_total[GLOBAL.ENABLED] or cfg.log_damage_extended[GLOBAL.ENABLED] or
                                        cfg.log_input_extended[GLOBAL.ENABLED],
            ALIASES.MAIN_GUN: lambda: cfg.main_gun[GLOBAL.ENABLED],
            ALIASES.DEBUG: lambda: cfg.debug_panel[GLOBAL.ENABLED],
            ALIASES.TIMER: lambda: cfg.battle_timer[GLOBAL.ENABLED],
            ALIASES.SIXTH_SENSE: lambda: cfg.sixth_sense[GLOBAL.ENABLED],
            ALIASES.TEAM_BASES: lambda: cfg.team_bases_panel[GLOBAL.ENABLED],
            ALIASES.ARMOR_CALC: lambda: cfg.armor_calculator[GLOBAL.ENABLED],
            ALIASES.FLIGHT_TIME: lambda: cfg.flight_time[GLOBAL.ENABLED],
            ALIASES.DISPERSION_TIMER: lambda: cfg.dispersion_circle[GLOBAL.ENABLED] and
                                              cfg.dispersion_circle[DISPERSION_CIRCLE.TIMER_ENABLED],
            ALIASES.PANELS: lambda: cfg.players_panels[GLOBAL.ENABLED],
            ALIASES.MINIMAP: lambda: cfg.minimap[MINIMAP.ZOOM][GLOBAL.ENABLED] and cfg.minimap[GLOBAL.ENABLED],
            ALIASES.USER_BACKGROUND: lambda: cfg.user_background[GLOBAL.ENABLED] or cfg.main[MAIN.BG] and
                                             cfg.hp_bars[HP_BARS.STYLE] == HP_BARS.NORMAL_STYLE,
            ALIASES.WG_COMP: lambda: True,
            ALIASES.DATE_TIME: lambda: cfg.clock[GLOBAL.ENABLED] and cfg.clock[CLOCK.IN_BATTLE][GLOBAL.ENABLED]
        }

    def getSetting(self, alias):
        if alias not in self.__cache:
            check = self.__alias_to_bool.get(alias)
            if check is not None and callable(check):
                self.__cache[alias] = check()
        return self.__cache[alias]

    def clear(self):
        self.__cache.clear()


g_settingsGetter = ElementsSettingsGetter()


def checkAndReplaceAlias(aliases):
    new_aliases = list(aliases)
    if g_settingsGetter.getSetting(ALIASES.TEAM_BASES) and BATTLE_VIEW_ALIASES.TEAM_BASES_PANEL in new_aliases:
        del new_aliases[new_aliases.index(BATTLE_VIEW_ALIASES.TEAM_BASES_PANEL)]
        new_aliases.append(ALIASES.TEAM_BASES)
    elif g_settingsGetter.getSetting(ALIASES.TIMER) and BATTLE_VIEW_ALIASES.BATTLE_TIMER in new_aliases:
        new_aliases.append(ALIASES.TIMER)
    elif g_settingsGetter.getSetting(ALIASES.DEBUG) and BATTLE_VIEW_ALIASES.DEBUG_PANEL in new_aliases:
        del new_aliases[new_aliases.index(BATTLE_VIEW_ALIASES.DEBUG_PANEL)]
        new_aliases.append(ALIASES.DEBUG)
    elif BATTLE_VIEW_ALIASES.FRAG_CORRELATION_BAR in new_aliases:
        if g_settingsGetter.getSetting(ALIASES.HP_BARS):
            new_aliases.append(ALIASES.HP_BARS)
        if g_settingsGetter.getSetting(ALIASES.PANELS):
            new_aliases.append(ALIASES.PANELS)
        if g_settingsGetter.getSetting(ALIASES.MAIN_GUN):
            new_aliases.append(ALIASES.MAIN_GUN)
    return tuple(new_aliases)


@overrideMethod(SharedPage)
def new_SharedPage_init(base, page, *args, **kwargs):
    base(page, *args, **kwargs)
    if b_core.isAllowedBattleType()[0]:
        config = page._SharedPage__componentsConfig._ComponentsConfig__config
        newConfig = tuple((i, checkAndReplaceAlias(aliases)) for i, aliases in config)
        page._SharedPage__componentsConfig._ComponentsConfig__config = newConfig

from armagomen.constants import GLOBAL, MINIMAP, CLOCK, ALIASES, DISPERSION, MAIN
from armagomen.utils.common import overrideMethod
from constants import ARENA_GUI_TYPE
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.daapi.view.battle.shared.page import SharedPage
from gui.Scaleform.genConsts.BATTLE_VIEW_ALIASES import BATTLE_VIEW_ALIASES
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider

BATTLES_RANGE = {ARENA_GUI_TYPE.RANDOM,
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


class ViewSettings(object):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)

    def isRandomBattle(self):
        return (self.sessionProvider.arenaVisitor.gui.isRandomBattle() or
                self.sessionProvider.arenaVisitor.gui.isMapbox())

    def notEpicBattle(self):
        return not self.sessionProvider.arenaVisitor.gui.isEpicBattle()

    def __init__(self, cfg):
        self.cfg = cfg
        overrideMethod(SharedPage)(self.new_SharedPage_init)

    def getSetting(self, alias):
        isAllowed = False
        arenaVisitor = self.sessionProvider.arenaVisitor
        if arenaVisitor is not None:
            isAllowed = arenaVisitor.getArenaGuiType() in BATTLES_RANGE
        if not isAllowed:
            return isAllowed

        if alias is ALIASES.HP_BARS:
            return self.cfg.hp_bars[GLOBAL.ENABLED] and self.notEpicBattle()
        elif alias is ALIASES.DAMAGE_LOG:
            return (self.cfg.log_total[GLOBAL.ENABLED] or self.cfg.log_damage_extended[GLOBAL.ENABLED] or
                    self.cfg.log_input_extended[GLOBAL.ENABLED])
        elif alias is ALIASES.MAIN_GUN:
            return self.cfg.main_gun[GLOBAL.ENABLED] and self.isRandomBattle()
        elif alias is ALIASES.DEBUG:
            return self.cfg.debug_panel[GLOBAL.ENABLED]
        elif alias is ALIASES.TIMER:
            return self.cfg.battle_timer[GLOBAL.ENABLED]
        elif alias is ALIASES.SIXTH_SENSE:
            return self.cfg.sixth_sense[GLOBAL.ENABLED]
        elif alias is ALIASES.TEAM_BASES:
            return self.cfg.team_bases_panel[GLOBAL.ENABLED]
        elif alias is ALIASES.ARMOR_CALC:
            return self.cfg.armor_calculator[GLOBAL.ENABLED]
        elif alias is ALIASES.FLIGHT_TIME:
            return self.cfg.flight_time[GLOBAL.ENABLED]
        elif alias is ALIASES.DISPERSION_TIMER:
            return (self.cfg.dispersion_circle[GLOBAL.ENABLED] and
                    self.cfg.dispersion_circle[DISPERSION.TIMER_ENABLED])
        elif alias is ALIASES.PANELS:
            return self.cfg.players_panels[GLOBAL.ENABLED] and self.notEpicBattle()
        elif alias is ALIASES.MINIMAP:
            return (self.cfg.minimap[MINIMAP.ZOOM][GLOBAL.ENABLED] and self.cfg.minimap[GLOBAL.ENABLED]
                    and self.notEpicBattle())
        elif alias is ALIASES.USER_BACKGROUND:
            return self.cfg.user_background[GLOBAL.ENABLED]
        elif alias is ALIASES.DATE_TIME:
            return self.cfg.clock[GLOBAL.ENABLED] and self.cfg.clock[CLOCK.IN_BATTLE][GLOBAL.ENABLED]
        elif alias is ALIASES.DISTANCE:
            return self.cfg.distance_to_enemy[GLOBAL.ENABLED] and self.notEpicBattle()
        elif alias is ALIASES.OWN_HEALTH:
            return self.cfg.own_health[GLOBAL.ENABLED]
        else:
            return False

    def new_SharedPage_init(self, base, page, *args, **kwargs):
        base(page, *args, **kwargs)
        config = page._SharedPage__componentsConfig._ComponentsConfig__config
        newConfig = tuple((i, self.checkAndReplaceAlias(aliases)) for i, aliases in config)
        page._SharedPage__componentsConfig._ComponentsConfig__config = newConfig

    def checkAndReplaceAlias(self, aliases):
        new_aliases = list(aliases)
        if self.getSetting(ALIASES.TEAM_BASES) and BATTLE_VIEW_ALIASES.TEAM_BASES_PANEL in new_aliases:
            new_aliases.remove(BATTLE_VIEW_ALIASES.TEAM_BASES_PANEL)
            new_aliases.append(ALIASES.TEAM_BASES)
        elif self.getSetting(ALIASES.TIMER) and BATTLE_VIEW_ALIASES.BATTLE_TIMER in new_aliases:
            new_aliases.append(ALIASES.TIMER)
        elif self.getSetting(ALIASES.OWN_HEALTH) and BATTLE_VIEW_ALIASES.DAMAGE_PANEL in new_aliases:
            new_aliases.append(ALIASES.OWN_HEALTH)
        elif self.getSetting(ALIASES.DEBUG) and BATTLE_VIEW_ALIASES.DEBUG_PANEL in new_aliases:
            new_aliases.remove(BATTLE_VIEW_ALIASES.DEBUG_PANEL)
            new_aliases.append(ALIASES.DEBUG)
        elif BATTLE_VIEW_ALIASES.FRAG_CORRELATION_BAR in new_aliases:
            if self.getSetting(ALIASES.HP_BARS):
                new_aliases.remove(BATTLE_VIEW_ALIASES.FRAG_CORRELATION_BAR)
                new_aliases.append(ALIASES.HP_BARS)
            if self.getSetting(ALIASES.PANELS):
                new_aliases.append(ALIASES.PANELS)
            if self.getSetting(ALIASES.MAIN_GUN):
                new_aliases.append(ALIASES.MAIN_GUN)
        return tuple(new_aliases)

    def getHiddenWGComponents(self):
        components = []
        if self.getSetting(ALIASES.HP_BARS):
            components.append(BATTLE_VIEW_ALIASES.FRAG_CORRELATION_BAR)
        if self.getSetting(ALIASES.SIXTH_SENSE):
            components.append(BATTLE_VIEW_ALIASES.SIXTH_SENSE)
        if self.getSetting(ALIASES.DEBUG):
            components.append(BATTLE_VIEW_ALIASES.DEBUG_PANEL)
        if self.getSetting(ALIASES.TIMER):
            components.append(BATTLE_VIEW_ALIASES.BATTLE_TIMER)
        if self.cfg.main[MAIN.HIDE_CHAT] and self.isRandomBattle():
            components.append(BATTLE_VIEW_ALIASES.BATTLE_MESSENGER)
        return components

    @staticmethod
    def getViewAliases():
        return (VIEW_ALIAS.CLASSIC_BATTLE_PAGE,
                VIEW_ALIAS.RANKED_BATTLE_PAGE,
                VIEW_ALIAS.EPIC_RANDOM_PAGE,
                VIEW_ALIAS.EPIC_BATTLE_PAGE)

from armagomen._constants import BATTLE_ALIASES, IS_WG_CLIENT
from gui.Scaleform.framework import ComponentSettings, ScopeTemplates

__all__ = ()


def getViewSettings():
    from armagomen.battle_observer.battle.armor_calculator import ArmorCalculator
    from armagomen.battle_observer.battle.battle_timer import BattleTimer
    from armagomen.battle_observer.battle.damage_log import DamageLog
    from armagomen.battle_observer.battle.date_times import DateTimes
    from armagomen.battle_observer.battle.dispersion_timer import DispersionTimer
    from armagomen.battle_observer.battle.distance_to_enemy import Distance
    from armagomen.battle_observer.battle.extended_damage_logs import ExtendedDamageLogs
    from armagomen.battle_observer.battle.flight_time import FlightTime
    from armagomen.battle_observer.battle.main_gun import MainGun
    from armagomen.battle_observer.battle.minimap import MinimapZoomPlugin
    from armagomen.battle_observer.battle.own_health import OwnHealth
    from armagomen.battle_observer.battle.players_panels import PlayersPanels
    if IS_WG_CLIENT:
        from armagomen.battle_observer.battle.sixth_sense import SixthSense
        from armagomen.battle_observer.battle.debug_panel import DebugPanel
    else:
        from armagomen.battle_observer.battle.sixth_sense import SixthSenseLesta as SixthSense
        from armagomen.battle_observer.battle.debug_panel import DebugPanelLesta as DebugPanel
    from armagomen.battle_observer.battle.team_bases import TeamBases
    from armagomen.battle_observer.battle.teams_hp import TeamsHP
    from armagomen.battle_observer.battle.wgr_and_icons import WGRAndIcons
    return (
        ComponentSettings(BATTLE_ALIASES.WGR_ICONS, WGRAndIcons, ScopeTemplates.DEFAULT_SCOPE),
        ComponentSettings(BATTLE_ALIASES.PANELS, PlayersPanels, ScopeTemplates.DEFAULT_SCOPE),
        ComponentSettings(BATTLE_ALIASES.ARMOR_CALC, ArmorCalculator, ScopeTemplates.DEFAULT_SCOPE),
        ComponentSettings(BATTLE_ALIASES.TIMER, BattleTimer, ScopeTemplates.DEFAULT_SCOPE),
        ComponentSettings(BATTLE_ALIASES.DAMAGE_LOG, DamageLog, ScopeTemplates.DEFAULT_SCOPE),
        ComponentSettings(BATTLE_ALIASES.DAMAGE_LOG_EXT, ExtendedDamageLogs, ScopeTemplates.DEFAULT_SCOPE),
        ComponentSettings(BATTLE_ALIASES.DATE_TIME, DateTimes, ScopeTemplates.DEFAULT_SCOPE),
        ComponentSettings(BATTLE_ALIASES.DEBUG, DebugPanel, ScopeTemplates.DEFAULT_SCOPE),
        ComponentSettings(BATTLE_ALIASES.DISPERSION_TIMER, DispersionTimer, ScopeTemplates.DEFAULT_SCOPE),
        ComponentSettings(BATTLE_ALIASES.DISTANCE, Distance, ScopeTemplates.DEFAULT_SCOPE),
        ComponentSettings(BATTLE_ALIASES.FLIGHT_TIME, FlightTime, ScopeTemplates.DEFAULT_SCOPE),
        ComponentSettings(BATTLE_ALIASES.MAIN_GUN, MainGun, ScopeTemplates.DEFAULT_SCOPE),
        ComponentSettings(BATTLE_ALIASES.OWN_HEALTH, OwnHealth, ScopeTemplates.DEFAULT_SCOPE),
        ComponentSettings(BATTLE_ALIASES.SIXTH_SENSE, SixthSense, ScopeTemplates.DEFAULT_SCOPE),
        ComponentSettings(BATTLE_ALIASES.TEAM_BASES, TeamBases, ScopeTemplates.DEFAULT_SCOPE),
        ComponentSettings(BATTLE_ALIASES.HP_BARS, TeamsHP, ScopeTemplates.DEFAULT_SCOPE),
        ComponentSettings(BATTLE_ALIASES.MAP, MinimapZoomPlugin, ScopeTemplates.DEFAULT_SCOPE),
    )


def getBusinessHandlers():
    from armagomen.battle_observer.view import ViewHandlerBattle
    return ViewHandlerBattle(),


def getContextMenuHandlers():
    return ()

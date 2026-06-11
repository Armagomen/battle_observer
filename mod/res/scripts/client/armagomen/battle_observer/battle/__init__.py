from armagomen._constants import BATTLE_ALIASES
from armagomen.battle_observer.shared import IViewSettings
from armagomen import IALogger
from armagomen.utils.common import addCallback
from frameworks.wulf import WindowLayer
from gui.app_loader.settings import APP_NAME_SPACE
from gui.Scaleform.framework import ComponentSettings, ScopeTemplates
from gui.Scaleform.framework.package_layout import PackageBusinessHandler
from gui.shared import EVENT_BUS_SCOPE
from helpers import dependency

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
    from armagomen.battle_observer.battle.sixth_sense import SixthSense
    from armagomen.battle_observer.battle.debug_panel import _DebugPanel
    from armagomen.battle_observer.battle.team_bases import TeamBases
    from armagomen.battle_observer.battle.teams_hp import TeamsHP
    from armagomen.battle_observer.battle.statistics_and_icons import StatisticsAndIcons
    return (
        ComponentSettings(BATTLE_ALIASES.WGR_ICONS, StatisticsAndIcons, ScopeTemplates.DEFAULT_SCOPE),
        ComponentSettings(BATTLE_ALIASES.PANELS, PlayersPanels, ScopeTemplates.DEFAULT_SCOPE),
        ComponentSettings(BATTLE_ALIASES.ARMOR_CALC, ArmorCalculator, ScopeTemplates.DEFAULT_SCOPE),
        ComponentSettings(BATTLE_ALIASES.TIMER, BattleTimer, ScopeTemplates.DEFAULT_SCOPE),
        ComponentSettings(BATTLE_ALIASES.DAMAGE_LOG, DamageLog, ScopeTemplates.DEFAULT_SCOPE),
        ComponentSettings(BATTLE_ALIASES.DAMAGE_LOG_EXT, ExtendedDamageLogs, ScopeTemplates.DEFAULT_SCOPE),
        ComponentSettings(BATTLE_ALIASES.DATE_TIME, DateTimes, ScopeTemplates.DEFAULT_SCOPE),
        ComponentSettings(BATTLE_ALIASES.DEBUG, _DebugPanel, ScopeTemplates.DEFAULT_SCOPE),
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
    return ViewHandlerBattle(),


def getContextMenuHandlers():
    return ()


class ViewHandlerBattle(PackageBusinessHandler):
    wiewSettings = dependency.descriptor(IViewSettings)
    logger = dependency.descriptor(IALogger)

    def __init__(self):
        listeners = tuple((alias, self.eventListener) for alias in self.wiewSettings.battlePages)
        super(ViewHandlerBattle, self).__init__(listeners, appNS=APP_NAME_SPACE.SF_BATTLE, scope=EVENT_BUS_SCOPE.BATTLE)
        self.__counter = 0

    def init(self):
        super(ViewHandlerBattle, self).init()
        self.wiewSettings.invalidateComponents()

    def fini(self):
        self.wiewSettings.clear()
        super(ViewHandlerBattle, self).fini()

    def eventListener(self, event):
        if self.wiewSettings.components:
            self.wiewSettings.registerViewComponents()
            self.__findView(event.alias)
            self.logger.logInfo("ViewHandlerBattle: Register components for view: {}: {}", event.alias, self.wiewSettings.components)

    def onViewFounded(self, view):
        view._blToggling.update(self.wiewSettings.components)
        view.flashObject.as_BattleObserverCreate(self.wiewSettings.components)

    def __try_load(self):
        self.__counter += 1
        return self.__counter < 80

    def __findView(self, alias):
        if not self.__try_load():
            return
        view = self.findViewByAlias(WindowLayer.VIEW, alias)
        if view and hasattr(view.flashObject, self.wiewSettings.AS_ATTRIBUTE_NAME):
            self.onViewFounded(view)
        else:
            self.logger.logDebug("_getView: {} not found in {} or view is None", self.wiewSettings.AS_ATTRIBUTE_NAME, str(view))
            addCallback(0.1, self.__findView, alias)

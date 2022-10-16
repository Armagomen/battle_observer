from armagomen.battle_observer.components.statistics.statistic_data_loader import StatisticsDataLoader
from armagomen.battle_observer.core import viewSettings
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import SWF, STATISTICS, VEHICLE_TYPES, ALIASES
from armagomen.utils.common import logError, logInfo, logDebug, callback, overrideMethod
from armagomen.utils.events import g_events
from gui.Scaleform.daapi.view.battle.shared.page import SharedPage
from gui.Scaleform.framework import ComponentSettings, ScopeTemplates
from gui.Scaleform.framework.package_layout import PackageBusinessHandler
from gui.app_loader.settings import APP_NAME_SPACE
from gui.shared import EVENT_BUS_SCOPE

__all__ = ()


def getViewSettings():
    from armagomen.battle_observer.battle.armor_calculator import ArmorCalculator
    from armagomen.battle_observer.battle.battle_timer import BattleTimer
    from armagomen.battle_observer.battle.damage_log import DamageLog
    from armagomen.battle_observer.battle.date_times import DateTimes
    from armagomen.battle_observer.battle.debug_panel import DebugPanel
    from armagomen.battle_observer.battle.dispersion_timer import DispersionTimer
    from armagomen.battle_observer.battle.distance_to_enemy import Distance
    from armagomen.battle_observer.battle.flight_time import FlightTime
    from armagomen.battle_observer.battle.main_gun import MainGun
    from armagomen.battle_observer.battle.own_health import OwnHealth
    from armagomen.battle_observer.battle.players_panels import PlayersPanels
    from armagomen.battle_observer.battle.sixth_sense import SixthSense
    from armagomen.battle_observer.battle.team_bases import TeamBases
    from armagomen.battle_observer.battle.teams_hp import TeamsHP
    return (ComponentSettings(ALIASES.ARMOR_CALC, ArmorCalculator, ScopeTemplates.DEFAULT_SCOPE),
            ComponentSettings(ALIASES.TIMER, BattleTimer, ScopeTemplates.DEFAULT_SCOPE),
            ComponentSettings(ALIASES.DAMAGE_LOG, DamageLog, ScopeTemplates.DEFAULT_SCOPE),
            ComponentSettings(ALIASES.DATE_TIME, DateTimes, ScopeTemplates.DEFAULT_SCOPE),
            ComponentSettings(ALIASES.DEBUG, DebugPanel, ScopeTemplates.DEFAULT_SCOPE),
            ComponentSettings(ALIASES.DISPERSION_TIMER, DispersionTimer, ScopeTemplates.DEFAULT_SCOPE),
            ComponentSettings(ALIASES.DISTANCE, Distance, ScopeTemplates.DEFAULT_SCOPE),
            ComponentSettings(ALIASES.FLIGHT_TIME, FlightTime, ScopeTemplates.DEFAULT_SCOPE),
            ComponentSettings(ALIASES.MAIN_GUN, MainGun, ScopeTemplates.DEFAULT_SCOPE),
            ComponentSettings(ALIASES.OWN_HEALTH, OwnHealth, ScopeTemplates.DEFAULT_SCOPE),
            ComponentSettings(ALIASES.PANELS, PlayersPanels, ScopeTemplates.DEFAULT_SCOPE),
            ComponentSettings(ALIASES.SIXTH_SENSE, SixthSense, ScopeTemplates.DEFAULT_SCOPE),
            ComponentSettings(ALIASES.TEAM_BASES, TeamBases, ScopeTemplates.DEFAULT_SCOPE),
            ComponentSettings(ALIASES.HP_BARS, TeamsHP, ScopeTemplates.DEFAULT_SCOPE))


def getBusinessHandlers():
    return ObserverBusinessHandlerBattle(),


def getContextMenuHandlers():
    return ()


@overrideMethod(SharedPage, "_startBattleSession")
def _startBattleSession(base, page):
    logDebug("_startBattleSession: {}", page.__class__.__name__)
    components = viewSettings.getComponents()
    if not components:
        return base(page)
    logDebug("_startBattleSession: {}", components)
    componentsConfig = page._SharedPage__componentsConfig
    newConfig = tuple((i, viewSettings.addReplaceAlias(aliases)) for i, aliases in componentsConfig.getConfig())
    componentsConfig._ComponentsConfig__config = newConfig
    base(page)


class ObserverBusinessHandlerBattle(PackageBusinessHandler):
    __slots__ = ('_iconsEnabled', '_statLoadTry', '_statisticsEnabled', 'minimapPlugin', 'statistics', 'viewAliases')

    def __init__(self):
        from armagomen.battle_observer.components.minimap_plugins import MinimapZoomPlugin
        self.viewAliases = viewSettings.getViewAliases()
        listeners = [(alias, self.eventListener) for alias in self.viewAliases]
        super(ObserverBusinessHandlerBattle, self).__init__(listeners, APP_NAME_SPACE.SF_BATTLE, EVENT_BUS_SCOPE.BATTLE)
        self.minimapPlugin = MinimapZoomPlugin()
        self.statistics = None
        self._iconsEnabled = viewSettings.isIconsEnabled()
        self._statLoadTry = 0
        self._statisticsEnabled = False

    def init(self):
        super(ObserverBusinessHandlerBattle, self).init()
        if viewSettings.isWTREnabled():
            self.statistics = StatisticsDataLoader()
            self._statisticsEnabled = self.statistics.enabled

    def fini(self):
        self.minimapPlugin.fini()
        self.minimapPlugin = None
        self._statLoadTry = 0
        super(ObserverBusinessHandlerBattle, self).fini()

    def eventListener(self, event):
        components = viewSettings.setComponents()
        if components:
            self._app.as_loadLibrariesS([SWF.BATTLE])
            self._app.loaderManager.onViewLoaded += self.onViewLoaded
            logInfo("{}: loading libraries swf={}, alias={}".format(self.__class__.__name__, SWF.BATTLE, event.alias))
            logDebug("View components added to loading: {}", components)

    def loadStatisticView(self, view):
        if self._statisticsEnabled:
            if not self.statistics.loaded and self._statLoadTry < 20:
                self._statLoadTry += 1
                return callback(0.5, self.loadStatisticView, view)
        statisticsItemsData = self.statistics.itemsWTRData if self._statisticsEnabled else {}
        cutWidth = settings.statistics[STATISTICS.PANELS_CUT_WIDTH]
        fullWidth = settings.statistics[STATISTICS.PANELS_FULL_WIDTH]
        typeColors = settings.vehicle_types[VEHICLE_TYPES.CLASS_COLORS]
        iconMultiplier = settings.statistics[STATISTICS.ICON_BLACKOUT]
        view.flashObject.as_createStatisticComponent(self._statisticsEnabled, self._iconsEnabled, statisticsItemsData,
                                                     cutWidth, fullWidth, typeColors, iconMultiplier)

    @staticmethod
    def delayLoading(view):
        view.flashObject.as_observerCreateComponents(viewSettings.getComponents())
        view.flashObject.as_observerHideWgComponents(viewSettings.getHiddenWGComponents())

    def onViewLoaded(self, view, *args):
        logDebug("ObserverBusinessHandler/onViewLoaded: {}", view.settings.alias)
        if view.settings is None or view.settings.alias not in self.viewAliases:
            return
        self._app.loaderManager.onViewLoaded -= self.onViewLoaded
        g_events.onBattlePageLoaded(view)
        if not hasattr(view.flashObject, SWF.ATTRIBUTE_NAME):
            to_format_str = "battle_page {}, has ho attribute {}"
            return logError(to_format_str, repr(view.flashObject), SWF.ATTRIBUTE_NAME)
        if self.minimapPlugin.enabled:
            self.minimapPlugin.init(view)
        if self._iconsEnabled or self._statisticsEnabled:
            self.loadStatisticView(view)
        callback(1.0, self.delayLoading, view)

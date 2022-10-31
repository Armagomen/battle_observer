from armagomen.battle_observer.core import viewSettings
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import SWF, STATISTICS, VEHICLE_TYPES, ALIASES
from armagomen.utils.common import logError, logInfo, logDebug, callback
from armagomen.utils.events import g_events
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


class ObserverBusinessHandlerBattle(PackageBusinessHandler):
    __slots__ = ('_iconsEnabled', '_statLoadTry', '_statisticsEnabled', 'minimapPlugin', 'statistics', 'viewAliases')

    def __init__(self):
        from armagomen.battle_observer.components.minimap_plugins import MinimapZoomPlugin
        from armagomen.battle_observer.components.statistics.statistic_data_loader import StatisticsDataLoader
        self.viewAliases = viewSettings.getViewAliases()
        listeners = [(alias, self.eventListener) for alias in self.viewAliases]
        super(ObserverBusinessHandlerBattle, self).__init__(listeners, APP_NAME_SPACE.SF_BATTLE, EVENT_BUS_SCOPE.BATTLE)
        self.minimapPlugin = MinimapZoomPlugin()
        self.statistics = StatisticsDataLoader()
        self._iconsEnabled = False
        self._statLoadTry = 0
        self._statisticsEnabled = False

    def init(self):
        super(ObserverBusinessHandlerBattle, self).init()
        self._statisticsEnabled = viewSettings.isWTREnabled() and self.statistics.enabled
        self._iconsEnabled = viewSettings.isIconsEnabled()

    def fini(self):
        self.minimapPlugin.fini()
        self.minimapPlugin = None
        self._statLoadTry = 0
        viewSettings.clear()
        super(ObserverBusinessHandlerBattle, self).fini()

    def eventListener(self, event):
        self._app.loaderManager.onViewLoaded += self.onViewLoaded
        components = viewSettings.setComponents()
        if components or self._statisticsEnabled or self._iconsEnabled or self.minimapPlugin.enabled:
            if self._statisticsEnabled:
                self.statistics.getStatisticsDataFromServer()
            if components:
                configs = viewSettings.getComponentsConfig()
                if configs:
                    viewSettings.sessionProvider.registerViewComponents(*configs)
            self._app.as_loadLibrariesS([SWF.BATTLE])
            logInfo("{}: loading libraries swf={}, alias={}".format(self.__class__.__name__, SWF.BATTLE, event.alias))

    def loadStatisticView(self, flashObject):
        if self._statisticsEnabled and not self.statistics.loaded and self._statLoadTry < 20:
            self._statLoadTry += 1
            return callback(1.0, self.loadStatisticView, flashObject)
        cutWidth = settings.statistics[STATISTICS.PANELS_CUT_WIDTH]
        fullWidth = settings.statistics[STATISTICS.PANELS_FULL_WIDTH]
        typeColors = settings.vehicle_types[VEHICLE_TYPES.CLASS_COLORS]
        iconMultiplier = settings.statistics[STATISTICS.ICON_BLACKOUT]
        flashObject.as_createStatisticComponent(self._iconsEnabled, self.statistics.itemsWTRData, cutWidth, fullWidth,
                                                typeColors, iconMultiplier)

    def delayLoading(self, flashObject):
        flashObject.as_observerCreateComponents(viewSettings.getComponents())
        flashObject.as_observerHideWgComponents(viewSettings.getHiddenWGComponents())
        if self.minimapPlugin.enabled:
            self.minimapPlugin.init(flashObject)
        if self._iconsEnabled or self._statisticsEnabled:
            callback(1.0, self.loadStatisticView, flashObject)
        callback(20.0, flashObject.as_observerUpdateDamageLogPosition, viewSettings.gui.isEpicRandomBattle())

    def onViewLoaded(self, view, *args):
        alias = view.getAlias()
        if alias not in self.viewAliases:
            return
        logDebug("ObserverBusinessHandler/onViewLoaded: {}", alias)
        self._app.loaderManager.onViewLoaded -= self.onViewLoaded
        g_events.onBattlePageLoaded(view)
        flashObject = view.flashObject
        if not hasattr(flashObject, SWF.ATTRIBUTE_NAME):
            to_format_str = "{} {}, has ho attribute {}"
            return logError(to_format_str, alias, repr(flashObject), SWF.ATTRIBUTE_NAME)
        callback(1.0, self.delayLoading, flashObject)

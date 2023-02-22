from armagomen.battle_observer.components.minimap_plugins import MinimapZoomPlugin
from armagomen.battle_observer.components.statistics.statistic_data_loader import StatisticsDataLoader
from armagomen.battle_observer.core import viewSettings
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import SWF, STATISTICS, VEHICLE_TYPES, BATTLE_ALIASES, GLOBAL, MINIMAP
from armagomen.utils.common import logError, logInfo, logDebug, callback, xvmInstalled
from armagomen.utils.events import g_events
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.framework import ComponentSettings, ScopeTemplates
from gui.Scaleform.framework.package_layout import PackageBusinessHandler
from gui.app_loader.settings import APP_NAME_SPACE
from gui.shared import EVENT_BUS_SCOPE

__all__ = ()

VIEW_ALIASES = (
    VIEW_ALIAS.CLASSIC_BATTLE_PAGE,
    VIEW_ALIAS.COMP7_BATTLE_PAGE,
    VIEW_ALIAS.EPIC_BATTLE_PAGE,
    VIEW_ALIAS.EPIC_RANDOM_PAGE,
    VIEW_ALIAS.RANKED_BATTLE_PAGE,
    VIEW_ALIAS.STRONGHOLD_BATTLE_PAGE
)


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
    return (ComponentSettings(BATTLE_ALIASES.ARMOR_CALC, ArmorCalculator, ScopeTemplates.DEFAULT_SCOPE),
            ComponentSettings(BATTLE_ALIASES.TIMER, BattleTimer, ScopeTemplates.DEFAULT_SCOPE),
            ComponentSettings(BATTLE_ALIASES.DAMAGE_LOG, DamageLog, ScopeTemplates.DEFAULT_SCOPE),
            ComponentSettings(BATTLE_ALIASES.DATE_TIME, DateTimes, ScopeTemplates.DEFAULT_SCOPE),
            ComponentSettings(BATTLE_ALIASES.DEBUG, DebugPanel, ScopeTemplates.DEFAULT_SCOPE),
            ComponentSettings(BATTLE_ALIASES.DISPERSION_TIMER, DispersionTimer, ScopeTemplates.DEFAULT_SCOPE),
            ComponentSettings(BATTLE_ALIASES.DISTANCE, Distance, ScopeTemplates.DEFAULT_SCOPE),
            ComponentSettings(BATTLE_ALIASES.FLIGHT_TIME, FlightTime, ScopeTemplates.DEFAULT_SCOPE),
            ComponentSettings(BATTLE_ALIASES.MAIN_GUN, MainGun, ScopeTemplates.DEFAULT_SCOPE),
            ComponentSettings(BATTLE_ALIASES.OWN_HEALTH, OwnHealth, ScopeTemplates.DEFAULT_SCOPE),
            ComponentSettings(BATTLE_ALIASES.PANELS, PlayersPanels, ScopeTemplates.DEFAULT_SCOPE),
            ComponentSettings(BATTLE_ALIASES.SIXTH_SENSE, SixthSense, ScopeTemplates.DEFAULT_SCOPE),
            ComponentSettings(BATTLE_ALIASES.TEAM_BASES, TeamBases, ScopeTemplates.DEFAULT_SCOPE),
            ComponentSettings(BATTLE_ALIASES.HP_BARS, TeamsHP, ScopeTemplates.DEFAULT_SCOPE))


def getBusinessHandlers():
    return ObserverBusinessHandlerBattle(),


def getContextMenuHandlers():
    return ()


class ObserverBusinessHandlerBattle(PackageBusinessHandler):
    __slots__ = ('_iconsEnabled', '_statisticsEnabled', 'minimapPlugin', 'statistics')

    def __init__(self):
        listeners = [(alias, self.eventListener) for alias in VIEW_ALIASES]
        super(ObserverBusinessHandlerBattle, self).__init__(listeners, APP_NAME_SPACE.SF_BATTLE, EVENT_BUS_SCOPE.BATTLE)
        self.minimapPlugin = None
        self.statistics = StatisticsDataLoader()
        self._iconsEnabled = False
        self._statisticsEnabled = False

    def fini(self):
        if self.minimapPlugin is not None:
            self.minimapPlugin.fini()
            self.minimapPlugin = None
        self.statistics = None
        viewSettings.clear()
        super(ObserverBusinessHandlerBattle, self).fini()

    def eventListener(self, event):
        self._app.loaderManager.onViewLoaded += self.onViewLoaded
        self._statisticsEnabled = viewSettings.isWTREnabled()
        self._iconsEnabled = viewSettings.isIconsEnabled()
        baseMapEnabled = settings.minimap[GLOBAL.ENABLED] and settings.minimap[MINIMAP.ZOOM] and not xvmInstalled
        if baseMapEnabled and not viewSettings.gui.isEpicBattle():
            self.minimapPlugin = MinimapZoomPlugin()
        components = viewSettings.setComponents()
        if components or self._statisticsEnabled or self._iconsEnabled or self.minimapPlugin is not None:
            if self._statisticsEnabled:
                self.statistics.getStatisticsDataFromServer()
            self._app.as_loadLibrariesS([SWF.BATTLE])
            logInfo("{}: loading libraries swf={}, alias={}".format(self.__class__.__name__, SWF.BATTLE, event.alias))

    def loadStatisticView(self, flashObject):
        if self._statisticsEnabled and not self.statistics.loaded:
            self.statistics.setCallback(flashObject.as_updateStatisticData)
        cutWidth = settings.statistics[STATISTICS.PANELS_CUT_WIDTH]
        fullWidth = settings.statistics[STATISTICS.PANELS_FULL_WIDTH]
        typeColors = settings.vehicle_types[VEHICLE_TYPES.CLASS_COLORS]
        iconMultiplier = settings.statistics[STATISTICS.ICON_BLACKOUT]
        flashObject.as_createStatisticComponent(self._iconsEnabled, self.statistics.itemsWTRData, cutWidth, fullWidth,
                                                typeColors, iconMultiplier)

    def onViewLoaded(self, view, *args):
        alias = view.getAlias()
        if alias not in VIEW_ALIASES:
            return
        logDebug("ObserverBusinessHandler/onViewLoaded: {}", alias)
        self._app.loaderManager.onViewLoaded -= self.onViewLoaded
        g_events.onBattlePageLoaded(view)
        if not hasattr(view.flashObject, SWF.ATTRIBUTE_NAME):
            to_format_str = "{} {}, has ho attribute {}"
            return logError(to_format_str, alias, repr(view.flashObject), SWF.ATTRIBUTE_NAME)
        view._blToggling.update(viewSettings.components)
        view.flashObject.as_observerCreateComponents(viewSettings.components)
        view.flashObject.as_observerHideWgComponents(viewSettings.hiddenComponents)
        if self.minimapPlugin is not None:
            self.minimapPlugin.init(view.flashObject)
        if not viewSettings.gui.isEpicBattle():
            callback(20.0, view.flashObject.as_observerUpdateDamageLogPosition, viewSettings.gui.isEpicRandomBattle())
        if self._iconsEnabled or self._statisticsEnabled:
            self.loadStatisticView(view.flashObject)

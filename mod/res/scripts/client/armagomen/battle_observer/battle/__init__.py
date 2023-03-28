from armagomen.battle_observer.components.controllers.players_damage_controller import damage_controller
from armagomen.battle_observer.components.minimap_plugins import MinimapZoomPlugin
from armagomen.battle_observer.components.statistics.statistic_data_loader import StatisticsDataLoader
from armagomen.battle_observer.core import viewSettings
from armagomen.constants import SWF, BATTLE_ALIASES, CURRENT_REALM
from armagomen.utils.common import logError, logInfo, logDebug, callback, xvmInstalled
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
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
    __slots__ = ('_iconsEnabled', '_statisticsEnabled', '_minimapPlugin', '_statistics')

    def __init__(self):
        aliases = (
            VIEW_ALIAS.CLASSIC_BATTLE_PAGE, VIEW_ALIAS.COMP7_BATTLE_PAGE, VIEW_ALIAS.EPIC_BATTLE_PAGE,
            VIEW_ALIAS.EPIC_RANDOM_PAGE, VIEW_ALIAS.RANKED_BATTLE_PAGE, VIEW_ALIAS.STRONGHOLD_BATTLE_PAGE,
        ) if CURRENT_REALM != "RU" else tuple()
        listeners = tuple((alias, self.eventListener) for alias in aliases)
        super(ObserverBusinessHandlerBattle, self).__init__(listeners, APP_NAME_SPACE.SF_BATTLE, EVENT_BUS_SCOPE.BATTLE)
        self._minimapPlugin = None
        self._statistics = StatisticsDataLoader()
        self._iconsEnabled = False
        self._statisticsEnabled = False

    def init(self):
        super(ObserverBusinessHandlerBattle, self).init()
        damage_controller.start()

    def fini(self):
        if self._minimapPlugin is not None:
            self._minimapPlugin.fini()
            self._minimapPlugin = None
        self._statistics = None
        viewSettings.clear()
        damage_controller.stop()
        super(ObserverBusinessHandlerBattle, self).fini()

    def eventListener(self, event):
        self._app.loaderManager.onViewLoaded += self.__onViewLoaded
        self._statisticsEnabled = viewSettings.isWTREnabled()
        self._iconsEnabled = viewSettings.isIconsEnabled()
        if viewSettings.isMinimapEnabled():
            self._minimapPlugin = MinimapZoomPlugin()
        components = viewSettings.setComponents()
        if components or self._statisticsEnabled or self._iconsEnabled or self._minimapPlugin is not None:
            if self._statisticsEnabled:
                self._statistics.getStatisticsDataFromServer()
            self._app.as_loadLibrariesS([SWF.BATTLE])
            logInfo("{}: loading libraries swf={}, alias={}".format(self.__class__.__name__, SWF.BATTLE, event.alias))

    def __loadStatisticView(self, flashObject):
        if self._statisticsEnabled and not self._statistics.loaded:
            self._statistics.setCallback(flashObject.as_BattleObserverUpdateStatisticData)
        flashObject.as_BattleObserverCreateStatistic(self._iconsEnabled, self._statistics.itemsWTRData,
                                                     *viewSettings.getStatisticsSettings())

    def __onViewLoaded(self, pyView, *args):
        alias = pyView.getAlias()
        logDebug("ObserverBusinessHandler/onViewLoaded: {}", alias)
        self._app.loaderManager.onViewLoaded -= self.__onViewLoaded
        if not hasattr(pyView.flashObject, SWF.ATTRIBUTE_NAME):
            to_format_str = "{}:flashObject, has ho attribute {}"
            return logError(to_format_str, alias, SWF.ATTRIBUTE_NAME)
        callback(2.0 if xvmInstalled else 0, self._loadView, pyView)
        callback(40.0, pyView.flashObject.as_BattleObserverUpdateDamageLogPosition)

    def _loadView(self, pyView):
        pyView._blToggling.update(viewSettings.components)
        pyView.flashObject.as_BattleObserverCreate(viewSettings.components, CURRENT_REALM)
        pyView.flashObject.as_BattleObserverHideWg(viewSettings.hiddenComponents, CURRENT_REALM)
        if self._minimapPlugin is not None:
            self._minimapPlugin.init(pyView.flashObject)
        if self._iconsEnabled or self._statisticsEnabled:
            self.__loadStatisticView(pyView.flashObject)

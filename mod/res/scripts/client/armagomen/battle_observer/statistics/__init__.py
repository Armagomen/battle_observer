from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import GLOBAL, STATISTICS
from armagomen.utils.common import overrideMethod
from armagomen.utils.events import g_events
from gui.Scaleform.daapi.view.battle.classic import ClassicPage
from gui.Scaleform.daapi.view.battle.classic.players_panel import PlayersPanel
from gui.Scaleform.daapi.view.battle.classic.stats_exchange import ClassicStatisticsDataController
from gui.Scaleform.daapi.view.battle.ranked.stats_exchange import RankedStatisticsDataController
from gui.Scaleform.genConsts.BATTLE_VIEW_ALIASES import BATTLE_VIEW_ALIASES
from helpers import dependency
from helpers.func_utils import callback
from skeletons.gui.battle_session import IBattleSessionProvider


@property
def moduleEnabled():
    return settings.statistics[GLOBAL.ENABLED] and (settings.statistics[STATISTICS.ICON_ENABLED] or
                                                    settings.statistics[STATISTICS.STATISTIC_ENABLED])


@overrideMethod(ClassicStatisticsDataController, "as_updateVehicleStatusS")
@overrideMethod(RankedStatisticsDataController, "as_updateVehicleStatusS")
def new_as_updateVehicleStatusS(base, controller, data):
    base(controller, data)
    if moduleEnabled:
        callback(0.1, g_events, "updateVehicleStatus", data["isEnemy"], data["vehicleID"])


@overrideMethod(ClassicStatisticsDataController, "as_updateVehiclesStatsS")
@overrideMethod(RankedStatisticsDataController, "as_updateVehiclesStatsS")
def new_as_updateVehiclesStatsS(base, controller, data):
    base(controller, data)
    if moduleEnabled:
        vehicleID = "vehicleID"
        rightItems = data.get("rightItems")
        if rightItems:
            for item in rightItems:
                callback(0.1, g_events, "updateVehicleStatus", True, item[vehicleID])
        leftItems = data.get("leftItems")
        if leftItems:
            for item in leftItems:
                callback(0.1, g_events, "updateVehicleStatus", False, item[vehicleID])


def updateAllItems():
    arenaDP = dependency.instance(IBattleSessionProvider).getArenaDP()
    allyTeam = arenaDP.getNumberOfTeam()
    for vinfoVO in arenaDP.getVehiclesInfoIterator():
        callback(0.1, g_events, "updateVehicleStatus", vinfoVO.team != allyTeam, vinfoVO.vehicleID)


@overrideMethod(PlayersPanel, "as_setOverrideExInfoS")
@overrideMethod(PlayersPanel, "as_setPanelModeS")
def setPanelsState(base, *args):
    base(*args)
    if moduleEnabled:
        updateAllItems()


@overrideMethod(ClassicPage, "as_setComponentsVisibilityS")
def new_as_setComponentsVisibilityS(base, page, visible, hidden):
    base(page, visible, hidden)
    if moduleEnabled and BATTLE_VIEW_ALIASES.PLAYERS_PANEL in visible:
        updateAllItems()

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

METHOD_NAME = "updateVehicleStatus"


class StatisticPlugin(object):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)

    def __init__(self, settings):
        self.settings = settings

    def start(self):
        overrideMethod(ClassicStatisticsDataController, "as_updateVehicleStatusS")(self.new_as_updateVehicleStatusS)
        overrideMethod(RankedStatisticsDataController, "as_updateVehicleStatusS")(self.new_as_updateVehicleStatusS)
        overrideMethod(ClassicStatisticsDataController, "as_updateVehiclesStatsS")(self.new_as_updateVehiclesStatsS)
        overrideMethod(RankedStatisticsDataController, "as_updateVehiclesStatsS")(self.new_as_updateVehiclesStatsS)
        overrideMethod(PlayersPanel, "as_setChatCommandsVisibilityS")(self.setPanelsState)
        overrideMethod(PlayersPanel, "as_setIsInteractiveS")(self.setPanelsState)
        overrideMethod(PlayersPanel, "as_setOverrideExInfoS")(self.setPanelsState)
        overrideMethod(PlayersPanel, "as_setPanelModeS")(self.setPanelsState)
        overrideMethod(ClassicPage, "as_setComponentsVisibilityS")(self.new_as_setComponentsVisibilityS)

    @staticmethod
    def updateItem(isEnemy, vehicleID):
        callback(0.1, g_events, METHOD_NAME, isEnemy, vehicleID)

    def updateAllItems(self):
        arenaDP = self.sessionProvider.getArenaDP()
        allyTeam = arenaDP.getNumberOfTeam()
        for vinfoVO in arenaDP.getVehiclesInfoIterator():
            self.updateItem(vinfoVO.team != allyTeam, vinfoVO.vehicleID)

    @property
    def moduleEnabled(self):
        if self.settings is None:
            return False
        return self.settings[GLOBAL.ENABLED] and (self.settings[STATISTICS.ICON_ENABLED] or
                                                  self.settings[STATISTICS.STATISTIC_ENABLED])

    def new_as_updateVehicleStatusS(self, base, controller, data):
        base(controller, data)
        if self.moduleEnabled:
            self.updateItem(data["isEnemy"], data["vehicleID"])

    def new_as_updateVehiclesStatsS(self, base, controller, data):
        base(controller, data)
        if self.moduleEnabled:
            vehicleID = "vehicleID"
            rightItems = data.get("rightItems")
            if rightItems:
                for item in rightItems:
                    self.updateItem(True, item[vehicleID])
            leftItems = data.get("leftItems")
            if leftItems:
                for item in leftItems:
                    self.updateItem(False, item[vehicleID])

    def setPanelsState(self, base, *args):
        base(*args)
        if self.moduleEnabled:
            self.updateAllItems()

    def new_as_setComponentsVisibilityS(self, base, page, visible, hidden):
        base(page, visible, hidden)
        if self.moduleEnabled and BATTLE_VIEW_ALIASES.PLAYERS_PANEL in visible:
            self.updateAllItems()

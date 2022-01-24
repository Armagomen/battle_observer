from armagomen.constants import GLOBAL, STATISTICS
from armagomen.utils.common import overrideMethod
from armagomen.utils.events import g_events
from gui.Scaleform.daapi.view.battle.classic.players_panel import PlayersPanel
from gui.Scaleform.daapi.view.battle.classic.stats_exchange import ClassicStatisticsDataController
from gui.Scaleform.daapi.view.battle.ranked.stats_exchange import RankedStatisticsDataController
from helpers import dependency
from helpers.func_utils import callback
from skeletons.gui.app_loader import IAppLoader, GuiGlobalSpaceID
from skeletons.gui.battle_session import IBattleSessionProvider


class StatisticPlugin(object):
    METHOD_NAME = "updateVehicleData"
    sessionProvider = dependency.descriptor(IBattleSessionProvider)
    appLoader = dependency.descriptor(IAppLoader)

    def __init__(self, settings):
        self.settings = settings
        self.moduleEnabled = False
        self.appLoader.onGUISpaceBeforeEnter += self.onGUISpaceBeforeEnter
        overrideMethod(ClassicStatisticsDataController, "as_updateVehicleStatusS")(self.new_as_updateVehicleStatusS)
        overrideMethod(RankedStatisticsDataController, "as_updateVehicleStatusS")(self.new_as_updateVehicleStatusS)
        overrideMethod(ClassicStatisticsDataController, "as_updateVehiclesStatsS")(self.new_as_updateVehiclesStatsS)
        overrideMethod(RankedStatisticsDataController, "as_updateVehiclesStatsS")(self.new_as_updateVehiclesStatsS)
        overrideMethod(PlayersPanel, "as_setChatCommandsVisibilityS")(self.updateItemsData)
        overrideMethod(PlayersPanel, "as_setIsInteractiveS")(self.updateItemsData)
        overrideMethod(PlayersPanel, "as_setOverrideExInfoS")(self.updateItemsData)
        overrideMethod(PlayersPanel, "as_setPanelModeS")(self.updateItemsData)

    def onGUISpaceBeforeEnter(self, spaceID):
        if spaceID == GuiGlobalSpaceID.BATTLE_LOADING:
            self.moduleEnabled = self.settings[GLOBAL.ENABLED] and (self.settings[STATISTICS.ICON_ENABLED] or
                                                                    self.settings[STATISTICS.STATISTIC_ENABLED])

    def onGUISpaceEntered(self, spaceID):
        if self.moduleEnabled and spaceID in (GuiGlobalSpaceID.BATTLE_LOADING, GuiGlobalSpaceID.BATTLE):
            self.updateAllItems()

    def updateItem(self, isEnemy, vehicleID):
        callback(0.1, g_events, self.METHOD_NAME, isEnemy, vehicleID)

    def updateAllItems(self):
        arenaDP = self.sessionProvider.getArenaDP()
        allyTeam = arenaDP.getNumberOfTeam()
        for vInfo in arenaDP.getVehiclesInfoIterator():
            self.updateItem(vInfo.team != allyTeam, vInfo.vehicleID)

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

    def updateItemsData(self, base, *args):
        base(*args)
        if self.moduleEnabled:
            self.updateAllItems()

import json
from httplib import responses
from math import floor, log

from account_helpers.settings_core.settings_constants import GAME
from armagomen._constants import API_KEY, STATISTICS, STATISTICS_REGION
from armagomen.battle_observer.meta.battle.wgr_and_icons_meta import WGRAndIconsMeta
from armagomen.utils.common import addCallback, cancelCallback, fetchURL
from armagomen.utils.keys_listener import g_keysListener
from armagomen.utils.logging import logDebug, logError
from gui.battle_control.arena_info.interfaces import IVehiclesAndPersonalInvitationsController
from gui.shared import EVENT_BUS_SCOPE, events
from Keys import KEY_LALT, KEY_TAB
from uilogging.core.core_constants import HTTP_OK_STATUS


class WGRAndIcons(WGRAndIconsMeta, IVehiclesAndPersonalInvitationsController):
    COLOR_WGR = 'colorWGR'
    DEFAULT_COLOR = "#fafafa"
    DEFAULT_WIN_RATE = 0.0
    K = 1000.0
    UNITS = ['', 'k', 'm', 'g', 't', 'p']

    def __init__(self):
        super(WGRAndIcons, self).__init__()
        self.ranges = ((3287, "bad"), (5150, "normal"), (7258, "good"), (9586, "very_good"), (11025, "unique"))
        self.itemsData = {}
        self.data_loader = None

    def _populate(self):
        super(WGRAndIcons, self)._populate()
        if self.settingsCore:
            self.settingsCore.onSettingsChanged += self.__onSettingsChanged
        self.addListener(events.GameEvent.NEXT_PLAYERS_PANEL_MODE, self.updateALL, EVENT_BUS_SCOPE.BATTLE)
        g_keysListener.registerComponent(self.updateALL, keyList=[KEY_LALT])
        if self.isComp7Battle():
            g_keysListener.registerComponent(self.updateFullStats, keyList=[KEY_TAB])
        if STATISTICS_REGION is not None and self.settings[STATISTICS.STATISTIC_ENABLED]:
            self.data_loader = StatisticsDataLoader(self._arenaDP, self.updateAllItems)
            self.data_loader.getStatisticsDataFromServer()
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onPeriodChange += self.updateALL
            if arena.isFogOfWarEnabled and self.data_loader is not None:
                arena.onVehicleAdded += self.data_loader.updateList
                arena.onVehicleUpdated += self.data_loader.updateList
        ctrl = self.sessionProvider.shared.vehicleState
        if ctrl is not None:
            ctrl.onVehicleStateUpdated += self.__onVehicleStateUpdated

    def _dispose(self):
        if self.settingsCore:
            self.settingsCore.onSettingsChanged -= self.__onSettingsChanged
        self.removeListener(events.GameEvent.NEXT_PLAYERS_PANEL_MODE, self.updateALL, EVENT_BUS_SCOPE.BATTLE)
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onPeriodChange -= self.updateALL
            if arena.isFogOfWarEnabled and self.data_loader is not None:
                arena.onVehicleAdded -= self.data_loader.updateList
                arena.onVehicleUpdated -= self.data_loader.updateList
        self.data_loader = None
        ctrl = self.sessionProvider.shared.vehicleState
        if ctrl is not None:
            ctrl.onVehicleStateUpdated -= self.__onVehicleStateUpdated
        super(WGRAndIcons, self)._dispose()

    def __onSettingsChanged(self, diff):
        playersHPBarsVisibleState = diff.get(GAME.SHOW_VEHICLE_HP_IN_PLAYERS_PANEL)
        if playersHPBarsVisibleState is not None:
            self.as_updateAll()

    def invalidateArenaInfo(self):
        self.as_updateAll()

    def invalidateVehiclesInfo(self, arenaDP):
        self.as_updateAll()

    def invalidateVehiclesStats(self, arenaDP):
        self.as_updateAll()

    def updateVehiclesStats(self, updated, arenaDP):
        self.as_updateAll()

    def addVehicleInfo(self, vo, arenaDP):
        self.as_updateAll()

    def updateVehiclesInfo(self, updated, arenaDP):
        self.as_updateAll()

    def invalidateVehicleStatus(self, flags, vo, arenaDP):
        self.as_updateAll()

    def invalidatePlayerStatus(self, flags, vo, arenaDP):
        self.as_updateAll()

    def updateFullStats(self, key):
        self.as_updateFullStats(100)

    def updateALL(self, *args):
        self.as_updateAll()

    def __onVehicleStateUpdated(self, state, value):
        self.as_updateAll()

    def getPattern(self, isEnemy, itemData):
        logDebug("WGRStatistics: isEnemy={}, data={}", isEnemy, itemData)
        if isEnemy:
            return self.settings[STATISTICS.FULL_RIGHT] % itemData, self.settings[STATISTICS.CUT_RIGHT] % itemData
        else:
            return self.settings[STATISTICS.FULL_LEFT] % itemData, self.settings[STATISTICS.CUT_LEFT] % itemData

    def updateAllItems(self, loadedData):
        player_team = self._arenaDP.getNumberOfTeam()
        for accountDBID, value in loadedData.iteritems():
            if not value:
                continue
            vehicle_id = self._arenaDP.getVehIDByAccDBID(int(accountDBID))
            veh_info = self.getVehicleInfo(vehicle_id)
            item_data = self.buildItemData(veh_info.player.clanAbbrev, value)
            full, cut = self.getPattern(veh_info.team != player_team, item_data)
            text_color = item_data[self.COLOR_WGR] if self.settings[STATISTICS.CHANGE_VEHICLE_COLOR] else None
            self.itemsData[vehicle_id] = {"fullName": full, "cutName": cut, "vehicleTextColor": text_color}
        if self.itemsData:
            self.as_update_wgr_data(self.itemsData)

    def __getWinRateAndBattlesCount(self, data):
        random = data["statistics"]["random"]
        battles = int(random["battles"])
        if battles:
            return round(float(random["wins"]) / battles * 100, 2), self.__battlesFormat(battles)
        return self.DEFAULT_WIN_RATE, str(battles)

    def __battlesFormat(self, battles):
        if battles >= self.K:
            magnitude = int(floor(log(battles, self.K)))
            return '%.1f%s' % (battles / self.K ** magnitude, self.UNITS[magnitude])
        return str(battles)

    def __getColor(self, wgr):
        result = "very_bad"
        for value, colorName in self.ranges:
            if wgr >= value:
                result = colorName
            else:
                break
        return self.settings[STATISTICS.COLORS].get(result, self.DEFAULT_COLOR)

    def buildItemData(self, clanTag, data):
        wgr = int(data.get("global_rating", 0))
        win_rate, battles = self.__getWinRateAndBattlesCount(data)
        return {"WGR": wgr, self.COLOR_WGR: self.__getColor(wgr), "winRate": win_rate, "battles": battles,
                "nickname": data.get("nickname"), "clanTag": "[{}]".format(clanTag) if clanTag else ""}


class StatisticsDataLoader(object):
    URL = "https://api.worldoftanks.{}/wot/account/info/?".format(STATISTICS_REGION)
    SEPARATOR = "%2C"
    FIELDS = SEPARATOR.join(("statistics.random.wins", "statistics.random.battles", "global_rating", "nickname"))
    STAT_URL = "{url}application_id={key}&account_id={ids}&extra=statistics.random&fields={fields}&language=en"

    def __init__(self, arenaDP, callback):
        self.arenaDP = arenaDP
        self.__callback = callback
        self._load_try = 0
        self.__getDataCallback = None
        self.__vehicles = set()
        self.__loaded = set()

    def onDataResponse(self, response):
        if response.responseCode == 304:
            return
        if response.responseCode == HTTP_OK_STATUS:
            response_data = json.loads(response.body)
            data = response_data.get("data", {})
            logDebug("StatisticsDataLoader/onDataResponse: FINISH request users data={}", data)
            self.__callback(data)
            self.__loaded.update(int(k) for k in data.keys())
        else:
            self.delayedLoad(response.responseCode)

    def delayedLoad(self, code):
        if self._load_try < 5:
            self._load_try += 1
            code = responses.get(code) if isinstance(code, int) else code
            logError("StatisticsDataLoader: error loading statistic data - {}/{}", self._load_try, code)
            addCallback(10.0, self.getStatisticsDataFromServer)

    def updateList(self, vehicleID):
        vInfo = self.arenaDP.getVehicleInfo(vehicleID)
        accountDBID = vInfo.player.accountDBID
        if not accountDBID or accountDBID in self.__loaded or vInfo.isObserver():
            return
        self.__vehicles.add(accountDBID)
        logDebug(self.__vehicles)
        if self.__getDataCallback is None:
            self.__getDataCallback = addCallback(5.0, self.requestData)

    @property
    def vehicles(self):
        while self.__vehicles:
            yield str(self.__vehicles.pop())

    def requestData(self):
        if self.__getDataCallback is not None:
            cancelCallback(self.__getDataCallback)
            self.__getDataCallback = None
        url = self.STAT_URL.format(ids=self.SEPARATOR.join(self.vehicles), key=API_KEY, url=self.URL, fields=self.FIELDS)
        fetchURL(url, self.onDataResponse)

    def getStatisticsDataFromServer(self):
        for vInfo in self.arenaDP.getVehiclesInfoIterator():
            accountDBID = vInfo.player.accountDBID
            if not accountDBID or accountDBID in self.__loaded or vInfo.isObserver():
                continue
            self.__vehicles.add(accountDBID)
        logDebug("getStatisticsDataFromServer: START request data: ids={}", self.__vehicles)
        if self.__vehicles:
            self.requestData()

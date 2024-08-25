from threading import Thread

from adisp import adisp_process
from armagomen._constants import MAIN
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.logging import logDebug, logWarning
from gui import SystemMessages
from gui.clans.clan_cache import g_clanCache
from gui.clans.data_wrapper.clan_supply import DataNames, PointStatus, QuestStatus
from gui.impl import backport
from gui.impl.gen import R
from gui.shared.money import Currency
from gui.wgcg.clan_supply.contexts import ClaimRewardsCtx, PurchaseProgressionStageCtx
from gui.wgnc import g_wgncEvents
from gui.wgnc.settings import WGNC_DATA_PROXY_TYPE
from helpers import dependency
from skeletons.gui.shared import IItemsCache
from skeletons.gui.shared.utils import IHangarSpace
from skeletons.gui.web import IWebController

REWARD_STATUS_OK = (QuestStatus.REWARD_AVAILABLE, QuestStatus.REWARD_PENDING)
NEXT_DOUBLE = (3, 8, 13, 18)


class AutoClaimClanReward(object):
    __webController = dependency.descriptor(IWebController)
    __itemsCache = dependency.descriptor(IItemsCache)
    __hangarSpace = dependency.descriptor(IHangarSpace)

    def __init__(self):
        user_settings.onModSettingsChanged += self.onSettingsChanged
        self.__hangarSpace.onSpaceCreate += self.onCreate
        self.__cachedProgressData = None
        self.__cachedQuestsData = None
        self.__cachedSettingsData = None
        self.__claim_started = False
        self.__enabled = user_settings.main[MAIN.AUTO_CLAIM_CLAN_REWARD]
        self.__maximum_level = "21"

    def onCreate(self):
        self.__hangarSpace.onSpaceCreate -= self.onCreate
        if not g_clanCache.isInClan:
            return
        g_wgncEvents.onProxyDataItemShowByDefault += self.__onProxyDataItemShow
        g_clanCache.clanSupplyProvider.onDataReceived += self.__onDataReceived
        self.updateCache()

    def updateCache(self):
        self.__cachedQuestsData = g_clanCache.clanSupplyProvider.getQuestsInfo().data
        self.__cachedSettingsData = g_clanCache.clanSupplyProvider.getProgressionSettings().data
        self.__cachedProgressData = g_clanCache.clanSupplyProvider.getProgressionProgress().data

    def onSettingsChanged(self, data, name):
        if name == MAIN.NAME:
            self.__enabled = data[MAIN.AUTO_CLAIM_CLAN_REWARD]
            if self.__enabled:
                self.updateCache()
                if all([self.__cachedQuestsData, self.__cachedProgressData, self.__cachedSettingsData]):
                    self.parseQuests(self.__cachedQuestsData)
                    self.parseProgression(self.__cachedProgressData)

    def __onProxyDataItemShow(self, _, item):
        if not self.__enabled:
            return
        if item.getType() == WGNC_DATA_PROXY_TYPE.CLAN_SUPPLY_QUEST_UPDATE:
            status = item.getStatus()
            if not self.__claim_started and status in REWARD_STATUS_OK:
                self.__claimRewards()
            elif status == QuestStatus.COMPLETE and all([self.__cachedProgressData, self.__cachedSettingsData]):
                self.parseProgression(self.__cachedProgressData)
            logDebug(item)

    @adisp_process
    def __claimRewards(self):
        self.__claim_started = True
        response = yield self.__webController.sendRequest(ctx=ClaimRewardsCtx())
        if not response.isSuccess():
            SystemMessages.pushMessage("Battle Observer: Auto Claim Clan Reward - " + backport.text(
                R.strings.clan_supply.messages.claimRewards.error()), type=SystemMessages.SM_TYPE.Error)
            logWarning('Failed to claim rewards. Code: {code}', code=response.getCode())
        else:
            self.__claim_started = False

    @adisp_process
    def __claimProgression(self, stageID, price):
        response = yield self.__webController.sendRequest(ctx=PurchaseProgressionStageCtx(stageID, price))
        if not response.isSuccess():
            SystemMessages.pushMessage("Battle Observer: Auto Claim Clan Reward - Failed to claim Progression.",
                                       type=SystemMessages.SM_TYPE.Error)
            logWarning('Failed to claim Progression. Code: {code}', code=response.getCode())

    def parseQuests(self, data):
        if self.__claim_started and any(q.status in REWARD_STATUS_OK for q in data.quests):
            self.__claimRewards()

    @property
    def currency(self):
        return self.__itemsCache.items.stats.dynamicCurrencies.get(Currency.TOUR_COIN, 0)

    def isMaximumPurchased(self, data):
        maximum_progress = data.points.get(self.__maximum_level)
        return maximum_progress is not None and maximum_progress.status == PointStatus.PURCHASED

    def parseProgression(self, data):
        if not self.__cachedSettingsData.enabled:
            return
        last_purchased = int(data.last_purchased or 0)
        to_purchased = 0
        if self.isMaximumPurchased(data):
            for stateID, stageProgress in sorted(data.points.items(), key=lambda i: int(i[0])):
                if stageProgress.status == PointStatus.AVAILABLE:
                    to_purchased = stateID
                    break
        else:
            to_purchased = last_purchased + 1 if last_purchased not in NEXT_DOUBLE else last_purchased + 2
        if not to_purchased:
            return
        next_points = self.__cachedSettingsData.points.get(str(to_purchased))
        if next_points is not None and self.currency >= next_points.price:
            self.__claimProgression(to_purchased, next_points.price)

    def __onDataReceived(self, dataName, data):
        logDebug("__onDataReceived {} {}", dataName, data)
        if dataName in (DataNames.QUESTS_INFO, DataNames.QUESTS_INFO_POST):
            self.__cachedQuestsData = data
            if self.__enabled:
                self.parseQuests(data)
        elif dataName == DataNames.PROGRESSION_PROGRESS:
            self.__cachedProgressData = data
            if self.__enabled:
                self.parseProgression(data)
        elif dataName == DataNames.PROGRESSION_SETTINGS:
            self.__cachedSettingsData = data


g_autoClaimClanReward = Thread(target=AutoClaimClanReward, name="Battle_observer_AutoClaimClanReward")
g_autoClaimClanReward.daemon = True
g_autoClaimClanReward.start()

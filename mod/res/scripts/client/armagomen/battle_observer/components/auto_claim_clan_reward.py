from adisp import adisp_process
from armagomen._constants import MAIN
from armagomen.utils.common import addCallback
from armagomen.utils.events import g_events
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
SKIP_LEVELS = (5, 10, 15, 20)


class AutoClaimClanReward(object):
    __webController = dependency.descriptor(IWebController)
    __itemsCache = dependency.descriptor(IItemsCache)
    __hangarSpace = dependency.descriptor(IHangarSpace)

    def __init__(self):
        self.__hangarSpace.onSpaceCreate += self.onCreate
        self.__cachedProgressData = None
        self.__cachedQuestsData = None
        self.__cachedSettingsData = None
        self.__claim_started = False
        self.__enabled = False

    def onCreate(self):
        self.__hangarSpace.onSpaceCreate -= self.onCreate

        def update():
            self.__cachedQuestsData = g_clanCache.clanSupplyProvider.getQuestsInfo().data
            self.__cachedSettingsData = g_clanCache.clanSupplyProvider.getProgressionSettings().data
            self.__cachedProgressData = g_clanCache.clanSupplyProvider.getProgressionProgress().data
            if self.__enabled and g_clanCache.isInClan:
                if self.__cachedQuestsData:
                    self.parseQuests(self.__cachedQuestsData)
                if self.__cachedProgressData and self.__cachedSettingsData:
                    self.parseProgression(self.__cachedProgressData)

        addCallback(3.0, update)

    def subscribe(self):
        g_events.onModSettingsChanged += self.onModSettingsChanged
        g_wgncEvents.onProxyDataItemShowByDefault += self.__onProxyDataItemShow
        g_clanCache.clanSupplyProvider.onDataReceived += self.__onDataReceived

    def unsubscribe(self):
        g_wgncEvents.onProxyDataItemShowByDefault -= self.__onProxyDataItemShow
        g_clanCache.clanSupplyProvider.onDataReceived -= self.__onDataReceived
        g_events.onModSettingsChanged -= self.onModSettingsChanged

    def onModSettingsChanged(self, name, data):
        if name == MAIN.NAME and self.__enabled != data[MAIN.AUTO_CLAIM_CLAN_REWARD]:
            self.__enabled = data[MAIN.AUTO_CLAIM_CLAN_REWARD]

    def __onProxyDataItemShow(self, _, item):
        if self.__enabled and g_clanCache.isInClan and item.getType() == WGNC_DATA_PROXY_TYPE.CLAN_SUPPLY_QUEST_UPDATE:
            status = item.getStatus()
            if not self.__claim_started and status in REWARD_STATUS_OK:
                self.__claimRewards()
            elif status == QuestStatus.COMPLETE and self.__cachedProgressData and self.__cachedSettingsData:
                self.parseProgression(self.__cachedProgressData)
            logDebug("AutoClaimClanReward __onProxyDataItemShow: {}", item)

    @adisp_process
    def __claimRewards(self):
        self.__claim_started = True
        response = yield self.__webController.sendRequest(ctx=ClaimRewardsCtx())
        if not response.isSuccess():
            SystemMessages.pushMessage("Battle Observer: Auto Claim Clan Reward - " + backport.text(
                R.strings.clan_supply.messages.claimRewards.error()), type=SystemMessages.SM_TYPE.Error)
            logWarning('AutoClaimClanReward Failed to claim rewards. Code: {code}', code=response.getCode())
        self.__claim_started = False

    @adisp_process
    def __claimProgression(self, stageID, price):
        response = yield self.__webController.sendRequest(ctx=PurchaseProgressionStageCtx(stageID, price))
        if not response.isSuccess():
            SystemMessages.pushMessage("Battle Observer: Auto Claim Clan Reward - Failed to claim Progression.",
                                       type=SystemMessages.SM_TYPE.Error)
            logWarning('AutoClaimClanReward Failed to claim Progression. Code: {code}', code=response.getCode())

    def parseQuests(self, data):
        if data is not None and not self.__claim_started and any(q.status in REWARD_STATUS_OK for q in data.quests):
            self.__claimRewards()

    @staticmethod
    def isMaximumLevelPurchased(data):
        maximum_level = data.points.get(str(max(map(int, data.points.keys()))), None)
        return maximum_level and maximum_level.status == PointStatus.PURCHASED

    def parseProgression(self, data):
        if not self.__cachedSettingsData.enabled or data is None:
            return
        maximum_level_purchased = self.isMaximumLevelPurchased(data)
        available_levels = [
            int(stateID) for stateID, stageProgress in data.points.items()
            if stageProgress.status == PointStatus.AVAILABLE and (int(stateID) not in SKIP_LEVELS or maximum_level_purchased)
        ]
        if not available_levels:
            return
        next_level = min(available_levels)
        next_point = self.__cachedSettingsData.points.get(str(next_level))
        currency = self.__itemsCache.items.stats.dynamicCurrencies.get(Currency.TOUR_COIN, 0)
        if next_point and currency >= next_point.price:
            self.__claimProgression(next_level, next_point.price)

    def __onDataReceived(self, dataName, data):
        logDebug("AutoClaimClanReward __onDataReceived: {} {}", dataName, data)
        if dataName in (DataNames.QUESTS_INFO, DataNames.QUESTS_INFO_POST):
            self.__cachedQuestsData = data
            if self.__enabled and g_clanCache.isInClan:
                self.parseQuests(data)
        elif dataName == DataNames.PROGRESSION_PROGRESS:
            self.__cachedProgressData = data
            if self.__enabled and g_clanCache.isInClan:
                self.parseProgression(data)
        elif dataName == DataNames.PROGRESSION_SETTINGS:
            self.__cachedSettingsData = data


clanRewards = AutoClaimClanReward()
clanRewards.subscribe()


def fini():
    clanRewards.unsubscribe()

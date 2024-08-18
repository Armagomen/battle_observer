import time
from threading import Thread

from adisp import adisp_process
from armagomen._constants import MAIN
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import callback
from armagomen.utils.logging import logWarning
from gui import SystemMessages
from gui.clans.clan_cache import g_clanCache
from gui.clans.data_wrapper.clan_supply import DataNames, QuestStatus
from gui.impl import backport
from gui.impl.gen import R
from gui.shared.money import Currency
from gui.wgcg.clan_supply.contexts import ClaimRewardsCtx, PurchaseProgressionStageCtx
from helpers import dependency
from PlayerEvents import g_playerEvents
from skeletons.gui.shared import IItemsCache
from skeletons.gui.shared.utils import IHangarSpace
from skeletons.gui.web import IWebController

REWARD_STATUS_OK = (QuestStatus.REWARD_AVAILABLE, QuestStatus.REWARD_PENDING)
next_double_up = (3, 8, 13, 18)


class AutoClaimClanReward(object):
    __webController = dependency.descriptor(IWebController)
    __itemsCache = dependency.descriptor(IItemsCache)
    hangarSpace = dependency.descriptor(IHangarSpace)

    def __init__(self):
        self.hangarSpace.onSpaceCreate += self.updateQuests
        g_clanCache.clanSupplyProvider.onDataReceived += self.__onDataReceived
        g_playerEvents.onBattleResultsReceived += self.updateQuests
        self.__cachedSettingsData = None
        self.__ignoreClaimQuests = False
        self.__callback = None
        self.__started = False

    def updateQuests(self, *args, **kwargs):
        time.sleep(5.0)
        if not self.__started:
            self.__started = True
            self.hangarSpace.onSpaceCreate -= self.updateQuests
        if user_settings.main[MAIN.AUTO_CLAIM_CLAN_REWARD] and g_clanCache.isInClan:
            quest_data = g_clanCache.clanSupplyProvider.getQuestsInfo().data
            if quest_data is None:
                g_clanCache.clanSupplyProvider._getData(DataNames.QUESTS_INFO_POST)
            else:
                self.parseQuests(quest_data.quests)

    @adisp_process
    def __claimRewards(self):
        response = yield self.__webController.sendRequest(ctx=ClaimRewardsCtx())
        if not response.isSuccess():
            SystemMessages.pushMessage("Battle Observer: Auto Claim Clan Reward - " + backport.text(
                R.strings.clan_supply.messages.claimRewards.error()), type=SystemMessages.SM_TYPE.Error)
            logWarning('Failed to claim rewards. Code: {code}', code=response.getCode())

    @adisp_process
    def __claimProgression(self, stageID, price):
        response = yield self.__webController.sendRequest(ctx=PurchaseProgressionStageCtx(stageID, price))
        if not response.isSuccess():
            SystemMessages.pushMessage("Battle Observer: Auto Claim Clan Reward - Failed to claim Progression.",
                                       type=SystemMessages.SM_TYPE.Error)
            logWarning('Failed to claim Progression. Code: {code}', code=response.getCode())

    def parseQuests(self, quests):
        if not self.__ignoreClaimQuests and any(q.status == QuestStatus.REWARD_AVAILABLE for q in quests):
            self.__ignoreClaimQuests = True
            self.__claimRewards()

            def cancelIgnore():
                self.__ignoreClaimQuests = False

            callback(10, cancelIgnore)

    @property
    def currency(self):
        return self.__itemsCache.items.stats.dynamicCurrencies.get(Currency.TOUR_COIN, 0)

    def parseProgression(self, data):
        last_lvl = int(data.last_purchased or 0)
        next_lvl = last_lvl + 1 if last_lvl not in next_double_up else last_lvl + 2
        next_lvl_currency = self.__cachedSettingsData.points.get(str(next_lvl))
        if next_lvl_currency is not None and self.currency >= next_lvl_currency.price:
            self.__claimProgression(next_lvl, next_lvl_currency.price)

    def __onDataReceived(self, dataName, data):
        if user_settings.main[MAIN.AUTO_CLAIM_CLAN_REWARD] and g_clanCache.isInClan:
            if dataName in (DataNames.QUESTS_INFO, DataNames.QUESTS_INFO_POST):
                self.parseQuests(data.quests)
                if self.__cachedSettingsData is None:
                    g_clanCache.clanSupplyProvider.getProgressionSettings()
            elif dataName == DataNames.PROGRESSION_PROGRESS:
                self.parseProgression(data)
            elif dataName == DataNames.PROGRESSION_SETTINGS:
                self.__cachedSettingsData = data
                g_clanCache.clanSupplyProvider.getProgressionProgress()


g_autoClaimClanReward = Thread(target=AutoClaimClanReward, name="Battle_observer_AutoClaimClanReward")
g_autoClaimClanReward.daemon = True
g_autoClaimClanReward.start()

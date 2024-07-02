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
from skeletons.gui.shared import IItemsCache
from skeletons.gui.shared.utils import IHangarSpace
from skeletons.gui.web import IWebController

REWARD_STATUS_OK = (QuestStatus.REWARD_AVAILABLE, QuestStatus.REWARD_PENDING)
next_double_up = (3, 8, 13, 18)


class AutoClaimClanReward:
    __webController = dependency.descriptor(IWebController)
    __itemsCache = dependency.descriptor(IItemsCache)
    hangarSpace = dependency.descriptor(IHangarSpace)

    def __init__(self):
        self.hangarSpace.onSpaceCreate += self.update
        self.__itemsCache.onSyncCompleted += self.update
        g_clanCache.clanSupplyProvider.onDataReceived += self.__onDataReceived
        self.__claimed = set()
        self.__settingsProgression = None

    def update(self, *args, **kwargs):
        if user_settings.main[MAIN.AUTO_CLAIM_CLAN_REWARD] and g_clanCache.isInClan:
            self.updateQuests()
            self.updateProgression()

    def updateQuests(self):
        quest_data = g_clanCache.clanSupplyProvider.getQuestsInfo().data
        if quest_data is None:
            g_clanCache.clanSupplyProvider._getData(DataNames.QUESTS_INFO_POST)
        else:
            self.parseQuests(quest_data)

    def updateProgression(self):
        if self.__settingsProgression is None:
            g_clanCache.clanSupplyProvider.getProgressionSettings()
        else:
            self.parseProgression(g_clanCache.clanSupplyProvider.getProgressionProgress().data)

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
            logWarning('Failed to claim Progression. Code: {code}', code=response.getCode())

    def parseQuests(self, data):
        claim = False
        for quest in data.quests:
            claim |= quest.status in REWARD_STATUS_OK and quest.name not in self.__claimed
            if claim:
                self.__claimed.add(quest.name)
        if claim:
            self.__claimRewards()
            callback(20, self.__claimed.clear)

    def parseProgression(self, data):
        if self.__settingsProgression is None or data is None:
            return callback(5.0, self.updateProgression)
        currency = self.__itemsCache.items.stats.dynamicCurrencies.get(Currency.TOUR_COIN, 0)
        last_lvl = data.last_purchased
        next_lvl = last_lvl + 1 if last_lvl not in next_double_up else last_lvl + 2
        next_lvl_currency = self.__settingsProgression.points.get(str(next_lvl))
        if next_lvl_currency is not None and currency >= next_lvl_currency.price:
            self.__claimProgression(next_lvl, next_lvl_currency.price)

    def __onDataReceived(self, dataName, data):
        if user_settings.main[MAIN.AUTO_CLAIM_CLAN_REWARD] and g_clanCache.isInClan:
            if dataName in (DataNames.QUESTS_INFO, DataNames.QUESTS_INFO_POST):
                self.parseQuests(data)
            elif dataName == DataNames.PROGRESSION_PROGRESS:
                self.parseProgression(data)
            elif dataName == DataNames.PROGRESSION_SETTINGS:
                self.__settingsProgression = data


g_autoClaimClanReward = AutoClaimClanReward()

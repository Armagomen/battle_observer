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
from gui.wgcg.clan_supply.contexts import ClaimRewardsCtx
from helpers import dependency
from PlayerEvents import g_playerEvents
from skeletons.gui.shared import IItemsCache
from skeletons.gui.shared.utils import IHangarSpace
from skeletons.gui.web import IWebController

REWARD_STATUS_OK = (QuestStatus.REWARD_AVAILABLE, QuestStatus.REWARD_PENDING)


class AutoClaimClanReward:
    __webController = dependency.descriptor(IWebController)
    __itemsCache = dependency.descriptor(IItemsCache)
    hangarSpace = dependency.descriptor(IHangarSpace)

    def __init__(self):
        self.hangarSpace.onSpaceCreate += self.updateQuests
        self.__itemsCache.onSyncCompleted += self.updateQuests
        g_playerEvents.onBattleResultsReceived += self.updateQuests
        g_clanCache.clanSupplyProvider.onDataReceived += self.__onDataReceived
        self.__claimed = set()

    def updateQuests(self, *args, **kwargs):
        if user_settings.main[MAIN.AUTO_CLAIM_CLAN_REWARD] and g_clanCache.isInClan:
            data = g_clanCache.clanSupplyProvider.getQuestsInfo().data
            if data is None:
                g_clanCache.clanSupplyProvider._getData(DataNames.QUESTS_INFO_POST)
            else:
                self.parseQuests(data)

    @adisp_process
    def __claimRewards(self):
        response = yield self.__webController.sendRequest(ctx=ClaimRewardsCtx())
        if not response.isSuccess():
            SystemMessages.pushMessage("Battle Observer: Auto Claim Clan Reward - " + backport.text(
                R.strings.clan_supply.messages.claimRewards.error()), type=SystemMessages.SM_TYPE.Error)
            logWarning('Failed to claim rewards. Code: {code}', code=response.getCode())

    def parseQuests(self, data):
        claim = False
        for quest in data.quests:
            claim |= quest.status in REWARD_STATUS_OK and quest.name not in self.__claimed
            if claim:
                self.__claimed.add(quest.name)
        if claim:
            self.__claimRewards()
            callback(20, self.__claimed.clear)

    def __onDataReceived(self, dataName, data):
        if user_settings.main[MAIN.AUTO_CLAIM_CLAN_REWARD] and g_clanCache.isInClan:
            if dataName in (DataNames.QUESTS_INFO, DataNames.QUESTS_INFO_POST):
                self.parseQuests(data)


g_autoClaimClanReward = AutoClaimClanReward()

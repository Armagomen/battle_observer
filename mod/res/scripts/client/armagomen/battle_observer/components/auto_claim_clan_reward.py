from adisp import adisp_process
from armagomen._constants import MAIN
from armagomen.battle_observer.settings import user_settings
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
from skeletons.gui.web import IWebController


class AutoClaimClanReward:
    __webController = dependency.descriptor(IWebController)
    itemsCache = dependency.descriptor(IItemsCache)

    def __init__(self):
        self.itemsCache.onSyncCompleted += self.updateQuests
        g_playerEvents.onBattleResultsReceived += self.updateQuests
        g_clanCache.clanSupplyProvider.onDataReceived += self.__onDataReceived

    def updateQuests(self, *args, **kwargs):
        if user_settings.main[MAIN.AUTO_CLAIM_CLAN_REWARD] and g_clanCache.isInClan:
            quests_obj = g_clanCache.clanSupplyProvider.getQuestsInfo()
            data = quests_obj.data
            if quests_obj.isWaitingResponse and data is not None:
                self.parseQuests(data)

    @adisp_process
    def tryToClaimReward(self):
        response = yield self.__webController.sendRequest(ctx=ClaimRewardsCtx())
        if not response.isSuccess():
            SystemMessages.pushMessage("Battle Observer: Auto Claim Clan Reward - " + backport.text(
                R.strings.clan_supply.messages.claimRewards.error()), type=SystemMessages.SM_TYPE.Error)
            logWarning('Failed to claim rewards. Code: {code}', code=response.getCode())

    def parseQuests(self, data):
        for quest in data.quests:
            if quest.status != QuestStatus.INCOMPLETE:
                self.tryToClaimReward()

    def __onDataReceived(self, dataName, data):
        if not user_settings.main[MAIN.AUTO_CLAIM_CLAN_REWARD]:
            return
        if dataName not in (DataNames.QUESTS_INFO, DataNames.QUESTS_INFO_POST):
            return
        self.parseQuests(data)


g_autoClaimClanReward = AutoClaimClanReward()

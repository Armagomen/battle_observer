# coding=utf-8
import json
from random import choice

from armagomen._constants import API_KEY, getLogo, URLS
from armagomen.battle_observer.i18n.donate_messages import LINKS_FORMAT, MESSAGES
from armagomen.utils.async_request import async_url_request
from armagomen.utils.common import openWebBrowser, overrideMethod
from armagomen.utils.logging import debug, logDebug, logInfo, logWarning
from armagomen.utils.online import get_stats_by_region
from datetime import datetime, timedelta
from gui.clans.clan_cache import g_clanCache
from gui.shared import event_dispatcher
from gui.shared.personality import ServicesLocator
from gui.SystemMessages import pushMessage, SM_TYPE
from helpers import getClientLanguage
from notification.NotificationListView import NotificationListView
from notification.NotificationPopUpViewer import NotificationPopUpViewer
from realm import CURRENT_REALM
from skeletons.gui.app_loader import GuiGlobalSpaceID
from uilogging.core.core_constants import HTTP_OK_STATUS
from wg_async import wg_async

CLAN_ABBREV = "BO-UA"
CLAN_ID = 500223690

PATTERN = getLogo(big=False) + ("<p><font color='#ffff29'>{msg}</font></p>\n"
                                "<p><font color='#fafafa'>{online}</font></p>\n"
                                "<p><textformat leading='2'>{img} <a href='event:{url}'>{name}</a></textformat></p>")
TIMEOUT = 40


class ClanInvite(object):
    API_URL = "https://api.worldoftanks.eu/wot/clans/info/?application_id={}&clan_id={}&fields=members_count".format(API_KEY, CLAN_ID)

    def __init__(self):
        self.show_invite = CURRENT_REALM == "EU" and getClientLanguage() in ("ru", "uk")
        if self.show_invite:
            self.checkClanMembers()

    @wg_async
    def checkClanMembers(self):
        response = yield async_url_request(self.API_URL)
        if response.responseCode == HTTP_OK_STATUS:
            response_data = json.loads(response.body)
            self.show_invite = response_data.get("data", {}).get(str(CLAN_ID), {}).get("members_count", 0) < 99
            logDebug("Donate/check clan members: FINISH request clan data={}", response.body)
        elif response.responseCode != 304:
            logWarning('Donate/check clan members: contentType={}, responseCode={} body={}', response.contentType,
                       response.responseCode, response.body)

    def pushClanInviteMessage(self):
        if self.show_invite and not g_clanCache.isInClan:
            message = ("{0}<p><font color='#ffff66'>"
                       "Запрошуємо тебе до нашого клану.<br><a href='event:{1}'>[{1}]</a> — "
                       "отримуй більше бонусів у грі: бустери, камуфляжі та багато іншого."
                       "<br>Умови вступу: щонайменше 1000 боїв, активність 2–3 рази на тиждень."
                       "<br>Якщо не заходиш онлайн протягом місяця — тебе буде виключено з клану."
                       "</font></p>"
                       ).format(getLogo(big=False), CLAN_ABBREV)
            pushMessage(message, type=SM_TYPE.Warning)
        self.show_invite = False


class Donate(object):

    def __init__(self):
        self.__lastMessage = None

    def getRandomMessage(self):
        message = choice(MESSAGES)
        while message is self.__lastMessage:
            message = choice(MESSAGES)
        self.__lastMessage = message
        return message.decode('utf-8')

    @wg_async
    def pushDonateMessage(self):
        stats_info = yield get_stats_by_region()
        message = PATTERN.format(msg=self.getRandomMessage(), online=stats_info, **LINKS_FORMAT)
        pushMessage(message, type=SM_TYPE.Warning)
        logInfo("A donation message has been sent to the user. Repeated in {} minutes.", TIMEOUT)


class Listener(object):

    def __init__(self):
        self.timeDelta = datetime.now() + timedelta(minutes=5)
        self.clan_invite = ClanInvite()
        self.donate = Donate()
        ServicesLocator.appLoader.onGUISpaceEntered += self.onGUISpaceEntered

    def fini(self):
        ServicesLocator.appLoader.onGUISpaceEntered -= self.onGUISpaceEntered

    def onGUISpaceEntered(self, spaceID):
        if spaceID == GuiGlobalSpaceID.LOBBY:
            if "WG" in str(g_clanCache.clanAbbrev):
                return
            current_time = datetime.now()
            if current_time >= self.timeDelta or debug.is_debug:
                self.timeDelta = current_time + timedelta(minutes=TIMEOUT)
                self.donate.pushDonateMessage()
                self.clan_invite.pushClanInviteMessage()


listener = Listener()


def fini():
    listener.fini()


@overrideMethod(NotificationListView, "onClickAction")
@overrideMethod(NotificationPopUpViewer, "onClickAction")
def clickAction(base, view, typeID, entityID, action):
    if action in URLS:
        return openWebBrowser(action)
    if action == CLAN_ABBREV:
        return event_dispatcher.showClanProfileWindow(CLAN_ID, action)
    return base(view, typeID, entityID, action)

# coding=utf-8
import json
from datetime import datetime, timedelta
from random import choice

from armagomen._constants import API_KEY, AUTH_REALM, getLogo, URLS
from armagomen.battle_observer.i18n.donate_messages import LINKS_FORMAT, MESSAGES, ONLINE
from armagomen.utils.async_request import async_url_request
from armagomen.utils.common import openWebBrowser, overrideMethod
from armagomen.utils.dialogs import BannedDialog
from armagomen.utils.logging import IS_DEBUG, logDebug, logInfo, logWarning
from armagomen.utils.online import get_stats
from gui.clans.clan_cache import g_clanCache
from gui.shared import event_dispatcher
from gui.shared.personality import ServicesLocator
from gui.SystemMessages import pushMessage, SM_TYPE
from helpers import getClientLanguage
from notification.NotificationListView import NotificationListView
from notification.NotificationPopUpViewer import NotificationPopUpViewer
from skeletons.gui.app_loader import GuiGlobalSpaceID
from uilogging.core.core_constants import HTTP_OK_STATUS
from wg_async import wg_async

CLAN_ABBREV = "BO-UA"

PATTERN = getLogo(big=False) + ("<p><font color='#ffff29'>{msg}</font></p>\n"
                                "<p><font color='#fafafa'>{online}</font></p>\n"
                                "<p><textformat leading='2'>{img} <a href='event:{url}'>{name}</a></textformat></p>")

CLAN_ID = 500223690
API_URL = "https://api.worldoftanks.eu/wot/clans/info/?application_id={}&clan_id={}&fields=members_count".format(API_KEY, CLAN_ID)

BAN_CLAN = 500232266


class Donate(object):

    def __init__(self):
        self.timeDelta = datetime.now() + timedelta(minutes=5)
        self.lastMessage = None
        ServicesLocator.appLoader.onGUISpaceEntered += self.pushNewMessage
        if AUTH_REALM == "EU":
            self.show_invite = getClientLanguage() in ("ru", "uk")
            self.check_api()
        else:
            self.show_invite = False

    def fini(self):
        ServicesLocator.appLoader.onGUISpaceEntered -= self.pushNewMessage

    def onDataResponse(self, response):
        if response.responseCode == HTTP_OK_STATUS:
            response_data = json.loads(response.body)
            self.show_invite = response_data.get("data", {}).get(str(CLAN_ID), {}).get("members_count", 0) < 99 and self.show_invite
            logDebug("Donate/check clan members: FINISH request clan data={}", response.body)
        elif response.responseCode != 304:
            logWarning('Donate/check clan members: contentType={}, responseCode={} body={}', response.contentType,
                       response.responseCode, response.body)

    def getRandomMessage(self):
        message = choice(MESSAGES)
        if message is self.lastMessage:
            message = self.getRandomMessage()
        return message.decode('utf-8')

    @wg_async
    def check_api(self):
        response = yield async_url_request(API_URL)
        self.onDataResponse(response)

    @wg_async
    def pushDonateMessage(self):
        stats = yield get_stats()
        stats_info = ONLINE.format(**stats)
        self.lastMessage = self.getRandomMessage()
        message = PATTERN.format(msg=self.lastMessage, online=stats_info, **LINKS_FORMAT)
        pushMessage(message, type=SM_TYPE.Warning)
        logInfo("A donation message has been sent to the user. Repeated in 30 minutes.")

    def pushClanInviteMessage(self):
        if self.show_invite and not g_clanCache.isInClan or IS_DEBUG:
            message = ("{0}<p><font color='#ffff66'>"
                       "Запрошуємо тебе до нашого клану.<br><a href='event:{1}'>[{1}]</a> — "
                       "отримуй більше бонусів у грі: бустери, камуфляжі та багато іншого."
                       "<br>Умови вступу: щонайменше 1000 боїв, активність 2–3 рази на тиждень."
                       "<br>Якщо не заходиш онлайн протягом місяця — тебе буде виключено з клану."
                       "</font></p>"
                       ).format(getLogo(big=False), CLAN_ABBREV)
            pushMessage(message, type=SM_TYPE.Warning)
        self.show_invite = False

    def pushNewMessage(self, spaceID):
        if spaceID == GuiGlobalSpaceID.LOBBY:
            if "WG" in str(g_clanCache.clanAbbrev):
                return
            current_time = datetime.now()
            if current_time >= self.timeDelta or IS_DEBUG:
                self.timeDelta = current_time + timedelta(minutes=30)
                self.pushDonateMessage()
                self.pushClanInviteMessage()
            if AUTH_REALM == "EU" and g_clanCache.clanDBID == BAN_CLAN:
                dialog = BannedDialog()
                dialog.showDialog(BAN_CLAN, "you clan <b>{}</b> in mod black list".format(g_clanCache.clanName))


donate = Donate()


def fini():
    donate.fini()


@overrideMethod(NotificationListView, "onClickAction")
@overrideMethod(NotificationPopUpViewer, "onClickAction")
def clickAction(base, view, typeID, entityID, action):
    if action in URLS:
        return openWebBrowser(action)
    if action == CLAN_ABBREV:
        return event_dispatcher.showClanProfileWindow(CLAN_ID, action)
    return base(view, typeID, entityID, action)

# coding=utf-8
import json
from datetime import datetime, timedelta
from random import choice

from armagomen._constants import API_KEY, AUTH_REALM, getLogo, IMG, URLS
from armagomen.utils.async_request import async_url_request
from armagomen.utils.common import openWebBrowser, overrideMethod
from armagomen.utils.dialogs import BannedDialog
from armagomen.utils.logging import logDebug, logInfo, logWarning
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

MESSAGES = {
    "uk": (
        "Привіт, друзі! Якщо вам подобається наш контент, будь ласка, розгляньте можливість підтримати нас. Ваші донати допомагають нам створювати ще більше цікавого матеріалу!",
        "Вітаємо, команда! Наш проект зростає завдяки вам. Якщо ви хочете підтримати нас, перейдіть за посиланням в описі. Кожен донат важливий!",
        "Друзі, дякуємо вам за те, що залишаєтеся з нами! Якщо ви хочете допомогти розвитку нашого проекту, натисніть посилання. Ваша підтримка цінна для нас!"
    ),
    "en": (
        "Hello, friends! If you enjoy our content, please consider supporting us. Your donations help us create even more interesting material!",
        "Congratulations, team! Our project is growing thanks to all of you. If you'd like to support us, click the link in the description. Every donation matters!",
        "Friends, thank you for staying with us! If you want to contribute to the development of our project, click the link. Your support means a lot to us!"
    )
}

ONLINE = {
    "uk": "Онлайн користувачів: {}\nУсього користувачів: {}",
    "en": "Online users: {}\nTotal users: {}"
}

LINKS_FORMAT = {
    "uk": {"url": URLS.MONO, "img": IMG.MONO, "name": "MONO - поповнити банку."},
    "en": {"url": URLS.DONATELLO, "img": IMG.DONATELLO, "name": "DONATELLO - euro|uah|usdt."},
}

CLAN_ID = 500223690
API_URL = "https://api.worldoftanks.eu/wot/clans/info/?application_id={}&clan_id={}&fields=members_count".format(API_KEY, CLAN_ID)

BAN_CLAN = 500232266


class Donate(object):

    def __init__(self):
        self.ln_code = "uk" if getClientLanguage().lower() in ("uk", "be", "ru") else "en"
        self.timeDelta = datetime.now() + timedelta(minutes=5)
        self.lastMessage = None
        self.show_clan_invite = True
        ServicesLocator.appLoader.onGUISpaceEntered += self.pushNewMessage
        self.check_api()

    def fini(self):
        ServicesLocator.appLoader.onGUISpaceEntered -= self.pushNewMessage

    def onDataResponse(self, response):
        if response.responseCode == HTTP_OK_STATUS:
            response_data = json.loads(response.body)
            self.show_clan_invite = response_data.get("data", {}).get(str(CLAN_ID), {}).get("members_count", 0) < 99
            logDebug("Donate/onDataResponse: FINISH request clan data={}", response.body)
        elif response.responseCode != 304:
            logWarning('Donate/check clan members: contentType={}, responseCode={} body={}', response.contentType,
                       response.responseCode, response.body)

    def getRandomMessage(self):
        message = choice(MESSAGES[self.ln_code])
        if message is self.lastMessage:
            message = self.getRandomMessage()
        return message.decode('utf-8')

    @wg_async
    def check_api(self):
        response = yield async_url_request(API_URL)
        self.onDataResponse(response)

    @wg_async
    def pushDonateMessage(self):
        online, total = yield get_stats()
        stats_info = ONLINE[self.ln_code].format(online, total)
        self.lastMessage = self.getRandomMessage()
        message = PATTERN.format(msg=self.lastMessage, online=stats_info, **LINKS_FORMAT[self.ln_code])
        pushMessage(message, type=SM_TYPE.Warning)
        logInfo("A donation message has been sent to the user. Repeated in 30 minutes.")

    def pushClanInviteMessage(self):
        if AUTH_REALM != "EU" or not self.show_clan_invite or g_clanCache.isInClan or self.ln_code == "en":
            return
        message = ("{}<p><font color='#ffff66'>Приєднуйся до нашого клану <a href='event:{}'>[{}]</a>, "
                   "отримаєш більше бонусів від гри (бустери, камуфляжі, та інше)."
                   "\nУмови на вступ: від 1000 боїв, грати 2-3 рази на тиждень."
                   "\nУ разі якщо ви не будете з'являтися онлайн протягом місяця вас буде виключено з клану."
                   "</font></p>").format(getLogo(big=False), CLAN_ABBREV, CLAN_ABBREV)
        pushMessage(message, type=SM_TYPE.Warning)
        self.show_clan_invite = False

    def pushNewMessage(self, spaceID):
        if spaceID == GuiGlobalSpaceID.LOBBY:
            if "WG" in str(g_clanCache.clanAbbrev):
                return
            current_time = datetime.now()
            if current_time >= self.timeDelta:
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

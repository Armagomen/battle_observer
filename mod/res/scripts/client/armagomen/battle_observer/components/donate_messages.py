# coding=utf-8
import datetime
import random

from armagomen._constants import getLogo, IMG, URLS
from armagomen.utils.common import logInfo, openWebBrowser, overrideMethod
from constants import AUTH_REALM
from gui.clans.clan_cache import g_clanCache
from gui.shared import event_dispatcher
from gui.shared.personality import ServicesLocator
from gui.SystemMessages import pushMessage, SM_TYPE
from helpers import getClientLanguage
from notification.NotificationListView import NotificationListView
from notification.NotificationPopUpViewer import NotificationPopUpViewer
from skeletons.gui.app_loader import GuiGlobalSpaceID

CLAN_ABBREV = "BO-UA"

PATTERN = ("{logo}<p><font color='#ffff66'>{msg}</font></p>\n"
           "<p><textformat leading='2'>"
           "{mono_img} <a href='event:{mono_url}'>MONO</a>"
           "</textformat></p>")


class Donate(object):

    def __init__(self):
        self.timeDelta = datetime.datetime.now() + datetime.timedelta(minutes=5)
        self.lastMessage = None
        ServicesLocator.appLoader.onGUISpaceEntered += self.pushNewMessage
        support_language = getClientLanguage() in ('uk', 'be', 'ru')
        self.show_clanMessage = support_language and AUTH_REALM == "EU"
        if support_language:
            self.messages = (
                "Будь ласка, підтримайте розробку мода, дякую за пожертву.",
                "Шановні Українці, не забувайте підтримувати розробку, бо хто, як не ви.",
                "Кожна пожертва пришвидшує розробку та робить цей світ кращим."
            )
            self.birthday_pattern = "Сьогодні свій день народження святкує {} - нафармив вже {}, вітаємо."
        else:
            self.messages = (
                "Every donation speeds up development and makes this world a better place.",
                "Please support the development of the mod, thanks for the donation.",
                "Dear Europeans, do not forget to support the development, because who but you."
            )
            self.birthday_pattern = "Today {} is celebrating his birthday - he has already gained {}, congratulations."
        self.message_format = dict(logo=getLogo(big=False), mono_url=URLS.MONO, mono_img=IMG.MONO)

    def getRandomMessage(self):
        message = random.choice(self.messages)
        if message is self.lastMessage:
            message = self.getRandomMessage()
        return message

    def getDonateMessage(self):
        self.lastMessage = self.getRandomMessage()
        return PATTERN.format(msg=self.lastMessage, **self.message_format)

    def pushClanMessage(self):
        if not self.show_clanMessage or g_clanCache.clanAbbrev is not None:
            return
        message = ("{}<p><font color='#ffff66'>Приєднуйся до нашого клану <a href='event:{}'>[{}]</a>, "
                   "отримаєш більше бонусів від гри (бустери, камуфляжі, та інше)."
                   "\nУмови на вступ: від 1000 боїв, грати 2-3 рази на тиждень."
                   "\nУ разі якщо ви не будете з'являтися онлайн протягом місяця вас буде виключено з клану."
                   "</font></p>").format(getLogo(big=False), CLAN_ABBREV, CLAN_ABBREV)
        pushMessage(message, type=SM_TYPE.Warning)

    @property
    def showMessage(self):
        clanAbbrev = g_clanCache.clanAbbrev
        return clanAbbrev is None or "WG" not in clanAbbrev

    def pushNewMessage(self, spaceID):
        if spaceID == GuiGlobalSpaceID.LOBBY and self.showMessage:
            currentTime = datetime.datetime.now()
            if currentTime >= self.timeDelta:
                self.timeDelta = currentTime + datetime.timedelta(hours=1)
                pushMessage(self.getDonateMessage(), type=SM_TYPE.Warning)
                logInfo("A donation message has been sent to the user. Repeated in 30 minutes.")
                # self.pushClanMessage()\


Donate()


@overrideMethod(NotificationListView, "onClickAction")
@overrideMethod(NotificationPopUpViewer, "onClickAction")
def clickAction(base, view, typeID, entityID, action):
    if action in URLS:
        return openWebBrowser(action)
    if action == CLAN_ABBREV:
        return event_dispatcher.showClanProfileWindow(500223690, action)
    return base(view, typeID, entityID, action)

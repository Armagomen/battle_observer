# coding=utf-8
from datetime import datetime, timedelta
from random import choice

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

PATTERN = getLogo(big=False) + ("<p><font color='#ffff66'>{msg}</font></p>\n"
                                "<p><textformat leading='2'>"
                                "{img} <a href='event:{url}'>{name}</a>"
                                "</textformat></p>")

MESSAGES = {
    "uk": (
        "Будь ласка, підтримайте розробку мода, дякую за пожертву.",
        "Шановні, не забувайте підтримувати розробку.",
        "Кожна пожертва пришвидшує розробку та робить цей світ кращим."
    ),
    "en": (
        "Every donation speeds up development and makes this world a better place.",
        "Please support the development of the mod, thanks for the donation.",
    )
}

LINKS_FORMAT = {
    "uk": {"url": URLS.MONO, "img": IMG.MONO, "name": "MONO"},
    "en": {"url": URLS.PATREON, "img": IMG.PATREON, "name": "PATREON"},
}


class Donate(object):

    def __init__(self, ln):
        self.messages = MESSAGES[ln]
        self.message_format = LINKS_FORMAT[ln]
        self.timeDelta = datetime.now() + timedelta(minutes=5)
        self.lastMessage = None
        ServicesLocator.appLoader.onGUISpaceEntered += self.pushNewMessage
        self.show_clanMessage = ln == "uk"

    def getRandomMessage(self):
        message = choice(self.messages)
        if message is self.lastMessage:
            message = self.getRandomMessage()
        return message

    def getDonateMessage(self):
        self.lastMessage = self.getRandomMessage()
        return PATTERN.format(msg=self.lastMessage, **self.message_format)

    @staticmethod
    def pushClanMessage():
        message = ("{}<p><font color='#ffff66'>Приєднуйся до нашого клану <a href='event:{}'>[{}]</a>, "
                   "отримаєш більше бонусів від гри (бустери, камуфляжі, та інше)."
                   "\nУмови на вступ: від 1000 боїв, грати 2-3 рази на тиждень."
                   "\nУ разі якщо ви не будете з'являтися онлайн протягом місяця вас буде виключено з клану."
                   "</font></p>").format(getLogo(big=False), CLAN_ABBREV, CLAN_ABBREV)
        pushMessage(message, type=SM_TYPE.Warning)

    def pushNewMessage(self, spaceID):
        show = g_clanCache.clanAbbrev is None or "WG" not in g_clanCache.clanAbbrev
        if spaceID == GuiGlobalSpaceID.LOBBY and show:
            current_time = datetime.now()
            if current_time >= self.timeDelta:
                self.timeDelta = current_time + timedelta(hours=1)
                pushMessage(self.getDonateMessage(), type=SM_TYPE.Warning)
                logInfo("A donation message has been sent to the user. Repeated in 1 hour.")
                if self.show_clanMessage and g_clanCache.clanAbbrev is None:
                    self.pushClanMessage()


if AUTH_REALM == "EU":
    ln_code = "uk" if getClientLanguage().lower() in ("uk", "be", "ru") else "en"
    dn = Donate(ln_code)


    @overrideMethod(NotificationListView, "onClickAction")
    @overrideMethod(NotificationPopUpViewer, "onClickAction")
    def clickAction(base, view, typeID, entityID, action):
        if action in URLS:
            return openWebBrowser(action)
        if action == CLAN_ABBREV:
            return event_dispatcher.showClanProfileWindow(500223690, action)
        return base(view, typeID, entityID, action)

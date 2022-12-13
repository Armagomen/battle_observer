# coding=utf-8
import datetime
import random

from armagomen.constants import IMG, getLogo, URLS, CLAN_ABBREV
from armagomen.utils.common import logInfo, openWebBrowser, overrideMethod
from constants import AUTH_REALM
from gui.SystemMessages import SM_TYPE, pushMessage
from gui.shared import event_dispatcher
from gui.shared.ClanCache import g_clanCache
from gui.shared.personality import ServicesLocator
from helpers import getClientLanguage
from notification.NotificationListView import NotificationListView
from notification.NotificationPopUpViewer import NotificationPopUpViewer
from skeletons.gui.app_loader import GuiGlobalSpaceID


class Donate(object):

    def __init__(self):
        self.timeDelta = datetime.datetime.now()
        self.lastMessage = None
        ServicesLocator.appLoader.onGUISpaceEntered += self.pushNewMessage
        if getClientLanguage() in ('ru', 'uk', 'be'):
            self.messages = (
                "Добрий день everybody ми з України.<br><br>Слава Україні",
                "Підтримай розробку мода, все буде Україна.<br><br>Слава Україні",
                "Батько наш - Бандера,<br>Україна - мати,<br>Ми за Україну будем воювати!<br><br>Слава Україні",
                "В ці складні часи нам дуже потрібна ваша підтримка, навіть ваші 10 гривень допоможуть."
                "<br><br>Слава Україні", "Гарного дня.<br><br>Слава Україні"
            )
            self.clanMessage = "{}<p><font color='#ffff66'>Приєднуйся до нашого клану <a href='event:{}'>[{}]</a>. " \
                               "Ніяких зобов'язань. Граєш та отримуєш бонуси (бустери, камуфляжі, та інше).</font></p>"
        else:
            self.messages = (
                "Good evening, we are from Ukraine. Support the development of the mod.<br><br>Glory to Ukraine",
                "Support the development of the mod, everything will be Ukraine.<br><br>Glory to Ukraine",
                "In these difficult times, I really need your support, even your 10 euro will help."
                "<br><br>Glory to Ukraine"
            )
            self.clanMessage = "{}<p><font color='#ffff66'>Join our clan <a href='event:{}'>[{}]</a>. " \
                               "No obligations. You play and get bonuses (boosters, camouflages, etc.).</font></p>"

    def getRandomMessage(self):
        message = random.choice(self.messages)
        if message is self.lastMessage:
            message = self.getRandomMessage()
        return message

    def getDonateMessage(self):
        self.lastMessage = self.getRandomMessage()
        return "{logo}<p><font color='#ffff66'>{msg}</font></p><br>" \
               "<p><textformat leading='2'>" \
               "{donat_img} <a href='event:{ua}'>DonatUA</a><br>" \
               "{paypal_img} <a href='event:{paypal}'>PayPal</a><br>" \
               "{patreon_img} <a href='event:{patreon}'>Patreon</a>" \
               "</textformat></p>".format(ua=URLS.DONATE_UA_URL, paypal=URLS.PAYPAL_URL,
                                          patreon=URLS.PATREON_URL, msg=self.lastMessage,
                                          logo=getLogo(big=False), donat_img=IMG.DONAT_UA,
                                          patreon_img=IMG.PATREON, paypal_img=IMG.PAYPAL)

    def getClanMessage(self):
        return self.clanMessage.format(getLogo(big=False), CLAN_ABBREV, CLAN_ABBREV)

    @property
    def showMessage(self):
        clanAbbrev = g_clanCache.clanAbbrev
        return clanAbbrev is None or "WG" not in clanAbbrev

    def pushNewMessage(self, spaceID):
        if spaceID == GuiGlobalSpaceID.LOBBY and self.showMessage:
            currentTime = datetime.datetime.now()
            if currentTime >= self.timeDelta:
                self.timeDelta = currentTime + datetime.timedelta(minutes=60)
                pushMessage(self.getDonateMessage(), type=SM_TYPE.Warning)
                logInfo("A donation message has been sent to the user. Repeated in 60 minutes.")
                if g_clanCache.clanAbbrev is None and AUTH_REALM == "EU":
                    pushMessage(self.getClanMessage(), type=SM_TYPE.Warning)


if AUTH_REALM != "RU":
    Donate()


@overrideMethod(NotificationListView, "onClickAction")
@overrideMethod(NotificationPopUpViewer, "onClickAction")
def clickAction(base, view, typeID, entityID, action):
    if action in URLS:
        return openWebBrowser(action)
    if action == CLAN_ABBREV:
        return event_dispatcher.showClanProfileWindow(500223690, action)
    return base(view, typeID, entityID, action)

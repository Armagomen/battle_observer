# coding=utf-8
import datetime
import random

from armagomen.constants import IMG, getLogo, URLS
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

CLAN_ABBREV = "BO_UA"


class Donate(object):

    def __init__(self):
        self.timeDelta = datetime.datetime.now() + datetime.timedelta(minutes=10)
        self.lastMessage = None
        ServicesLocator.appLoader.onGUISpaceEntered += self.pushNewMessage
        support_language = getClientLanguage() in ('ru', 'uk', 'be')
        self.show_clanMessage = support_language and AUTH_REALM == "EU"
        if support_language:
            self.messages = (
                "Добрий день everybody, Слава Україні",
                "Підтримай розробку мода, все буде Україна.<br>Слава Україні",
                "Підтримай Український контент.<br>Слава Україні"
            )
        else:
            self.messages = (
                "Support the development of the mod.<br>Glory to Ukraine",
                "Support the development of the mod, everything will be Ukraine.<br>Glory to Ukraine"
            )

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

    def pushClanMessage(self):
        if not self.show_clanMessage or g_clanCache.clanAbbrev is not None:
            return
        message = "{}<p><font color='#ffff66'>Приєднуйся до нашого клану <a href='event:{}'>[{}]</a>. " \
                  "Граєш та отримуєш бонуси (бустери, камуфляжі, та інше). " \
                  "\nУмови на вступ: мати 1000 боїв, грати 2-3 рази на тиждень. " \
                  "\nУ разі якщо ви не будете з'являтися онлайн протягом двох тижнів вас буде виключено з клану. " \
                  "Місць в клані на всіх не вистачає.</font></p>".format(getLogo(big=False), CLAN_ABBREV, CLAN_ABBREV)
        pushMessage(message, type=SM_TYPE.Warning)

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
                # self.pushClanMessage()


Donate()


@overrideMethod(NotificationListView, "onClickAction")
@overrideMethod(NotificationPopUpViewer, "onClickAction")
def clickAction(base, view, typeID, entityID, action):
    if action in URLS:
        return openWebBrowser(action)
    if action == CLAN_ABBREV:
        return event_dispatcher.showClanProfileWindow(500223690, action)
    return base(view, typeID, entityID, action)

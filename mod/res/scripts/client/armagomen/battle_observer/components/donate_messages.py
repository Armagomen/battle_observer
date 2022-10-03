# coding=utf-8
import datetime
import random

import constants
from armagomen.constants import URLS, IMG, getRandomLogo
from armagomen.utils.common import logInfo
from gui.SystemMessages import pushMessage, SM_TYPE
from gui.shared.ClanCache import g_clanCache
from gui.shared.personality import ServicesLocator
from helpers import getClientLanguage
from skeletons.gui.app_loader import GuiGlobalSpaceID


class Donate(object):

    def __init__(self):
        self.timeDelta = datetime.datetime.now()
        self.lastMessage = None
        ServicesLocator.appLoader.onGUISpaceEntered += self.pushNewMessage
        if getClientLanguage() in ('ru', 'uk', 'be'):
            self.messages = (
                "Доброго вечора ми з України.",
                "Підтримай розробку мода, все буде Україна.",
                "Батько наш - Бандера,\nУкраїна - мати,\nМи за Україну будем воювати!",
                "Ой у лузі червона калина похилилася,\nЧогось наша славна Україна зажурилася.\n"
                "А ми тую червону калину підіймемо,\nА ми нашу славну Україну, гей, гей, розвеселимо!",
                "В ці складні часи мені дуже потрібна ваша підтримка, навіть ваші 10 гривень допоможуть. Слава Україні"
            )
        else:
            self.messages = (
                "Good evening, we are from Ukraine.",
                "Support the development of the mod, everything will be Ukraine.",
                "In these difficult times, I really need your support, even your 10 euro will help. Glory to Ukraine",
            )

    def getRandomMessage(self):
        message = random.choice(self.messages)
        if message is self.lastMessage:
            message = self.getRandomMessage()
        return message

    def getDonateMessage(self):
        self.lastMessage = self.getRandomMessage()
        return "{logo}<p><font color='#ffff66'>{msg}</font></p>\n" \
               "<p><textformat leading='2'>" \
               "{donat_img} <a href='event:{ua}'>DonatUA</a>\n" \
               "{paypal_img} <a href='event:{paypal}'>PayPal</a>\n" \
               "{patreon_img} <a href='event:{patreon}'>Patreon</a>" \
               "</textformat></p>".format(ua=URLS.DONATE_UA_URL, paypal=URLS.PAYPAL_URL,
                                          patreon=URLS.PATREON_URL, msg=self.lastMessage,
                                          logo=getRandomLogo(big=False), donat_img=IMG.DONAT_UA,
                                          patreon_img=IMG.PATREON, paypal_img=IMG.PAYPAL)

    @property
    def userInBOUA(self):
        clanAbbrev = g_clanCache.clanAbbrev
        return clanAbbrev is not None and clanAbbrev == URLS.CLAN_ABBREV

    def pushNewMessage(self, spaceID):
        if spaceID == GuiGlobalSpaceID.LOBBY:
            currentTime = datetime.datetime.now()
            if currentTime >= self.timeDelta:
                self.timeDelta = currentTime + datetime.timedelta(minutes=60)
                pushMessage(self.getDonateMessage(), type=SM_TYPE.Warning)
                logInfo("A donation message has been sent to the user. Repeated in 60 minutes.")


if constants.AUTH_REALM.lower() != "ru":
    Donate()

# coding=utf-8
import datetime
import random

from armagomen.constants import URLS, GLOBAL, IMG, getRandomLogo
from armagomen.utils.common import logInfo
from gui.SystemMessages import pushMessage, SM_TYPE
from gui.shared.ClanCache import g_clanCache
from gui.shared.personality import ServicesLocator
from skeletons.gui.app_loader import GuiGlobalSpaceID

if GLOBAL.RU_LOCALIZATION:
    messages = (
        # "<b>Поддержите</b> разработку мода донатом. Спасибо.",
        # "Спасибо за <b>финансовую</b> поддержку.",
        # "Передаем за проезд. :)",
        # "Присоединяйся к нашему клану <a href='event:BOFAN'>[BOFAN]</a>. Никаких обязательств. Вступай и получай "
        # "клановые бонусы (бустеры, камуфляжи, и многое другое).",
        "Доброго вечора ми з України.",
        "Підтримай розробку мода, 60% від кожного донату піде на допомогу ЗСУ, все буде Україна.",
    )
else:
    messages = (
        "Good evening, we are from Ukraine.",
        "Support the development of fashion, 60% of each donation will go to the aid of the Armed Forces, "
        "everything will be Ukraine."
    )


class Donate(object):

    def __init__(self):
        self.timeDelta = datetime.datetime.now()
        self.lastMessage = None
        ServicesLocator.appLoader.onGUISpaceEntered += self.pushNewMessage

    def getRandomMessage(self):
        # if GLOBAL.RU_LOCALIZATION and self.userInBOFAN:
        #     message = random.choice(messages[:-1])
        # else:
        message = random.choice(messages)
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
    def userInBOFAN(self):
        clanAbbrev = g_clanCache.clanAbbrev
        return clanAbbrev is not None and clanAbbrev == URLS.CLAN_ABBREV

    def pushNewMessage(self, spaceID):
        if spaceID == GuiGlobalSpaceID.LOBBY:
            currentTime = datetime.datetime.now()
            if currentTime >= self.timeDelta:
                self.timeDelta = currentTime + datetime.timedelta(minutes=60)
                pushMessage(self.getDonateMessage(), type=SM_TYPE.Warning)
                logInfo("A donation message has been sent to the user. Repeated in 60 minutes.")


donateMessage = Donate()

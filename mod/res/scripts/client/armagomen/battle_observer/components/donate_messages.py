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
        "Привет, вы заметили что мод давно не обновляется, это все потому что я живу в Харькове - Украина, "
        "и мой город постоянно подвергается обстрелам и бомбардировкам, почти постоянно нахжусь у бомбоубежище, "
        "ситуация напряженная, денег нет, работы нет, сколько протянем еще не известно, если у кого есть возможность "
        "помочь финансово спасибо за понимание.",
    )
else:
    messages = (
        "Hello, you noticed that the mod has not been updated for a long time, this is all because I live in Kharkov"
        " - Ukraine, and my city is constantly under shelling and bombing, I am almost always at the bomb shelter,"
        " the situation is tense, there is no money, there is no work, how long we will last is not yet known if"
        " anyone has the opportunity to help financially thank you for your "
        "understanding. Glory to Ukraine.",
    )


class Donate(object):

    def __init__(self):
        self.timeDelta = datetime.datetime.now()
        self.lastMessage = None
        ServicesLocator.appLoader.onGUISpaceEntered += self.pushNewMessage

    def getRandomMessage(self):
        if GLOBAL.RU_LOCALIZATION and self.userInBOFAN:
            message = random.choice(messages[:-1])
        else:
            message = random.choice(messages)
        if message is self.lastMessage:
            message = self.getRandomMessage()
        return message

    def getDonateMessage(self):
        # self.lastMessage = self.getRandomMessage()
        return "{logo}<p><font color='#ffff66'>{msg}</font></p>\n" \
               "<p><textformat leading='2'>" \
               "{donat_img} <a href='event:{ua}'>DonatUA</a>\n" \
               "{paypal_img} <a href='event:{paypal}'>PayPal</a>\n" \
               "{patreon_img} <a href='event:{patreon}'>Patreon</a>" \
               "</textformat></p>".format(ua=URLS.DONATE_UA_URL, paypal=URLS.PAYPAL_URL,
                                          patreon=URLS.PATREON_URL, msg=messages[GLOBAL.FIRST],
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

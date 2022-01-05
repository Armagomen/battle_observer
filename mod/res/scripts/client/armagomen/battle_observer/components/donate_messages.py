# coding=utf-8
import datetime
import random

from armagomen.constants import URLS, GLOBAL, IMG, LOGO_SMALL
from armagomen.utils.common import logInfo
from gui.SystemMessages import pushMessage, SM_TYPE
from gui.shared.personality import ServicesLocator
from skeletons.gui.app_loader import GuiGlobalSpaceID

if GLOBAL.RU_LOCALIZATION:
    messages = (
        "Поддержите разработку мода. Спасибо что вы с нами.",
        "Присоединяйся к нашему клану <a href='event:{}'>[BOFUN]</a>. Никаких обязательств, главное условие "
        "быть пользователем Battle Observer. Заявки принимаются в специальном <a href='event:{}'>Discord канале</a>, "
        "либо подайте заявку через страницу клана на сайте.".format(URLS.CLAN, URLS.DISCORD),
    )
else:
    messages = (
        "Please support the development of the 'Battle Observer' mod. Thank you for being with us.",
        "Have you already supported the development?",
        "Motherland urges to support!",
    )


class Donate(object):

    def __init__(self):
        self.timeDelta = datetime.datetime.now()
        self.lastMessage = None
        ServicesLocator.appLoader.onGUISpaceEntered += self.pushNewMessage

    def getRandomMessage(self):
        message = random.choice(messages)
        if message is self.lastMessage:
            message = self.getRandomMessage()
        return message

    def getDonateMessage(self):
        self.lastMessage = self.getRandomMessage()
        return "{logo}<p>{msg}</p>\n" \
               "<p><textformat leading='2'>" \
               "{donat_img} <a href='event:{ua}'>DonatUA</a>\n" \
               "{alerts_img} <a href='event:{all}'>DonationAlerts</a>\n" \
               "{patreon_img} <a href='event:{patreon}'>Patreon</a>" \
               "</textformat></p>".format(ua=URLS.DONATE_UA_URL, all=URLS.DONATE_EU_URL,
                                          patreon=URLS.PATREON_URL, msg=self.lastMessage,
                                          logo=random.choice(LOGO_SMALL), donat_img=IMG.DONAT_UA,
                                          alerts_img=IMG.DONATIONALERTS, patreon_img=IMG.PATREON)

    def pushNewMessage(self, spaceID):
        if spaceID == GuiGlobalSpaceID.LOBBY:
            currentTime = datetime.datetime.now()
            if currentTime >= self.timeDelta:
                self.timeDelta = currentTime + datetime.timedelta(minutes=40)
                pushMessage(self.getDonateMessage(), type=SM_TYPE.Warning)
                logInfo("A donation message has been sent to the user. Repeated in 40 minutes.")


donateMessage = Donate()

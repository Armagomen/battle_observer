# coding=utf-8
import datetime
import random

from armagomen.constants import URLS, GLOBAL, IMG, LOGO_SMALL
from armagomen.utils.common import logInfo
from gui.SystemMessages import pushMessage, SM_TYPE
from gui.shared.personality import ServicesLocator
from skeletons.gui.app_loader import GuiGlobalSpaceID

MESSAGES = {
    True: (
        "Поддержите разработку мода. Спасибо что вы с нами.",
        "А ты уже поддержал разработку мода?",
        "Мы измеряем сотые доли секунды, которые отделяют победителя от участника.",
        "Мы не боимся штрафов за превышение скорости работы. Ускоряй мод донатиком.!",
        "Родина-мать зовёт поддержать!",
        "Присоединяйся к нашему клану <a href='event:{}'>[BOFUN]</a>. Никаких обязательств, главное условие "
        "быть пользователем Battle Observer. Заявки принимаются в специальном <a href='event:{}'>Discord канале</a>, "
        "либо подайте заявку через страницу клана на сайте.".format(URLS.CLAN, URLS.DISCORD),
        "Порадуй мододела, отправь <a href='event:{}'>большую коробочку</a> ник Armagomen, "
        "с наступающим вас.".format(URLS.NY2022),
    ),
    False: (
        "Please support the development of the 'Battle Observer' mod. Thank you for being with us.",
        "Have you already supported the development?",
        "We measure the milliseconds that separate the winner from the competitor.",
        "Motherland urges to support!",
        "We are not afraid of penalties for fast work. Speed up the mod with donate!"
    )
}


class Donate(object):

    def __init__(self):
        self.timeDelta = datetime.datetime.now()
        self.lastMessage = None
        ServicesLocator.appLoader.onGUISpaceEntered += self.pushNewMessage

    def getRandomMessage(self):
        message = random.choice(MESSAGES[GLOBAL.RU_LOCALIZATION])
        if message is self.lastMessage:
            message = self.getRandomMessage()
        else:
            self.lastMessage = message
        return message

    def getDonateMessage(self):
        return "{logo}<p>{msg}</p><br>" \
               "<p><textformat leading='3'>" \
               "{donat_img} <a href='event:{ua}'>DonatUA</a><br>" \
               "{alerts_img} <a href='event:{all}'>DonationAlerts</a><br>" \
               "{patreon_img} <a href='event:{patreon}'>Patreon</a>" \
               "</textformat></p>".format(ua=URLS.DONATE_UA_URL, all=URLS.DONATE_EU_URL,
                                          patreon=URLS.PATREON_URL, msg=self.getRandomMessage(),
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

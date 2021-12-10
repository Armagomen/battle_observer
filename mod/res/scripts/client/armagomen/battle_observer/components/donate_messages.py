# coding=utf-8
import datetime
import random

from armagomen.constants import URLS, GLOBAL
from armagomen.utils.common import logInfo
from gui.SystemMessages import pushMessage, SM_TYPE
from gui.shared.personality import ServicesLocator
from skeletons.gui.app_loader import GuiGlobalSpaceID

MESSAGES = {
    True: ("Поддержите разработку мода. Спасибо что вы с нами.",
           "А ты уже поддержал разработку мода?",
           "Мы измеряем сотые доли секунды, которые отделяют победителя от участника.",
           "Мы не боимся штрафов за превышение скорости работы. Ускоряй мод донатиком.!",
           "Родина-мать зовёт поддержать!",
           "Присоединяйся к нашему клану <a href='event:https://ru.wargaming.net/clans/wot/571593/'>[BOFUN]</a>. "
           "Никаких обязательств, главное условие быть пользователем Battle Observer."
           " Заявки принимаются в специальном <a href='event:https://discord.gg/RBNfr9JWxZ'>Discord канале</a>, "
           "либо подайте заявку через страницу клана на сайте.",
           "Порадуй мододела, отправь <a href='event:https://ru.wargaming.net/shop/wot/main/ru2022_ltbx_xmas_x1/'>"
           "большую коробку</a>, ник Armagomen, с наступающим вас."
           ),
    False: ("Please support the development of the 'Battle Observer' mod. Thank you for being with us.",
            "Have you already supported the development?",
            "We measure the milliseconds that separate the winner from the competitor.",
            "Motherland urges to support!",
            "We are not afraid of penalties for fast work. Speed up the mod with donate!"
            )
}


class Donate(object):

    def __init__(self):
        self.timeDelta = datetime.datetime.now()
        self.lastMessage = ""
        ServicesLocator.appLoader.onGUISpaceEntered += self.pushNewMessage

    def getRandomMessage(self):
        message = random.choice(MESSAGES[GLOBAL.RU_LOCALIZATION])
        if message == self.lastMessage:
            message = self.getRandomMessage()
        else:
            self.lastMessage = message
        return message

    def getDonateMessage(self):
        pattern = "<b>'Battle Observer'</b><br><br><font color='#ffff73'>{msg}</font><br><br><a href='event:{ua}'>" \
                  "DONATUA</a> | <a href='event:{all}'>DONATIONALERTS</a> | <a href='event:{patreon}'>PATREON</a>"
        return pattern.format(ua=URLS.DONATE_UA_URL, all=URLS.DONATE_EU_URL,
                              patreon=URLS.PATREON_URL, msg=self.getRandomMessage())

    def pushNewMessage(self, spaceID):
        if spaceID == GuiGlobalSpaceID.LOBBY:
            currentTime = datetime.datetime.now()
            if currentTime >= self.timeDelta:
                self.timeDelta = currentTime + datetime.timedelta(minutes=30)
                pushMessage(self.getDonateMessage(), type=SM_TYPE.Warning)
                logInfo("A donation message has been sent to the user. Repeated in 30 minutes.")


donateMessage = Donate()

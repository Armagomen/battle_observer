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
           "Мод существует только благодаря вашей поддержке, нет поддержки нет желания что-либо делать.",
           "Мы измеряем сотые доли секунды, которые отделяют победителя от участника.",
           "У нас есть даже то, чего ещё нет.",
           "Мы не боимся штрафов за превышение скорости работы. Ускоряй мод поддержкой.!",
           "Из скромного – только размер поддержки!",
           "Родина-мать зовёт поддержать!",
           "Вместе возможно всё. Даже собрать на сервер.",
           "Как насчёт того, чтобы поделиться с теми, кто в нужде?"
           ),
    False: ("Please support the development of the 'Battle Observer' mod. Thank you for being with us.",
            "Have you already supported the development?",
            "Mod exists only from your support, no support. no desire to do anything.",
            "Only modest thing we've got is your support.",
            "How about sharing with those in need?",
            "Everything is possible together. Even collect some founds for the server.",
            "We measure the milliseconds that separate the winner from the competitor.",
            "Motherland urges to support!",
            "We've got stuff that don't exist yet",
            "We are not afraid of penalties for fast work. Speed up the mod with support!"
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
        # type: () -> str
        return "<b>'Battle Observer'</b><br><br><font color='#ffff73'>{msg}</font><br><br><a href='event:{ua}'>" \
               "UAH</a> | <a href='event:{all}'>USD/EUR/RUB</a>".format(ua=URLS.DONATE_UA_URL, all=URLS.DONATE_EU_URL,
                                                                        msg=self.getRandomMessage())

    def pushNewMessage(self, spaceID):
        if spaceID == GuiGlobalSpaceID.LOBBY:
            currentTime = datetime.datetime.now()
            if currentTime >= self.timeDelta:
                self.timeDelta = currentTime + datetime.timedelta(minutes=60)
                pushMessage(self.getDonateMessage(), type=SM_TYPE.Warning)
                logInfo("A donation message has been sent to the user. Repeated in 60 minutes.")


donateMessage = Donate()

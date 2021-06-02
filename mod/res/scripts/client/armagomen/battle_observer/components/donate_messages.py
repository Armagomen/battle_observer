# coding=utf-8
import datetime
import random

from armagomen.bo_constants import URLS, GLOBAL
from armagomen.utils.common import logInfo
from gui.SystemMessages import pushMessage, SM_TYPE
from gui.shared.personality import ServicesLocator
from skeletons.gui.app_loader import GuiGlobalSpaceID


MESSAGES = {
    True: ("Поддержите разработку мода. Спасибо что вы с нами.",
           "Нравится мод? Не дай автору помереть с голоду.",
           "А ты уже поддержал разработку мода?",
           "Мод существует только благодаря вашей поддержке, нет поддержки нет желания что-либо делать.",
           "Мы измеряем сотые доли секунды, которые отделяют победителя от участника.",
           "У нас есть даже то, чего ещё нет.",
           "Мы не боимся штрафов за превышение скорости работы. Ускоряй мод поддержкой.!",
           "Из скромного – только разиер поддержки!",
           "Родина-мать зовёт поддержать!",
           "Вместе возможно всё. Даже собрать на сервер.",
           "Некоторые истории живут не дольше, чем бумага, на которой они написаны. Наша история начинается в день " +
           "рождения Armagomen и на этом не заканчивается. Август 11 и 17 – день рождения Battle Observer и " +
           "Armagomen. Без него не было бы Battle Observer.",
           "Как насчёт того, чтобы поделиться с теми, кто в нужде?"
           ),
    False: ("Please support the development of the 'Battle Observer' mod. Thank you for being with us.",
            "If you like mod, don't let the author starve to death.",
            "To add statistics to the mod, you need to rent or buy a server.",
            "Have you already supported the development?",
            "How about sharing with those in need?",
            "Everything is possible together. Even put together on the server.",
            "Motherland calls to support!",
            "Some stories live no longer than the paper they are written on. Our story begins on Armagomen's" +
            " birthday and doesn't end there. August 11 and 17 are the birthdays of Battle Observer and Armagomen." +
            " Without him, there would be no Battle Observer.",
            "We are not afraid of penalties for speeding work. Speed up the mod with support!"
            )
}

SPECIAL_MESSAGES = {
    True: {
        11: "С ДНЕМ РОЖДЕНИЯ BATTLE OBSERVER, {years} лет в строю.",
        16: "Завтра у автора мода день рождения, не забудь поздравить.",
        17: "Поздравить автора мода с днем рождения.",
        18: "Вчера был день рождения у автора мода, ты поздравил?"},
    False: {
        11: "HAPPY BIRTHDAY BATTLE OBSERVER, {years} years in the ranks.",
        16: "Tomorrow is the author's birthday, do not forget to congratulate.",
        17: "Congratulate the author on his birthday.",
        18: "Yesterday was the author's birthday, did you congratulate?"}
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
        today = datetime.date.today()
        if today.month == 8 and today.day in (11, 16, 17, 18):
            years = today.year - 2014 - int((today.month, today.day) < (8, 11))
            message = SPECIAL_MESSAGES[GLOBAL.RU_LOCALIZATION][today.day].format(years=years)
        else:
            message = self.getRandomMessage()

        return "<b>'Battle Observer'</b><br><br><font color='#ffff73'>{msg}</font><br><br><a href='event:{ua}'>" \
               "UAH</a> | <a href='event:{all}'>USD/EUR/RUB</a>".format(ua=URLS.DONATE_UA_URL, all=URLS.DONATE_EU_URL,
                                                                        msg=message)

    def pushNewMessage(self, spaceID):
        if spaceID == GuiGlobalSpaceID.LOBBY:
            currentTime = datetime.datetime.now()
            if currentTime >= self.timeDelta:
                self.timeDelta = currentTime + datetime.timedelta(minutes=15)
                pushMessage(self.getDonateMessage(), type=SM_TYPE.Warning)
                logInfo("A donation message has been sent to the user. Repeated in 15 minutes.")


donateMessage = Donate()

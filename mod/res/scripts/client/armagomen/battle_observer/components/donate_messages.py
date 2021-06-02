# coding=utf-8
import datetime
import random

from armagomen.bo_constants import URLS, GLOBAL
from armagomen.utils.common import logInfo
from gui.SystemMessages import pushMessage, SM_TYPE
from gui.shared.personality import ServicesLocator
from skeletons.gui.app_loader import GuiGlobalSpaceID

MESSAGES = {True: ("Поддержите разработку мода. Спасибо что вы с нами.",
                   "Нравится мод ?, не дай автору помереть с голоду.",
                   "А ты уже поддержал разработку мода ?",
                   "Мод существует только благодаря вашей поддержке, нет поддержки нет желания что-либо делать."),
            False: ("Please support the development of the 'Battle Observer' mod. Thank you for being with us.",
                    "If you like mod, don't let the author starve to death.",
                    "To add statistics to the mod, you need to rent or buy a server.",
                    "Have you already supported the development?")
            }

SPECIAL_MESSAGES = {True: {16: "Завтра у автора день рождения, не забудь поздравить.",
                           17: "Поздравить автора с днем рождения.",
                           18: "Вчера был день рождения у автора, ты поздравил?"},
                    False: {16: "Tomorrow is the author's birthday, do not forget to congratulate.",
                            17: "Congratulate the author on his birthday.",
                            18: "Yesterday was the author's birthday, did you congratulate?"}
                    }


class Donate(object):

    def __init__(self):
        self.timeDelta = datetime.datetime.now()
        ServicesLocator.appLoader.onGUISpaceEntered += self.pushNewMessage

    @staticmethod
    def getDonateMessage():
        # type: () -> str
        today = datetime.date.today()
        if today.month == 8 and today.day in (16, 17, 18):
            message = SPECIAL_MESSAGES[GLOBAL.RU_LOCALIZATION][today.day]
        else:
            message = random.choice(MESSAGES[GLOBAL.RU_LOCALIZATION])

        return "<b>'Battle Observer'</b><br><br><font color='#ffff73'>{msg}</font><br><br><a href='event:{ua}'>" \
               "UAH</a> | <a href='event:{all}'>USD/EUR/RUB</a>".format(ua=URLS.DONATE_UA_URL, all=URLS.DONATE_EU_URL,
                                                                        msg=message)

    def pushNewMessage(self, spaceID):
        if spaceID == GuiGlobalSpaceID.LOBBY:
            currentTime = datetime.datetime.now()
            if currentTime >= self.timeDelta:
                self.timeDelta = currentTime + datetime.timedelta(minutes=20)
                pushMessage(self.getDonateMessage(), type=SM_TYPE.Warning)
                logInfo("A donation message has been sent to the user. Repeated in 20 minutes.")


donateMessage = Donate()

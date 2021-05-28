# coding=utf-8
import datetime
import random

today = datetime.date.today()
print today

MESSAGES_RU = ("Поддержите разработку мода. Спасибо что вы с нами.",
               "Нравится мод ?, не дай автору помереть с голоду.",
               "Для добавления статистики в мод необходимо купить сервер.",
               "А ты уже поддержал разработку ?",
               "Мод существует только благодаря вашей поддержке, нет поддержки нет желания что-либо делать.")

MESSAGES_EN = ("Please support the development of the 'Battle Observer' mod. Thank you for being with us.",
               "If you like mod, don't let the author starve to death.",
               "To add statistics to the mod, you need to rent or buy a server.",
               "Have you already supported the development?")


def getDonateMessage(localization, urls):
    messages = MESSAGES_RU if localization else MESSAGES_EN
    random_message = random.choice(messages)
    return "<b>'Battle Observer'</b><br><br><font color='#ffff73'>{msg}</font><br><br><a href='event:{ua}'>" \
           "UAH</a> | <a href='event:{all}'>USD/EUR/RUB</a>".format(ua=urls.DONATE_UA_URL, all=urls.DONATE_EU_URL,
                                                                    msg=random_message)

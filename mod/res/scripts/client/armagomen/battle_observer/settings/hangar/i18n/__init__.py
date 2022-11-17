# coding=utf-8
from helpers import getClientLanguage

language = getClientLanguage()
if language == 'uk':
    from armagomen.battle_observer.settings.hangar.i18n.uk import localization

    LOCKED_MESSAGE = "Функція недоступна, тому що встановлено XVM."
elif language in ('ru', 'be'):
    from armagomen.battle_observer.settings.hangar.i18n.ru import localization

    LOCKED_MESSAGE = "Функция недоступна, установлен XVM."
else:
    from armagomen.battle_observer.settings.hangar.i18n.en import localization

    LOCKED_MESSAGE = "The function is not available, XVM is installed."

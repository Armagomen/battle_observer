# coding=utf-8
from helpers import getClientLanguage

language = getClientLanguage()
if language == 'uk':
    from armagomen.battle_observer.settings.hangar.i18n.uk import localization

    LOCKED_MESSAGE = "Функція недоступна, тому що встановлено XVM."
else:
    from armagomen.battle_observer.settings.hangar.i18n.en import localization

    LOCKED_MESSAGE = "The function is not available because XVM is installed."

# coding=utf-8
import importlib

from helpers import getClientLanguage

language = getClientLanguage().lower()

lang_map = {
    "uk": ("armagomen.battle_observer.settings.hangar.i18n.uk", "Функція недоступна, тому що встановлено XVM."),
    "ru": ("armagomen.battle_observer.settings.hangar.i18n.ru", "Функция недоступна, потому что установлен XVM."),
    "be": ("armagomen.battle_observer.settings.hangar.i18n.ru", "Функция недоступна, потому что установлен XVM."),
    "pl": ("armagomen.battle_observer.settings.hangar.i18n.pl", "Funkcja niedostępna, ponieważ zainstalowano XVM."),
    "de": ("armagomen.battle_observer.settings.hangar.i18n.de", "Funktion nicht verfügbar, da XVM installiert ist.")
}

# fallback to English
module_path, LOCKED_MESSAGE = lang_map.get(language, (
    "armagomen.battle_observer.settings.hangar.i18n.en",
    "The function is not available because XVM is installed."
))

localization = importlib.import_module(module_path).localization

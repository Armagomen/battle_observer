# coding=utf-8
import importlib

from helpers import getClientLanguage

lang_map = {
    "uk": ("armagomen.battle_observer.i18n.hangar_settings.uk", "Функція недоступна, тому що встановлено XVM."),
    "ru": ("armagomen.battle_observer.i18n.hangar_settings.ru", "Функция недоступна, потому что установлен XVM."),
    "pl": ("armagomen.battle_observer.i18n.hangar_settings.pl", "Funkcja niedostępna, ponieważ zainstalowano XVM."),
    "de": ("armagomen.battle_observer.i18n.hangar_settings.de", "Funktion nicht verfügbar, da XVM installiert ist.")
}

# fallback to English
module_path, LOCKED_MESSAGE = lang_map.get(getClientLanguage(), (
    "armagomen.battle_observer.i18n.hangar_settings.en",
    "The function is not available because XVM is installed."
))

localization = importlib.import_module(module_path).localization

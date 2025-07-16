# coding=utf-8
from helpers import getClientLanguage

LOCKED_MESSAGE = {
    "uk": "Save Shot: Постріл у {} заблоковано",
    "ru": "Save Shot: Выстрел в {} заблокирован",
    "pl": "Save Shot: Strzał w {} zablokowany",
    "de": "Save Shot: Schuss auf {} blockiert"
}.get(getClientLanguage(), "Save Shot: Shot in {} blocked")
# coding=utf-8
from helpers import getClientLanguage

TEMPLATE_BY_LANG = {
    "uk": "{0:.1f} до {1}",
    "ru": "{0:.1f} до {1}",
    "pl": "{0:.1f} do {1}",
    "de": "{0:.1f} bis {1}"
}.get(getClientLanguage(), "{0:.1f} to {1}")

# coding=utf-8
from helpers import getClientLanguage

TEMPLATE_BY_LANG = {
    "uk": "<font color='{}' size='{}'>%.1f до %s</font>",
    "ru": "<font color='{}' size='{}'>%.1f до %s</font>",
    "pl": "<font color='{}' size='{}'>%.1f do %s</font>",
    "de": "<font color='{}' size='{}'>%.1f bis %s</font>"
}.get(getClientLanguage(), "<font color='{}' size='{}'>%.1f to %s</font>")
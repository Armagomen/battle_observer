# coding=utf-8
from helpers import getClientLanguage

language = getClientLanguage()

TEXTFORMAT = "<textformat tabstops='[36, 115]'>{}</textformat>"

ONLINE = {
    "uk": "<b>{}</b>:<tab>Онлайн: <font color='#82ff29'>{}</font><tab>Усього: <font color='#ffff29'>{}</font>",
    "ru": "<b>{}</b>:<tab>Онлайн: <font color='#82ff29'>{}</font><tab>Всего: <font color='#ffff29'>{}</font>",
    "de": "<b>{}</b>:<tab>Online: <font color='#82ff29'>{}</font><tab>Gesamtzahl: <font color='#ffff29'>{}</font>",
    "pl": "<b>{}</b>:<tab>W sieci: <font color='#82ff29'>{}</font><tab>Łączna liczba: <font color='#ffff29'>{}</font>"
}.get(language, "<b>{}</b>:<tab>Online: <font color='#82ff29'>{}</font><tab>Total: <font color='#ffff29'>{}</font>")

FALLBACK = {
    "uk": "Статистика тимчасово недоступна",
    "ru": "Статистика временно недоступна",
    "pl": "Statystyki chwilowo niedostępne",
    "de": "Statistik vorübergehend nicht verfügbar"
}.get(language, "Statistics are temporarily unavailable.")

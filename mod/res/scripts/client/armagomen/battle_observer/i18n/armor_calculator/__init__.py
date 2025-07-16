# coding=utf-8
from helpers import getClientLanguage

language = getClientLanguage()

NO_DAMAGE = {
    "uk": "Крит без шкоди",
    "pl": "Bez obrażeń",
    "de": "Ohne Schaden",
    "ru": "Крит без урона",
}.get(language, "Non-damaging crit")

RICOCHET = {
    "uk": "Рикошет",
    "pl": "Rykoszet",
    "de": "Abpraller",
    "ru": "Рикошет",
}.get(language, "Ricochet")
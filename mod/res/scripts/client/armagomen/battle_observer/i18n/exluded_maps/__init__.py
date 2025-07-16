# coding=utf-8
from helpers import getClientLanguage

EXCLUDED_MAPS_BY_LANG = {
    "uk": {
        "header": "Список виключених карт",
        "message": "Ви маєте %s доступних слотів для виключення карт.\nПерейти до вибору карт для виключення?"
    },
    "pl": {
        "header": "Lista wykluczonych map",
        "message": "Masz %s dostępnych slotów na wykluczenie map.\nPrzejść do wyboru map do wykluczenia?"
    },
    "de": {
        "header": "Liste ausgeschlossener Karten",
        "message": "Du hast %s verfügbare Slots zum Ausschließen von Karten.\nZur Kartenauswahl wechseln?"
    },
    "ru": {
        "header": "Список исключённых карт",
        "message": "У вас %s доступных слотов для исключения карт.\nПерейти к выбору карт для исключения?"
    }
}.get(getClientLanguage(), {
    "header": "List of excluded maps",
    "message": "You have %s available slots for map exclusion.\nGo to map selection?"
})
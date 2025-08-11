# coding=utf-8
from helpers import getClientLanguage

CREW_DIALOG_BY_LANG = {
    "uk": {
        "enable": "Увімкнути пришвидшене навчання екіпажу?",
        "disable": "Вимкнути пришвидшене навчання екіпажу?",
        "notAvailable": "Польова модернізація недоступна для даної техніки",
        "isFullXp": "Ви набрали необхідну кількість досвіду для повної прокачки польової модернізації",
        "isFullComplete": "Ви прокачали польову модернізацію до максимально можливого рівня",
        "needTurnOff": "У вас не прокачана польова модернізація. Рекомендовано вимкнути пришвидшене навчання екіпажу."
    },
    "pl": {
        "enable": "Włączyć przyspieszone szkolenie załogi?",
        "disable": "Wyłączyć przyspieszone szkolenie załogi?",
        "notAvailable": "Modernizacja polowa jest niedostępna dla tego pojazdu",
        "isFullXp": "Zdobyto wymaganą ilość doświadczenia do pełnej modernizacji polowej",
        "isFullComplete": "Modernizacja polowa została ukończona do maksymalnego poziomu",
        "needTurnOff": "Modernizacja polowa nie została ukończona. Zaleca się wyłączenie przyspieszonego szkolenia załogi."
    },
    "de": {
        "enable": "Beschleunigtes Crew-Training aktivieren?",
        "disable": "Beschleunigtes Crew-Training deaktivieren?",
        "notAvailable": "Feldmodifikation ist für dieses Fahrzeug nicht verfügbar",
        "isFullXp": "Erforderliche Erfahrung für vollständige Feldmodifikation erreicht",
        "isFullComplete": "Feldmodifikation wurde auf das maximale Niveau verbessert",
        "needTurnOff": "Feldmodifikation ist nicht abgeschlossen. Es wird empfohlen, das beschleunigte Crew-Training zu deaktivieren."
    },
    "ru": {
        "enable": "Включить ускоренное обучение экипажа?",
        "disable": "Отключить ускоренное обучение экипажа?",
        "notAvailable": "Полевое улучшение недоступно для данной техники",
        "isFullXp": "Вы набрали необходимое количество опыта для полной прокачки полевого улучшения",
        "isFullComplete": "Вы прокачали полевое улучшение до максимального уровня",
        "needTurnOff": "Полевое улучшение не прокачано. Рекомендуется отключить ускоренное обучение экипажа."
    }
}.get(getClientLanguage(), {
    "enable": "Enable accelerated crew training?",
    "disable": "Disable accelerated crew training?",
    "notAvailable": "Field modification is not available for this vehicle",
    "isFullXp": "You have gained enough experience for full field modification",
    "isFullComplete": "You have completed field modification to the maximum level",
    "needTurnOff": "Field modification is not completed. It is recommended to disable accelerated crew training."
})
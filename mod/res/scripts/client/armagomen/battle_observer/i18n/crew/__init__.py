# coding=utf-8
from collections import namedtuple

from helpers import getClientLanguage

CREW_XP = namedtuple("CREW_XP", (
    "NAME", "NOT_AVAILABLE", "IS_FULL_COMPLETE", "NED_TURN_OFF", "NOT_ELITE", "ENABLE", "DISABLE", "THRESHOLD"))(
    "crewDialog", "notAvailable", "isFullComplete", "needTurnOff", "notElite", "enable", "disable", "threshold_to_11")

CREW_DIALOG_BY_LANG = {
    "uk": {
        CREW_XP.ENABLE: "Увімкнути пришвидшене навчання екіпажу?",
        CREW_XP.DISABLE: "Вимкнути пришвидшене навчання екіпажу?",
        CREW_XP.NOT_AVAILABLE: "Польова модернізація недоступна для даної техніки",
        CREW_XP.IS_FULL_COMPLETE: "Ви набрали необхідну кількість досвіду для повної прокачки польової модернізації або вже прокачали її "
                                  "повністю, рекомендується увімкнути пришвидшене навчання екіпажу.",
        CREW_XP.NED_TURN_OFF: "У вас не прокачана польова модернізація. Рекомендовано вимкнути пришвидшене навчання екіпажу."
                              "\n\nЗалишилось заробити ще - {}.",
        CREW_XP.NOT_ELITE: "У вас не досліджені всі модулі техніки, необхідно вимкнути прискорене навчання екіпажу.",
        CREW_XP.THRESHOLD: "Увімкнено параметр попереднього досвіду для прокачки 11 рівня. Досвід, потрібний для польової модернізації 10 "
                           "рівня, теж враховується, навіть якщо вона ще не досліджена.\n\nЗалишилось заробити ще - {}."
    },
    "pl": {
        CREW_XP.ENABLE: "Włączyć przyspieszone szkolenie załogi?",
        CREW_XP.DISABLE: "Wyłączyć przyspieszone szkolenie załogi?",
        CREW_XP.NOT_AVAILABLE: "Modernizacja polowa jest niedostępna dla tego pojazdu",
        CREW_XP.IS_FULL_COMPLETE: "Zdobyłeś wymaganą ilość doświadczenia do pełnej modernizacji polowej lub już ją ukończyłeś, zaleca się "
                                  "włączenie przyspieszonego szkolenia załogi.",
        CREW_XP.NED_TURN_OFF: "Modernizacja polowa nie została ukończona. Zaleca się wyłączenie przyspieszonego szkolenia załogi."
                              "\n\n Pozostało jeszcze {} do zarobienia.",
        CREW_XP.NOT_ELITE: "Nie zbadano wszystkich modułów pojazdu, należy wyłączyć przyspieszone szkolenie załogi.",
        CREW_XP.THRESHOLD: "Włączony parametr wstępnego doświadczenia do odblokowania poziomu 11. Doświadczenie wymagane do modernizacji "
                           "polowej na poziomie 10 jest również uwzględniane, nawet jeśli nie została jeszcze zbadana."
                           "\n\n Pozostało jeszcze {} do zarobienia."
    },
    "de": {
        CREW_XP.ENABLE: "Beschleunigtes Crew-Training aktivieren?",
        CREW_XP.DISABLE: "Beschleunigtes Crew-Training deaktivieren?",
        CREW_XP.NOT_AVAILABLE: "Feldmodifikation ist für dieses Fahrzeug nicht verfügbar",
        CREW_XP.IS_FULL_COMPLETE: "Sie haben die erforderliche Erfahrung für die vollständige Feldaufrüstung gesammelt oder diese bereits "
                                  "abgeschlossen, es wird empfohlen, das beschleunigte Besatzungstraining zu aktivieren.",
        CREW_XP.NED_TURN_OFF: "Feldmodifikation ist nicht abgeschlossen. Es wird empfohlen, das beschleunigte Crew-Training zu deaktivieren."
                              "\n\nEs gibt noch {} zu verdienen.",
        CREW_XP.NOT_ELITE: "Es sind nicht alle Fahrzeugmodule erforscht, beschleunigtes Besatzungstraining muss deaktiviert werden.",
        CREW_XP.THRESHOLD: "Voreingestellte Erfahrung für das Freischalten von Stufe 11 aktiviert. Die für die Feldmodifikation auf Stufe "
                           "10 benötigte Erfahrung wird ebenfalls berücksichtigt, auch wenn sie noch nicht erforscht ist."
                           "\n\nEs gibt noch {} zu verdienen."
    },
    "ru": {
        CREW_XP.ENABLE: "Включить ускоренное обучение экипажа?",
        CREW_XP.DISABLE: "Отключить ускоренное обучение экипажа?",
        CREW_XP.NOT_AVAILABLE: "Полевое улучшение недоступно для данной техники",
        CREW_XP.IS_FULL_COMPLETE: "Вы набрали необходимое количество опыта для полной прокачки полевой модернизации или уже прокачали её "
                                  "полностью, рекомендуется включить ускоренное обучение экипажа.",
        CREW_XP.NED_TURN_OFF: "Полевое улучшение не прокачано. Рекомендуется отключить ускоренное обучение экипажа."
                              "\n\n Осталось заработать еще - {}.",
        CREW_XP.NOT_ELITE: "У вас не исследованы все модули техники, необходимо отключить ускоренное обучение экипажа.",
        CREW_XP.THRESHOLD: "Включён параметр предварительного опыта для открытия 11 уровня. Опыт, необходимый для полевой модернизации 10 "
                           "уровня, также учитывается, даже если она ещё не исследована.\n\n Осталось заработать еще - {}."
    }
}.get(getClientLanguage(), {
    CREW_XP.ENABLE: "Enable accelerated crew training?",
    CREW_XP.DISABLE: "Disable accelerated crew training?",
    CREW_XP.NOT_AVAILABLE: "Field modification is not available for this vehicle",
    CREW_XP.IS_FULL_COMPLETE: "You have gained the required amount of experience for full field upgrade or have already completed it, "
                              "it is recommended to enable accelerated crew training.",
    CREW_XP.NED_TURN_OFF: "Field modification is not completed. It is recommended to disable accelerated crew training."
                          "\n\nThere is still {} left to earn.",
    CREW_XP.NOT_ELITE: "Not all vehicle modules have been researched, accelerated crew training must be disabled.",
    CREW_XP.THRESHOLD: "Preset experience enabled for unlocking level 11. The experience required for Field Modification at level 10 is "
                       "also counted, even if it has not been researched.\n\nThere is still {} left to earn."
})

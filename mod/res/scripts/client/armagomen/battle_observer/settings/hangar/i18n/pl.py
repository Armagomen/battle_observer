# coding=utf-8

timeFormat_tooltip = "<br>".join((
    "Format – Znaczenie",
    "%a – Skrócona nazwa dnia tygodnia",
    "%A – Pełna nazwa dnia tygodnia",
    "%b – Skrócona nazwa miesiąca",
    "%B – Pełna nazwa miesiąca",
    "%c – Data i godzina",
    "%d – Dzień miesiąca [01,31]",
    "%H – Godzina (24-godz.) [00,23]",
    "%I – Godzina (12-godz.) [01,12]",
    "%j – Dzień roku [001,366]",
    "%m – Numer miesiąca [01,12]",
    "%M – Minuty [00,59]",
    "%p – Przed/po południu (12-godz.)",
    "%S – Sekundy [00,61]",
    "%U – Numer tygodnia (niedziela jako pierwszy dzień) [00,53]",
    "%w – Numer dnia tygodnia [0(niedziela),6]",
    "%W – Numer tygodnia (poniedziałek jako pierwszy dzień) [00,53]",
    "%x – Data w formacie lokalnym systemu",
    "%X – Godzina w formacie lokalnym systemu",
    "%y – Rok bez stulecia [00,99]",
    "%Y – Rok ze stuleciem",
    "%Z – Nazwa strefy czasowej (pusta, jeśli brak)",
    "%% – Znak '%'"
))

RESTART_TOOLTIP = "Aby włączyć/wyłączyć, wymagany jest restart gry."

localization = {
    "configSelect": {
        "header": "Opcje konfiguracji",
        "selector": "Wybierz konfigurację:",
        "donate_button_ua": "MONO Bank",
        "discord_button": "Serwer Discord modyfikacji",
        "reload_config": "Przeładuj ustawienia"
    },
    "main": {
        "header": "Ustawienia ogólne",
        "DEBUG_MODE": "Tryb debugowania (nie aktywować bez potrzeby)",
        "anti_anonymous": "Oznaczaj graczy z ukrytym pseudonimem",
        "clear_cache_automatically": "Czyść cache automatycznie po wyjściu z gry",
        "clear_cache_automatically_tooltip": "Usuwa pliki tymczasowe z: AppData/Roaming/Wargaming.net/WorldOfTanks",
        "auto_crew_training": "Automatycznie przełączaj 'Przyspieszone szkolenie załogi'",
        "auto_crew_training_tooltip": "Monitoruje status modernizacji polowej i aktywuje/dezaktywuje szkolenie zależnie od dostępności.",
        "auto_return_crew": "Automatyczny powrót załogi",
        "auto_return_crew_tooltip": "Jeśli załoga pojazdu jest dostępna i nie uczestniczy w bitwie, wróci automatycznie.",
        "disable_score_sound": "Wyłącz dźwięk zniszczenia czołgu",
        "disable_stun_sound": "Wyłącz dźwięk ogłuszenia artyleryjskiego",
        "directives_only_from_storage": "Używaj dyrektyw tylko z magazynu",
        "directives_only_from_storage_tooltip": "Zapobiega zakupowi dyrektyw za obligacje/srebro, gdy ich brak w magazynie. "
                                                "Włącza 'automatyczne uzupełnianie', jeśli dyrektywy są dostępne.",
        "hide_badges": "Ukryj odznaki w bitwie",
        "hide_badges_tooltip": "Dezaktywuje odznaki w panelach graczy, widoku Tab i ekranie ładowania.",
        "hide_clan_abbrev": "Ukryj skróty klanów w bitwie",
        "hide_button_counters_on_top_panel": "Ukryj liczniki i podpowiedzi na górnym panelu garażu",
        "hide_button_counters_on_top_panel_tooltip": RESTART_TOOLTIP,
        "hide_dog_tags": "Ukryj żetony graczy w bitwie",
        "hide_field_mail": "Wyłącz pocztę polową",
        "hide_hint_panel": "Ukryj panel wskazówek w bitwie",
        "hide_main_chat_in_hangar": "Wyłącz czat ogólny w garażu",
        "hide_main_chat_in_hangar_tooltip": RESTART_TOOLTIP,
        "ignore_commanders_voice": "Ignoruj głosy dowódców",
        "ignore_commanders_voice_tooltip": "Zastępuje unikalne głosy standardowym dźwiękiem załogi lub zainstalowanym modem.",
        "premium_time": "Wyświetl zegar konta premium",
        "premium_time_tooltip": "Zmiana nie jest natychmiastowa — należy poczekać do 1 minuty lub przełączyć zakładkę garażu.",
        "show_friends": "Oznaczaj przyjaciół i członków klanu na listach drużyn",
        "useKeyPairs": "Używaj parowanych klawiszy Ctrl, Alt, Shift",
        "useKeyPairs_tooltip": "Lewy i prawy klawisz działają jako jeden — niezależnie od ustawień modułu.",
        "save_shot": "Blokuj strzał w sojuszników i wraki",
        "mute_team_base_sound": "Wyłącz syrenę przejęcia bazy",
        "hide_prestige_hangar_widget": "Ukryj widżet prestiżu w garażu",
        "hide_prestige_battle_widget": "Ukryj widżet prestiżu w bitwie",
        "hide_prestige_profile_widget": "Ukryj widżet prestiżu w profilu gracza",
        "excluded_map_slots_notification": "Powiadamiaj o dostępnych slotach do wykluczenia map",
        "auto_claim_clan_reward": "Automatycznie odbieraj nagrody klanowe",
        "hideEventBanner": "Ukryj banery wydarzeń"
    },
    "statistics": {
        "header": "Statystyki graczy i ikony pojazdów",
        "icons": "Ikony: Kolory według typów pojazdów",
        "icons_tooltip": "Funkcja zmienia kolory ikon pojazdów na ekranie ładowania, w panelach drużyn i oknie Tab. Filtr wpływa na "
                         "jasność. Zalecana wartość: -1.25.",
        "icons_blackout": "Ikony: Intensywność filtra (jasność)",
        "statistics": "Włącz statystyki graczy (WGR)",
        "statistics_vehicle_name_color": "Koloruj nazwę pojazdu według statystyki gracza",
        "statistics_tooltip": "Statystyki wyświetlane są na ekranie ładowania, w panelach drużyn i oknie Tab. Szczegóły dostępne w pliku "
                              "statistics.json. Makra: WGR, colorWGR, winRate, nickname, battles, clanTag.",
        "statistics_colors*very_bad": "Bardzo niski poziom",
        "statistics_colors*bad": "Niski poziom",
        "statistics_colors*normal": "Średni poziom",
        "statistics_colors*good": "Wysoki poziom",
        "statistics_colors*very_good": "Bardzo wysoki poziom",
        "statistics_colors*unique": "Unikalny poziom",
        "statistics_panels_full_width": "Szerokość pola nazwy gracza (szeroki panel)",
        "statistics_panels_cut_width": "Szerokość pola nazwy gracza (wąski panel)"
    },
    "dispersion_circle": {
        "header": "Celownik – ustawienia kręgu skupienia",
        "server_aim": "Włącz celownik serwerowy (dodatkowy krąg)",
        "server_aim_tooltip": "Dodaje serwerowy krąg skupienia na ekranie.",
        "replace": "Zastąp oryginalny krąg skupienia",
        "scale": "Skalowanie kręgu: 30–100% (0.3–1.0)",
        "scale_tooltip": "Wartość 0.3 oznacza minimalny rozmiar, 1.0 – domyślny. Nie zaleca się ustawień poniżej 0.6."
    },
    "dispersion_timer": {
        "header": "Timer skupienia",
        "x": "Pozycja pozioma",
        "y": "Pozycja pionowa",
        "color": "Kolor – brak skupienia",
        "done_color": "Kolor – pełne skupienie",
        "align": "Wyrównanie tekstu",
        "timer": "Wyświetl pozostały czas",
        "percent": "Wyświetl procent"
    },
    "effects": {
        "header": "Efekty wizualne",
        "noShockWave": "Wyłącz drgania kamery przy trafieniu",
        "noFlashBang": "Usuń błysk przy otrzymaniu obrażeń",
        "noBinoculars": "Usuń przyciemnienie w trybie snajperskim",
        "noSniperDynamic": "Wyłącz dynamiczną kamerę snajperską"
    },
    "debug_panel": {
        "header": "Panel FPS i PING",
        "fpsColor": "Kolor FPS",
        "pingColor": "Kolor PING",
        "style": "Styl panelu"
    },
    "battle_timer": {
        "header": "Timer bitwy",
        "timerTemplate": "Szablon formatowania",
        "timerTemplate_tooltip": "Makra:<br>%(timer)s – czas<br>%(timerColor)s – kolor czasu",
        "timerColorEndBattle": "Kolor gdy pozostało < 2 minuty",
        "timerColor": "Kolor gdy pozostało > 2 minuty"
    },
    "clock": {
        "header": "Zegar w garażu i bitwie",
        "battle*enabled": "Zegar w bitwie",
        "battle*format": "Format zegara w bitwie",
        "battle*format_tooltip": timeFormat_tooltip,
        "battle*x": "Pozycja pozioma zegara (bitwa)",
        "battle*y": "Pozycja pionowa zegara (bitwa)",
        "hangar*enabled": "Zegar w garażu",
        "hangar*format": "Format zegara w garażu",
        "hangar*format_tooltip": timeFormat_tooltip,
        "hangar*x": "Pozycja pozioma zegara (garaż)",
        "hangar*y": "Pozycja pionowa zegara (garaż)"
    },
    "hp_bars": {
        "header": "Panel wytrzymałości drużyn",
        "showAliveCount": "Wyświetl liczbę żywych",
        "style": "Styl panelu"
    },
    "armor_calculator": {
        "header": "Kalkulator efektywnego pancerza",
        "position*x": "Pozycja pozioma względem środka",
        "position*y": "Pozycja pionowa względem środka",
        "display_on_allies": "Wyświetl także na sojusznikach",
        "show_piercing_power": "Wyświetl siłę penetracji",
        "show_counted_armor": "Wyświetl wartość pancerza",
        "show_piercing_reserve": "Wyświetl zapas penetracji",
        "show_caliber": "Wyświetl kaliber"
    },
    "wg_logs": {
        "header": "Ustawienia logu wydarzeń WG",
        "wg_log_hide_assist": "Ukryj obrażenia ze wsparcia",
        "wg_log_hide_assist_tooltip": "Ukrywa obrażenia z zwiadu w szczegółowym logu",
        "wg_log_hide_block": "Ukryj zablokowane obrażenia",
        "wg_log_hide_block_tooltip": "Ukrywa zablokowane obrażenia w szczegółowym logu",
        "wg_log_hide_critics": "Ukryj trafienia krytyczne bez obrażeń",
        "wg_log_hide_critics_tooltip": "Ukrywa trafienia krytyczne w szczegółowym logu",
        "wg_log_pos_fix": "Popraw pozycję logu (jak w starszych modach)",
        "wg_log_pos_fix_tooltip": "Zamienia miejsca logów obrażeń zadanych i otrzymanych"
    },
    "log_total": {
        "header": "Ustawienia logu ogólnej efektywności gracza",
        "settings*inCenter": "Wyświetl log na środku ekranu",
        "settings*x": "Pozycja pozioma logu",
        "settings*y": "Pozycja pionowa logu",
        "settings*align": "Wyrównanie tekstu:",
        "settings*align_tooltip": "left – lewo<br>center – środek<br>right – prawo",
        "mainLogScale": "Skalowanie logu"
    },
    "log_extended": {
        "header": "Szczegółowy log obrażeń",
        "logsAltMode_hotkey": "Klawisz przełączania trybu logu",
        "settings*x": "Pozycja pozioma",
        "settings*x_tooltip": "Względem pozycji logu WG",
        "settings*y": "Pozycja pionowa",
        "settings*y_tooltip": "Względem pozycji logu WG",
        "settings*align": "Wyrównanie tekstu:",
        "settings*align_tooltip": "left – lewo<br>center – środek<br>right – prawo",
        "reverse": "Dodawaj nowe wpisy na górze",
        "reverse_tooltip": "Nowe wpisy pojawiają się na początku logu",
        "shellColor*gold": "Kolor pocisków premium",
        "shellColor*normal": "Kolor zwykłych pocisków",
        "top_enabled": "Log obrażeń zadanych",
        "bottom_enabled": "Log obrażeń otrzymanych"
    },
    "main_gun": {
        "header": "Medal 'Główne kaliber' – ustawienia",
        "x": "Pozycja pozioma (od środka ekranu)",
        "y": "Pozycja pionowa (od górnej krawędzi)",
        "progress_bar": "Pasek postępu"
    },
    "team_bases_panel": {
        "header": "Panel przejęcia bazy",
        "y": "Pozycja pionowa paska przejęcia",
        "width": "Szerokość paska w pikselach"
    },
    "vehicle_types_colors": {
        "header": "Kolory typów pojazdów",
        "AT-SPG": "Niszczyciel czołgów (TD)",
        "SPG": "Artyleria (SPG)",
        "heavyTank": "Czołg ciężki",
        "lightTank": "Czołg lekki",
        "mediumTank": "Czołg średni",
        "unknown": "Nieznany (mapa globalna)"
    },
    "players_panels": {
        "header": "Panel listy graczy – ustawienia",
        "players_damages_enabled": "Wyświetl obrażenia zadane przez graczy",
        "players_damages_hotkey": "Klawisz wyświetlania obrażeń",
        "players_damages_settings*x": "Pozycja pozioma tekstu",
        "players_damages_settings*y": "Pozycja pionowa tekstu",
        "players_bars_enabled": "Wyświetl pasek wytrzymałości pojazdów",
        "players_bars_hotkey": "Klawisz wyświetlania wytrzymałości",
        "players_bars_classColor": "Koloruj paski według klasy pojazdu",
        "players_bars_on_key_pressed": "Wyświetl paski tylko po naciśnięciu klawisza",
        "panels_spotted_fix": "Popraw rozmiar i pozycję ikon wykrycia"
    },
    "zoom": {
        "header": "Tryb snajperski – ustawienia",
        "disable_cam_after_shot": "Wyłącz kamerę po strzale",
        "disable_cam_after_shot_tooltip": "Automatycznie przełącza na kamerę arcade po strzale, jeśli kaliber działa przekracza 60 mm.",
        "disable_cam_after_shot_latency": "Opóźnienie wyłączenia trybu snajperskiego",
        "disable_cam_after_shot_skip_clip": "Nie wychodź z trybu przy magazynowym systemie ładowania",
        "dynamic_zoom": "Automatyczny wybór powiększenia",
        "dynamic_zoom_tooltip": "Funkcja ignoruje ustawienie stałe. Powiększenie zależy od odległości do celu podzielonej przez czułość.",
        "steps_enabled": "Zastąp poziomy zoomu",
        "steps_range": "Poziomy zoomu",
        "steps_range_tooltip": "Podaj wartości oddzielone przecinkiem lub przecinkiem i spacją. Dowolna liczba kroków."
    },
    "arcade_camera": {
        "header": "Kamera dowódcy – ustawienia",
        "max": "Maksymalna odległość (domyślnie: 25)",
        "min": "Minimalna odległość (domyślnie: 2)",
        "startDeadDist": "Odległość przy rozpoczęciu/śmierci (domyślnie: 15)",
        "scrollSensitivity": "Czułość scrolla (domyślnie: 4)"
    },
    "strategic_camera": {
        "header": "Kamera artyleryjska – ustawienia",
        "max": "Maksymalna odległość (domyślnie: 100)",
        "min": "Minimalna odległość (domyślnie: 40)",
        "scrollSensitivity": "Czułość scrolla (domyślnie: 10)"
    },
    "flight_time": {
        "header": "Czas lotu pocisku i odległość – ustawienia",
        "x": "Pozycja pozioma tekstu",
        "x_tooltip": "Odległość względem środka ekranu (pozioma)",
        "y": "Pozycja pionowa tekstu",
        "y_tooltip": "Odległość względem środka ekranu (pionowa)",
        "spgOnly": "Wyświetlaj tylko dla artylerii",
        "align": "Wyrównanie tekstu",
        "time": "Wyświetl czas",
        "distance": "Wyświetl odległość",
        "color": "Kolor tekstu"
    },
    "minimap": {
        "header": "Minimapa – ustawienia",
        "zoom": "Włącz powiększenie na środek",
        "permanentMinimapDeath": "Pokazuj zniszczone pojazdy na mapie",
        "showDeathNames": "Pokazuj nazwy zniszczonych pojazdów",
        "real_view_radius": "Zezwól na zasięg widzenia powyżej 445 m",
        "yaw_limits": "Pokazuj kąty celowania dla wszystkich pojazdów",
        "zoom_hotkey": "Klawisz powiększenia mapy"
    },
    "colors": {
        "header": "Kolory globalne – ustawienia",
        "armor_calculator*green": "Pancerz: 100% szansy na penetrację",
        "armor_calculator*orange": "Pancerz: 50% szansy",
        "armor_calculator*red": "Pancerz: 0% szansy",
        "armor_calculator*yellow": "Pancerz: 50% (tryb daltonizmu)",
        "armor_calculator*purple": "Pancerz: 0% (tryb daltonizmu)",
        "armor_calculator*normal": "Rykoszet lub trafienie bez obrażeń",
        "global*ally": "Kolor globalny: sojusznik",
        "global*bgColor": "Kolor tła paneli",
        "global*enemyColorBlind": "Kolor globalny: wróg (daltonizm)",
        "global*enemy": "Kolor globalny: wróg",
        "vehicle_types_colors*AT-SPG": "Niszczyciel czołgów",
        "vehicle_types_colors*SPG": "Artyleria",
        "vehicle_types_colors*heavyTank": "Czołg ciężki",
        "vehicle_types_colors*lightTank": "Czołg lekki",
        "vehicle_types_colors*mediumTank": "Czołg średni",
        "vehicle_types_colors*unknown": "Nieznany (mapa globalna)"
    },
    "service_channel_filter": {
        "header": "Filtr wiadomości kanału systemowego",
        "sys_keys*CustomizationForCredits": "Personalizacja za kredyty",
        "sys_keys*CustomizationForGold": "Personalizacja za złoto",
        "sys_keys*DismantlingForCredits": "Demontaż za kredyty",
        "sys_keys*DismantlingForCrystal": "Demontaż za obligacje",
        "sys_keys*DismantlingForGold": "Demontaż za złoto",
        "sys_keys*GameGreeting": "Powitanie gry",
        "sys_keys*Information": "Informacje systemowe",
        "sys_keys*MultipleSelling": "Sprzedaż wielu przedmiotów",
        "sys_keys*PowerLevel": "Badania modułów i pojazdów",
        "sys_keys*PurchaseForCredits": "Zakup za kredyty",
        "sys_keys*PurchaseForCrystal": "Zakup za obligacje",
        "sys_keys*PurchaseForGold": "Zakup za złoto",
        "sys_keys*Remove": "Usunięcie przedmiotu",
        "sys_keys*Repair": "Naprawa",
        "sys_keys*Restore": "Przywrócenie",
        "sys_keys*Selling": "Sprzedaż pojedynczego przedmiotu",
        "sys_keys*autoMaintenance": "Automatyczna obsługa pojazdu",
        "sys_keys*customizationChanged": "Zmiana personalizacji"
    },
    "service": {
        "name": "Battle Observer – v{0}",
        "description": "Otwórz ustawienia Battle Observer",
        "windowTitle": "Battle Observer – v{0} – ustawienia",
        "buttonOK": "OK",
        "buttonCancel": "Anuluj",
        "buttonApply": "Zastosuj",
        "enableButtonTooltip": "{HEADER}WŁ./WYŁ.{/HEADER}{BODY}Włącz/wyłącz moduł{/BODY}"
    },
    "sixth_sense": {
        "header": "Szósty zmysł – ustawienia",
        "default_icon": "Użyj wbudowanej ikony",
        "default_icon_name": "Wybierz wbudowaną ikonę",
        "default_icon_tooltip": "Zostanie użyty domyślny obraz z modów zamiast ikony użytkownika",
        "lampShowTime": "Czas wyświetlania (sekundy)",
        "lampShowTime_tooltip": "<b>Jak długo cel pozostaje widoczny?</b><br>Po wykryciu pojazdu przeciwnika przez promień widoczności, "
                                "pozostaje on widoczny nawet po zaniku interakcji. Standardowo: 10 sekund, zależnie od załogi, "
                                "wyposażenia – od 8 do 16–18 sekund.",
        "playTickSound": "Odtwórz dźwięk timera",
        "show_timer": "Włącz timer",
        "show_timer_graphics": "Włącz graficzny timer",
        "show_timer_graphics_color": "Kolor grafiki",
        "show_timer_graphics_radius": "Promień graficznego kręgu",
        "icon_size": "Rozmiar ikony (px), max 180"
    },
    "distance_to_enemy": {
        "header": "Ustawienia odległości do najbliższego wykrytego przeciwnika",
        "x": "Pozycja pozioma tekstu",
        "x_tooltip": "Pozycja względem środka ekranu (pozioma)",
        "y": "Pozycja pionowa tekstu",
        "y_tooltip": "Pozycja względem środka ekranu (pionowa)",
        "template": "Szablon tekstu. Makra: %(distance)s, %(name)s",
        "align": "Wyrównanie tekstu"
    },
    "own_health": {
        "header": "Ustawienia wyświetlania wytrzymałości własnego pojazdu",
        "x": "Pozycja pozioma tekstu",
        "x_tooltip": "Pozycja względem środka ekranu (pozioma)",
        "y": "Pozycja pionowa tekstu",
        "y_tooltip": "Pozycja względem środka ekranu (pionowa)"
    },
    "crewDialog": {
        "enable": "<br>Włączyć przyspieszone szkolenie załogi?",
        "disable": "<br>Wyłączyć przyspieszone szkolenie załogi?",
        "notAvailable": "Modernizacja polowa niedostępna dla tego pojazdu",
        "isFullXp": "Zebrano pełne doświadczenie do modernizacji",
        "isFullComplete": "Modernizacja ukończona w pełni",
        "needTurnOff": "Brak modernizacji polowej – zaleca się wyłączyć szkolenie załogi"
    },
    "excludedMaps": {
        "header": "Lista wykluczonych map",
        "message": "Masz %s wolnych slotów do wykluczenia map.\nPrzejść do wyboru map?"
    },
    "avg_efficiency_in_hangar": {
        "header": "Ustawienia widżetu statystyk pojazdu w garażu",
        "avg_damage": "Wyświetl średnie zadane uszkodzenia",
        "avg_assist": "Wyświetl średnie uszkodzenia z pomocą",
        "avg_blocked": "Wyświetl średnie uszkodzenia zablokowane przez pancerz",
        "avg_stun": "Wyświetl średnie ogłuszenie celu (artyleria)",
        "gun_marks": "Wyświetl procent postępu oznaczenia działa",
        "win_rate": "Wyświetl współczynnik zwycięstw",
        "battles": "Wyświetl liczbę rozegranych bitew"
    }
}
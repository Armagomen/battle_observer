# coding=utf-8
from armagomen.battle_observer import __version__

timeFormat_tooltip = ("Directive Meaning\n"
                      "%a  Locale’s abbreviated weekday name.\n"
                      "%A  Locale’s full weekday name.\n"
                      "%b  Locale’s abbreviated month name.\n"
                      "%B  Locale’s full month name.\n"
                      "%c  Locale’s appropriate date and time representation.\n"
                      "%d  Day of the month as a decimal number [01,31].\n"
                      "%H  Hour (24-hour clock) as a decimal number [00,23].\n"
                      "%I  Hour (12-hour clock) as a decimal number [01,12].\n"
                      "%j  Day of the year as a decimal number [001,366].\n"
                      "%m  Month as a decimal number [01,12].\n"
                      "%M  Minute as a decimal number [00,59].\n"
                      "%p  Locale’s equivalent of either AM or PM.\n"
                      "%S  Second as a decimal number [00,61].\n"
                      "%U  Week number of the year (Sunday as the first day of the week) as a decimal number [00,53].\n"
                      "%w  Weekday as a decimal number [0(Sunday),6].\n"
                      "%W  Week number of the year (Monday as the first day of the week) as a decimal number [00,53].\n"
                      "%x  Locale’s appropriate date representation.\n"
                      "%X  Locale’s appropriate time representation.\n"
                      "%y  Year without century as a decimal number [00,99].\n"
                      "%Y  Year with century as a decimal number.\n"
                      "%Z  Time zone name (no characters if no time zone exists).\n"
                      "%%  A literal '%' character.")
translate = {
    "configSelect": {
        "header": "Wähle Konfiguration (Verzeichnis: mods/configs/mod_battle_observer)",
        "selector": "Config",
        "donate_button_ua": "DONATE UA - Гривна",
        "donate_button_eu": "DONATE EUR|USD|RUB",
        "donate_button_patreon": "Subscribe on Patreon",
        "discord_button": "Discord support & chat"
    },
    "main": {
        "header": "Allgemeine Einstellungen",
        "DEBUG_MODE": "DEBUG_MODE",
        "showFriendsAndClanInEars": "Markiere Clanfreunde und dich in den Teamlisten.",
        "autoClearCache": "Löschen Sie den Spiel-Cache beim Beenden.",
        "autoClearCache_tooltip": "Bereinigen der temporären Dateien des Spiels im Ordner "
                                  "AppData/Roaming/Wargaming.net/WorldOfTanks."
                                  "<br> Dort geänderte Ordner sind nicht betroffen.",
        "removeShadowInPrebattle": "Entferne den Blackout-Timer zu Beginn des Kampfes",
        "smallDoubleCarousel": "Verwenden Sie kleine Symbole im Karussell.",
        "carouselRows": "Reihenanzahl des mehrreihigen Panzerkarussells.",
        "hideBadges": "Deaktivieren Sie Chevrons/Ribbons im Spielerpanel",
        "fps_enableFPSLimiter": "FPS-Limiter aktivieren",
        "enableFPSLimiter_tooltip": "Achtung, um das Spiel vollständig zu deaktivieren oder zu aktivieren,"
                                    " müssen Sie das Spiel neu starten.",
        "fps_maxFrameRate": "Maximum Frame Rate",
        "hideClanAbbrev": "Deaktiviere Clan-Anzeige im Playerspanel, Tab Screen, Ladebildschirm.",
        "hideChatInRandom": "Chat in Zufallsgefechten deaktivieren",
        "hideChatInRandom_tooltip": "Chat in Zufsallsgefechten komplett deaktivieren."
                                    "<br> incl. Chat-Formular und alles, was damit verbunden ist",
        "anonymousEnableShow": "Show Anonymous.",
        "anonymousEnableShow_tooltip": "Nur wenn die Spielerstatistik deaktiviert ist, wird der Parameter"
                                       " bei aktivierter Statistik nicht berücksichtigt.",
        "useKeyPairs": "Use key pairs Alt, Ctrl, Shift",
        "anonymousNameChange": "Change Anonymous Name",
        "hide_dog_tags": "Deaktivieren Sie die Anzeige von Token.",
        "ignore_commanders_voice": "Ignore commander voiceover.",
        "ignore_commanders_voice_tooltip": "Once enabled, the standard crew voiceover will be forcibly used. "
                                           "The parameter will replace all voiceovers of bloggers, "
                                           "Chuck Norris and so on with the standard / from the voiceover mod. ",
        "disable_score_sound": "Deaktivieren Sie den Sound zur Änderung der Partitur",
        "premium_time": "Display exact premium time.",
        "auto_crew_training": "Deaktivieren / aktivieren Sie Beschleunigtes Besatzungstraining Automatisch.",
        "auto_crew_training_tooltip": "Wenn das 'Feld-Upgrade' für den Panzer verfügbar ist und nicht gepumpt "
                                      "wird, wird das Kontrollkästchen für die Besatzung automatisch deaktiviert, "
                                      "sobald die Fortschrittsstufe maximal ist, werden Sie aufgefordert, sie "
                                      "wieder einzuschalten.",
        "do_not_buy_directives_for_currency_automatically": "Do not replenish directives for currency (automatically)",
        "do_not_buy_directives_for_currency_automatically_tooltip":
            "Prevent automatic replenishment of instructions for game currency if they are not in stock. "
            "It will also turn on automatic replenishment from the warehouse if they are there and you forgot to "
            "tick the box.",
        "hide_hint_panel": "Hinweise im Kampf deaktivieren",
        "hide_field_mail": "Feldmail deaktivieren",
        "auto_return_crew": "Automatische Crew-Rückkehr",
    },
    "statistics": {
        "header": "WTR (WGR) Player Statistics | Tank icons",
        "statistics_enabled": "Enable player statistics",
        "statistics_change_vehicle_name_color": "Change the color of the tank name in the ears to the color "
                                                "of the statistics",
        "statistics_enabled_tooltip": "Statistics will be displayed on: loading screen, in ears, taboo window. "
                                      "For more fine-tuning see the statistics.json file."
                                      "Available macro names: WTR, colorWTR, winRate, nickname, battles, clanTag",
        "icon_enabled": "Repaint tank icons in the colors of vehicle classes",
        "icon_enabled_tooltip": "This function repaints any vehicle icons in the ears, taboo window, on the loading "
                                "screen in the color of vehicle classes.<br>"
                                "Filter strength affects brightness.<br>Recommended filter strength -1.25",
        "icon_blackout": "Filter strength (brightness)",

        "panels_full_width": "Player Name Field Width - Big Ears",
        "panels_cut_width": "Player Name Field Width - Small Ears"
    },
    "dispersion_circle": {
        "header": "Kreis für Streuung der Kanone. (Mischen)",
        "circle_enabled": "Verbessertes Mischen.",
        "circle_use_lock_prediction": "Das Fadenkreuz des Servers bleibt bei der Zielerfassung hängen.",
        "circle_extraServerLap": "Anzeige des Kreises für die Streuung der Kanone.",
        "circle_extraServerLap_tooltip": "Fügt einen zweiten Kreis der Server-Sichtung hinzu.",
        "circle_replaceOriginalCircle": "Ersetzen des originalen Kreises.",
        "circle_scale": "Kreisgrößenmultiplikator 1 - 100 %",
        "circle_scale_tooltip": "Es wird nicht empfohlen, den Wert unter 65 einzustellen.",
        "timer_enabled": "Schalten Sie den Reduktions-Timer ein.",
        "timer_position_x": "Timer Position X",
        "timer_position_y": "Timer Position Y",
        "timer_color": "Timerfarbe, noch nicht konvergiert.",
        "timer_done_color": "Timer / Nachrichtenfarbe (volle Reduzierung).",
        "timer_align": "Text align."
    },
    "tank_carousel": {
        "header": "TANK CAROUSEL SETUP",
        "carouselRows": "Anzahl der Reihen eines mehrreihigen Tankkarussells.",
        "carouselRows_toltip": "Funktioniert nur, wenn das mehrzeilige Karussell im Client aktiviert ist.",
        "smallDoubleCarousel": "Erzwingen Sie die Verwendung kleiner Symbole im Tankkarussell."
    },
    "effects": {
        "header": "Visuelle Kameraeffekte anpassen",
        "noShockWave": "Keine Kameraerschütterung, wenn Panzer getroffen wurde",
        "noFlashBang": "Roten Blitz ausschalten, wenn eigener Panzer getroffen wurde",
        "noLightEffect": "Blitz und Flamme nach dem Brennen entfernen.",
        "noBinoculars": "Schwarzen Schatten im Zielfernrohr entfernen",
        "noSniperDynamic": "Deaktivieren Sie die dynamische Kamera im Scharfschützenmodus."
    },
    "debug_panel": {
        "header": "Panel für PING/FPS",
        "debugText*text": "Format vom Panel: PING/FPS",
        "debugText*text_tooltip": "HTML Formatierung möglich<br>verfügbare Makros:<br>%(PING)s<tab>- aktueller Ping"
                                  "<br>%(FPS)s<tab>- aktuelle FPS<br>%(PingLagColor)s<tab>- Farbe für PING/LAG",
        "debugText*x": "Position waagerecht (X-Achse)",
        "debugText*y": "Position senkrecht (Y-Achse)",
        "debugText*scale": "Skalierung des 'Debug' Panels",
        "debugGraphics*enabled": "Zeige ping / fps-Bänder",
        "colors*fpsColor": "Farbe Makro %(fpsColor)s - FPS",
        "colors*pingColor": "Farbe Makro %(pingLagColor)s - Keine LAG",
        "colors*pingLagColor": "Farbe Makro %(pingLagColor)s - LAG"
    },
    "battle_timer": {
        "header": "Gefechtstimer",
        "timerTemplate": "Formatierung des Textfeldes für den Gefechtstimer",
        "timerTemplate_tooltip": "Verfügbare Makros:<br> %(timer)s<br> %(timerColor)s<br>HTML Formatierung möglich",
        "timerColorEndBattle": "Farbe Makro %(timerColor)s wenn weniger als 2:00 Min.",
        "timerColor": "Farbe Makro %(timerColor)s"
    },
    "clock": {
        "header": "CLOCK",
        "battle*enabled": "Display in battle.",
        "hangar*enabled": "Display in hangar.",
        "battle*format": "format.",
        "battle*format_tooltip": timeFormat_tooltip,
        "hangar*format": "format.",
        "hangar*format_tooltip": timeFormat_tooltip,
        "battle*x": "X.",
        "battle*y": "Y.",
        "hangar*x": "X.",
        "hangar*y": "Y."
    },
    "hp_bars": {
        "header": "TOTAL HP PANEL (HP Pool Bar)",
        "barsWidth": "Breite des Panels",
        "differenceHP": "Anzeige der Differenz zwischen den Teams",
        "showAliveCount": "Zeige die Anzahl lebendigen Panzer im Panel, statt der zerstörten",
        "style": "Stil des HP Panels",
        "outline*enabled": "Kantenbänder im Stil normal",
        "outline*color": "Benutzerdefinierte Farbe.",
        "markers*enabled": "Panzerklassen Panel (unter HP Panel)",
        "markers*markersClassColor": "Fahrzeugklassen farbig anzeigen (siehe ' FARBEINSTELLUNGEN')",
        "markers*x": "Позиция по Горизонтали от центра.",
        "markers*x_tooltip": "Позиция маркеров по Горизонтали от центра экрана.",
        "markers*y": "Позиция по Вертикали от верха.",
        "markers*y_tooltip": "Позиция маркеров по Вертикали от верха экрана.",
        "markers*showMarkers_hotkey": "Taste zum Einschalten/Ausschalten des Panels:"
    },
    "armor_calculator": {
        "header": "Durchschlagsanzeiger (Berechnung der Panzerung)",
        "position*x": "Position des Haupt Textfeldes waagerecht",
        "position*y": "Position des Haupt Textfeldes senkrecht",
        "template": "Formatierung des Haupt-Textfeldes",
        "display_on_allies": "Bei Verbündeten anzeigen",
        "template_tooltip": "Makroformat:% (Name) Datentyp s:d:f.<br>"
                            "s-string, d-dezimal, f-gleitkomma <br><br>"
                            "Liste der verfügbaren Makros:<br>"
                            "<li>%(countedArmor)d - Gezählte Rüstung.</li>"
                            "<li>%(piercingPower)d - Entfernungsbasierte Projektildurchdringung.</li>"
                            "<li>%(piercingReserve)d - Penetrationsreserve nach dem Durchbohren der Rüstung.</li>"
                            "<li>%(caliber)d - Geschosskaliber.</li>"
                            "<li>%(message)s - Nachricht aus dem Nachrichtenabschnitt in der Konfigurationsdatei.</li>"
                            "<li>%(ricochet)s - Potenzielle Abprallerwarnung.</li>"
                            "<li>%(noDamage)s - Benachrichtigung, dass kein Schaden entsteht. Das Projektil trifft "
                            "das Modul unter Umgehung Hauptpanzerung. Raupe ohne Schaden, Rad ohne Schaden usw.</li>"
                            "<li>%(color)s - Farbe (siehe Farbeinstellung).</li>"
    },
    "log_global": {
        "header": "Allgemeine Einstellungen für Schadensprotokoll",
        "logsAltmode_hotkey": "Taste zum Umschalten auf Alternativen Modus",
        "wg_log_hide_assist": "Verstecke 'Unterstützungs Schaden'",
        "wg_log_hide_assist_tooltip": "Entfernte 'Unterstützungs Schaden' aus dem detaillierten WG Protokoll",
        "wg_log_hide_block": "Verstecke 'geblockten Schaden'",
        "wg_log_hide_block_tooltip": "Entfernte 'blockierten Schaden' aus dem detaillierten WG Protokoll",
        "wg_log_hide_crits": "Verstecke 'kritische Treffer'",
        "wg_log_hide_crits_tooltip": "Entfernte 'kritische Treffer' aus dem detaillierten WG Protokoll",
        "wg_log_pos_fix": "Verschiebe Protokolle an die richtigen Positionen",
        "wg_log_pos_fix_tooltip": "Tauscht die Protokolle für verursachten und erhaltenen Schadens aus,"
                                  "<br>Erhaltenen Schaden nach unten, Verursachten Schaden nach oben."
                                  "<br>Ansonsten umgekehrt."
    },
    "log_total": {
        "header": "Gesamtprotokoll der Effizienz des Spielers",
        "settings*inCenter": "Zeigen Sie das Protokoll in der Mitte des Bildschirms an",
        "settings*x": "Position waagerecht:",
        "settings*y": "Position senkrecht:",
        "settings*align": "Ausrichtung text:",
        "mainLogScale": "Skalierung:"
    },
    "log_damage_extended": {
        "header": "Erweitertes Protokoll für verursachten Schaden",
        "settings*x": "Position detailliertes Protokoll waagerecht",
        "settings*x_tooltip": "Bezogen auf die Liste Spieler.",
        "settings*y": "Position detailliertes Protokoll senkrecht",
        "settings*y_tooltip": "Bezogen auf die Liste Spieler.",
        "settings*align": "Ausrichtung text:",
        "reverse": "zeige detailiertes Protokoll für einzelne Treffer"
    },
    "log_input_extended": {
        "header": "Erweitertes Protokoll für erhaltenen Schaden",
        "settings*x": "Position des detailierten Protokolls waagerecht",
        "settings*x_tooltip": "In Bezug auf die Schadensanzeige.",
        "settings*y": "Position des detailierten Protokolls senkrecht",
        "settings*align": "Ausrichtung text:",
        "settings*align_tooltip": "Ausrichtung:<br>left - Linksbündig<br>center - Zentriert ausgerichtet"
                                  "<br>right - Rechtsbündig",
        "settings*y_tooltip": "In Bezug auf die Schadensanzeige.",
        "reverse": "zeige detailiertes Protokoll für einzelne Treffer",
        "shellColor*gold": "Einstellung für Makro: %(shellColor)s - Premium Munition",
        "shellColor*normal": "Einstellung für Makro: %(shellColor)s - Standard Munition"
    },
    "main_gun": {
        "header": "Grosskaliber",
        "settings*x": "Position waagerecht von der Mitte gemessen",
        "settings*y": "Position senkrecht vom oberen Rand gemessen",
        "settings*align": "Ausrichtung des Textes:",
        "settings*align_tooltip": "Ausrichtung:<br>left - Linksbündig<br>center - Zentriert ausgerichtet"
                                  "<br>right - Rechtsbündig"
    },
    "team_bases_panel": {
        "header": "TEAM BASES PANEL (Leiste zur Anzeige der Basiseroberung)",
        "y": "Position der Eroberungsleiste senkrecht",
        "scale": "Skalierung Eroberungsleiste",
        "boBases": "Panel für Basiseroberung vom Mod einschalten.",
        "outline*enabled": "Rahmen aktivieren.",
        "outline*color": "Benutzerdefinierte Farbe."
    },
    "vehicle_types": {
        "header": "Farben für die Panzerklassen",
        "vehicleClassColors*AT-SPG": "Jagdpanzer",
        "vehicleClassColors*SPG": "Artillerie",
        "vehicleClassColors*heavyTank": "Schwere Panzer",
        "vehicleClassColors*lightTank": "Leichte Panzer",
        "vehicleClassColors*mediumTank": "Mittlere Panzer",
        "vehicleClassColors*unknown": "Unbekannt (CC)"
    },
    "players_panels": {
        "header": "Panels mit einer Liste von Spielern (Ohren).",
        "players_damages_enabled": "Schaden für Spieler auf Mannschaftslisten.",
        "players_damages_hotkey": "Schlüssel zum Anzeigen von Schäden.",
        "players_damages_settings*x": "Horizontale Textposition",
        "players_damages_settings*y": "Vertikale Textposition",
        "players_bars_enabled": "HP Spieler in den Ohren.",
        "players_bars_settings*players_bars_bar*outline*enabled": "Gliederung einschließen.",
        "players_bars_settings*players_bars_bar*outline*customColor": "Benutzerdefinierte Umrissfarbe.",
        "players_bars_settings*players_bars_bar*outline*color": "Benutzerdefinierte Umrissfarbe.",
        "players_bars_settings*players_bars_bar*outline*alpha": "Gliederungstransparenz.",
        "players_bars_hotkey": "HP Display-Taste",
        "players_bars_classColor": "Färben Sie die HP-Streifen in den Ohren entsprechend der Farbe des Techniktyps.",
        "players_bars_on_key_pressed": "Streifen nur beim Tastendruck anzeigen.",
        "panels_spotted_fix": "Richtige Größe und Position des Erkennungsstatus."
    },
    "zoom": {
        "header": "Zoom für Richtschützenansicht (Sniper Zoom IN)",
        "disable_cam_after_shot": "Disable sniper mode after the shot.",
        "disable_cam_after_shot_tooltip": "Automatically switches the camera to arcade mode after "
                                          "a shot if the caliber of the gun is more than 60mm.",
        "disable_cam_after_shot_latency": "Delay automatic shutdown of the camera.",
        "disable_cam_after_shot_skip_clip": "Не выходить если магазинная система заряжания",
        "dynamic_zoom*enabled": "Automatische Auswahl der Zoomstufen beim wechsel in den Richtschützenmodus",
        "dynamic_zoom*steps_only": "Bewegen Sie sich nur in festen Schritten.",
        "dynamic_zoom*enabled_tooltip": "Wenn diese Option aktiviert ist, wird der <b>Fester Zoom</b> deaktiviert.",
        "zoomToGunMarker": "Aktivieren der Annäherung der Kamera an die Zentralmarkierung",
        "dynamic_zoom*zoomXMeters": "Empfindlichkeit bei Annäherung: in Metern",
        "dynamic_zoom*zoomXMeters_tooltip": "(Dynamischer Zoom = Enfernung / Empfindlichkeit bei Annäherung)"
                                            "<br>Standard: alle 17 Meter + 1 (je kleiner die Zahl, desto mehr Zoom",
        "zoomSteps*enabled": "Zoom Stufen.",
        "zoomSteps*steps": "Zooms Stufen. (Trennung durch Komma)",
        "zoomSteps*steps_tooltip": "Sie können beliebig viele Werte (getrennt durch Komma und Leerzeichren)"
                                   " schreiben."
    },
    "arcade_camera": {
        "header": "Zoom für Arcade Ansicht (Arcade Zoom Out)",
        "max": "Maximale Entfernung vom Panzer. Standard: 25.0",
        "min": "Minimaler Abstand vom Panzer. Standard: 2.0",
        "startDeadDist": "Abstand bei Start / bei zerstört",
        "startDeadDist_tooltip": "Der Abstand vom Panzer beim Start des Gefechtes / "
                                 "b.z.w. der Abstand wenn der Panzer zerstört wurde. Standard ist: 15",
        "scrollSensitivity": "Scroll-Empfindlichkeit, Standard 4"
    },
    "strategic_camera": {
        "header": "Zoom für Artillerieansicht (Strategic Zoom Out)",
        "max": "Maximale Enfernung der Kamera vom Panzer. Standard: 100.0",
        "min": "Minimaler Abstand der Kamera vom Panzer. Standard: 40.0",
        "scrollSensitivity": "Scroll-Empfindlichkeit, Standard 10"
    },
    "flight_time": {
        "header": "Granaten Flugzeit Anzeige",
        "x": "Position des Textes waagerecht",
        "x_tooltip": "Position von der Mitte des Bildschirmes gemessen. Textausrichtung ---|Zentriert|---",
        "y": "Position des Textes senkrechtrecht",
        "y_tooltip": "Position von der Mitte des Bildschirmes gemessen.",
        "spgOnly": "zeige Text ausschliesslich für Artillerie",
        "template": "Text: verfügbare Makro(s):%(flightTime).1f , %(distance).1f",
        "wgDistDisable": "Basisentfernung in Sichtweite ausblenden.",
        "align": "Text align."
    },
    "save_shoot": {
        "header": "Blockiere Teambeschuss (SAVE SHOOT LITE)",
        "block_on_destroyed": "Blockiere den Schuss auf den Zerstörten.",
        "msg": "Eine Nachricht über eine erfolgreiche Sperre ist nur für Sie sichtbar.",
        "msg_tooltip": "Diese Nachricht wird nur angezeigt, wenn der Schuss von einem Verbündeten geblockt wird."
    },
    "minimap": {
        "header": "MINI-KARTE",
        "zoom*enabled": "Zentrierung der Minikarte aktivieren.",
        "zoom*zoom_hotkey": "Minikarte zentrieren auf",
        "zoom*indent": "Einrücken von den Rändern des Bildschirms",
        "zoom*indent_tooltip": "Es ist notwendig, einen Einzug nur von der oberen Kante aus zu spezifizieren, "
                               "darunter wird es gleich sein.",
        "permanentMinimapDeath": "Zeige immer die zerstörten Panzer auf der Karte",
        "showDeathNames": "Zeige die Namen der zerstörten Panzer an."
    },
    "shadow_settings": {
        "header": "SETTING SHADOWS TEXT (Glow)",
        "inner": "Determines whether the glow is an internal glow.",
        "knockout": "Determines whether a knockout effect is applied to an object.",
        "blurX": "The degree of blurring horizontally.",
        "blurY": "The amount of vertical blur.",
        "alpha": "The alpha transparency value of the color.",
        "color": "Glow color.",
        "strength": "The degree of indentation or application.",
        "blurY_tooltip": "Values that are powers of 2 (i.e. 2, 4, 8, 16, and 32) are optimized and "
                         "run faster than others.",
        "blurX_tooltip": "Values that are powers of 2 (i.e. 2, 4, 8, 16, and 32) are optimized and "
                         "run faster than others.",
        "inner_tooltip": "The value 'On' indicates that the glow is internal. The value 'Off' sets the "
                         "external glow (glow around the outer contour of the object).",
        "knockout_tooltip": "The value 'Enabled' makes the object's fill transparent and makes the background "
                            "color of the document visible. The default is 'Off' (no knockout effect).",
        "strength_tooltip": "The higher the value, the more saturated the color of the shadow and the stronger "
                            "the contrast between the glow and the background. "
                            "Valid values are from 0 to 255. The default is 2."
    },
    "colors": {
        "header": "Globale Farbeinstellungen.",
        "armor_calculator*green": "Reduzierte Rüstung: 100% Durchdringung",
        "armor_calculator*orange": "Reduzierte Rüstung: 50% Penetration",
        "armor_calculator*red": "Reduzierte Rüstung: 0% Penetration",
        "armor_calculator*yellow": "Reduzierte Rüstung: 50% Durchdringung (farbenblinder Modus)",
        "armor_calculator*purple": "Reduzierte Rüstung: 0% Penetration (Farbenblindmodus)",
        "main_gun*mainGunColor": "Hauptkaliber: Makrofarbe% (mainGunColor) s",
        "global*ally": "Globale Farbe: Verbündete",
        "global*bgColor": "Hintergrundfarbe des Bedienfelds",
        "global*enemyColorBlind": "Globale Farbe: Feind ist farbenblind",
        "global*enemy": "Globale Farbe: Feind",
        "global*alpha": "Transparenz der Panels",
        "global*alpha_tooltip": "0 - vollständig transparent. <br> 1 - nicht transparent.",
        "global*bgAlpha": "Hintergrundtransparenz von Panels",
        "global*bgAlpha_tooltip": "0 - vollständig transparent. <br> 1 - nicht transparent.",
        "global*deadColor": "Zerstört",
    },
    "service_channel_filter": {
        "header": "Filter für Meldungen im Mitteilungscenter - (Blendet die Nachrichten für die "
                  "ausgewählten Kategorien aus.)",
        "sys_keys*CustomizationForCredits": "Anpassung der Ausrüstung für Kredits.",
        "sys_keys*CustomizationForGold": "Anpassung der Ausrüstung für Gold.",
        "sys_keys*DismantlingForCredits": "Entfernen der Ausrüstung für Kredits.",
        "sys_keys*DismantlingForCrystal": "Entfernen der Ausrüstung für Anleihen.",
        "sys_keys*DismantlingForGold": "Entfernen der Ausrüstung für Gold.",
        "sys_keys*GameGreeting": "Spiel: Willkommensnachrichten.",
        "sys_keys*Information": "Informationsnachrichten.",
        "sys_keys*MultipleSelling": "Verkauf aus Lager (mehrere Artikel)",
        "sys_keys*PowerLevel": "Erforschen von Modulen und Technologie",
        "sys_keys*PurchaseForCredits": "Einkauf für Kredits.",
        "sys_keys*PurchaseForCrystal": "Einkauf für Anleihen.",
        "sys_keys*PurchaseForGold": "Einkauf für Gold.",
        "sys_keys*Remove": "Enfernung",
        "sys_keys*Repair": "Reparatur",
        "sys_keys*Restore": "Wiederherstellung",
        "sys_keys*Selling": "Verkauft",
        "sys_keys*autoMaintenance": "Automatische Reparatur.",
        "sys_keys*customizationChanged": "Änderung der Anpassung"
    },
    "service": {
        "name": "Battle Observer - v{0}".format(__version__),
        "description": "Battle Observer Einstellungen",
        "windowTitle": "Battle Observer Einstellungen - v{0}".format(__version__),
        "buttonOK": "OK",
        "buttonCancel": "Abbrechen",
        "buttonApply": "Speichern",
        "enableButtonTooltip": "{HEADER}EIN/AUS{/HEADER}{BODY}Einschalten/Ausschalten des Modules{/BODY}"
    },
    "updateDialog": {
        "buttonOK": "RESTART",
        "buttonWAIT": "WAIT",
        "titleWAIT": "Battle Observer Update - WAIT",
        "titleOK": "Battle Observer Update - Press RESTART",
        "messageWAIT": "Wait while downloading Updates v{0}",
        "messageOK": "Click RESTART to complete the Upgrade process. v{0}",
        "buttonAUTO": "Automatically",
        "buttonHANDLE": "Manually",
        "buttonCancel": "Cancel",
        "messageNEW":
            "<font size='15'><font size='20' color='#FFFF00'><b>Choose a download option.</b></font>\n"
            "<p align='left'><font color ='#00FF00'><b>Automatically</b></font> - download and unpack the archive"
            "updates to the folder {0}\n<font color='#FFFF00'><b>Manually</b></font> - will open a link to"
            "the same archive, but you will have to extract the package and copy the *.wotmod file manually.</p></font>"
            "\n<font size='20 'color='#FFFF00'><b>Changelog</b></font>\n",
        "titleNEW": "Battle Observer\n<font size='20'>Update available <font color='#FFFF00'>v{0}</font></font>"
    },
    "sixth_sense": {
        "header": "Sixth sense.",
        "showTimer": "Show timer.",
        "lampShowTime": "Timer sec.",
        "playTickSound": "Play tick sound."
    },
    "distance_to_enemy": {
        "header": "Entfernung zum nächsten entdeckten Feind.",
        "x": "Position des Textes waagerecht",
        "x_tooltip": "Position von der Mitte des Bildschirmes gemessen. Textausrichtung ---|Zentriert|---",
        "y": "Position des Textes senkrechtrecht",
        "y_tooltip": "Position von der Mitte des Bildschirmes gemessen.",
        "template": "String-Muster. Makros: %(distance)s, %(name)s",
        "align": "Text align."
    },
    "own_health": {
        "header": "Own health.",
        "x": "Position des Textes waagerecht",
        "x_tooltip": "Position von der Mitte des Bildschirmes gemessen. Textausrichtung ---|Zentriert|---",
        "y": "Position des Textes senkrechtrecht",
        "y_tooltip": "Position von der Mitte des Bildschirmes gemessen.",
        "template": "String-Muster. Makros: %(cur_health)s, %(max_health)s, %(per_health)s",
        "align": "Text align.",
    },
    "crewDialog": {
        "enable": "Enable accelerated crew training?",
        "disable": "Disable accelerated crew training?",
        "submit": "Apply",
        "cancel": "Cancel",
        "notAvailable": "Field upgrades are not available for this vehicle.",
        "isFullXp": "You have accumulated the necessary amount of experience to fully upgrade the field upgrade.",
        "isFullComplete": "You have pumped the field upgrade to the highest possible level.",
        "needTurnOff": "You do not have field upgrades, it is recommended to disable accelerated crew training."
    },
}

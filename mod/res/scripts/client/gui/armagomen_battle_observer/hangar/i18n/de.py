# coding=utf-8
from ...core.bo_constants import MOD_VERSION

timeFormat_tooltip = """Directive Meaning
%a  Locale’s abbreviated weekday name.
%A  Locale’s full weekday name.
%b  Locale’s abbreviated month name.
%B  Locale’s full month name.
%c  Locale’s appropriate date and time representation.
%d  Day of the month as a decimal number [01,31].
%H  Hour (24-hour clock) as a decimal number [00,23].
%I  Hour (12-hour clock) as a decimal number [01,12].
%j  Day of the year as a decimal number [001,366].
%m  Month as a decimal number [01,12].
%M  Minute as a decimal number [00,59].
%p  Locale’s equivalent of either AM or PM.
%S  Second as a decimal number [00,61].
%U  Week number of the year (Sunday as the first day of the week) as a decimal number [00,53].
%w  Weekday as a decimal number [0(Sunday),6].
%W  Week number of the year (Monday as the first day of the week) as a decimal number [00,53].
%x  Locale’s appropriate date representation.
%X  Locale’s appropriate time representation.
%y  Year without century as a decimal number [00,99].
%Y  Year with century as a decimal number.
%Z  Time zone name (no characters if no time zone exists).
%%  A literal '%' character."""
translate = {
    "configSelect": {
        "header": "Wähle Konfiguration (Verzeichnis: mods\configs\mod_battle_observer)",
        "selectedConfig": "Config",
        "donate_button_ua": "DONATE UA - Гривна",
        "donate_button_ru": "DONATE RU - Рубль",
        "donate_button_eu": "DONATE EU - EUR / USD",
        "support_button": "Discord support"
    },
    "main": {
        "header": "Allgemeine Einstellungen",
        "enableBarsAnimation": "Aktivieren Sie die Animation aller Bedienfelder.",
        "showFriendsAndClanInEars": "Markiere Clanfreunde und dich in den Teamlisten.",
        "autoClearCache": "Löschen Sie den Spiel-Cache beim Beenden.",
        "autoClearCache_tooltip": "Bereinigen der temporären Dateien des Spiels im Ordner "
                                  "AppData/Roaming/Wargaming.net/WorldOfTanks."
                                  "<br> Dort geänderte Ordner sind nicht betroffen.",
        "backgroundTransparency": "Transparenz für den Hintergrund",
        "background": "Hintergrund im Style 'normal'",
        "removeShadowInPrebattle": "Entferne den Blackout-Timer zu Beginn des Kampfes",
        "smallDoubleCarousel": "Verwenden Sie kleine Symbole im Karussell.",
        "carouselRows": "Reihenanzahl des mehrreihigen Panzerkarussells.",
        "hideBadges": "Deaktivieren Sie Chevrons/Ribbons im Spielerpanel",
        "fps_enableFPSLimiter": "Включить ограничитель FPS",
        "enableFPSLimiter_tooltip": "Внимание, для полного отключения или включения необходим перезапуск игры.",
        "fps_maxFrameRate": "Maximum Frame Rate",
        "hideClanAbbrev": "Deaktiviere Clan-Anzeige im Playerspanel, Tab Screen, Ladebildschirm.",
        "hideChatInRandom": "Chat in Zufallsgefechten deaktivieren",
        "hideChatInRandom_tooltip": "Chat in Zufsallsgefechten komplett deaktivieren."
                                    "<br> incl. Chat-Formular und alles, was damit verbunden ist",
        "anonymousEnableShow": "Show Anonymous.",
        "useKeyPairs": "Use key pairs Alt, Ctrl, Shift",
        "anonymousNameChange": "Сhange Anonymous Name",
        "removeHandbrake": "Handbremse für AT-SPG deaktivieren."
    },
    "dispersion_circle": {
        "header": "Kreis für Streuung der Kanone. (Mischen)",
        "asExtraServerLap": "Anzeige des Kreises für die Streuung der Kanone.",
        "asExtraServerLap_tooltip": "Fügt einen zweiten Kreis der Server-Sichtung hinzu.",
        "replaceOriginalCircle": "Ersetzen des originalen Kreises.",
        "circle_scale": "Kreisgrößenmultiplikator 1 - 100 %",
        "circle_scale_tooltip": "Es wird nicht empfohlen, den Wert unter 65 einzustellen.",
        "timer_enabled": "Schalten Sie den Reduktions-Timer ein.",
        "timer_position_x": "Timer Position X",
        "timer_position_y": "Timer Position Y",
        "timer_color": "Timerfarbe, noch nicht konvergiert.",
        "timer_done_color": "Timer- / Nachrichtenfarbe (volle Reduzierung).",
        "timer_align": "Text align."
    },
    "tank_carousel": {
        "header": "TANK CAROUSEL SETUP",
        "carouselRows": "Anzahl der Reihen eines mehrreihigen Tankkarussells.",
        "carouselRows_toltip": "Funktioniert nur, wenn das mehrzeilige Karussell im Client aktiviert ist.",
        "smallDoubleCarousel": "Erzwingen Sie die Verwendung kleiner Symbole im Tankkarussell."
    },
    "postmortem_panel": {
        "header": "Panel nach Zerstörung.",
        "hideKillerInfo": "Informationen über den Zerstörer entfernen."
    },
    "effects": {
        "header": "Visuelle Kameraeffekte anpassen",
        "noShockWave": "Keine Kameraerschütterung, wenn Panzer getroffen wurde",
        "noFlashBang": "Roten Blitz ausschalten, wenn eigener Panzer getroffen wurde",
        "noLightEffect": "Blitz beim Schuss entfernen.",
        "noBinoculars": "Schwarzen Schatten im Zielfernrohr entfernen"
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
        "bars_colors": "Farbeinstellung HP Panel",
        "colors*ally": "HP Balken und Differenz: Team",
        "colors*bgColor": "HP Balken Hintergrundfarbe",
        "colors*enemyColorBlind": "HP Balken und Differenz: Gegner (Modus für Farbenblinde)",
        "colors*enemy": "HP Balken und Differenz: Gegner",
        "colors*alpha": "Tranzparenz des HP Balkens",
        "colors*alpha_tooltip": "0 - Komplett Transparent<br>1 - nicht Transparent",
        "colors*bgAlpha": "Hintergrund Transparenz HP Balken",
        "colors*bgAlpha_tooltip": "0 - Komplett Transparent.<br>1 - Nicht Transparent.",
        "outline*enabled": "Kantenbänder im Stil normal",
        "outline*color": "Benutzerdefinierte Farbe."
    },
    "markers": {
        "header": "Panzerklassen Panel (unter HP Panel)",
        "markersClassColor": "Fahrzeugklassen farbig anzeigen (siehe ' FARBEINSTELLUNGEN')",
        "x": "Позиция по Горизонтали от центра.",
        "x_tooltip": "Позиция маркеров по Горизонтали от центра экрана.",
        "y": "Позиция по Вертикали от верха.",
        "y_tooltip": "Позиция маркеров по Вертикали от верха экрана.",
        "showMarkers_KEY": "Taste zum Einschalten/Ausschalten des Panels:"
    },
    "armor_calculator": {
        "header": "Durchschlagsanzeiger (Berechnung der Panzerung)",
        "calcPosition*x": "Position des Haupt Textfeldes waagerecht",
        "calcPosition*y": "Position des Haupt Textfeldes senkrecht",
        "showCalcPoints": "Zeige Haupt Textfeld",
        "template": "Formatierung des Haupt-Textfeldes",
        "template_tooltip": "HTML Formatierung möglich<br>Macros:<br>%(calcedArmor)s - verminderte Panzerung"
                            "<br>%(armor)s - Panzerung ohne Neigung. "
                            "<br>%(piercingPower)s - Durchschlag der Granate mit Berechnung der Enfernung"
                            "<br>%(caliber)s - Kaliber der Granate<br>%(color)s - Farbe (siehe Farbeinstellungen)"
    },
    "log_global": {
        "header": "Allgemeine Einstellungen für Schadensprotokoll",
        "attackReas": "Einstellung für Makro %(attackReason)s - Art des Schadens",
        "attackReason*drowning": "Ertrinken",
        "attackReason*fire": "Feuer",
        "attackReason*overturn": "Umgekippt",
        "attackReason*ramming": "Rammen",
        "attackReason*shot": "Schaden durch Treffer",
        "attackReason*world_collision": "Schaden durch Fallen",
        "logsAltmode_KEY": "Taste zum Umschalten auf Alternativen Modus",
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
        "settings*background": "Aktivieren Sie Hintergrundsubstrat log (nur, wenn es in der Mitte)",
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
        "mainGunDoneIcon": "Einstellung für Makro: %(mainGunDoneIcon)s",
        "mainGunDynamic": "Dynamische Berechnung für verbl. Schaden bis zum 'Grosskaliber'",
        "mainGunFailureIcon": "Einstellung für Makro: %(mainGunFailureIcon)s",
        "mainGunIcon": "Einstellung für Makro: %(mainGunIcon)s",
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
        "colors*green": "Panel Basiseroberung: Verbündete",
        "colors*bgColor": "Panel Basiseroberung: Hintergrundfarbe",
        "colors*red": "Panel Basiseroberung: Gegner",
        "colors*purple": "Panel Basiseroberung: Gegner (Farbenblindmodus)",
        "colors*alpha": "Transparenz der Farbe",
        "colors*alpha_tooltip": "0 - Transparenz 100%.<br>1 - Transparenz 0%.",
        "colors*bgAlpha": "Hintergrundstreifen, Transparenz",
        "colors*bgAlpha_tooltip": "0 - Transparenz 100%.<br>1 - Transparenz 0%.",
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
    "players_spotted": {
        "header": "Anzeige für aufgedeckte Gegner in der Team-Anzeige (Playerspanel)",
        "settings*align": "Ausrichtung text:",
        "settings*align_tooltip": "Ausrichtung:<br>left - Linksbündig<br>center - Zentriert<br>right - Rechtsbündig",
        "settings*x": "Position relativ zum Symbol waagerecht",
        "settings*y": "Position relativ zum Symbol senkrecht",
        "status*donotlight": "wenn Gegner nicht mehr aufgedeckt ist",
        "status*lights": "wenn Gegner aufgedeckt ist"
    },
    "players_damages": {
        "header": "Verursachter Schaden in der Team-Anzeige (Playerspanel)",
        "damages_settings*align": "Ausrichtung des Textes:",
        "damages_settings*align_tooltip": "Ausrichtung:<br>left - Linksbündig<br>center - "
                                          "Zentriert ausgerichtet<br>right - Rechtsbündig",
        "damages_KEY": "Taste zum Anzeigen des Textes",
        "damages_settings*x": "Position waagerecht",
        "damages_settings*y": "Position senkrecht",
        "damages_text": "Textbox: verfügbare Makro(s): %(damage)s"
    },
    "players_bars": {
        "header": "HP Anzeige in der Team-Anzeige (Playerspanel)",
        "bar_settings*bar*height": "Höhe des HP-Balkens:",
        "bar_settings*bar*width": "Breite des HP-Balkens:",
        "bar_settings*bar*x": "Position des  HP-Balkens waagerecht",
        "bar_settings*bar*y": "Position des  HP-Balkens senkrecht",
        "bar_settings*bar*colors*ally": "Verbündete",
        "bar_settings*bar*colors*bgColor": "Hintergrundfarbe",
        "bar_settings*bar*colors*enemy": "Gegner",
        "bar_settings*bar*colors*enemyBlind": "Gegner - Farbenblindheit",
        "bar_settings*bar*colors*alpha": "Transparenz",
        "bar_settings*bar*colors*alpha_tooltip": "0 - Transparenz 100%.<br>1 - Transparenz 0%.",
        "bar_settings*bar*colors*bgAlpha": "Hintergrundstreifen, Transparenz",
        "bar_settings*bar*colors*bgAlpha_tooltip": "0 - Transparenz 100%.<br>1 - Transparenz 0%.",
        "bar_settings*bar*outline*enabled": "Rahmen aktivieren.",
        "bar_settings*bar*outline*customColor": "Benutzerdefinierte Rahmenfarbe.",
        "bar_settings*bar*outline*color": "Benutzerdefinierte Farbe.",
        "bar_settings*bar*outline*alpha": "Transparenz der Fransen.",
        "bar_settings*text*x": "Position waagerecht",
        "bar_settings*text*y": "Position senkrecht",
        "bar_settings*text*align": "Ausrichtung text:",
        "bar_settings*text*align_tooltip": "Ausrichtung:left - Linksbündig, center - "
                                           "Zentriert ausgerichtet, right - Rechtsbündig",
        "hp_text": "Textbox: verfügbare Makro(s): %(health)s | %(maxHealth)s | %(percent)s.",
        "hpbarsShow_KEY": "Taste zum Anzeigen der HP-Anzeige: ",
        "hpbarsclassColor": "HP-Balken in der Farbe der Panzerklassen anzeigen",
        "showHpBarsOnKeyDown": "nur zeigen, wenn Taste gedrückt ist"
    },
    "panels_icon": {
        "header": "Farbfilter für die Symbole in der Team-Anzeige (Playerspanel)",
        "icon_info": "Diese Funktion umkreist jedes Symbol der Technologie in der Team-Anzeige in der Farbe der "
                     "Technologieklassen.<br>Der folgende Regler beeinflusst die Helligkeit: "
                     "Die empfohlene Filterstärke ist -1",
        "blackout": "Filterstärke (Helligkeit)"
    },
    "zoom": {
        "header": "Zoom für Richtschützenansicht (Sniper Zoom IN)",
        "LENS_EFFECTS_ENABLED": "Grünen Rand im Snipermodus entfernen..",
        "LENS_EFFECTS_ENABLED_tooltip": "ERFORDERLICHER NEUSTART DES SPIELS",
        "disable_cam_after_shoot": "Отключать снайперский режим после выстрела.",
        "disable_SniperCamera_After_Shoot_tooltip": "Автоматически переключает камеру в аркадный режим "
                                                    "после выстрела если калибр орудия больше 40мм.",
        "disable_cam_skip_clip": "Не выходить если магазинная система заряжания",
        "default_zoom*zoom_default": "Multiplikator für Festen Zoom",
        "default_zoom*enabled": "Fester Zoom",
        "dynamic_zoom*enabled": "Automatische Auswahl der Zoomstufen beim wechsel in den Richtschützenmodus",
        "dynamic_zoom*enabled_tooltip": "Wenn diese Option aktiviert ist, wird der <b>Fester Zoom</b> deaktiviert.",
        "dynamic_zoom*zoom_max": "Maximaler Zoom Faktor für automatische Auswahl: bis zu 40.0",
        "dynamic_zoom*zoom_min": "Minimaler Zoom Faktor für automatische Auswahl: beginnend von 2.0",
        "dynamic_zoom*zoomToGunMarker": "Aktivieren der Annäherung der Kamera an die Zentralmarkierung",
        "dynamic_zoom*zoomXMeters": "Empfindlichkeit bei Annäherung: in Metern",
        "dynamic_zoom*zoomXMeters_tooltip": "(Dynamischer Zoom = Enfernung / Empfindlichkeit bei Annäherung)"
                                            "<br>Standard: alle 17 Meter + 1 (je kleiner die Zahl, desto mehr Zoom",
        "zoomSteps*enabled": "Zoom Stufen.",
        "zoomSteps*steps": "Zooms Stufen. (Trennung durch Komma)",
        "zoomSteps*steps_tooltip": "Sie können beliebig viele Werte (getrennt durch Komma und Leerzeichren) schreiben."
    },
    "arcade_camera": {
        "header": "Zoom für Arcade Ansicht (Arcade Zoom Out)",
        "max": "Maximale Entfernung vom Panzer. Standard: 25.0",
        "min": "Minimaler Abstand vom Panzer. Standard: 2.0",
        "startDeadDist": "Abstand bei Start / bei zerstört",
        "startDeadDist_tooltip": "Der Abstand vom Panzer beim Start des Gefechtes / "
                                 "b.z.w. der Abstand wenn der Panzer zerstört wurde. Standard ist: 15"
    },
    "strategic_camera": {
        "header": "Zoom für Artillerieansicht (Strategic Zoom Out)",
        "max": "Maximale Enfernung der Kamera vom Panzer. Standard: 100.0",
        "min": "Minimaler Abstand der Kamera vom Panzer. Standard: 40.0"
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
        "aliveOnly": "Blockiere den Schuss auf den Zerstörten.",
        "msg": "Eine Nachricht über eine erfolgreiche Sperre ist nur für Sie sichtbar.",
        "msg_tooltip": "Diese Nachricht wird nur angezeigt, wenn der Schuss von einem Verbündeten geblockt wird."
    },
    "minimap": {
        "header": "MINI-KARTE",
        "zoom*enabled": "Zentrierung der Minikarte aktivieren.",
        "zoom*zoom_KEY": "Minikarte zentrieren auf",
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
        "header": "Farbeinstellungen",
        "armor_calculator*green": "Durchschlag 100%",
        "armor_calculator*orange": "Durchschlag von 50%",
        "armor_calculator*red": "Durchschlag von 0%",
        "armor_calculator*yellow": "Durchschlag von 50% (Modus für Farbenblinde)",
        "armor_calculator*purple": "Durchschlag von 0% (Modus für Farbenblinde)",
        "calculator_colors": "Farbeinstellung für den 'Durchschlagsanzeiger'",
        "colorAvg_colors": "Farbgrenzen für Makro: %(tankDamageAvgColor)s",
        "main_gun*mainGunColor": "Farbe Makro %(mainGunColor)s",
        "mark_colors": "Farbe der Fahrzeugklassen (Standard)",
        "markers*ally": "Verbündete",
        "markers*deadColor": "Zerstört",
        "markers*enemyColorBlind": "Gegner (Modus für Farbenblinde)",
        "markers*enemy": "Gegner"
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
        "name": "Battle Observer - v{0}".format(MOD_VERSION),
        "description": "Battle Observer Einstellungen",
        "windowTitle": "Battle Observer Einstellungen - v{0}".format(MOD_VERSION),
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
        "messageNEW": "New version is available. v{0}\n\n"
                      "<b>Сhoose one of the following download options.</b>\n\n"
                      "<b>Automatic</b> - will download and unzip the update to your update {1} folder\n\n"
                      "<b>Manually</b> - will open link in the browser to the same archive but you will have "
                      "to extract the package and copy the *.wotmod files manually.\n",
        "titleNEW": "New version is available. v{0}"
    },
    "sixth_sense": {
        "header": "Sixth sense.",
        "showTimer": "Show timer.",
        "lampShowTime": "Timer sec.",
        "playTickSound": "Play tick sound."
    }
}

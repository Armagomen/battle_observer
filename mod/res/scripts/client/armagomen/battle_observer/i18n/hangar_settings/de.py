# coding=utf-8

timeFormat_tooltip = "<br>".join((
    "Format - Bedeutung",
    "%a - Abkürzung des Wochentags",
    "%A - Vollständiger Name des Wochentags",
    "%b - Abkürzung des Monatsnamens",
    "%B - Vollständiger Monatsname",
    "%c - Datum und Uhrzeit",
    "%d - Tag des Monats [01,31]",
    "%H - Stunde (24-Stunden-Format) [00,23]",
    "%I - Stunde (12-Stunden-Format) [01,12]",
    "%j - Tag des Jahres [001,366]",
    "%m - Monatsnummer [01,12]",
    "%M - Minutenanzahl [00,59]",
    "%p - AM oder PM (bei 12-Stunden-Format)",
    "%S - Sekundenanzahl [00,61]",
    "%U - Kalenderwoche (beginnend am Sonntag) [00,53]",
    "%w - Wochentagsnummer [0(Sonntag),6]",
    "%W - Kalenderwoche (beginnend am Montag) [00,53]",
    "%x - Datum im systemabhängigen Format",
    "%X - Uhrzeit im systemabhängigen Format",
    "%y - Jahr ohne Jahrhundert [00,99]",
    "%Y - Jahr mit Jahrhundert",
    "%Z - Name der Zeitzone (leer, wenn nicht vorhanden)",
    "%% - Zeichen '%'"
))

RESTART_TOOLTIP = "Ein Neustart des Spiels ist erforderlich, um die Funktion zu aktivieren/deaktivieren."

localization = {
    "configSelect": {
        "header": "Einstellungsoptionen",
        "selector": "Einstellungen auswählen:",
        "donate_button_ua": "MONO Bank",
        "discord_button": "Discord-Modserver",
        "reload_config": "Einstellungen neu laden",
    },
    "main": {
        "header": "Nicht kategorisierte Einstellungen",
        "DEBUG_MODE": "Debug-Modus (nur bei Bedarf aktivieren)",
        "anti_anonymous": "Spieler mit verborgenem Spitznamen markieren",
        "clear_cache_automatically": "Cache beim Verlassen des Spiels automatisch löschen",
        "clear_cache_automatically_tooltip": "Löschen temporärer Spieldateien unter: AppData/Roaming/Wargaming.net/WorldOfTanks",
        "auto_crew_training": "'Schnelle Ausbildung der Besatzung' automatisch umschalten",
        "auto_crew_training_tooltip": "Überwacht den Status der 'Feldmodifikation' und aktiviert oder deaktiviert entsprechend die 'Schnelle Ausbildung der Besatzung'.",
        "auto_return_crew": "Besatzung automatisch zurückbringen",
        "auto_return_crew_tooltip": "Wenn die ausgewählte Panzerbesatzung fehlt, aber verfügbar ist und nicht in einem anderen Gefecht steckt, wird sie automatisch zurückgebracht.",
        "disable_score_sound": "Sound beim Zerstören eines verbündeten oder feindlichen Panzers deaktivieren",
        "disable_stun_sound": "Artillerie-Betäubungssound deaktivieren",
        "directives_only_from_storage": "Bonds und Silber beim Kauf von Direktiven sparen",
        "directives_only_from_storage_tooltip": "Verhindert das automatische Auffüllen von Direktiven mit Bonds oder Silber, wenn keine im Lager vorhanden sind. Aktiviert auch das Kontrollkästchen 'Automatisches Auffüllen', falls Vorräte vorhanden sind.",
        "hide_badges": "Abzeichen im Gefecht ausblenden",
        "hide_badges_tooltip": "Blendet Symbole in den Ohren, der Tab-Ansicht und dem Ladebildschirm aus.",
        "hide_clan_abbrev": "Clantags im Gefecht ausblenden",
        "hide_button_counters_on_top_panel": "Zähler und Hinweise auf Garagenkopfleisten-Knöpfen deaktivieren",
        "hide_button_counters_on_top_panel_tooltip": RESTART_TOOLTIP,
        "hide_dog_tags": "Erkennungsmarken im Gefecht ausblenden",
        "hide_field_mail": "Feldpost deaktivieren",
        "hide_hint_panel": "Hinweistafel im Gefecht ausblenden",
        "hide_main_chat_in_hangar": "Gemeinsamen Chat in der Garage deaktivieren",
        "hide_main_chat_in_hangar_tooltip": RESTART_TOOLTIP,
        "ignore_commanders_voice": "Kommandantenstimme ignorieren",
        "ignore_commanders_voice_tooltip": "Nach Aktivierung wird die Standardbesatzungsstimme erzwungen. Diese Einstellung ersetzt einzigartige Kommandantenstimmen durch die Standardstimme oder ein installiertes Modpack.",
        "premium_time": "Premium-Account-Timer anzeigen",
        "premium_time_tooltip": "Aktivierung oder Deaktivierung erfolgt nicht sofort—bitte bis zu 1 Minute warten oder die Garagenansicht wechseln.",
        "show_friends": "Freunde und Clanmitglieder in Teamlisten markieren",
        "useKeyPairs": "Gleichzeitige Nutzung linker/rechter Ctrl-, Alt- und Shift-Tasten",
        "useKeyPairs_tooltip": "Nach Aktivierung funktionieren die linken und rechten Tasten gleich, unabhängig von Moduleinstellungen.",
        "save_shot": "Schüsse auf Verbündete und zerstörte Panzer blockieren",
        "mute_team_base_sound": "Basisalarm-Sirene deaktivieren",
        "hide_prestige_hangar_widget": "Prestige-Widget in der Garage ausblenden",
        "hide_prestige_battle_widget": "Prestige-Widget im Gefecht ausblenden",
        "hide_prestige_profile_widget": "Prestige-Widget im Spielerprofil ausblenden",
        "excluded_map_slots_notification": "Benachrichtigung über verfügbare Kartensperrslots anzeigen",
        "auto_claim_clan_reward": "Clanbelohnungen automatisch abholen",
        "hideEventBanner": "Eventbanner deaktivieren"
    },
    "statistics": {
        "header": "Spielerstatistiken und Fahrzeug-Icon-Einstellungen",
        "icons": "Icons: Einfärbung nach Fahrzeugklassen",
        "icons_tooltip": "Diese Funktion verändert die Farben aller Fahrzeug-Icons im Ladebildschirm, in den Ohren und im Tab-Fenster. Der Filter beeinflusst die Helligkeit. Empfohlene Filterstärke: -1.25.",
        "icons_blackout": "Icons: Filterintensität (Helligkeit)",
        "statistics": "Spielerstatistiken nach WGR aktivieren",
        "statistics_vehicle_name_color": "Fahrzeugname entsprechend Spielerstatistik einfärben",
        "statistics_tooltip": "Statistiken werden im Ladebildschirm, in den Ohren und im Tab-Fenster angezeigt. Für genauere Einstellungen verwende die Datei statistics.json. Verfügbare Makros: WGR, colorWGR, winRate, nickname, battles, clanTag.",
        "statistics_colors*very_bad": "Sehr niedriges Niveau",
        "statistics_colors*bad": "Niedriges Niveau",
        "statistics_colors*normal": "Mittleres Niveau",
        "statistics_colors*good": "Hohes Niveau",
        "statistics_colors*very_good": "Sehr hohes Niveau",
        "statistics_colors*unique": "Einzigartiges Niveau",
        "statistics_panels_full_width": "Spielernamensfeldbreite (breite Ohren)",
        "statistics_panels_cut_width": "Spielernamensfeldbreite (schmale Ohren)"
    },
    "dispersion_circle": {
        "header": "Fadenkreuz- und Serverziel-Einstellungen",
        "server_aim": "Serverziel aktivieren (zusätzlicher Kreis)",
        "server_aim_tooltip": "Aktiviert einen zusätzlichen Zielkreis des Serverfadenkreuzes.",
        "replace": "Originalen Zielkreis ersetzen",
        "scale": "Größenmultiplikator des Kreises 30–100 % (0.3–1.0)",
        "scale_tooltip": "Dieser Parameter beeinflusst die endgültige Größe des zusätzlichen Zielkreises. Bei 0.3 (30%) ist er minimal, bei 1.0 (100%) maximal — also unverändert, wie voreingestellt. Ein Wert unter 0.6 (60%) wird nicht empfohlen."
    },
    "dispersion_timer": {
        "header": "Zielzeit-Timer-Einstellungen",
        "x": "Horizontale Position",
        "y": "Vertikale Position",
        "align": "Textausrichtung",
        "timer": "Restzeit anzeigen",
        "percent": "Prozent anzeigen"
    },
    "effects": {
        "header": "Einstellungen visueller Effekte",
        "noShockWave": "Kameravibration bei Treffer deaktivieren",
        "noFlashBang": "Blitz bei Schaden entfernen",
        "noBinoculars": "Abdunklung im Scharfschützenmodus entfernen",
        "noSniperDynamic": "Dynamische Kamera im Scharfschützenmodus deaktivieren"
    },
    "debug_panel": {
        "header": "FPS- und PING-Panel-Einstellungen",
        "fpsColor": "FPS-Farbanzeige",
        "pingColor": "PING-Farbanzeige",
        "style": "Panelstil"
    },
    "battle_timer": {
        "header": "Gefechtstimer-Einstellungen",
        "timerTemplate": "Feld zur Timer-Formatierung",
        "timerTemplate_tooltip": "Verfügbare Makros:<br>%(timer)s – Timer<br>%(timerColor)s – Timerfarbe.",
        "timerColorEndBattle": "Makrofarbe %(timerColor)s: weniger als 2 Min. verbleiben",
        "timerColor": "Makrofarbe %(timerColor)s: mehr als 2 Min. verbleiben"
    },
    "clock": {
        "header": "Uhranzeige in Garage und Gefecht",
        "battle*enabled": "Uhr im Gefecht",
        "battle*format": "Uhr im Gefecht: Formatierung",
        "battle*format_tooltip": timeFormat_tooltip,
        "battle*x": "Uhr im Gefecht: horizontale Position",
        "battle*y": "Uhr im Gefecht: vertikale Position",
        "hangar*enabled": "Uhr in der Garage",
        "hangar*format": "Uhr in der Garage: Formatierung",
        "hangar*format_tooltip": timeFormat_tooltip,
        "hangar*x": "Uhr in der Garage: horizontale Position",
        "hangar*y": "Uhr in der Garage: vertikale Position"
    },
    "hp_bars": {
        "header": "Team-Haltbarkeitsleisten-Einstellungen",
        "showAliveCount": "Zähler durch Lebendanzahl ersetzen",
        "style": "Leistenstil"
    },
    "armor_calculator": {
        "header": "Einstellungen des effektiven Panzerungsrechners",
        "position*x": "Horizontale Position vom Zentrum",
        "position*y": "Vertikale Position vom Zentrum",
        "display_on_allies": "Bei Verbündeten anzeigen",
        "show_piercing_power": "Durchschlagskraft anzeigen",
        "show_counted_armor": "Berechnete Panzerungsstärke anzeigen",
        "show_counted_armor_tooltip": "Panzerungsstärke unter Berücksichtigung von Neigungswinkel und Normalisierung",
        "show_piercing_reserve": "Restdurchschlag anzeigen",
        "show_caliber": "Kaliber anzeigen"
    },
    "wg_logs": {
        "header": "WG-Ereignisverlauf-Einstellungen",
        "wg_log_hide_assist": "Schaden durch Unterstützung ausblenden",
        "wg_log_hide_assist_tooltip": "Blendet Aufklärungsschaden aus dem detaillierten Ereignisverlauf aus",
        "wg_log_hide_block": "Geblockten Schaden ausblenden",
        "wg_log_hide_block_tooltip": "Blendet geblockten Schaden aus dem detaillierten Ereignisverlauf aus",
        "wg_log_hide_critics": "Kritische Treffer ohne Schaden ausblenden",
        "wg_log_hide_critics_tooltip": "Blendet kritische Treffer aus dem detaillierten Ereignisverlauf aus",
        "wg_log_pos_fix": "Verlauf an korrekte Position setzen (wie bei alten Mods)",
        "wg_log_pos_fix_tooltip": "Tauscht Positionen von erhaltenem und verursachtem Schaden im Ereignisverlauf"
    },
    "log_total": {
        "header": "Spielergesamteffizienz-Einstellungen",
        "settings*inCenter": "Log im Bildschirmzentrum anzeigen",
        "settings*x": "Horizontale Position des Hauptlogs",
        "settings*y": "Vertikale Position des Hauptlogs",
        "settings*align": "Textausrichtung:",
        "settings*align_tooltip": "left – links<br>center – zentriert<br>right – rechts"
    },
    "log_extended": {
        "header": "Detailierter Schadensverlauf-Einstellungen",
        "logsAltMode_hotkey": "Schadensverlauf in Alternativmodus umschalten",
        "settings*x": "Horizontale Position des Detailverlaufs",
        "settings*x_tooltip": "Bezogen auf die WG-Logposition",
        "settings*y": "Vertikale Position des Detailverlaufs",
        "settings*y_tooltip": "Bezogen auf die WG-Logposition",
        "settings*align": "Textausrichtung:",
        "settings*align_tooltip": "left – links<br>center – zentriert<br>right – rechts",
        "reverse": "Neue Ereignisse oben hinzufügen",
        "reverse_tooltip": "Neue Zeile am Anfang des Verlaufs hinzufügen",
        "shellColor*gold": "Farbe von Premiumgranaten",
        "shellColor*normal": "Farbe von Standardgranaten",
        "top_enabled": "Detailverlauf für verursachten Schaden",
        "bottom_enabled": "Detailverlauf für erlittenen Schaden"
    },
    "main_gun": {
        "header": "Einstellungen für die Medaille 'Hauptkaliber'",
        "x": "Horizontale Position (vom Bildschirmzentrum)",
        "y": "Vertikale Position (vom oberen Rand)",
        "progress_bar": "Fortschrittsbalken"
    },
    "team_bases_panel": {
        "header": "Einstellungen der Basis-Eroberungsanzeige",
        "y": "Vertikale Position des Eroberungsbalkens",
        "width": "Balkenbreite in Pixel"
    },
    "vehicle_types_colors": {
        "header": "Farbkonfiguration nach Fahrzeugklassen",
        "AT-SPG": "Jagdpanzer (Panzerjäger)",
        "SPG": "Artillerie (Selbstfahrlafette)",
        "heavyTank": "Schwerer Panzer",
        "lightTank": "Leichter Panzer",
        "mediumTank": "Mittlerer Panzer",
        "unknown": "Unbekannt (Globale Karte)"
    },
    "players_panels": {
        "header": "Spielerliste-Panel-Einstellungen",
        "players_damages_enabled": "Von Spielern verursachter Schaden",
        "players_damages_hotkey": "Taste zur Anzeige des Schadens",
        "players_damages_settings*x": "Horizontale Textposition",
        "players_damages_settings*y": "Vertikale Textposition",
        "players_bars_enabled": "Fahrzeughaltbarkeit anzeigen",
        "players_bars_hotkey": "Taste zur Anzeige der Haltbarkeit",
        "players_bars_classColor": "Haltbarkeitsbalken nach Fahrzeugtyp einfärben",
        "players_bars_on_key_pressed": "Balken nur bei Tastendruck anzeigen",
        "panels_spotted_fix": "Größe und Position der Aufklärungsindikatoren korrigieren"
    },
    "zoom": {
        "header": "Scharfschützenmodus-Einstellungen",
        "disable_cam_after_shot": "Scharfschützenmodus nach Schuss deaktivieren",
        "disable_cam_after_shot_tooltip": "Wechselt automatisch zur Arcade-Kamera nach dem Schuss, falls das Kaliber über 60mm liegt.",
        "disable_cam_after_shot_latency": "Verzögerung beim automatischen Verlassen des Scharfschützenmodus",
        "disable_cam_after_shot_skip_clip": "Nicht verlassen, wenn Magazinladesystem aktiv ist",
        "dynamic_zoom": "Automatischer Zoomstufen-Wähler",
        "dynamic_zoom_tooltip": "Bei aktivierter Funktion wird <b>die feste Einstellung</b> ignoriert. Die Zoomstufe wird automatisch anhand der Entfernung zum Ziel (in Metern) geteilt durch die Empfindlichkeit gewählt.<br>",
        "steps_enabled": "Zoomstufen ersetzen",
        "steps_range": "Zoomstufen-Schritte",
        "steps_range_tooltip": "Zoomstufen als Werte mit Komma oder Komma plus Leerzeichen angeben. Beliebige Anzahl an Stufen möglich."
    },
    "arcade_camera": {
        "header": "Kommandantenkamera-Einstellungen",
        "max": "Maximale Entfernung (Standard: 25)",
        "min": "Maximale Nähe (Standard: 2)",
        "startDeadDist": "Kameraentfernung beim Start/Tod (Standard: 15)",
        "scrollSensitivity": "Scroll-Empfindlichkeit (Standard: 4)"
    },
    "strategic_camera": {
        "header": "Artilleriekamera-Einstellungen",
        "max": "Maximale Entfernung (Standard: 100)",
        "min": "Maximale Nähe (Standard: 40)",
        "scrollSensitivity": "Scroll-Empfindlichkeit (Standard: 10)"
    },
    "flight_time": {
        "header": "Einstellungen für Flugzeit und Zielentfernung",
        "x": "Horizontale Textposition",
        "x_tooltip": "Entfernung vom Bildschirmzentrum auf der horizontalen Achse.",
        "y": "Vertikale Textposition",
        "y_tooltip": "Entfernung vom Bildschirmzentrum auf der vertikalen Achse.",
        "spgOnly": "Flugzeit nur für Artillerie anzeigen",
        "align": "Textausrichtung",
        "time": "Zeit anzeigen",
        "distance": "Entfernung anzeigen",
        "color": "Textfarbe"
    },
    "minimap": {
        "header": "Minikarten-Einstellungen",
        "zoom": "Mini-Karten-Zoom zentriert aktivieren",
        "permanentMinimapDeath": "Zerstörte Fahrzeuge auf der Karte anzeigen",
        "showDeathNames": "Namen zerstörter Panzer anzeigen",
        "real_view_radius": "Sichtradius über 445m zulassen",
        "yaw_limits": "Horizontale Zielwinkel für alle möglichen Fahrzeuge anzeigen",
        "zoom_hotkey": "Taste für Kartenvergrößerung"
    },
    "colors": {
        "header": "Globale Farbanpassungen des Mods",
        "armor_calculator*green": "Effektive Panzerung: Durchschlagschance 100%",
        "armor_calculator*orange": "Effektive Panzerung: Durchschlagschance 50%",
        "armor_calculator*red": "Effektive Panzerung: Durchschlagschance 0%",
        "armor_calculator*yellow": "Effektive Panzerung: 50% Chance (Farbenblindheitsmodus)",
        "armor_calculator*purple": "Effektive Panzerung: 0% Chance (Farbenblindheitsmodus)",
        "armor_calculator*normal": "Effektive Panzerung: Abpraller oder Treffer ohne Schaden",
        "global*ally": "Globale Farbe, Verbündeter",
        "global*bgColor": "Hintergrundfarbe der Panels",
        "global*enemyColorBlind": "Globale Farbe: Gegner (Farbenblindheitsmodus)",
        "global*enemy": "Globale Farbe, Gegner",
        "vehicle_types_colors*AT-SPG": "Jagdpz. (Panzerjäger)",
        "vehicle_types_colors*SPG": "Artillerie (Selbstfahrlafette)",
        "vehicle_types_colors*heavyTank": "Schwerer Panzer",
        "vehicle_types_colors*lightTank": "Leichter Panzer",
        "vehicle_types_colors*mediumTank": "Mittlerer Panzer",
        "vehicle_types_colors*unknown": "Unbekannt (Globale Karte)"
    },
    "service_channel_filter": {
        "header": "Systemkanal-Meldungsfilter",
        "sys_keys*CustomizationForCredits": "Fahrzeuganpassung gegen Credits",
        "sys_keys*CustomizationForGold": "Fahrzeuganpassung gegen Gold",
        "sys_keys*DismantlingForCredits": "Demontage gegen Credits",
        "sys_keys*DismantlingForCrystal": "Demontage gegen Bonds",
        "sys_keys*DismantlingForGold": "Demontage gegen Gold",
        "sys_keys*GameGreeting": "Spielbegrüßung",
        "sys_keys*Information": "Informationsmeldungen",
        "sys_keys*MultipleSelling": "Mehrfachverkauf",
        "sys_keys*PowerLevel": "Modul- und Fahrzeugforschung",
        "sys_keys*PurchaseForCredits": "Kauf mit Credits",
        "sys_keys*PurchaseForCrystal": "Kauf mit Bonds",
        "sys_keys*PurchaseForGold": "Kauf mit Gold",
        "sys_keys*Remove": "Gegenstand entfernen",
        "sys_keys*Repair": "Reparatur",
        "sys_keys*Restore": "Wiederherstellung",
        "sys_keys*Selling": "Einzelverkauf",
        "sys_keys*autoMaintenance": "Automatische Fahrzeugwartung",
        "sys_keys*customizationChanged": "Anpassung geändert"
    },
    "service": {
        "name": "Battle Observer – v{0}",
        "description": "Mod-Einstellungen für Battle Observer öffnen",
        "windowTitle": "Mod-Einstellungen Battle Observer – v{0}",
        "buttonOK": "OK",
        "buttonCancel": "Abbrechen",
        "buttonApply": "Übernehmen",
        "enableButtonTooltip": "{HEADER}AN/AUS{/HEADER}{BODY}Modul aktivieren/deaktivieren{/BODY}"
    },
    "sixth_sense": {
        "header": "Sechster Sinn – Einstellungen",
        "default_icon": "Integriertes Bild verwenden.",
        "default_icon_name": "Integriertes Bild auswählen.",
        "default_icon_tooltip": "Das im Mod enthaltene Bild wird anstelle eines benutzerdefinierten verwendet.",
        "lampShowTime": "Anzeigedauer in Sekunden",
        "lampShowTime_tooltip": "<b>Wie lange bleibt das Ziel sichtbar?</b><br>Nachdem sich die Sichtstrahlen eines Fahrzeugs mit den "
                                "Erkennungspunkten eines anderen kreuzen, bleibt das erste Fahrzeug sichtbar – auch wenn keine aktive "
                                "Sichtverbindung mehr besteht. Die normale Sichtdauer beträgt 10 Sekunden, kann jedoch durch Ausrüstung, "
                                "Besatzungsskills und Direktiven auf 8 bis 16–18 Sekunden angepasst werden.",
        "playTickSound": "Timer-Sound abspielen",
        "show_timer": "Timer aktivieren.",
        "show_timer_graphics": "Grafischen Timer aktivieren.",
        "show_timer_graphics_color": "Grafikfarbe.",
        "show_timer_graphics_radius": "Grafikkreisradius.",
        "icon_size": "Bildgröße in Pixel. Maximal 180"
    },
    "distance_to_enemy": {
        "header": "Entfernung zum nächsten erkannten Gegner – Einstellungen",
        "x": "Horizontale Textposition",
        "x_tooltip": "Position relativ zur Bildschirmmitte",
        "y": "Vertikale Textposition",
        "y_tooltip": "Position relativ zur Bildschirmmitte",
        "align": "Textausrichtung"
    },
    "own_health": {
        "header": "Spielerfahrzeug-Haltbarkeitsanzeige – Einstellungen",
        "x": "Horizontale Textposition",
        "x_tooltip": "Position relativ zur Bildschirmmitte",
        "y": "Vertikale Textposition",
        "y_tooltip": "Position relativ zur Bildschirmmitte"
    },
    "avg_efficiency_in_hangar": {
        "header": "Statistik-Widget im Hangar – Einstellungen",
        "avg_damage": "Durchschnittlicher verursachter Schaden anzeigen",
        "avg_assist": "Durchschnittlicher Unterstützungsschaden anzeigen",
        "avg_blocked": "Durchschnittlich durch Panzerung geblockten Schaden anzeigen",
        "avg_stun": "Durchschnittlicher Betäubungsschaden (Artillerie) anzeigen",
        "gun_marks": "Prozentsatz der Markierungsfortschritte anzeigen",
        "win_rate": "Siegquote anzeigen",
        "battles": "Anzahl der Gefechte anzeigen"
    }
}

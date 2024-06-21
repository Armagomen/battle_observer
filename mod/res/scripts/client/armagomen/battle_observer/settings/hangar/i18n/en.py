# coding=utf-8

timeFormat_tooltip = "<br>".join((
    "Directive Meaning",
    "%a - Locale’s abbreviated weekday name.",
    "%A - Locale’s full weekday name.",
    "%b - Locale’s abbreviated month name.",
    "%B - Locale’s full month name.",
    "%c - Locale’s appropriate date and time representation.",
    "%d - Day of the month as a decimal number [01,31].",
    "%H - Hour (24-hour clock) as a decimal number [00,23].",
    "%I - Hour (12-hour clock) as a decimal number [01,12].",
    "%j - Day of the year as a decimal number [001,366].",
    "%m - Month as a decimal number [01,12].",
    "%M - Minute as a decimal number [00,59].",
    "%p - Locale’s equivalent of either AM or PM.",
    "%S - Second as a decimal number [00,61].",
    "%U - Week number of the year (Sunday as the first day of the week) as a decimal number [00,53].",
    "%w - Weekday as a decimal number [0(Sunday),6].",
    "%W - Week number of the year (Monday as the first day of the week) as a decimal number [00,53].",
    "%x - Locale’s appropriate date representation.",
    "%X - Locale’s appropriate time representation.",
    "%y - Year without century as a decimal number [00,99].",
    "%Y - Year with century as a decimal number.",
    "%Z - Time zone name (no characters if no time zone exists).",
    "%% - A literal '%' character."
))

RESTART_TOOLTIP = "To enable / disable you need to restart the game."

localization = {
    "configSelect": {
        "header": "SELECT CONFIG from mods/configs/mod_battle_observer",
        "selector": "Config",
        "donate_button_ua": "MONO BANK",
        "discord_button": "Discord support & chat"
    },
    "main": {
        "header": "GENERAL SETTINGS",
        "DEBUG_MODE": "DEBUG_MODE",
        "hide_badges": "Disable chevrons/ribbons: in ears, on tab window, on boot screen.",
        "hide_clan_abbrev": "Disable clan display: in ears, on tab window, on boot screen.",
        "show_friends": "Mark friends and clan players in team lists.",
        "clear_cache_automatically": "Clear the game cache on startup.",
        "clear_cache_automatically_tooltip": "Cleaning the temporary files of the game in the folder "
                                             "AppData/Roaming/Wargaming.net/WorldOfTanks."
                                             "<br>Folders that are modified there are not affected.",
        "smallDoubleCarousel": "Use small icons in the tank carousel.",
        "carouselRows": "number of rows of multi-row tank carousel",
        "anti_anonymous": "Mark players with a hidden nickname.",
        "useKeyPairs": "Use key pairs Alt, Ctrl, Shift",
        "useKeyPairs_tooltip": "Once enabled, the left and right keys will work as one, regardless of which one you "
                               "chose in the module settings.",
        "hide_dog_tags": "Disable display of tokens.",
        "ignore_commanders_voice": "Ignore commander voiceover.",
        "ignore_commanders_voice_tooltip": "Once enabled, the standard crew voiceover will be forcibly used. "
                                           "The parameter will replace all voiceover of bloggers, "
                                           "Chuck Norris and so on with the standard / from the voiceover mod. ",
        "disable_score_sound": "Disable score change sound",
        "premium_time": "Display exact premium time.",
        "auto_crew_training": "Automatic switching of 'Accelerated crew training'",
        "auto_crew_training_tooltip": "Monitors whether 'Field Upgrade' is upgraded/available and enables or disables"
                                      " 'Expedited Crew Training' accordingly.",
        "directives_only_from_storage": "Do not replenish directives for currency (automatically)",
        "directives_only_from_storage_tooltip":
            "Prevent automatic replenishment of instructions for game currency if they are not in stock. It will also "
            "turn on automatic replenishment from the warehouse if they are there and you forgot to tick the box.",
        "hide_hint_panel": "Disable hints in battle",
        "hide_field_mail": "Disable field mail",
        "auto_return_crew": "Automatic crew return",
        "auto_return_crew_tooltip": "If there is no crew on the selected tank, but there is one for it and is not in "
                                    "battle on another tank, the crew will be returned to the tank automatically.",
        "disable_stun_sound": "Remove stun sound",
        "hide_main_chat_in_hangar": "Disable general chat in the hangar",
        "hide_main_chat_in_hangar_tooltip": RESTART_TOOLTIP,
        "hide_button_counters_on_top_panel": "Disable tooltips on buttons in the hangar header",
        "hide_button_counters_on_top_panel_tooltip": RESTART_TOOLTIP,
        "save_shot": "Block shooting at allies and destroyed.",
        "mute_team_base_sound": "Mute base capture siren.",
        "hide_hangar_prestige_widget": "Hide elite levels widget in hangar.",
        "hide_battle_prestige_widget": "Hide elite levels widget in battle.",
        "hide_profile_prestige_widget": "Hide elite levels widget in vehicle statistics in profile.",
        "excluded_map_slots_notification": "Notify about available excluded map slots.",
        "auto_claim_clan_reward": "Collect clan rewards automatically.",
    },
    "statistics": {
        "header": "WTR (WGR) Player Statistics | Tank icons",
        "statistics_enabled": "Enable player statistics WTR rating",
        "statistics_change_vehicle_name_color": "Change the color of the tank name in the ears to the color "
                                                "of the statistics",
        "statistics_enabled_tooltip": "Statistics will be displayed on: loading screen, in ears, taboo window. "
                                      "For more fine-tuning see the statistics.json file."
                                      " Available macro names: WTR, colorWTR, winRate, nickname, battles, clanTag",
        "icon_enabled": "Repaint tank icons in the colors of vehicle classes",
        "icon_enabled_tooltip": "This function repaints any vehicle icons in the ears, taboo window, on the loading "
                                "screen in the color of vehicle classes.<br>"
                                "Filter strength affects brightness.<br>Recommended filter strength -1.25",
        "icon_blackout": "Filter strength (brightness)",

        "panels_full_width": "Player Name Field Width - Big Ears",
        "panels_cut_width": "Player Name Field Width - Small Ears"
    },
    "dispersion_circle": {
        "header": "Setting the collapsing circle, server sight",
        "replace": "Replace Original Circle.",
        "server_aim": "Enable server scope (extra lap)",
        "server_aim_tooltip": "Enabling the feature will create an extra server lapping circle.",
        "scale": "Circle size multiplier 30-100% (0.3-1.0)",
        "scale_tooltip": "This parameter affects what the additional summation circle will be in the result."
                         "If the value is 0.3 (30%), then the circle will be the minimum possible, "
                         "and at 1.0 (100%) - the maximum, i.e. without changes."
                         "It is not recommended to set a value lower than 65%."
    },
    "dispersion_timer": {
        "header": "Setting the reduction timer",
        "x": "Horizontal position",
        "y": "Vertical position",
        "color": "Color: Not reduced",
        "done_color": "Color: Reduced",
        "align": "Text alignment"
    },
    "tank_carousel": {
        "header": "TANK CAROUSEL SETUP",
        "carouselRows": "Number of rows of multi-row tank carousel.",
        "carouselRows_toltip": "Only works if there is no event that changes the standard carousel.",
        "smallDoubleCarousel": "Forcibly use small icons in tank carousel."
    },
    "effects": {
        "header": "Customize effects",
        "noShockWave": "Remove camera shaking when hit by tank.",
        "noFlashBang": "Remove red flash when taking damage.",
        "noBinoculars": "Remove the blackout in sniper mode.",
        "noSniperDynamic": "Disable dynamic camera in sniper mode."
    },
    "debug_panel": {
        "header": "FPS and PING panel settings",
        "fpsColor": "FPS Color",
        "pingColor": "PING Color",
        "pingLagColor": "LAG color - Lags present",
        "style": "Panel style",
    },
    "battle_timer": {
        "header": "TIMER",
        "timerTemplate": "Field to format the timer",
        "timerTemplate_tooltip": "Available macros:<br> %(timer)s<br> %(timerColor)s<br>HTML - YES",
        "timerColorEndBattle": "Color macro %(timerColor)s if there are less than 2 mim",
        "timerColor": "Color macro %(timerColor)s"
    },
    "clock": {
        "header": "CLOCK",
        "battle*enabled": "Display in battle.",
        "battle*format": "format.",
        "battle*format_tooltip": timeFormat_tooltip,
        "battle*x": "battle X",
        "battle*y": "battle Y",
        "hangar*enabled": "Display in hangar.",
        "hangar*format": "format.",
        "hangar*format_tooltip": timeFormat_tooltip,
        "hangar*x": "hangar X",
        "hangar*y": "hangar Y"
    },
    "hp_bars": {
        "header": "TOTAL HP PANEL",
        "showAliveCount": "Show survivors on the panel",
        "style": "Style panel HP"
    },
    "armor_calculator": {
        "header": "Penetration indicator - CALCULATOR GIVEN ARMOR",
        "position*x": "Position the main text box of the calculator Horizontally",
        "position*y": "Position the main text box of the calculator Vertically",
        "template": "Template Main text field",
        "display_on_allies": "Display on allies",
        "template_tooltip": "Macro format:% (name) data type s:d:f.<br>"
                            "s-string, d-decimal, f-floating point<br><br>"
                            "List of available macros:<br>"
                            "<li>%(countedArmor)d - Counted armor.</li>"
                            "<li>%(piercingPower)d - Distance-based projectile penetration.</li>"
                            "<li>%(piercingReserve)d - Penetration reserve after piercing armor.</li>"
                            "<li>%(caliber)d - Projectile caliber. </li>"
                            "<li>%(message)s - Message from the messages section in the config file.</li>"
                            "<li>%(ricochet)s - Potential ricochet alert.</li>"
                            "<li>%(noDamage)s - Notification that there will be no damage. The projectile will hit the "
                            "module bypassing main armor. Caterpillar no damage, wheel no damage, and so on.</li>"
                            "<li>%(color)s - color (see color setting).</li>"
    },
    "wg_logs": {
        "header": "WG LOG SETTINGS",
        "wg_log_hide_assist": "Hide damage intelligence",
        "wg_log_hide_assist_tooltip": "Removes the damage from intelligence detailed log WG",
        "wg_log_hide_block": "Hide blocked damage",
        "wg_log_hide_block_tooltip": "Removes the blocked damage from a detailed log WG",
        "wg_log_hide_critics": "Hide critical hits",
        "wg_log_hide_critics_tooltip": "Removes critical hits from the detailed log WG",
        "wg_log_pos_fix": "Put logs into the right places.",
        "wg_log_pos_fix_tooltip": "Switches positions of caused damage and received damage logs."
                                  "<br>If enabled - received is at the bottom, caused is at the top."
    },
    "log_total": {
        "header": "TOTAL LOG OF THE EFFECTIVENESS OF THE PLAYER",
        "settings*inCenter": "Display the log in the middle of the screen",
        "settings*x": "the Position of the main log Horizontal",
        "settings*y": "the Position of the main log Vertical",
        "settings*align": "Alignment text:",
        "mainLogScale": "Scaling functions."
    },
    "log_extended": {
        "header": "DETAILED LOG OF THE DAMAGE",
        "log_extended_shellColor*normal": "configure macro %(shellColor)s - Silver",
        "logsAltMode_hotkey": "Key switch logs in the alternate mode",
        "settings*x": "Position detailed log Horizontal",
        "settings*x_tooltip": "Relatively damage panel.",
        "settings*y": "Position detailed log Vertical",
        "settings*y_tooltip": "Relatively damage panel.",
        "settings*align": "Alignment text:",
        "reverse": "Expand log",
        "reverse_tooltip": "Add a new line to the beginning of the story",
        "shellColor*gold": "Color of premium shells",
        "shellColor*normal": "Color of normal shells",
        "top_enabled": "Detailed history of damage inflicted",
        "bottom_enabled": "Detailed history of damage received",
    },
    "main_gun": {
        "header": "MAIN GUN",
        "x": "the horizontal Position of (center of screen)",
        "y": "the vertical Position (upper edge)",
        "progress_bar": "Progress bar"
    },
    "team_bases_panel": {
        "header": "TEAM BASES PANEL",
        "y": "The vertical position of the capture",
        "width": "Bar width in pixels.",
    },
    "players_panels": {
        "header": "Panels with a list of players (ears).",
        "players_damages_enabled": "Damage to players on team rosters.",
        "players_damages_hotkey": "Key to display damage.",
        "players_damages_settings*x": "Horizontal text position",
        "players_damages_settings*y": "Vertical text position",
        "players_bars_enabled": "HP players in the ears.",
        "players_bars_settings*players_bars_bar*outline": "Include outline.",
        "players_bars_hotkey": "HP display key",
        "players_bars_classColor": "Color the HP stripes in the ears according to the color of the technique type.",
        "players_bars_on_key_pressed": "Show stripes only on key press.",
        "panels_spotted_fix": "Correct size and position of detection status."
    },
    "zoom": {
        "header": "SNIPER MODE, ZOOM-X",
        "disable_cam_after_shot": "Disable sniper mode after the shot.",
        "disable_cam_after_shot_tooltip": "Automatically switches the camera to arcade mode after "
                                          "a shot if the caliber of the gun is more than 60mm.",
        "disable_cam_after_shot_latency": "Delay automatic shutdown of the camera.",
        "disable_cam_after_shot_skip_clip": "Do not exit if magazine loading system.",
        "dynamic_zoom*enabled": "Automatic selection of the zoom ratio when switching to sniper mode.",
        "dynamic_zoom*steps_only": "Move only in fixed steps.",
        "dynamic_zoom*enabled_tooltip": "If this option is enabled, <b>fixed zoom</b> will not work.",
        "dynamic_zoom*zoomXMeters_tooltip": "(dynamic_zoom = distance / Sensitivity of approach)<br>"
                                            "The default is every 17 meters + 1 (the smaller the number, the more zoom",
        "zoomSteps*enabled": "Enable Steps of zoom.",
        "zoomSteps*steps": "Steps of zoom.",
        "zoomSteps*steps_tooltip": "You can write any number of commas and spaces or just a comma."
    },
    "arcade_camera": {
        "header": "COMMANDER CAMERA (FAR CAMERA)",
        "max": "Maximum distance from the tank to the camera: default 25.0",
        "min": "Maximum approximation of the camera to the tank: the default 2.0",
        "startDeadDist": "The start / dead distance",
        "startDeadDist_tooltip": "The distance of the camera from the Tank at the start of the battle / "
                                 "after the destruction of the Tank: the default is 15",
        "scrollSensitivity": "Scroll sensitivity, default 4"
    },
    "strategic_camera": {
        "header": "STRATEGIC CAMERA (FAR CAMERA)",
        "max": "Maximum Camera Distance: Default is 100.0",
        "min": "Maximum approximation of the camera: Default is 40.0",
        "scrollSensitivity": "Scroll sensitivity, default 10"
    },
    "flight_time": {
        "header": "SHELLS FLIGHT TIME",
        "x": "Horizontal text position",
        "x_tooltip": "Position from the center of the screen. Align text ---|center|---",
        "y": "Vertical text position",
        "y_tooltip": "Position from the center of the screen.",
        "spgOnly": "Display flight time only for artillery.",
        "template": "A string template with values. Macro: %(flightTime).1f , %(distance).1f",
        "align": "Text align."
    },
    "minimap": {
        "header": "MINIMAP",
        "zoom": "Enable minimap centered on key down.",
        "permanentMinimapDeath": "Always show the destroyed on the map",
        "showDeathNames": "Display the names of destroyed tanks",
        "real_view_radius": "Remove the limitation of the circle of vision 445m",
        "yaw_limits": "Show Hover Angles on all vehicles where they are",
        "zoom_hotkey": "Hot key for zoom."
    },
    "colors": {
        "header": "Global color settings.",
        "armor_calculator*green": "Reduced Armor: 100% Penetration",
        "armor_calculator*orange": "Reduced Armor: 50% Penetration",
        "armor_calculator*red": "Reduced Armor: 0% Penetration",
        "armor_calculator*yellow": "Reduced Armor: 50% Penetration (Colorblind Mode)",
        "armor_calculator*purple": "Reduced Armor: 0% Penetration (Colorblind Mode)",
        "global*ally": "Global color: allies",
        "global*bgColor": "Panel background color",
        "global*enemyColorBlind": "Global color: enemy is color blind",
        "global*enemy": "Global color: enemy",
        "vehicle_types_colors*AT-SPG": "AT-SPG",
        "vehicle_types_colors*SPG": "Artillery",
        "vehicle_types_colors*heavyTank": "Heavy Tank",
        "vehicle_types_colors*lightTank": "Light Tank",
        "vehicle_types_colors*mediumTank": "Medium Tank",
        "vehicle_types_colors*unknown": "Unknown (GM)"
    },
    "service_channel_filter": {
        "header": "MESSAGE FILTER IN THE SYSTEM CHANNEL - (hides messages of selected categories)",
        "sys_keys*CustomizationForCredits": "Customization for Credits.",
        "sys_keys*CustomizationForGold": "Customization for Gold.",
        "sys_keys*DismantlingForCredits": "Dismantling for Credits.",
        "sys_keys*DismantlingForCrystal": "Dismantling for Bonds.",
        "sys_keys*DismantlingForGold": "Dismantling for Gold.",
        "sys_keys*GameGreeting": "Game greeting.",
        "sys_keys*Information": "Informational messages.",
        "sys_keys*MultipleSelling": "Multiple Selling",
        "sys_keys*PowerLevel": "Research modules and equipment",
        "sys_keys*PurchaseForCredits": "PURCHASES FOR CREDITS.",
        "sys_keys*PurchaseForCrystal": "PURCHASES FOR BONDS.",
        "sys_keys*PurchaseForGold": "PURCHASES FOR GOLD.",
        "sys_keys*Remove": "Remove",
        "sys_keys*Repair": "Repair",
        "sys_keys*Restore": "Restore",
        "sys_keys*Selling": "Selling",
        "sys_keys*autoMaintenance": "Auto-Maintenance.",
        "sys_keys*customizationChanged": "Customization Change"
    },
    "service": {
        "name": "Battle Observer - v{}",
        "description": "Battle Observer settings",
        "windowTitle": "Battle Observer settings - v{}",
        "buttonOK": "OK",
        "buttonCancel": "Cancel",
        "buttonApply": "Apply",
        "enableButtonTooltip": "{HEADER}ON/OFF{/HEADER}{BODY}Enable/Disable module{/BODY}"
    },
    "sixth_sense": {
        "header": "Sixth sense.",
        "lampShowTime": "Timer sec.",
        "playTickSound": "Play tick sound.",
        "default_icon": "Use embedded image.",
        "default_icon_name": "Select an embedded image.",
        "default_icon_tooltip": "The image built into the mod will be used instead of the custom one.",
    },
    "distance_to_enemy": {
        "header": "Distance to the closest spotted enemy.",
        "x": "Horizontal text position",
        "x_tooltip": "Position from the center of the screen. Align text ---|center|---",
        "y": "Vertical text position",
        "y_tooltip": "Position from the center of the screen.",
        "template": "String pattern. Macros: %(distance)s, %(name)s",
        "align": "Text align."
    },
    "own_health": {
        "header": "Player vehicle health.",
        "x": "Horizontal text position",
        "x_tooltip": "Position from the center of the screen.",
        "y": "Vertical text position",
        "y_tooltip": "Position from the center of the screen.",
    },
    "crewDialog": {
        "enable": "<br>Enable accelerated crew training?",
        "disable": "<br>Disable accelerated crew training?",
        "notAvailable": "Field upgrades are not available for this vehicle.",
        "isFullXp": "You have accumulated the necessary amount of experience to fully upgrade the field upgrade.",
        "isFullComplete": "You have pumped the field upgrade to the highest possible level.",
        "needTurnOff": "You do not have field upgrades, it is recommended to disable accelerated crew training."
    },
    "excludedMaps": {
        "header": "Excluded Maps",
        "message": "You have %s available slots for maps to exclude.\nProceed to the maps exclusion list?"
    },
    "avg_efficiency_in_hangar": {
        "header": "Tuning the tank stats widget in the garage",
        "avg_damage": "Display average damage dealt",
        "avg_assist": "Display average damage done with your assistance",
        "avg_blocked": "Display average armor blocked damage",
        "avg_stun": "Display average damage to targets whose crews you have stunned (SPG)",
        "gun_marks": "Display gun mark percentage",
        "win_rate": "Show win percentage",
    }
}

# coding=utf-8

timeFormat_tooltip = (
    "Directive Meaning\n"
    "%a - Locale’s abbreviated weekday name.\n"
    "%A - Locale’s full weekday name.\n"
    "%b - Locale’s abbreviated month name.\n"
    "%B - Locale’s full month name.\n"
    "%c - Locale’s appropriate date and time representation.\n"
    "%d - Day of the month as a decimal number [01,31].\n"
    "%H - Hour (24-hour clock) as a decimal number [00,23].\n"
    "%I - Hour (12-hour clock) as a decimal number [01,12].\n"
    "%j - Day of the year as a decimal number [001,366].\n"
    "%m - Month as a decimal number [01,12].\n"
    "%M - Minute as a decimal number [00,59].\n"
    "%p - Locale’s equivalent of either AM or PM.\n"
    "%S - Second as a decimal number [00,61].\n"
    "%U - Week number of the year (Sunday as the first day of the week) as a decimal number [00,53].\n"
    "%w - Weekday as a decimal number [0(Sunday),6].\n"
    "%W - Week number of the year (Monday as the first day of the week) as a decimal number [00,53].\n"
    "%x - Locale’s appropriate date representation.\n"
    "%X - Locale’s appropriate time representation.\n"
    "%y - Year without century as a decimal number [00,99].\n"
    "%Y - Year with century as a decimal number.\n"
    "%Z - Time zone name (no characters if no time zone exists).\n"
    "%% - A literal '%' character."
)

RESTART_TOOLTIP = "To enable / disable you need to restart the game."

localization = {
    "configSelect": {
        "header": "SELECT CONFIG from mods/configs/mod_battle_observer",
        "selector": "Config",
        "donate_button_ua": "DONATE UA - Гривна",
        "donate_button_paypal": "DONATE PayPal",
        "donate_button_patreon": "Subscribe on Patreon",
        "discord_button": "Discord support & chat"
    },
    "main": {
        "header": "GENERAL SETTINGS",
        "DEBUG_MODE": "DEBUG_MODE",
        "hideBadges": "Disable chevrons/ribbons: in ears, on tab window, on boot screen.",
        "hideClanAbbrev": "Disable clan display: in ears, on tab window, on boot screen.",
        "showFriendsAndClanInEars": "Mark clan friends and yourself in the team lists.",
        "autoClearCache": "Clear the game cache on startup.",
        "autoClearCache_tooltip": "Cleaning the temporary files of the game in the folder "
                                  "AppData/Roaming/Wargaming.net/WorldOfTanks."
                                  "\nFolders that are modified there are not affected.",
        "smallDoubleCarousel": "Use small icons in the tank carousel.",
        "carouselRows": "number of rows of multi-row tank carousel",
        "anonymousEnableShow": "Mark as team-killer players with an anonymizer.",
        "anonymousEnableShow_tooltip": "Only if player statistics is disabled, the parameter will "
                                       "not be taken into account if statistics are enabled.",
        "useKeyPairs": "Use key pairs Alt, Ctrl, Shift",
        "anonymousNameChange": "Change Anonymous Name",
        "hide_dog_tags": "Disable display of tokens.",
        "ignore_commanders_voice": "Ignore commander voiceover.",
        "ignore_commanders_voice_tooltip": "Once enabled, the standard crew voiceover will be forcibly used. "
                                           "The parameter will replace all voiceover of bloggers, "
                                           "Chuck Norris and so on with the standard / from the voiceover mod. ",
        "disable_score_sound": "Disable score change sound",
        "premium_time": "Display exact premium time.",
        "auto_crew_training": "Uncheck / Tick Accelerated Crew Training Automatically.",
        "auto_crew_training_tooltip": "If the 'Field Upgrade' is available for the tank and is not pumped, the "
                                      "checkbox for the crew will be unchecked automatically, as soon as the level "
                                      "of progression is at its maximum, you will be prompted to turn it back on.",
        "do_not_buy_directives_for_currency_automatically": "Do not replenish directives for currency (automatically)",
        "do_not_buy_directives_for_currency_automatically_tooltip":
            "Prevent automatic replenishment of instructions for game currency if they are not in stock. "
            "It will also turn on automatic replenishment from the warehouse if they are there and you forgot to "
            "tick the box.",
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
                                "screen in the color of vehicle classes.\n"
                                "Filter strength affects brightness.\nRecommended filter strength -1.25",
        "icon_blackout": "Filter strength (brightness)",

        "panels_full_width": "Player Name Field Width - Big Ears",
        "panels_cut_width": "Player Name Field Width - Small Ears"
    },
    "dispersion_circle": {
        "header": "Real circle scatter guns (reduction)",
        "circle_enabled": "Improved crosshair.",
        "circle_use_lock_prediction": "The server crosshair sticks on target lock.",
        "circle_extraServerLap": "Display server scatter circle.",
        "circle_extraServerLap_tooltip": "Adds a second circle of server crosshair.",
        "circle_replaceOriginalCircle": "Replace Original Circle.",
        "circle_scale": "Circle size multiplier, 30-100% (0.3-1.0)",
        "circle_scale_tooltip": "It is not recommended to set the value below 65.",
        "timer_enabled": "Turn on the reduction timer.",
        "timer_position_x": "Timer position X",
        "timer_position_y": "Timer position Y",
        "timer_color": "Timer color, not yet converged.",
        "timer_done_color": "Timer / message color (full reduction).",
        "timer_align": "Text align."
    },
    "tank_carousel": {
        "header": "TANK CAROUSEL SETUP",
        "carouselRows": "Number of rows of multi-row tank carousel.",
        "carouselRows_toltip": "It works only if the multi-row carousel is enable in the client.",
        "smallDoubleCarousel": "Forcibly use small icons in tank carousel."
    },
    "effects": {
        "header": "Customize effects",
        "noShockWave": "Remove camera shaking when hit by tank.",
        "noFlashBang": "Remove red flash when taking damage.",
        "noLightEffect": "Remove flash and flame after firing.",
        "noBinoculars": "Remove the blackout in sniper mode.",
        "noSniperDynamic": "Disable dynamic camera in sniper mode."
    },
    "debug_panel": {
        "header": "PANEL PING/FPS",
        "debugText*text": "text box to format the PING / FPS",
        "debugText*text_tooltip": "HTML - YES\nmacros debug panel\n%(PING)s<tab>-Ping"
                                  "\n%(PING)s <tab>Ping"
                                  "\n%(FPS)s <tab>Current FPS"
                                  "\n%(pingColor)s <tab>PING/LAG color."
                                  "\n%(fpsColor)s <tab>FPS color",
        "debugText*x": "window Position on the X-axis",
        "debugText*y": "window Position on the Y-axis",
        "debugGraphics*enabled": "Show fps/ping graphics bars",
        "colors*fpsColor": "Color macro %(fpsColor)s",
        "colors*pingColor": "Color macro %(pingLagColor)s - No lags",
        "colors*pingLagColor": "Color macro %(pingLagColor)s - Lag",
        "debugGraphics*fpsBar*color": "FPS Bar Color",
        "debugGraphics*fpsBar*enabled": "Enable graphics for FPS",
        "debugGraphics*pingBar*color": "PING Bar Color",
        "debugGraphics*pingBar*enabled": "Enable Graphics for PING"
    },
    "battle_timer": {
        "header": "TIMER",
        "timerTemplate": "Field to format the timer",
        "timerTemplate_tooltip": "Available macros:\n %(timer)s\n %(timerColor)s\nHTML - YES",
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
        "barsWidth": "Width of strips HP",
        "differenceHP": "Show the difference between the overall health of teams",
        "showAliveCount": "Show survivors on the panel",
        "style": "Style panel HP",
        "outline*enabled": "enabled outline in normal style",
        "outline*color": "outline color.",
        "markers*enabled": "MARKERS UNDER PANEL",
        "markers*markersClassColor": "Paint icons by color of the class.",
        "markers*x": "Horizontal position from the center.",
        "markers*x_tooltip": "The position of the markers horizontally from the center of the screen.",
        "markers*y": "Vertical position from the top.",
        "markers*y_tooltip": "The position of the markers vertically from the top of the screen.",
        "markers*showMarkers_hotkey": "Key to enable/disable Markers."
    },
    "armor_calculator": {
        "header": "Penetration indicator - CALCULATOR GIVEN ARMOR",
        "position*x": "Position the main text box of the calculator Horizontally",
        "position*y": "Position the main text box of the calculator Vertically",
        "template": "Template Main text field",
        "display_on_allies": "Display on allies",
        "template_tooltip": "Macro format:% (name) data type s:d:f.\n"
                            "s-string, d-decimal, f-floating point\n\n"
                            "List of available macros:\n"
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
                                  "\nIf enabled - received is at the bottom, caused is at the top."
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
        "shellColor*gold": "configure macro %(shellColor)s - gold"
    },
    "main_gun": {
        "header": "MAIN GUN",
        "settings*x": "the horizontal Position of (center of screen)",
        "settings*y": "the vertical Position (upper edge)",
        "settings*align": "Alignment text:"
    },
    "team_bases_panel": {
        "header": "TEAM BASES PANEL",
        "y": "The vertical position of the capture",
        "scale": "Scaling capture bars.",
        "boBases": "Enable the capture bars from the mod.",
        "outline*enabled": "Enable border.",
        "outline*color": "Border color."
    },
    "vehicle_types": {
        "header": "COLOR OF CLASS ENGINE'S",
        "vehicleClassColors*AT-SPG": "AT-SPG",
        "vehicleClassColors*SPG": "Artillery",
        "vehicleClassColors*heavyTank": "Heavy Tank",
        "vehicleClassColors*lightTank": "Light Tank",
        "vehicleClassColors*mediumTank": "Medium Tank",
        "vehicleClassColors*unknown": "Unknown (GM)"
    },
    "players_panels": {
        "header": "Panels with a list of players (ears).",
        "players_damages_enabled": "Damage to players on team rosters.",
        "players_damages_hotkey": "Key to display damage.",
        "players_damages_settings*x": "Horizontal text position",
        "players_damages_settings*y": "Vertical text position",
        "players_bars_enabled": "HP players in the ears.",
        "players_bars_settings*players_bars_bar*outline*enabled": "Include outline.",
        "players_bars_settings*players_bars_bar*outline*customColor": "Custom outline color.",
        "players_bars_settings*players_bars_bar*outline*color": "Custom outline color.",
        "players_bars_settings*players_bars_bar*outline*alpha": "Outline transparency.",
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
        "dynamic_zoom*zoomXMeters": "Sensitivity of approach in meters.",
        "dynamic_zoom*zoomXMeters_tooltip": "(dynamic_zoom = distance / Sensitivity of approach)\n"
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
        "wgDistDisable": "Hide base distance in sight.",
        "align": "Text align."
    },
    "save_shoot": {
        "header": "SAVE SHOOT LITE",
        "block_on_destroyed": "Block the shot on the destroyed.",
        "msg": "A message about a successful lock is visible only to you.",
        "msg_tooltip": "This message is displayed only if the shot is blocked by an ally."
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
    "shadow_settings": {
        "header": "SETTING SHADOWS TEXT (Glow)",
        "inner": "Determines whether the glow is an internal glow.",
        "knockout": "Determines whether a knockout effect is applied to an object.",
        "blurX": "The degree of blurring horizontally.",
        "blurY": "The amount of vertical blur.",
        "alpha": "The alpha transparency value of the color.",
        "color": "Glow color.",
        "strength": "The degree of indentation or application.",
        "blurY_tooltip": "Values that are powers of 2 (i.e. 2, 4, 8, 16, and 32)"
                         " are optimized and run faster than others.",
        "blurX_tooltip": "Values that are powers of 2 (i.e. 2, 4, 8, 16, and 32)"
                         " are optimized and run faster than others.",
        "inner_tooltip": "The value 'On' indicates that the glow is internal."
                         " The value 'Off' sets the external glow (glow around the outer contour of the object).",
        "knockout_tooltip": "The value 'Enabled' makes the object's fill transparent and makes the background color"
                            " of the document visible. The default is 'Off' (no knockout effect).",
        "strength_tooltip": "The higher the value, the more saturated the color of the shadow and the stronger the "
                            "contrast between the glow and the background. "
                            "Valid values are from 0 to 255. The default is 2."
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
        "global*alpha": "Panels transparency",
        "global*alpha_tooltip": "0 - completely transparent. \n 1 - not transparent.",
        "global*bgAlpha": "Background transparency of panels",
        "global*bgAlpha_tooltip": "0 - completely transparent. \n 1 - not transparent.",
        "global*deadColor": "Destroyed",
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
        "showTimer": "Show timer.",
        "lampShowTime": "Timer sec.",
        "playTickSound": "Play tick sound."
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
        "x_tooltip": "Position from the center of the screen. Text align ---|center|---",
        "y": "Vertical text position",
        "y_tooltip": "Position from the center of the screen.",
        "template": "String pattern. Macros: %(cur_health)s, %(max_health)s, %(per_health)s",
        "align": "Text align.",
    },
    "crewDialog": {
        "enable": "Enable accelerated crew training?",
        "disable": "Disable accelerated crew training?",
        "notAvailable": "Field upgrades are not available for this vehicle.",
        "isFullXp": "You have accumulated the necessary amount of experience to fully upgrade the field upgrade.",
        "isFullComplete": "You have pumped the field upgrade to the highest possible level.",
        "needTurnOff": "You do not have field upgrades, it is recommended to disable accelerated crew training."
    },
}

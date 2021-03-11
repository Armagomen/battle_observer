# coding=utf-8
from armagomen.battle_observer.core.constants import MOD_VERSION

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
        "header": "SELECT CONFIG",
        "selectedConfig": "Config",
        "donate_button_ua": "DONATE UA - Гривна",
        "donate_button_eu": "DONATE EUR|USD|RUB",
        "support_button": "Discord support"
    },
    "main": {
        "header": "GENERAL SETTINGS",
        "hideBadges": "Disable chevrons/ribbons: in ears, on tab window, on boot screen.",
        "hideClanAbbrev": "Disable clan display: in ears, on tab window, on boot screen.",
        "hideChatInRandom": "Disable chat in random battles",
        "hideChatInRandom_tooltip": "Completely disables the chat in random battles. "
                                    "<br> Removes the chat form and everything associated with it.",
        "enableBarsAnimation": "Enable animation of all panels.",
        "showFriendsAndClanInEars": "Mark clan friends and yourself in the team lists.",
        "autoClearCache": "Clear the game cache on startup.",
        "autoClearCache_tooltip": "Cleaning the temporary files of the game in the folder "
                                  "AppData/Roaming/Wargaming.net/WorldOfTanks."
                                  "<br>Folders that are modified there are not affected.",
        "fps_enableFPSLimiter": "Enable FPS Limiter",
        "enableFPSLimiter_tooltip": "Attention, to completely turn off or on, you must restart the game.",
        "fps_maxFrameRate": "Maximum Frame Rate",
        "removeShadowInPrebattle": "Remove the blackout timer at the beginning of the battle",
        "smallDoubleCarousel": "Use small icons in the tank carousel.",
        "carouselRows": "number of rows of multi-row tank carousel",
        "anonymousEnableShow": "Show Anonymous.",
        "useKeyPairs": "Use key pairs Alt, Ctrl, Shift",
        "anonymousNameChange": "Change Anonymous Name",
        "removeHandbrake": "Disabling the hand brake for AT-SPG.",
        "hide_dog_tags": "Disable display of tokens.",
        "ignore_commanders_voice": "Ignore commander voiceover.",
        "ignore_commanders_voice_tooltip": "Once enabled, the standard crew voiceover will be forcibly used. "
                                           "The parameter will replace all voiceovers of bloggers, "
                                           "Chuck Norris and so on with the standard / from the voiceover mod. "
    },
    "dispersion_circle": {
        "header": "Real circle scatter guns (reduction)",
        "circle_enabled": "Улучшенный круг сведения.",
        "circle_extraServerLap": "Display server scatter circle.",
        "circle_extraServerLap_tooltip": "Adds a second circle of server crosshair.",
        "circle_replaceOriginalCircle": "Replace Original Circle.",
        "circle_scale": "Circle size multiplier, 1 - 100 %",
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
        "noLightEffect": "Remove the flash from a shot in sniper mode.",
        "noBinoculars": "Remove the blackout in sniper mode."
    },
    "debug_panel": {
        "header": "PANEL PING/FPS",
        "debugText*text": "text box to format the PING / FPS",
        "debugText*text_tooltip": "HTML - YES<br>macros debug panel<br>%(PING)s<tab>-Ping"
                                  "<br>%(FPS)s<tab>is the current fps"
                                  "<br>%(PingLagColor)s<tab>-color of ping/lag is configured in the color settings.",
        "debugText*x": "window Position on the X-axis",
        "debugText*y": "window Position on the Y-axis",
        "debugText*scale": "Scale debug panel",
        "debugGraphics*enabled": "Show fps/ping graphics bars",
        "colors*fpsColor": "Color macro %(fpsColor)s",
        "colors*pingColor": "Color macro %(pingLagColor)s - No lags",
        "colors*pingLagColor": "Color macro %(pingLagColor)s - Lag"
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
        "header": "CALCULATOR GIVEN ARMOR",
        "calcPosition*x": "Position the main text box of the calculator Horizontally",
        "calcPosition*y": "Position the main text box of the calculator Vertically",
        "showCalcPoints": "Show text field of the calculator.",
        "template": "Template Main text field",
        "template_tooltip": "HTML - YES<br>Macros <br>%(calcedArmor)s - reduced armor."
                            "<br>%(armor)s - armor without inclination."
                            "<br>%(piercingPower)s - penetration of the projectile with distance."
                            "<br>%(caliber)s - is the caliber of the projectile."
                            "<br>%(color)s | s:d:f | type data - color (see colors settings)"
    },
    "log_global": {
        "header": "GENERAL LOG SETTINGS",
        "logsAltmode_hotkey": "Key switch logs in the alternate mode",
        "wg_log_hide_assist": "Hide damage intelligence",
        "wg_log_hide_assist_tooltip": "Removes the damage from intelligence detailed log WG",
        "wg_log_hide_block": "Hide blocked damage",
        "wg_log_hide_block_tooltip": "Removes the blocked damage from a detailed log WG",
        "wg_log_hide_crits": "Hide critical hits",
        "wg_log_hide_crits_tooltip": "Removes critical hits from the detailed log WG",
        "wg_log_pos_fix": "Put logs into the right places.",
        "wg_log_pos_fix_tooltip": "Switches positions of caused damage and received damage logs."
                                  "<br>If enabled - received is at the bottom, caused is at the top."
    },
    "log_total": {
        "header": "TOTAL LOG OF THE EFFECTIVENESS OF THE PLAYER",
        "settings*inCenter": "Display the log in the middle of the screen",
        "settings*background": "Enable background substrate log (only when it is in the center)",
        "settings*x": "the Position of the main log Horizontal",
        "settings*y": "the Position of the main log Vertical",
        "settings*align": "Alignment text:",
        "mainLogScale": "Scaling functions."
    },
    "log_damage_extended": {
        "header": "A DETAILED LOG OF THE DAMAGE",
        "settings*x": "Position detailed log Horizontal",
        "settings*x_tooltip": "Relative to the players list.",
        "settings*y": "Position detailed log Vertical",
        "settings*y_tooltip": "Relative to the players list.",
        "settings*align": "Alignment text:",
        "reverse": "Expand log"
    },
    "log_input_extended": {
        "header": "DETAILED LOG OF THE DAMAGE RECEIVED",
        "log_input_extended_shellColor*normal": "configure macro %(shellColor)s - Silver",
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
        "mainGunDoneIcon": "configure macro %(mainGunDoneIcon)s",
        "mainGunDynamic": "Dynamic calc. of the damage up to receive the medal 'Main Gun'",
        "mainGunFailureIcon": "configure macro %(mainGunFailureIcon)s",
        "mainGunIcon": "configure macro %(mainGunIcon)s",
        "settings*x": "the horizontal Position of (center of screen)",
        "settings*y": "the vertical Position (upper edge)",
        "settings*align": "Alignment text:"
    },
    "team_bases_panel": {
        "header": "TEAM BASES PANEL",
        "y": "The vertical position of the capture",
        "scale": "Scaling capture bars.",
        "boBases": "Enable the capture bars from the mod.",
        "colors*green": "Allies",
        "colors*bgColor": "background color",
        "colors*red": "Enemy",
        "colors*purple": "Enemy c/b",
        "colors*alpha": "Primary band, transparency.",
        "colors*alpha_tooltip": "0 - completely transparent.<br>1 - not transparent.",
        "colors*bgAlpha": "Background band, transparency",
        "colors*bgAlpha_tooltip": "0 - completely transparent.<br>1 - not transparent.",
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
        "panels_icon_enabled": "Repaint tank icons.",
        "panels_icon_enabled_tooltip": "This function repaints any vehicle icons in the ears in the color of vehicle "
                                       "classes. <br> The slider below affects the brightness. <br> Recommended "
                                       "filter strength -1.25",
        "panels_icon_filter_strength": "Filter strength (brightness)",
        "panels_spotted_fix": "Correct size and position of detection status."
    },
    "zoom": {
        "header": "SNIPER MODE, ZOOM-X",
        "disable_cam_after_shoot": "Disable sniper mode after the shot.",
        "disable_SniperCamera_After_Shoot_tooltip": "Automatically switches the camera to arcade mode after "
                                                    "a shot if the caliber of the gun is more than 40mm.",
        "disable_cam_skip_clip": "Do not exit if magazine loading system.",
        "dynamic_zoom*enabled": "Automatic selection of the zoom ratio when switching to sniper mode.",
        "dynamic_zoom*enabled_tooltip": "If this option is enabled, <b>fixed zoom</b> will not work.",
        "dynamic_zoom*zoomToGunMarker": "Enable the approximation of the camera to the Central marker information",
        "dynamic_zoom*zoomXMeters": "Sensitivity of approach in meters.",
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
                                 "after the destruction of the Tank: the default is 15"
    },
    "strategic_camera": {
        "header": "STRATEGIC CAMERA (FAR CAMERA)",
        "max": "Maximum Camera Distance: Default is 100.0",
        "min": "Maximum approximation of the camera: Default is 40.0"
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
        "aliveOnly": "Block the shot on the destroyed.",
        "msg": "A message about a successful lock is visible only to you.",
        "msg_tooltip": "This message is displayed only if the shot is blocked by an ally."
    },
    "minimap": {
        "header": "MINIMAP",
        "zoom*enabled": "Enable minimap centered.",
        "zoom*zoom_hotkey": "Centering mini map on",
        "zoom*indent": "Indenting from the edges of the screen",
        "zoom*indent_tooltip": "It is necessary to specify an indent only from the top edge, below it will be the same",
        "permanentMinimapDeath": "Always show the destroyed on the map",
        "showDeathNames": "Display the names of destroyed tanks."
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
        "main_gun*mainGunColor": "Main caliber: Macro color% (mainGunColor) s",
        "global*ally": "Global color: allies",
        "global*bgColor": "Panel background color",
        "global*enemyColorBlind": "Global color: enemy is color blind",
        "global*enemy": "Global color: enemy",
        "global*alpha": "Panels transparency",
        "global*alpha_tooltip": "0 - completely transparent. <br> 1 - not transparent.",
        "global*bgAlpha": "Background transparency of panels",
        "global*bgAlpha_tooltip": "0 - completely transparent. <br> 1 - not transparent.",
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
        "name": "Battle Observer - v{0}".format(MOD_VERSION),
        "description": "Battle Observer settings",
        "windowTitle": "Battle Observer settings - v{0}".format(MOD_VERSION),
        "buttonOK": "OK",
        "buttonCancel": "Cancel",
        "buttonApply": "Apply",
        "enableButtonTooltip": "{HEADER}ON/OFF{/HEADER}{BODY}Enable/Disable module{/BODY}"
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
                      "<b>Choose one of the following download options.</b>\n\n"
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

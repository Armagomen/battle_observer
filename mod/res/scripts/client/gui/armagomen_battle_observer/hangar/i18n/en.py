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
        "header": "SELECT CONFIG",
        "selectedConfig": "Config",
        "donate_button_ua": "DONATE UA - Гривна",
        "donate_button_ru": "DONATE RU - Рубль",
        "support_button": "Discord support",
        "donate_button_alerts": "Donation Alerts"
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
        "backgroundTransparency": "the Transparency of the background panel",
        "background": "the background panel in the style of 'normal'",
        "fps_enableFPSLimiter": "Enable FPS Limiter",
        "enableFPSLimiter_tooltip": "Attention, to completely turn off or on, you must restart the game.",
        "fps_maxFrameRate": "Maximum Frame Rate",
        "removeShadowInPrebattle": "Remove the blackout timer at the beginning of the battle",
        "smallDoubleCarousel": "Use small icons in the tank carousel.",
        "carouselRows": "number of rows of multi-row tank carousel",
        "anonymousEnableShow": "Show Anonymous.",
        "useKeyPairs": "Use key pairs Alt, Ctrl, Shift",
        "anonymousNameChange": "Сhange Anonymous Name",
        "removeHandbrake": "Disabling the hand brake for AT-SPG."
    },
    "dispersion_circle": {
        "header": "Real circle scatter guns",
        "asExtraServerLap": "Display server scatter circle.",
        "replaceOriginalCircle": "Replace Original Circle.",
        "circle_scale": "Множитель размера круга, 1 - 100 %",
        "timer_enabled": "Включить таймер сведения.",
        "timer_position_x": "Позиция таймера X",
        "timer_position_y": "Позиция таймера Y",
        "timer_color": "Цвет таймера еще не свелся.",
        "timer_done_color": "Цвет таймера/сообщения (полное сведение)."
    },
    "tank_carousel": {
        "header": "TANK CAROUSEL SETUP",
        "carouselRows": "Number of rows of multi-row tank carousel.",
        "carouselRows_toltip": "It works only if the multi-row carousel is enable in the client.",
        "smallDoubleCarousel": "Forcibly use small icons in tank carousel."
    },
    "postmortem_panel": {
        "header": "POSTMORTEM PANEL",
        "hideKillerInfo": "Remove information destroyed."
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
        "bars_colors": "color settings main panel",
        "colors*ally": "Stripe HP and difference: allies",
        "colors*bgColor": "Stripe HP background color",
        "colors*enemyColorBlind": "Stripe HP and difference: the opponent - color blindness",
        "colors*enemy": "Stripe HP and difference: the enemy",
        "colors*alpha": "Transparency of the main HP strips.",
        "colors*alpha_tooltip": "0 - fully transparent.<br>1 - not transparent.",
        "colors*bgAlpha": "Background HP-Bars transparency",
        "colors*bgAlpha_tooltip": "0 - fully transparent.<br>1 - not transparent.",
        "outline*enabled": "enabled outline in normal style",
        "outline*color": "outline color."
    },
    "markers": {
        "header": "MARKERS UNDER PANEL",
        "markersClassColor": "Paint icons by color of the class.",
        "x": "Horizontal position from the center.",
        "x_tooltip": "The position of the markers horizontally from the center of the screen.",
        "y": "Vertical position from the top.",
        "y_tooltip": "The position of the markers vertically from the top of the screen.",
        "showMarkers_KEY": "Key to enable/disable Markers."
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
                            "<br>%(color)s | s:d:f | type data - clor (see colors settings)"
    },
    "log_global": {
        "header": "GENERAL LOG SETTINGS",
        "attackReas": "configure macro %(attackReason)s",
        "attackReason*drowning": "drowning",
        "attackReason*fire": "FIRE",
        "attackReason*overturn": "overturn",
        "attackReason*ramming": "ramming",
        "attackReason*shot": "SHOT",
        "attackReason*world_collision": "FALL",
        "logsAltmode_KEY": "Key switch logs in the alternate mode",
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
    "players_spotted": {
        "header": "INDICATORS OF LIGHT IN THE EARS",
        "settings*align": "Alignment text:",
        "settings*x": "Position relative to the icon. Horizontal",
        "settings*y": "Position relative to the icon. Vertical",
        "status*donotlight": "Lost from sight",
        "status*lights": "Lights at the moment"
    },
    "players_damages": {
        "header": "DAMAGE ON THE PANELS",
        "damages_settings*align": "Alignment text:",
        "damages_KEY": "Key to display the damages.",
        "damages_settings*x": "text Position horizontally",
        "damages_settings*y": "text Position vertical",
        "damages_text": "Text box to format increased damage. the macro %(damage)s | s:d:f | type data"
    },
    "players_bars": {
        "header": "PLAYERS HEALTH IN THE PANEL",
        "bar_settings*bar*height": "The height of the strips",
        "bar_settings*bar*width": "The width of the strips",
        "bar_settings*bar*x": "Horizontal position",
        "bar_settings*bar*y": "Vertical position",
        "bar_settings*bar*colors*ally": "HP Strip: Allies",
        "bar_settings*bar*colors*bgColor": "HP Strip: background color",
        "bar_settings*bar*colors*enemy": "HP Strip: Enemy",
        "bar_settings*bar*colors*enemyBlind": "HP Strip: the enemy is color blindness",
        "bar_settings*bar*colors*alpha": "Transparency of the main bands HP.",
        "bar_settings*bar*colors*alpha_tooltip": "0 - completely transparent.<br>1 - not transparent.",
        "bar_settings*bar*colors*bgAlpha": "Background bandwidth HP, transparency",
        "bar_settings*bar*colors*bgAlpha_tooltip": "0 - completely transparent.<br>1 - not transparent.",
        "bar_settings*bar*outline*enabled": "Enable border.",
        "bar_settings*bar*outline*customColor": "Custom border color.",
        "bar_settings*bar*outline*color": "Custom color.",
        "bar_settings*bar*outline*alpha": "Transparency of the fringing.",
        "bar_settings*text*x": "text Position horizontally",
        "bar_settings*text*y": "text Position vertical",
        "bar_settings*text*align": "Alignment text:",
        "hp_text": "Template text box HP tank",
        "hp_text_tooltip": "macroses: <br> %(health)s | s:d:f | type data <br> %(maxHealth)s | s:d:f | type data "
                           "<br> %(percent)s | s:d:f | type data.",
        "hpbarsShow_KEY": "The bar display button",
        "hpbarsclassColor": "Paint strip HP in the ears by color type of technology.",
        "showHpBarsOnKeyDown": "Show the band only pressed."
    },
    "panels_icon": {
        "header": "COLOR FILTERS FOR THE ICONS IN THE EARS",
        "icon_info": "This function recolors any icons of technology in the ears in the color classes of technology."
                     "<br>The slider below affects the brightness.<br>Recommended filter force 1",
        "blackout": "Filter force (brightness)"
    },
    "zoom": {
        "header": "SNIPER MODE, ZOOM-X",
        "disable_cam_after_shoot": "Disable sniper mode after the shot.",
        "disable_SniperCamera_After_Shoot_tooltip": "Automatically switches the camera to arcade mode after "
                                                    "a shot if the caliber of the gun is more than 40mm.",
        "disable_cam_skip_clip": "Do not exit if magazine loading system.",
        "default_zoom*zoom_default": "Multiplicity of fixed zoom.",
        "default_zoom*enabled": "Use only fixed zoom",
        "dynamic_zoom*enabled": "Automatic selection of the zoom ratio when switching to sniper mode.",
        "dynamic_zoom*enabled_tooltip": "If this option is enabled, <b>fixed zoom</b> will not work.",
        "dynamic_zoom*zoom_max": "Maximum zoom ratio for automatic selection",
        "dynamic_zoom*zoom_min": "Minimum zoom ratio for automatic selection",
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
        "wgDistDisable": "Hide base distance in sight."
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
        "zoom*zoom_KEY": "Centering mini map on",
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
        "header": "COLOR SETTINGS",
        "armor_calculator*green": "Penetration 100%",
        "armor_calculator*orange": "breaking the 50%",
        "armor_calculator*red": "the Break of 0%",
        "armor_calculator*yellow": "breaking the 50% (color blindness)",
        "armor_calculator*purple": "the Break of 0% (color blindness)",
        "calculator_colors": "Color of the counter of data reduced armor",
        "colorAvg_colors": "Color boundaries for the %(tankDamageAvgColor)s",
        "main_gun*mainGunColor": "Color macro %(mainGunColor)s",
        "mark_colors": "Color icons under the panel",
        "markers*ally": "Ally",
        "markers*deadColor": "Destroyed.",
        "markers*enemyColorBlind": "Enemy, color blindness",
        "markers*enemy": "Enemy"
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

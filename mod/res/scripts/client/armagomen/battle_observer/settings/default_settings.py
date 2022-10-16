# coding=utf-8
from collections import defaultdict, namedtuple

import Keys
from Event import SafeEvent
from armagomen.constants import (
    ARCADE, ARMOR_CALC, BATTLE_TIMER, CAROUSEL, CLOCK, COLORS, DAMAGE_LOG, DEBUG_PANEL,
    DISPERSION, EFFECTS, FLIGHT_TIME, GLOBAL, HP_BARS, MAIN, MAIN_GUN, MARKERS,
    MINIMAP, PANELS, SAVE_SHOOT, SERVICE_CHANNEL, SIXTH_SENSE, SNIPER, STRATEGIC,
    TEAM_BASES, VEHICLE_TYPES, DISTANCE, OWN_HEALTH, STATISTICS,
)
from constants import ATTACK_REASON, ATTACK_REASONS, SHELL_TYPES_LIST
from gui.shared.gui_items.Vehicle import VEHICLE_CLASS_NAME


class DefaultSettings(object):

    def __init__(self):
        self.onModSettingsChanged = SafeEvent()
        self.onUserConfigUpdateComplete = SafeEvent()

        self.main = {
            MAIN.SHOW_FRIENDS: False,
            MAIN.SHOW_ANONYMOUS: False,
            MAIN.CHANGE_ANONYMOUS_NAME: False,
            MAIN.ANONYMOUS_STRING: "Anonymous",
            MAIN.HIDE_BADGES: False,
            MAIN.HIDE_CLAN_ABBREV: False,
            MAIN.ENABLE_FPS_LIMITER: False,
            MAIN.MAX_FRAME_RATE: 200,
            MAIN.AUTO_CLEAR_CACHE: False,
            MAIN.USE_KEY_PAIRS: False,
            MAIN.IGNORE_COMMANDERS: False,
            MAIN.HIDE_DOG_TAGS: False,
            MAIN.DISABLE_SCORE_SOUND: False,
            MAIN.DEBUG: False,
            MAIN.PREMIUM_TIME: True,
            MAIN.CREW_TRAINING: True,
            MAIN.DIRECTIVES: True,
            MAIN.HIDE_HINT: False,
            MAIN.FIELD_MAIL: False,
            MAIN.CREW_RETURN: False,
            MAIN.STUN_SOUND: False,
            MAIN.HIDE_MAIN_CHAT: False,
            MAIN.HIDE_BTN_COUNTERS: False
        }
        self.tank_carousel = {
            GLOBAL.ENABLED: False,
            CAROUSEL.SMALL: False,
            CAROUSEL.ROWS: 2
        }
        self.clock = {
            GLOBAL.ENABLED: False,
            CLOCK.IN_LOBBY: {
                GLOBAL.ENABLED: False,
                CLOCK.FORMAT: CLOCK.DEFAULT_FORMAT_HANGAR,
                GLOBAL.X: -240,
                GLOBAL.Y: GLOBAL.ZERO
            },
            CLOCK.IN_BATTLE: {
                GLOBAL.ENABLED: False,
                CLOCK.FORMAT: CLOCK.DEFAULT_FORMAT_BATTLE,
                GLOBAL.X: -270,
                GLOBAL.Y: GLOBAL.ZERO
            }
        }
        self.sixth_sense = {
            GLOBAL.ENABLED: False,
            SIXTH_SENSE.SHOW_TIMER: True,
            SIXTH_SENSE.PLAY_TICK_SOUND: False,
            SIXTH_SENSE.TIME: 12,
            SIXTH_SENSE.TIMER: {
                GLOBAL.X: -1,
                GLOBAL.Y: 125,
                SIXTH_SENSE.TEMPLATE: "<font size='34' color='#fafafa'><b>%(timeLeft)d</b></font>",
                GLOBAL.ALPHA: 0.9
            },
            SIXTH_SENSE.IMAGE: {
                GLOBAL.SMOOTHING: True,
                GLOBAL.X: GLOBAL.ZERO,
                GLOBAL.Y: 100,
                GLOBAL.ALPHA: 0.85,
                GLOBAL.SCALE: 0.6,
                GLOBAL.IMG: "mods/configs/mod_battle_observer/armagomen/SixthSenseIcon.png"
            }
        }
        self.dispersion_circle = {
            GLOBAL.ENABLED: False,
            DISPERSION.ENABLED: False,
            DISPERSION.CIRCLE_EXTRA_LAP: False,
            DISPERSION.CIRCLE_REPLACE: False,
            DISPERSION.CIRCLE_SCALE_CONFIG: DISPERSION.SCALE,
            DISPERSION.TIMER_ENABLED: False,
            DISPERSION.TIMER_POSITION_X: 110,
            DISPERSION.TIMER_POSITION_Y: GLOBAL.ZERO,
            DISPERSION.TIMER_ALIGN: GLOBAL.ALIGN_LIST.left,
            DISPERSION.TIMER_COLOR: "#f5ff8f",
            DISPERSION.TIMER_DONE_COLOR: "#a6ffa6",
            DISPERSION.TIMER_REGULAR_TEMPLATE: "<font color='%(color)s'>%(timer).1fs. - %(percent)d%%</font>",
            DISPERSION.TIMER_DONE_TEMPLATE: "<font color='%(color_done)s'>reduced - %(percent)d%%</font>"
        }
        self.debug_panel = {
            GLOBAL.ENABLED: False,
            DEBUG_PANEL.TEXT: {
                GLOBAL.X: 5,
                GLOBAL.Y: GLOBAL.ZERO,
                DEBUG_PANEL.TEMPLATE: ("<textformat tabstops='[75]'>FPS <font color='#E0E06D'><b>%(FPS)d</b></font>"
                                       "<tab>PING <font color='%(PingLagColor)s'><b>%(PING)d</b></font></textformat>")
            },
            DEBUG_PANEL.GRAPHICS: {
                GLOBAL.ENABLED: False,
                DEBUG_PANEL.PING_BAR: {
                    GLOBAL.ENABLED: False,
                    GLOBAL.X: 83,
                    GLOBAL.Y: 27,
                    GLOBAL.WIDTH: 75,
                    GLOBAL.HEIGHT: 4,
                    GLOBAL.ALPHA: 0.95,
                    GLOBAL.BG_ALPHA: 0.5,
                    GLOBAL.COLOR: COLORS.NORMAL_TEXT,
                    GLOBAL.GLOW_FILTER: {
                        GLOBAL.COLOR: COLORS.GREEN,
                        GLOBAL.ALPHA: 1.0,
                        GLOBAL.BLUR_X: 4,
                        GLOBAL.BLUR_Y: 4,
                        GLOBAL.INNER: False,
                        GLOBAL.KNOCKOUT: False,
                        GLOBAL.STRENGTH: 2
                    }
                },
                DEBUG_PANEL.FPS_BAR: {
                    GLOBAL.ENABLED: False,
                    GLOBAL.X: 3,
                    GLOBAL.Y: 27,
                    GLOBAL.WIDTH: 70,
                    GLOBAL.HEIGHT: 4,
                    GLOBAL.ALPHA: 0.95,
                    GLOBAL.BG_ALPHA: 0.5,
                    GLOBAL.COLOR: COLORS.NORMAL_TEXT,
                    GLOBAL.GLOW_FILTER: {
                        GLOBAL.COLOR: COLORS.GREEN,
                        GLOBAL.ALPHA: 1.0,
                        GLOBAL.BLUR_X: 4,
                        GLOBAL.BLUR_Y: 4,
                        GLOBAL.INNER: False,
                        GLOBAL.KNOCKOUT: False,
                        GLOBAL.STRENGTH: 2
                    }
                }
            },
            COLORS.NAME: {
                DEBUG_PANEL.FPS_COLOR: COLORS.S_YELLOW,
                DEBUG_PANEL.PING_COLOR: COLORS.S_YELLOW,
                DEBUG_PANEL.LAG_COLOR: COLORS.RED
            }
        }
        self.battle_timer = {
            GLOBAL.ENABLED: False,
            BATTLE_TIMER.TEMPLATE: "<font color='%(timerColor)s'>%(timer)s</font>",
            BATTLE_TIMER.COLOR: COLORS.S_YELLOW,
            BATTLE_TIMER.END_COLOR: COLORS.RED
        }
        self.effects = {
            EFFECTS.NO_FLASH_BANG: False,
            EFFECTS.NO_SHOCK_WAVE: False,
            EFFECTS.NO_BINOCULARS: False,
            EFFECTS.NO_SNIPER_DYNAMIC: False,
        }
        self.zoom = {
            GLOBAL.ENABLED: False,
            SNIPER.DISABLE_SNIPER: False,
            SNIPER.DISABLE_LATENCY: 0.5,
            SNIPER.SKIP_CLIP: True,
            SNIPER.DYN_ZOOM: {
                GLOBAL.ENABLED: False,
                SNIPER.STEPS_ONLY: True,
                SNIPER.METERS: 20.0
            },
            SNIPER.ZOOM_STEPS: {
                GLOBAL.ENABLED: False,
                SNIPER.STEPS: SNIPER.DEFAULT_STEPS
            }
        }
        self.arcade_camera = {
            GLOBAL.ENABLED: False,
            ARCADE.MIN: 4.0,
            ARCADE.MAX: 150.0,
            ARCADE.START_DEAD_DIST: 20.0,
            ARCADE.SCROLL_SENSITIVITY: 4.0,
        }
        self.strategic_camera = {
            GLOBAL.ENABLED: False,
            STRATEGIC.MIN: 40.0,
            STRATEGIC.MAX: 150.0,
            STRATEGIC.SCROLL_SENSITIVITY: 10.0,
        }
        self.armor_calculator = {
            GLOBAL.ENABLED: False,
            ARMOR_CALC.POSITION: {GLOBAL.X: GLOBAL.ZERO, GLOBAL.Y: 30},
            ARMOR_CALC.TEMPLATE: ARMOR_CALC.DEFAULT_TEMPLATE,
            ARMOR_CALC.MESSAGES: ARMOR_CALC.MESSAGES_TEMPLATE,
            ARMOR_CALC.RICOCHET: ARMOR_CALC.RICOCHET_MESSAGE,
            ARMOR_CALC.NO_DAMAGE: ARMOR_CALC.NO_DAMAGE_MESSAGE,
            ARMOR_CALC.ON_ALLY: False,
        }
        self.colors = {
            COLORS.GLOBAL: {
                COLORS.ALLY_MAME: COLORS.GREEN,
                COLORS.ENEMY_MAME: COLORS.RED,
                COLORS.ENEMY_BLIND_MAME: COLORS.BLIND,
                COLORS.C_BG: COLORS.BLACK,
                COLORS.DEAD_COLOR: COLORS.B_SILVER,
                GLOBAL.ALPHA: 0.4,
                GLOBAL.BG_ALPHA: 0.4
            },
            ARMOR_CALC.NAME: {
                COLORS.C_GREEN: COLORS.GREEN,
                COLORS.C_ORANGE: COLORS.ORANGE,
                COLORS.C_RED: COLORS.RED,
                COLORS.C_YELLOW: COLORS.YELLOW,
                COLORS.C_PURPLE: COLORS.BLIND
            }
        }
        self.log_global = {
            DAMAGE_LOG.WG_POS: False,
            DAMAGE_LOG.WG_CRITICS: False,
            DAMAGE_LOG.WG_BLOCKED: False,
            DAMAGE_LOG.WG_ASSIST: False,
            DAMAGE_LOG.HOT_KEY: [[Keys.KEY_LALT]],
            DAMAGE_LOG.ATTACK_REASON: defaultdict(lambda: "", {
                ATTACK_REASON.SHOT: "<img src='{dir}/damage.png' {size} {vspace}>".format(**GLOBAL.IMG_PARAMS),
                ATTACK_REASON.FIRE: "<img src='{dir}/fire.png' {size} {vspace}>".format(**GLOBAL.IMG_PARAMS),
                ATTACK_REASON.RAM: "<img src='{dir}/ram.png' {size} {vspace}>".format(**GLOBAL.IMG_PARAMS),
                ATTACK_REASON.WORLD_COLLISION: "<img src='{dir}/ram.png' {size} {vspace}>".format(**GLOBAL.IMG_PARAMS)
            })
        }
        additional = {reason: "<img src='{dir}/module.png' {size} {vspace}>".format(**GLOBAL.IMG_PARAMS) for reason
                      in ATTACK_REASONS if reason not in self.log_global[DAMAGE_LOG.ATTACK_REASON]}
        self.log_global[DAMAGE_LOG.ATTACK_REASON].update(additional)
        self.log_total = {
            GLOBAL.ENABLED: False,
            GLOBAL.SETTINGS: {
                GLOBAL.X: -255,
                GLOBAL.Y: GLOBAL.ZERO,
                GLOBAL.ALIGN: GLOBAL.ALIGN_LIST.right,
                DAMAGE_LOG.IN_CENTER: True
            },
            DAMAGE_LOG.TEMPLATE_MAIN_DMG: ("<textformat leading='-3'>%(damageIcon)s"
                                           "<font color='%(tankDamageAvgColor)s'>%(playerDamage)s</font>"
                                           "%(blockedIcon)s%(blockedDamage)s%(assistIcon)s%(assistDamage)s"
                                           "%(spottedIcon)s%(spottedTanks)s%(stunIcon)s%(stun)s</textformat>"),
            DAMAGE_LOG.ICONS: {
                "assistIcon": "<img src='{dir}/help.png' {size} vspace='-10'>".format(**GLOBAL.IMG_PARAMS),
                "blockedIcon": "<img src='{dir}/armor.png' {size} vspace='-9'>".format(**GLOBAL.IMG_PARAMS),
                "damageIcon": "<img src='{dir}/damage.png' {size} vspace='-10'>".format(**GLOBAL.IMG_PARAMS),
                "spottedIcon": "<img src='{dir}/detection.png' {size} vspace='-10'>".format(**GLOBAL.IMG_PARAMS),
                "stunIcon": "<img src='{dir}/stun.png' {size} vspace='-10'>".format(**GLOBAL.IMG_PARAMS)
            },
            GLOBAL.AVG_COLOR: {"saturation": 0.5, "brightness": 1.0}
        }
        shellTypes = defaultdict(str, **{shell_type: "" for shell_type in SHELL_TYPES_LIST})
        shellIcons = defaultdict(str, **{shell_icon: "" for shell_icon in SHELL_TYPES_LIST +
                                         DAMAGE_LOG.PREMIUM_SHELLS + ("HIGH_EXPLOSIVE_SPG_STUN", "HIGH_EXPLOSIVE_SPG")})
        self.log_damage_extended = {
            GLOBAL.ENABLED: False,
            DAMAGE_LOG.REVERSE: False,
            GLOBAL.SETTINGS: {
                GLOBAL.X: 10,
                GLOBAL.Y: GLOBAL.ZERO,
                GLOBAL.ALIGN: GLOBAL.ALIGN_LIST.left
            },
            DAMAGE_LOG.KILLED_ICON: "<img src='{dir}/destruction.png' {size} {vspace}>".format(**GLOBAL.IMG_PARAMS),
            DAMAGE_LOG.LOG_MODE[GLOBAL.FIRST]: [
                "<textformat leading='-8' tabstops='[20, 55, 80, 100]'><font face='$TitleFont' size='15'>",
                "<font size='12'>%(index)02d:</font><tab>",
                "<font color='#E0E06D'>%(totalDamage)s</font><tab>",
                "%(attackReason)s<tab>",
                "<font color='%(tankClassColor)s'>%(classIcon)s</font><tab>",
                "%(tankName)s%(killedIcon)s",
                "</font></textformat>"
            ],
            DAMAGE_LOG.LOG_MODE[GLOBAL.LAST]: [
                "<textformat leading='-8' tabstops='[20, 55, 80, 100]'><font face='$TitleFont' size='15'>",
                "<font size='12'>%(shots)d:</font><tab>",
                "<font color='#E0E06D'>%(lastDamage)s</font><tab>",
                "%(attackReason)s<tab>",
                "<font color='%(tankClassColor)s'>%(classIcon)s</font><tab>",
                "%(userName).12s %(killedIcon)s",
                "</font></textformat>"
            ],
            DAMAGE_LOG.SHELL_TYPES: shellTypes,
            DAMAGE_LOG.SHELL_ICONS: shellIcons,
            DAMAGE_LOG.SHELL_COLOR: {
                DAMAGE_LOG.NORMAL: COLORS.NORMAL_TEXT,
                DAMAGE_LOG.GOLD: COLORS.GOLD
            },
            GLOBAL.AVG_COLOR: {"saturation": 0.5, "brightness": 1.0}
        }
        self.log_input_extended = {
            GLOBAL.ENABLED: False,
            DAMAGE_LOG.REVERSE: False,
            GLOBAL.SETTINGS: {
                GLOBAL.X: 10,
                GLOBAL.Y: -20,
                GLOBAL.ALIGN: GLOBAL.ALIGN_LIST.left
            },
            DAMAGE_LOG.KILLED_ICON: "<img src='{dir}/destruction.png' {size} {vspace}>".format(**GLOBAL.IMG_PARAMS),
            DAMAGE_LOG.LOG_MODE[GLOBAL.FIRST]: [
                "<textformat leading='-8' tabstops='[20, 55, 80, 100, 125]'><font face='$TitleFont' size='15'>",
                "<font size='12'>%(index)02d:</font><tab>",
                "<font color='#E0E06D'>%(totalDamage)s</font><tab>",
                "<font color='%(shellColor)s'>%(shellType)s</font><tab>",
                "%(attackReason)s<tab>",
                "<font color='%(tankClassColor)s'>%(classIcon)s</font><tab>",
                "%(tankName)s%(killedIcon)s",
                "</font></textformat>"
            ],
            DAMAGE_LOG.LOG_MODE[GLOBAL.LAST]: [
                "<textformat leading='-8' tabstops='[20, 55, 80, 100, 125]'><font face='$TitleFont' size='15'>",
                "<font size='12'>%(shots)d:</font><tab>",
                "<font color='#E0E06D'>%(lastDamage)s</font><tab>",
                "<font color='%(shellColor)s'>%(shellType)s</font><tab>",
                "%(attackReason)s<tab>",
                "<font color='%(tankClassColor)s'>%(classIcon)s</font><tab>",
                "%(userName).12s %(killedIcon)s",
                "</font></textformat>"
            ],
            DAMAGE_LOG.SHELL_TYPES: shellTypes,
            DAMAGE_LOG.SHELL_ICONS: shellIcons,
            DAMAGE_LOG.SHELL_COLOR: {
                DAMAGE_LOG.NORMAL: COLORS.NORMAL_TEXT,
                DAMAGE_LOG.GOLD: COLORS.GOLD
            },
            GLOBAL.AVG_COLOR: {"saturation": 0.5, "brightness": 1.0}
        }
        self.hp_bars = {
            GLOBAL.ENABLED: True,
            HP_BARS.STYLE: HP_BARS.STYLES.league,
            HP_BARS.WIDTH: 200,
            HP_BARS.DIFF: True,
            HP_BARS.ALIVE: False,
            GLOBAL.OUTLINE: {
                GLOBAL.ENABLED: True,
                GLOBAL.COLOR: COLORS.NORMAL_TEXT
            },
            MARKERS.NAME: {
                GLOBAL.ENABLED: False,
                MARKERS.HOT_KEY: [Keys.KEY_NUMPAD0],
                MARKERS.CLASS_COLOR: False,
                GLOBAL.X: 5,
                GLOBAL.Y: 31
            }
        }
        self.team_bases_panel = {
            GLOBAL.ENABLED: False,
            GLOBAL.Y: 100,
            GLOBAL.WIDTH: 400,
            GLOBAL.HEIGHT: 24,
            GLOBAL.OUTLINE: {
                GLOBAL.ENABLED: True,
                GLOBAL.COLOR: COLORS.NORMAL_TEXT
            },
            TEAM_BASES.TEXT_SETTINGS: {
                TEAM_BASES.FONT: TEAM_BASES.BASE_FONT,
                TEAM_BASES.SIZE: TEAM_BASES.FONT_SIZE,
                GLOBAL.COLOR: COLORS.NORMAL_TEXT,
                TEAM_BASES.BOLD: False,
                TEAM_BASES.ITALIC: False,
                TEAM_BASES.UNDERLINE: False,
                GLOBAL.Y: GLOBAL.ZERO
            }
        }
        self.main_gun = {
            GLOBAL.ENABLED: False,
            MAIN_GUN.TEMPLATE: "%(mainGunIcon)s%(mainGunDoneIcon)s%(mainGunFailureIcon)s"
                               "<font color='%(mainGunColor)s'>%(mainGun)s</font>",
            GLOBAL.SETTINGS: {
                GLOBAL.X: 255,
                GLOBAL.Y: GLOBAL.ZERO,
                GLOBAL.ALIGN: GLOBAL.ALIGN_LIST.left
            },
            MAIN_GUN.GUN_ICON: "<img src='{}/achievement/32x32/mainGun.png' width='26' height='25'"
                               " vspace='-7'>".format(GLOBAL.ICONS_DIR),
            MAIN_GUN.DONE_ICON: "<img src='{}/library/done.png' width='24' height='24'"
                                " vspace='-8'>".format(GLOBAL.ICONS_DIR),
            MAIN_GUN.FAILURE_ICON: "<img src='{}/library/icon_alert_32x32.png' width='22' height='22'"
                                   " vspace='-6'>".format(GLOBAL.ICONS_DIR)
        }
        self.vehicle_types = {
            VEHICLE_TYPES.CLASS_COLORS: {
                VEHICLE_CLASS_NAME.HEAVY_TANK: "#FF9933",
                VEHICLE_CLASS_NAME.MEDIUM_TANK: "#FFCC00",
                VEHICLE_CLASS_NAME.AT_SPG: "#3399CC",
                VEHICLE_CLASS_NAME.SPG: "#FF3300",
                VEHICLE_CLASS_NAME.LIGHT_TANK: "#66FF00",
                VEHICLE_TYPES.UNKNOWN: COLORS.NORMAL_TEXT
            },
            VEHICLE_TYPES.CLASS_ICON: {
                VEHICLE_CLASS_NAME.AT_SPG: VEHICLE_TYPES.TEMPLATE.format("J"),
                VEHICLE_CLASS_NAME.SPG: VEHICLE_TYPES.TEMPLATE.format("S"),
                VEHICLE_CLASS_NAME.HEAVY_TANK: VEHICLE_TYPES.TEMPLATE.format("H"),
                VEHICLE_CLASS_NAME.LIGHT_TANK: VEHICLE_TYPES.TEMPLATE.format("L"),
                VEHICLE_CLASS_NAME.MEDIUM_TANK: VEHICLE_TYPES.TEMPLATE.format("M"),
                VEHICLE_TYPES.UNKNOWN: VEHICLE_TYPES.TEMPLATE.format("U")
            }
        }
        self.players_panels = {
            GLOBAL.ENABLED: False,
            PANELS.SPOTTED_FIX: True,
            PANELS.DAMAGES_ENABLED: True,
            PANELS.DAMAGES_HOT_KEY: [[Keys.KEY_LALT]],
            PANELS.DAMAGES_TEMPLATE: "<font color='#FFFF00'>%(damage)s</font>",
            PANELS.DAMAGES_SETTINGS: {GLOBAL.X: -50, GLOBAL.Y: -2, GLOBAL.ALIGN: GLOBAL.ALIGN_LIST.left},
            PANELS.BARS_ENABLED: True,
            PANELS.BAR_CLASS_COLOR: False,
            PANELS.ON_KEY_DOWN: False,
            PANELS.BAR_HOT_KEY: [[Keys.KEY_LALT]],
            PANELS.HP_TEMPLATE: "<font face='$FieldFont' color='#FAFAFA' size='15'>%(health)s</font>",
            PANELS.BAR_SETTINGS: {
                PANELS.BAR_TEXT_SETTINGS: {GLOBAL.X: 35, GLOBAL.Y: GLOBAL.ZERO, GLOBAL.ALIGN: GLOBAL.ALIGN_LIST.center},
                PANELS.BAR: {
                    GLOBAL.X: GLOBAL.ZERO,
                    GLOBAL.Y: 2,
                    GLOBAL.WIDTH: 70,
                    GLOBAL.HEIGHT: 22,
                    GLOBAL.OUTLINE: {
                        GLOBAL.ENABLED: True,
                        GLOBAL.COLOR: COLORS.NORMAL_TEXT,
                        GLOBAL.CUSTOM_COLOR: False,
                        GLOBAL.ALPHA: 0.5
                    }
                }
            }
        }
        self.flight_time = {
            GLOBAL.ENABLED: False,
            GLOBAL.X: -110,
            GLOBAL.Y: GLOBAL.ZERO,
            FLIGHT_TIME.SPG_ONLY: True,
            FLIGHT_TIME.ALIGN: GLOBAL.ALIGN_LIST.right,
            FLIGHT_TIME.TEMPLATE: "<font color='#f5ff8f'>%(flightTime).1fs. - %(distance).1f m.</font>"
        }
        self.distance_to_enemy = {
            GLOBAL.ENABLED: False,
            GLOBAL.X: GLOBAL.ZERO,
            GLOBAL.Y: -190,
            GLOBAL.ALIGN: GLOBAL.ALIGN_LIST.center,
            DISTANCE.TEMPLATE: "<font color='#f5ff8f'>%(distance).1fm. to %(name)s.</font>"
        }
        self.own_health = {
            GLOBAL.ENABLED: False,
            GLOBAL.X: GLOBAL.ZERO,
            GLOBAL.Y: 120,
            GLOBAL.WIDTH: 140,
            GLOBAL.HEIGHT: 20,
            GLOBAL.ALPHA: 0.4,
            GLOBAL.ALIGN: GLOBAL.ALIGN_LIST.center,
            OWN_HEALTH.TEMPLATE: "%(health)s/%(maxHealth)s (%(percent)s%%)",
            GLOBAL.AVG_COLOR: {"saturation": 1.0, "brightness": 1.0}
        }
        self.save_shoot = {
            GLOBAL.ENABLED: False,
            SAVE_SHOOT.DESTROYED_BLOCK: True,
            SAVE_SHOOT.MSG: SAVE_SHOOT.TEMPLATE
        }
        self.minimap = {
            GLOBAL.ENABLED: False,
            MINIMAP.DEATH_PERMANENT: False,
            MINIMAP.SHOW_NAMES: False,
            MINIMAP.VIEW_RADIUS: False,
            MINIMAP.YAW: True,
            MINIMAP.ZOOM: False,
            MINIMAP.ZOOM_KEY: [[29]]
        }
        self.shadow_settings = {
            GLOBAL.COLOR: COLORS.BLACK,
            GLOBAL.ALPHA: 0.6,
            GLOBAL.BLUR_X: 2,
            GLOBAL.BLUR_Y: 2,
            GLOBAL.INNER: False,
            GLOBAL.KNOCKOUT: False,
            GLOBAL.STRENGTH: 5
        }
        self.service_channel_filter = {
            GLOBAL.ENABLED: False,
            SERVICE_CHANNEL.KEYS: dict.fromkeys(SERVICE_CHANNEL.SYSTEM_CHANNEL_KEYS, False)
        }
        _logs = namedtuple('Logs', ('log_total', 'log_damage_extended', 'log_input_extended', 'log_global'))
        self.damage_log = _logs(self.log_total, self.log_damage_extended, self.log_input_extended, self.log_global)
        self.statistics = {
            GLOBAL.ENABLED: False,
            STATISTICS.STATISTIC_ENABLED: False,
            STATISTICS.CHANGE_VEHICLE_COLOR: False,
            STATISTICS.FULL_LEFT: "<font color='%(colorWTR)s'>%(WTR)d | %(nickname).12s</font>%(clanTag)s",
            STATISTICS.FULL_RIGHT: "%(clanTag)s<font color='%(colorWTR)s'>%(nickname).12s | %(WTR)d</font>",
            STATISTICS.CUT_LEFT: "<font color='%(colorWTR)s'>%(nickname).9s</font>",
            STATISTICS.CUT_RIGHT: "<font color='%(colorWTR)s'>%(nickname).9s</font>",
            STATISTICS.PANELS_CUT_WIDTH: 60,
            STATISTICS.PANELS_FULL_WIDTH: 150,
            STATISTICS.COLORS: {
                "very_good": "#02C9B3",
                "bad": "#FE7903",
                "normal": "#F8F400",
                "good": "#60FF00",
                "unique": "#D042F3",
                "very_bad": "#FE0E00",
            },
            STATISTICS.ICON_ENABLED: False,
            STATISTICS.ICON_BLACKOUT: -1.25,
        }


settings = DefaultSettings()

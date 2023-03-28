from collections import defaultdict, namedtuple

import Keys
from Event import SafeEvent
from armagomen.constants import (
    ARCADE, ARMOR_CALC, BATTLE_TIMER, CAROUSEL, CLOCK, COLORS, DAMAGE_LOG, DEBUG_PANEL, DISPERSION, EFFECTS,
    FLIGHT_TIME, GLOBAL, HP_BARS, MAIN, MINIMAP, PANELS, SERVICE_CHANNEL, SIXTH_SENSE,
    SNIPER, STRATEGIC, TEAM_BASES, VEHICLE_TYPES_COLORS, DISTANCE, OWN_HEALTH, STATISTICS, AVG_EFFICIENCY_HANGAR,
    DISPERSION_TIMER
)
from constants import ATTACK_REASON, ATTACK_REASONS
from gui.shared.gui_items.Vehicle import VEHICLE_CLASS_NAME


class DefaultSettings(object):

    def __init__(self):
        self.onModSettingsChanged = SafeEvent()
        self.onUserConfigUpdateComplete = SafeEvent()

        self.main = {
            MAIN.AUTO_CLEAR_CACHE: False,
            MAIN.CREW_RETURN: False,
            MAIN.CREW_TRAINING: False,
            MAIN.DEBUG: False,
            MAIN.DIRECTIVES: False,
            MAIN.DISABLE_SCORE_SOUND: False,
            MAIN.FIELD_MAIL: False,
            MAIN.HIDE_BADGES: False,
            MAIN.HIDE_BTN_COUNTERS: True,
            MAIN.HIDE_CLAN_ABBREV: False,
            MAIN.HIDE_DOG_TAGS: False,
            MAIN.HIDE_HINT: False,
            MAIN.HIDE_MAIN_CHAT: False,
            MAIN.IGNORE_COMMANDERS: False,
            MAIN.PREMIUM_TIME: True,
            MAIN.SAVE_SHOT: False,
            MAIN.SHOW_ANONYMOUS: False,
            MAIN.SHOW_FRIENDS: False,
            MAIN.STUN_SOUND: False,
            MAIN.USE_KEY_PAIRS: True,
            MAIN.MUTE_BASES_SOUND: False,
        }
        self.tank_carousel = {
            GLOBAL.ENABLED: False,
            CAROUSEL.SMALL: False,
            CAROUSEL.ROWS: 2
        }
        self.avg_efficiency_in_hangar = {
            GLOBAL.ENABLED: False,
            GLOBAL.X: 140,
            GLOBAL.Y: 0,
            "icons": {
                "assistIcon": "<img src='{dir}/help.png' {size} vspace='-10'>".format(**GLOBAL.IMG_PARAMS_HANGAR),
                "blockedIcon": "<img src='{dir}/armor.png' {size} vspace='-9'>".format(**GLOBAL.IMG_PARAMS_HANGAR),
                "damageIcon": "<img src='{dir}/damage.png' {size} vspace='-10'>".format(**GLOBAL.IMG_PARAMS_HANGAR),
                "stunIcon": "<img src='{dir}/stun.png' {size} vspace='-10'>".format(**GLOBAL.IMG_PARAMS_HANGAR)
            },
            AVG_EFFICIENCY_HANGAR.DAMAGE: True,
            AVG_EFFICIENCY_HANGAR.ASSIST: True,
            AVG_EFFICIENCY_HANGAR.BLOCKED: True,
            AVG_EFFICIENCY_HANGAR.STUN: True,
            AVG_EFFICIENCY_HANGAR.MARKS_ON_GUN: True
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
            SIXTH_SENSE.PLAY_TICK_SOUND: True,
            SIXTH_SENSE.DEFAULT: True,
            SIXTH_SENSE.ICON_NAME: SIXTH_SENSE.ICONS[GLOBAL.ZERO],
            SIXTH_SENSE.TIME: 10,
            SIXTH_SENSE.USER_ICON: "mods/configs/mod_battle_observer/__icon__path__200x200.png"
        }
        self.dispersion_circle = {
            GLOBAL.ENABLED: False,
            DISPERSION.CIRCLE_EXTRA_LAP: False,
            DISPERSION.CIRCLE_REPLACE: False,
            DISPERSION.CIRCLE_SCALE_CONFIG: DISPERSION.SCALE,
        }
        self.dispersion_timer = {
            GLOBAL.ENABLED: False,
            GLOBAL.X: 110,
            GLOBAL.Y: GLOBAL.ZERO,
            GLOBAL.ALIGN: GLOBAL.ALIGN_LIST.left,
            GLOBAL.COLOR: "#f5ff8f",
            DISPERSION_TIMER.DONE_COLOR: "#a6ffa6",
            DISPERSION_TIMER.REGULAR_TEMPLATE: "<font color='%(color)s'>%(timer).1fs. - %(percent)d%%</font>",
            DISPERSION_TIMER.DONE_TEMPLATE: "<font color='%(color_done)s'>reduced - %(percent)d%%</font>"
        }
        self.debug_panel = {
            GLOBAL.ENABLED: False,
            DEBUG_PANEL.STYLE: DEBUG_PANEL.STYLES.minimal,
            DEBUG_PANEL.FPS_COLOR: "#B3FE95",
            DEBUG_PANEL.PING_COLOR: "#B3FE95",
            DEBUG_PANEL.LAG_COLOR: "#FD9675"
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
            ARMOR_CALC.ON_ALLY: False,
        }
        self.colors = {
            COLORS.GLOBAL: {
                COLORS.ALLY_MAME: COLORS.GREEN,
                COLORS.ENEMY_MAME: COLORS.RED,
                COLORS.ENEMY_BLIND_MAME: COLORS.BLIND,
                COLORS.C_BG: COLORS.BLACK,
                GLOBAL.ALPHA: 0.5,
                GLOBAL.BG_ALPHA: 0.5
            },
            ARMOR_CALC.NAME: {
                COLORS.C_GREEN: COLORS.GREEN,
                COLORS.C_ORANGE: COLORS.ORANGE,
                COLORS.C_RED: COLORS.RED,
                COLORS.C_YELLOW: COLORS.YELLOW,
                COLORS.C_PURPLE: COLORS.BLIND
            },
            VEHICLE_TYPES_COLORS.NAME: {
                VEHICLE_CLASS_NAME.HEAVY_TANK: "#F9B200",
                VEHICLE_CLASS_NAME.MEDIUM_TANK: "#FDEF6C",
                VEHICLE_CLASS_NAME.AT_SPG: "#0094EC",
                VEHICLE_CLASS_NAME.SPG: "#A90400",
                VEHICLE_CLASS_NAME.LIGHT_TANK: "#37BC00",
                VEHICLE_TYPES_COLORS.UNKNOWN: COLORS.NORMAL_TEXT
            }
        }
        self.wg_logs = {
            GLOBAL.ENABLED: False,
            DAMAGE_LOG.WG_POS: False,
            DAMAGE_LOG.WG_CRITICS: False,
            DAMAGE_LOG.WG_BLOCKED: False,
            DAMAGE_LOG.WG_ASSIST: False,
        }
        self.log_total = {
            GLOBAL.ENABLED: False,
            GLOBAL.SETTINGS: {
                GLOBAL.X: -255,
                GLOBAL.Y: GLOBAL.ZERO,
                GLOBAL.ALIGN: GLOBAL.ALIGN_LIST.right,
                DAMAGE_LOG.IN_CENTER: True
            },
            DAMAGE_LOG.TEMPLATE_MAIN_DMG: (
                "<textformat leading='-3'>"
                "%(damageIcon)s<font color='%(tankDamageAvgColor)s'>%(playerDamage)s</font>"
                "%(blockedIcon)s<font color='%(tankBlockedAvgColor)s'>%(blockedDamage)s</font>"
                "%(assistIcon)s<font color='%(tankAssistAvgColor)s'>%(assistDamage)s</font>"
                "%(spottedIcon)s%(spottedTanks)s"
                "%(stunIcon)s<font color='%(tankStunAvgColor)s'>%(stun)s</font>"
                "</textformat>"
            ),
            DAMAGE_LOG.ICONS: {
                "assistIcon": "<img src='{dir}/help.png' {size} vspace='-10'>".format(**GLOBAL.IMG_PARAMS),
                "blockedIcon": "<img src='{dir}/armor.png' {size} vspace='-9'>".format(**GLOBAL.IMG_PARAMS),
                "damageIcon": "<img src='{dir}/damage.png' {size} vspace='-10'>".format(**GLOBAL.IMG_PARAMS),
                "spottedIcon": "<img src='{dir}/detection.png' {size} vspace='-10'>".format(**GLOBAL.IMG_PARAMS),
                "stunIcon": "<img src='{dir}/stun.png' {size} vspace='-10'>".format(**GLOBAL.IMG_PARAMS)
            },
            GLOBAL.AVG_COLOR: {"saturation": 0.5, "brightness": 1.0}
        }
        self.log_extended = {
            GLOBAL.ENABLED: False,
            DAMAGE_LOG.REVERSE: False,
            DAMAGE_LOG.D_DONE_ENABLED: True,
            DAMAGE_LOG.D_RECEIVED_ENABLED: True,
            GLOBAL.SETTINGS: {
                GLOBAL.X: 0,
                GLOBAL.Y: 0,
                GLOBAL.ALIGN: GLOBAL.ALIGN_LIST.left
            },
            DAMAGE_LOG.KILLED_ICON: "<img src='{dir}/destruction.png' {size} {vspace}>".format(**GLOBAL.IMG_PARAMS),
            DAMAGE_LOG.LOG_MODE[GLOBAL.FIRST]: [
                "<textformat leading='-8' tabstops='[20, 55, 80, 100, 125]'><font face='$TitleFont' size='15'>",
                "<font size='12'>%(index)02d:</font><tab>",
                "<font color='%(percentDamageAvgColor)s'>%(totalDamage)s</font><tab>",
                "<font color='%(shellColor)s'>%(shellType)s</font><tab>",
                "%(attackReason)s<tab>",
                "<font color='%(tankClassColor)s'>%(classIcon)s</font><tab>",
                "%(tankName)s %(killedIcon)s",
                "</font></textformat>"
            ],
            DAMAGE_LOG.LOG_MODE[GLOBAL.LAST]: [
                "<textformat leading='-8' tabstops='[20, 55, 80, 100, 125]'><font face='$TitleFont' size='15'>",
                "<font size='12'>%(shots)d:</font><tab>",
                "<font color='%(percentDamageAvgColor)s'>%(lastDamage)s</font><tab>",
                "<font color='%(shellColor)s'>%(shellType)s</font><tab>",
                "%(attackReason)s<tab>",
                "<font color='%(tankClassColor)s'>%(classIcon)s</font><tab>",
                "%(userName).12s %(killedIcon)s",
                "</font></textformat>"
            ],
            DAMAGE_LOG.SHELL_COLOR: {
                DAMAGE_LOG.NORMAL: COLORS.NORMAL_TEXT,
                DAMAGE_LOG.GOLD: COLORS.GOLD
            },
            DAMAGE_LOG.HOT_KEY: [[Keys.KEY_LALT]],
            DAMAGE_LOG.ATTACK_REASON: defaultdict(lambda: "", {
                ATTACK_REASON.SHOT: "<img src='{dir}/damage.png' {size} {vspace}>".format(**GLOBAL.IMG_PARAMS),
                ATTACK_REASON.FIRE: "<img src='{dir}/fire.png' {size} {vspace}>".format(**GLOBAL.IMG_PARAMS),
                ATTACK_REASON.RAM: "<img src='{dir}/ram.png' {size} {vspace}>".format(**GLOBAL.IMG_PARAMS),
                ATTACK_REASON.WORLD_COLLISION: "<img src='{dir}/ram.png' {size} {vspace}>".format(**GLOBAL.IMG_PARAMS)
            }),
            GLOBAL.AVG_COLOR: {"saturation": 0.5, "brightness": 1.0}
        }
        additional = {reason: "<img src='{dir}/module.png' {size} {vspace}>".format(**GLOBAL.IMG_PARAMS) for reason
                      in ATTACK_REASONS if reason not in self.log_extended[DAMAGE_LOG.ATTACK_REASON]}
        self.log_extended[DAMAGE_LOG.ATTACK_REASON].update(additional)
        _logs = namedtuple('Logs', ('log_total', 'log_extended'))
        self.damage_log = _logs(self.log_total, self.log_extended)
        self.hp_bars = {
            GLOBAL.ENABLED: False,
            HP_BARS.STYLE: HP_BARS.STYLES.league,
            HP_BARS.ALIVE: False
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
            GLOBAL.X: 255,
            GLOBAL.Y: GLOBAL.ZERO,
            "progress_bar": False
        }
        self.players_panels = {
            GLOBAL.ENABLED: False,
            PANELS.SPOTTED_FIX: True,
            PANELS.DAMAGES_ENABLED: False,
            PANELS.DAMAGES_HOT_KEY: [[Keys.KEY_LALT]],
            PANELS.DAMAGES_TEMPLATE: "<font color='#FFFF00'>%(damage)s</font>",
            PANELS.DAMAGES_SETTINGS: {GLOBAL.X: -50, GLOBAL.Y: -2, GLOBAL.ALIGN: GLOBAL.ALIGN_LIST.left},
            PANELS.BARS_ENABLED: False,
            PANELS.BAR_CLASS_COLOR: False,
            PANELS.ON_KEY_DOWN: False,
            PANELS.BAR_HOT_KEY: [[Keys.KEY_LALT]],
            PANELS.HP_TEMPLATE: "%(health)s",
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
        self.minimap = {
            GLOBAL.ENABLED: False,
            MINIMAP.DEATH_PERMANENT: False,
            MINIMAP.SHOW_NAMES: False,
            MINIMAP.VIEW_RADIUS: False,
            MINIMAP.YAW: True,
            MINIMAP.ZOOM: False,
            MINIMAP.ZOOM_KEY: [[29]]
        }
        self.service_channel_filter = {
            GLOBAL.ENABLED: False,
            SERVICE_CHANNEL.KEYS: dict.fromkeys(SERVICE_CHANNEL.SYSTEM_CHANNEL_KEYS, False)
        }
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

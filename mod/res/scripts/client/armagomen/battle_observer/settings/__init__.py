import Keys
from armagomen._constants import (ALIAS_TO_CONFIG_NAME, ALIAS_TO_CONFIG_NAME_LOBBY, ARCADE, ARMOR_CALC, AVG_EFFICIENCY_HANGAR, BATTLE_TIMER,
                                  CLOCK, COLORS, DAMAGE_LOG, DEBUG_PANEL, DISPERSION, DISPERSION_TIMER, EFFECTS, EX_LOGS_ICONS,
                                  FLIGHT_TIME, GLOBAL, HP_BARS, IMAGE_DIR, LOGS_ICONS, MAIN, MINIMAP, PANELS, SERVICE_CHANNEL, SIXTH_SENSE,
                                  SNIPER, STATISTICS, STRATEGIC, TEAM_BASES, VEHICLE_TYPES_COLORS)
from constants import ATTACK_REASON
from gui.shared.gui_items.Vehicle import VEHICLE_CLASS_NAME


class UserSettings(object):

    def __init__(self):
        self.main = {
            MAIN.AUTO_CLAIM_CLAN_REWARD: False,
            MAIN.AUTO_CLEAR_CACHE: False,
            MAIN.CREW_RETURN: False,
            MAIN.CREW_TRAINING: False,
            MAIN.DEBUG: False,
            MAIN.DIRECTIVES: False,
            MAIN.DISABLE_SCORE_SOUND: False,
            MAIN.EXCLUDED_MAP_SLOTS_NOTIFICATION: False,
            MAIN.FIELD_MAIL: False,
            MAIN.HIDE_BADGES: False,
            MAIN.HIDE_CLAN_ABBREV: False,
            MAIN.HIDE_DOG_TAGS: False,
            MAIN.HIDE_HINT: False,
            MAIN.IGNORE_COMMANDERS: False,
            MAIN.MUTE_BASES_SOUND: False,
            MAIN.SAVE_SHOT: False,
            MAIN.SHOW_ANONYMOUS: False,
            MAIN.SHOW_FRIENDS: False,
            MAIN.STUN_SOUND: False,
            MAIN.USE_KEY_PAIRS: True
        }

        self.avg_efficiency_in_hangar = {
            GLOBAL.ENABLED: False,
            AVG_EFFICIENCY_HANGAR.ASSIST: True,
            AVG_EFFICIENCY_HANGAR.BATTLES: True,
            AVG_EFFICIENCY_HANGAR.BLOCKED: True,
            AVG_EFFICIENCY_HANGAR.DAMAGE: True,
            AVG_EFFICIENCY_HANGAR.MARKS_ON_GUN: True,
            AVG_EFFICIENCY_HANGAR.STUN: True,
            AVG_EFFICIENCY_HANGAR.WIN_RATE: True
        }

        self.clock = {
            GLOBAL.ENABLED: False,
            CLOCK.IN_LOBBY: {
                GLOBAL.ENABLED: False,
                CLOCK.FORMAT: CLOCK.DEFAULT_FORMAT_HANGAR
            },
            CLOCK.IN_BATTLE: {
                GLOBAL.ENABLED: False,
                CLOCK.FORMAT: CLOCK.DEFAULT_FORMAT_BATTLE,
                GLOBAL.X: -270,
                GLOBAL.Y: 0
            }
        }

        self.sixth_sense = {
            GLOBAL.ENABLED: False,
            SIXTH_SENSE.PLAY_TICK_SOUND: True,
            SIXTH_SENSE.ICON_NAME: "lamp_2.png",
            SIXTH_SENSE.SHOW_TIMER: False,
            SIXTH_SENSE.TIMER_GRAPHICS: True,
            SIXTH_SENSE.RANDOM: False,
            SIXTH_SENSE.TIMER_GRAPHICS_COLOR: "#ffa500",
            SIXTH_SENSE.TIMER_GRAPHICS_RADIUS: 38,
            SIXTH_SENSE.ICON_SIZE: 70
        }

        self.dispersion_circle = {
            GLOBAL.ENABLED: False,
            DISPERSION.SERVER: False,
            DISPERSION.REPLACE: False,
            DISPERSION.SCALE: 0.7
        }

        self.dispersion_timer = {
            GLOBAL.ENABLED: False,
            GLOBAL.X: 110,
            GLOBAL.Y: 0,
            GLOBAL.ALIGN: GLOBAL.ALIGN_LIST.left,
            DISPERSION_TIMER.TIMER: True,
            DISPERSION_TIMER.PERCENT: True,
            "text_size": 18
        }

        self.debug_panel = {
            GLOBAL.ENABLED: False,
            DEBUG_PANEL.STYLE: DEBUG_PANEL.STYLES.minimal,
            DEBUG_PANEL.FPS_COLOR: "#B3FE95",
            DEBUG_PANEL.PING_COLOR: "#B3FE95"
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
            EFFECTS.NO_SNIPER_DYNAMIC: False
        }

        self.zoom = {
            GLOBAL.ENABLED: False,
            SNIPER.DISABLE_SNIPER: False,
            SNIPER.DISABLE_LATENCY: 0.5,
            SNIPER.SKIP_CLIP: True,
            SNIPER.DYN_ZOOM: False,
            SNIPER.ZOOM_STEPS: False,
            SNIPER.STEPS: SNIPER.DEFAULT_STEPS
        }

        self.arcade_camera = {
            GLOBAL.ENABLED: False,
            ARCADE.DIST_RANGE: [10.0, 150.0],
            ARCADE.START_DEAD_DIST: 20.0,
            ARCADE.SCROLL_SENSITIVITY: 4.0
        }

        self.strategic_camera = {
            GLOBAL.ENABLED: False,
            STRATEGIC.DIST_RANGE: [40.0, 150.0],
            STRATEGIC.SCROLL_SENSITIVITY: 10.0
        }

        self.armor_calculator = {
            GLOBAL.ENABLED: False,
            ARMOR_CALC.POSITION: {GLOBAL.X: 0, GLOBAL.Y: 60},
            ARMOR_CALC.ON_ALLY: False,
            ARMOR_CALC.SHOW_PIERCING_RESERVE: False,
            ARMOR_CALC.SHOW_COUNTED_ARMOR: True,
            ARMOR_CALC.SHOW_PIERCING_POWER: True,
            ARMOR_CALC.SHOW_CALIBER: False,
            "splitter": " | ",
            "text_size": 18
        }

        self.colors = {
            COLORS.GLOBAL: {
                COLORS.ALLY_MAME: COLORS.GREEN,
                COLORS.ENEMY_MAME: COLORS.RED,
                COLORS.ENEMY_BLIND_MAME: COLORS.BLIND,
                COLORS.C_BG: COLORS.BLACK
            },
            ARMOR_CALC.NAME: {
                COLORS.C_GREEN: COLORS.GREEN,
                COLORS.C_ORANGE: COLORS.ORANGE,
                COLORS.C_RED: COLORS.RED,
                COLORS.C_YELLOW: COLORS.YELLOW,
                COLORS.C_PURPLE: COLORS.BLIND,
                COLORS.C_NORMAL: COLORS.WHITE
            },
            VEHICLE_TYPES_COLORS.NAME: {
                VEHICLE_CLASS_NAME.HEAVY_TANK: "#F9B200",
                VEHICLE_CLASS_NAME.MEDIUM_TANK: "#FDEF6C",
                VEHICLE_CLASS_NAME.AT_SPG: "#0094EC",
                VEHICLE_CLASS_NAME.SPG: "#A90400",
                VEHICLE_CLASS_NAME.LIGHT_TANK: "#37BC00",
                VEHICLE_TYPES_COLORS.UNKNOWN: COLORS.WHITE
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
                GLOBAL.X: -260,
                GLOBAL.Y: 0,
                GLOBAL.ALIGN: GLOBAL.ALIGN_LIST.right,
                DAMAGE_LOG.IN_CENTER: True
            },
            DAMAGE_LOG.TEMPLATE_MAIN_DMG: [
                "%(damageIcon)s<font color='%(tankDamageAvgColor)s'>%(playerDamage)s</font>",
                "%(blockedIcon)s<font color='%(tankBlockedAvgColor)s'>%(blockedDamage)s</font>",
                "%(assistIcon)s<font color='%(tankAssistAvgColor)s'>%(assistDamage)s</font>",
                "%(spottedIcon)s%(spottedTanks)s",
                "%(stunIcon)s<font color='%(tankStunAvgColor)s'>%(stun)s</font>"
            ],
            DAMAGE_LOG.ICONS: {
                "assistIcon": "<img src='{}/efficiency/help.png' {}>".format(IMAGE_DIR, LOGS_ICONS),
                "blockedIcon": "<img src='{}/efficiency/armor.png' {}>".format(IMAGE_DIR, LOGS_ICONS),
                "damageIcon": "<img src='{}/efficiency/damage.png' {}>".format(IMAGE_DIR, LOGS_ICONS),
                "stunIcon": "<img src='{}/efficiency/stun.png' {}>".format(IMAGE_DIR, LOGS_ICONS),
                "spottedIcon": "<img src='{}/efficiency/detection.png' {}>".format(IMAGE_DIR, LOGS_ICONS)
            },
            DAMAGE_LOG.TOP_LOG_SEPARATE: "  ",
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
            DAMAGE_LOG.ATTACK_REASON: {
                ATTACK_REASON.SHOT: "<img src='{}/efficiency/damage.png' {}>".format(IMAGE_DIR, EX_LOGS_ICONS),
                ATTACK_REASON.FIRE: "<img src='{}/efficiency/fire.png' {}>".format(IMAGE_DIR, EX_LOGS_ICONS),
                ATTACK_REASON.RAM: "<img src='{}/efficiency/ram.png' {}>".format(IMAGE_DIR, EX_LOGS_ICONS)
            },
            DAMAGE_LOG.KILLED_ICON: "<img src='{}/efficiency/destruction.png' {}>".format(IMAGE_DIR, EX_LOGS_ICONS),
            "textformat": {
                "normal": "<textformat leading='-2' tabstops='[20, 55, 80, 100]'><font face='$TitleFont' size='15'>{}</font></textformat>",
                "alt": "<textformat leading='-2' tabstops='[20]'><font face='$TitleFont' size='15'>{}</font></textformat>"
            },
            DAMAGE_LOG.TEMPLATES: {
                "normal": [
                    "<font size='12'>%(index)02d:</font><tab>",
                    "<font color='%(percentDamageAvgColor)s'>%(totalDamage)s</font><tab>",
                    "<font color='%(shellColor)s'>%(shellType)s</font><tab>",
                    "%(attackReason)s<tab>",
                    "%(classIcon)s%(tankName)s %(killedIcon)s"
                ],
                "alt": [
                    "<font size='12'>%(shots)d:</font><tab>",
                    "%(allDamages)s",
                    "%(classIcon)s%(userName).12s %(killedIcon)s"
                ]
            },
            DAMAGE_LOG.SHELL_COLOR: {
                DAMAGE_LOG.NORMAL: COLORS.WHITE,
                DAMAGE_LOG.GOLD: COLORS.GOLD
            },
            DAMAGE_LOG.HOT_KEY: [[Keys.KEY_LALT]],
            GLOBAL.AVG_COLOR: {"saturation": 0.5, "brightness": 1.0}
        }

        self.hp_bars = {
            GLOBAL.ENABLED: False,
            HP_BARS.STYLE: HP_BARS.STYLES.league,
            HP_BARS.ALIVE: False
        }

        self.team_bases_panel = {
            GLOBAL.ENABLED: False,
            GLOBAL.Y: 60,
            GLOBAL.WIDTH: 400,
            GLOBAL.HEIGHT: 24,
            TEAM_BASES.TEXT_SETTINGS: {
                TEAM_BASES.FONT: "$TitleFont",
                TEAM_BASES.SIZE: 16,
                GLOBAL.COLOR: COLORS.WHITE,
                TEAM_BASES.BOLD: False,
                TEAM_BASES.ITALIC: False,
                TEAM_BASES.UNDERLINE: False,
                GLOBAL.Y: 0
            }
        }

        self.main_gun = {
            GLOBAL.ENABLED: False,
            GLOBAL.X: 260,
            GLOBAL.Y: 0,
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
            PANELS.HP_TEMPLATE: "%(health)s"
        }

        self.flight_time = {
            GLOBAL.ENABLED: False,
            GLOBAL.X: -110,
            GLOBAL.Y: 0,
            GLOBAL.COLOR: "#f5ff8f",
            FLIGHT_TIME.TIME: True,
            FLIGHT_TIME.DISTANCE: True,
            FLIGHT_TIME.SPG_ONLY: True,
            FLIGHT_TIME.ALIGN: GLOBAL.ALIGN_LIST.right,
            "text_size": 18
        }

        self.distance_to_enemy = {
            GLOBAL.ENABLED: False,
            GLOBAL.X: 0,
            GLOBAL.Y: -190,
            GLOBAL.ALIGN: GLOBAL.ALIGN_LIST.center,
            GLOBAL.COLOR: "#f5ff8f",
            "text_size": 18
        }

        self.own_health = {
            GLOBAL.ENABLED: False,
            GLOBAL.X: 0,
            GLOBAL.Y: 350,
            GLOBAL.AVG_COLOR: {"saturation": 0.7, "brightness": 0.9}
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
            STATISTICS.FULL_LEFT: "<b><font color='%(colorWGR)s'>%(WGR)d | %(battles)s | %(nickname).12s</font>%(clanTag)s</b>",
            STATISTICS.FULL_RIGHT: "<b>%(clanTag)s<font color='%(colorWGR)s'>%(nickname).12s | %(battles)s | %(WGR)d</font></b>",
            STATISTICS.CUT_LEFT: "<b><font color='%(colorWGR)s'>%(nickname).12s</font></b>",
            STATISTICS.CUT_RIGHT: "<b><font color='%(colorWGR)s'>%(nickname).12s</font></b>",
            STATISTICS.PANELS_CUT_WIDTH: 60,
            STATISTICS.PANELS_FULL_WIDTH: 150,
            STATISTICS.COLORS: {
                "bad": "#FE7B23",
                "good": "#88D957",
                "normal": "#F5F373",
                "unique": "#A874BE",
                "very_bad": "#FC4A3C",
                "very_good": "#44DBCB"
            },
            STATISTICS.ICON_ENABLED: False,
            STATISTICS.ICON_BLACKOUT: -1.25
        }

    def getSettingDictByAliasBattle(self, name):
        return getattr(self, ALIAS_TO_CONFIG_NAME.get(name, GLOBAL.EMPTY_LINE), self)

    def getSettingDictByAliasLobby(self, name):
        return getattr(self, ALIAS_TO_CONFIG_NAME_LOBBY.get(name, GLOBAL.EMPTY_LINE), self)


user_settings = UserSettings()

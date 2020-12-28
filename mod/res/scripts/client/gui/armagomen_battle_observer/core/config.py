# coding=utf-8
import codecs
import json
import os
import time

import Keys
from constants import ATTACK_REASON, ATTACK_REASONS, SHELL_TYPES_LIST
from gui.shared.gui_items.Vehicle import VEHICLE_CLASS_NAME
from .bo_constants import ARCADE, ARMOR_CALC, BATTLE_TIMER, CAROUSEL, CLOCK, COLORS, DAMAGE_LOG, DEBUG_PANEL, \
    DISPERSION_CIRCLE, EFFECTS, FLIGHT_TIME, GLOBAL, HANGAR_CAMERA, HP_BARS, LOAD_LIST, MAIN, MAIN_GUN, MARKERS, \
    MINIMAP, PANELS, POSTMORTEM, SAVE_SHOOT, SERVICE_CHANNEL, SIXTH_SENSE, SNIPER, STRATEGIC, TEAM_BASES, \
    USER_BACKGROUND, VEHICLE_TYPES
from .bw_utils import logInfo, logWarning
from .core import m_core
from .events import g_events


class Config(object):

    def __init__(self):
        icons_dir = GLOBAL.ICONS_DIR
        efficiency_dir = GLOBAL.EFFICIENCY_DIR
        img_params = GLOBAL.IMG_PARAMS
        img_format = (efficiency_dir, img_params)

        self.main = {
            MAIN.HIDE_CHAT: False,
            MAIN.SHOW_FRIENDS: False,
            MAIN.SHOW_ANONYMOUS: False,
            MAIN.CHANGE_ANONYMOUS_NAME: False,
            MAIN.ANONYMOUS_STRING: "Anonymous",
            MAIN.BG: False,
            MAIN.BG_TRANSPARENCY: 0.25,
            MAIN.REMOVE_SHADOW_IN_PREBATTLE: False,
            MAIN.HIDE_BADGES: False,
            MAIN.HIDE_CLAN_ABBREV: False,
            MAIN.ENABLE_BARS_ANIMATION: True,
            MAIN.ENABLE_FPS_LIMITER: False,
            MAIN.MAX_FRAME_RATE: 200,
            MAIN.AUTO_CLEAR_CACHE: False,
            MAIN.USE_KEY_PAIRS: False,
            MAIN.REMOVE_HANDBRAKE: False
        }
        self.user_background = {
            GLOBAL.ENABLED: False,
            USER_BACKGROUND.LABELS: [{
                GLOBAL.SMOOTHING: True,
                GLOBAL.X: GLOBAL.ZERO,
                GLOBAL.Y: GLOBAL.ZERO,
                GLOBAL.ALPHA: 0.9,
                GLOBAL.IMG: "mods/configs/mod_battle_observer/*.png",
                GLOBAL.WIDTH: 300,
                GLOBAL.HEIGHT: 150,
                USER_BACKGROUND.CENTERED_X: False,
                USER_BACKGROUND.CENTERED_Y: False,
                GLOBAL.ENABLED: False,
                USER_BACKGROUND.LAYER: GLOBAL.EMPTY_LINE
            }]
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
                GLOBAL.Y: 54
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
                GLOBAL.X: -2,
                GLOBAL.Y: 130,
                SIXTH_SENSE.TEMPLATE: "<font size='40'>%(timeLeft)d</font>",
                GLOBAL.ALPHA: 0.75
            },
            SIXTH_SENSE.IMAGE: {
                GLOBAL.SMOOTHING: True,
                GLOBAL.X: GLOBAL.ZERO,
                GLOBAL.Y: 100,
                GLOBAL.ALPHA: 0.85,
                GLOBAL.SCALE: 0.65,
                GLOBAL.IMG: "mods/configs/mod_battle_observer/SixthSenseIcon.png"
            }
        }
        self.dispersion_circle = {
            GLOBAL.ENABLED: False,
            DISPERSION_CIRCLE.EXTRA_LAP: False,
            DISPERSION_CIRCLE.REPLACE: False,
            DISPERSION_CIRCLE.SCALE_CONFIG: DISPERSION_CIRCLE.SCALE,
            DISPERSION_CIRCLE.TIMER_ENABLED: False,
            DISPERSION_CIRCLE.TIMER_POSITION_X: 110,
            DISPERSION_CIRCLE.TIMER_POSITION_Y: 0,
            DISPERSION_CIRCLE.TIMER_ALIGN: GLOBAL.LEFT,
            DISPERSION_CIRCLE.TIMER_COLOR: "#f5ff8f",
            DISPERSION_CIRCLE.TIMER_DONE_COLOR: "#a6ffa6",
            DISPERSION_CIRCLE.TIMER_REGULAR_TEMPLATE: "<font color='%(color)s'>%(timer).1fs. - %(percent)d%%</font>",
            DISPERSION_CIRCLE.TIMER_DONE_TEMPLATE: "<font color='%(color_done)s'>reduction - %(percent)d%%</font>"
        }
        self.debug_panel = {
            GLOBAL.ENABLED: False,
            DEBUG_PANEL.TEXT: {
                GLOBAL.X: 5,
                GLOBAL.Y: GLOBAL.ZERO,
                GLOBAL.SCALE: 1.0,
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
            EFFECTS.NO_LIGHT_EFFECT: False,
            EFFECTS.NO_BINOCULARS: False
        }
        self.zoom = {
            GLOBAL.ENABLED: False,
            SNIPER.DISABLE_AFTER_SHOOT: False,
            SNIPER.SKIP_CLIP: True,
            SNIPER.DYN_ZOOM: {
                GLOBAL.ENABLED: False,
                SNIPER.GUN_ZOOM: False,
                SNIPER.MAX_ZOOM_NUM: 30.0,
                SNIPER.MIN_ZOOM_NUM: 2.0,
                SNIPER.METERS: 20.0
            },
            SNIPER.DEF_ZOOM: {
                GLOBAL.ENABLED: False,
                SNIPER.DEF_ZOOM_NUM: 4.0
            },
            SNIPER.ZOOM_STEPS: {
                GLOBAL.ENABLED: False,
                SNIPER.STEPS: SNIPER.DEFAULT_STEPS
            }
        }
        self.arcade_camera = {
            GLOBAL.ENABLED: False,
            ARCADE.MIN: 4.0,
            ARCADE.MAX: 80.0,
            ARCADE.START_DEAD_DIST: 20.0,
            POSTMORTEM.TRANSITION: True,
            POSTMORTEM.DURATION: POSTMORTEM.CALLBACK_TIME_SEC
        }
        self.strategic_camera = {
            GLOBAL.ENABLED: False,
            STRATEGIC.MIN: 40.0,
            STRATEGIC.MAX: 150.0
        }
        self.hangar_camera = {
            GLOBAL.ENABLED: False,
            GLOBAL.SETTINGS: {
                HANGAR_CAMERA.DIST_CONSTR: [2, 25],
                HANGAR_CAMERA.START_DIST: 16.0,
                HANGAR_CAMERA.START_ANGLES: [100, -20],
                HANGAR_CAMERA.DIST_SENS: 0.0065
            }
        }
        self.armor_calculator = {
            GLOBAL.ENABLED: False,
            ARMOR_CALC.SHOW_POINTS: True,
            ARMOR_CALC.POSITION: {GLOBAL.X: GLOBAL.ZERO, GLOBAL.Y: 100},
            ARMOR_CALC.TEMPLATE: "<font color='%(color)s'>%(calcedArmor).1f | %(piercingPower)s</font>",
            ARMOR_CALC.MESSAGES: ARMOR_CALC.DEFAULT_MESSAGES,
            ARMOR_CALC.SHOW_MESSAGE: False,
            ARMOR_CALC.TEXT_POSITION: {GLOBAL.X: GLOBAL.ZERO, GLOBAL.Y: 150}
        }
        self.colors = {
            MAIN_GUN.NAME: {
                MAIN_GUN.COLOR: COLORS.S_YELLOW
            },
            MARKERS.NAME: {
                MARKERS.ALLY: COLORS.GREEN,
                MARKERS.ENEMY: COLORS.RED,
                MARKERS.ENEMY_COLOR_BLIND: COLORS.BLIND,
                MARKERS.DEAD_COLOR: COLORS.B_SILVER
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
            DAMAGE_LOG.WG_CRITS: False,
            DAMAGE_LOG.WG_BLOCKED: False,
            DAMAGE_LOG.WG_ASSIST: False,
            DAMAGE_LOG.HOT_KEY: [[Keys.KEY_LALT]],
            DAMAGE_LOG.ATTACK_REASON: {
                ATTACK_REASON.SHOT: "<img src='%s/damage.png' %s>" % img_format,
                ATTACK_REASON.FIRE: "<img src='%s/fire.png' %s>" % img_format,
                ATTACK_REASON.RAM: "<img src='%s/ram.png' %s>" % img_format,
                ATTACK_REASON.WORLD_COLLISION: "<img src='%s/ram.png' %s>" % img_format
            }
        }
        additional = {reason: "<img src='%s/module.png' %s>" % img_format for reason in ATTACK_REASONS
                      if reason not in self.log_global[DAMAGE_LOG.ATTACK_REASON]}
        self.log_global[DAMAGE_LOG.ATTACK_REASON].update(additional)
        self.log_total = {
            GLOBAL.ENABLED: False,
            GLOBAL.SETTINGS: {
                GLOBAL.X: -255,
                GLOBAL.Y: GLOBAL.ZERO,
                GLOBAL.ALIGN: GLOBAL.RIGHT,
                DAMAGE_LOG.IN_CENTER: True
            },
            DAMAGE_LOG.TEMPLATE_MAIN_DMG: ("<textformat leading='-3'>%(damageIcon)s"
                                           "<font color='%(tankDamageAvgColor)s'>%(playerDamage)s</font>"
                                           "%(blockedIcon)s%(blockedDamage)s%(assistIcon)s%(assistDamage)s"
                                           "%(spottedIcon)s%(spottedTanks)s%(stunIcon)s%(stun)s</textformat>"),
            DAMAGE_LOG.ICONS: {
                "assistIcon": "<img src='%s/help.png' %s vspace='-10'>" % (efficiency_dir, img_params[:22]),
                "blockedIcon": "<img src='%s/armor.png' %s vspace='-9'>" % (efficiency_dir, img_params[:22]),
                "damageIcon": "<img src='%s/damage.png' %s vspace='-10'>" % (efficiency_dir, img_params[:22]),
                "spottedIcon": "<img src='%s/detection.png' %s vspace='-10'>" % (efficiency_dir, img_params[:22]),
                "stunIcon": "<img src='%s/stun.png' %s vspace='-10'>" % (efficiency_dir, img_params[:22])
            },
            DAMAGE_LOG.AVG_COLOR: {"saturation": 0.5, "brightness": 1.0}
        }
        self.log_damage_extended = {
            GLOBAL.ENABLED: False,
            DAMAGE_LOG.REVERSE: False,
            GLOBAL.SETTINGS: {
                GLOBAL.X: 10,
                GLOBAL.Y: GLOBAL.ZERO,
                GLOBAL.ALIGN: GLOBAL.LEFT
            },
            DAMAGE_LOG.KILLED_ICON: "<img src='%s/destruction.png' %s>" % img_format,
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
            DAMAGE_LOG.SHELL_TYPES: {shell_type: "" for shell_type in SHELL_TYPES_LIST},
            DAMAGE_LOG.SHELL_ICONS: {shell: "" for shell in DAMAGE_LOG.SHELL_LIST},
            DAMAGE_LOG.SHELL_COLOR: {
                DAMAGE_LOG.NORMAL: COLORS.NORMAL_TEXT,
                DAMAGE_LOG.GOLD: COLORS.GOLD
            },
            DAMAGE_LOG.AVG_COLOR: {"saturation": 0.5, "brightness": 1.0}
        }
        self.log_damage_extended[DAMAGE_LOG.SHELL_TYPES][DAMAGE_LOG.UNDEFINED] = ""
        self.log_damage_extended[DAMAGE_LOG.SHELL_ICONS][DAMAGE_LOG.UNDEFINED] = ""
        self.log_input_extended = {
            GLOBAL.ENABLED: False,
            DAMAGE_LOG.REVERSE: False,
            GLOBAL.SETTINGS: {
                GLOBAL.X: 10,
                GLOBAL.Y: -20,
                GLOBAL.ALIGN: GLOBAL.LEFT
            },
            DAMAGE_LOG.KILLED_ICON: "<img src='%s/destruction.png' %s>" % img_format,
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
            DAMAGE_LOG.SHELL_TYPES: {shell_type: "" for shell_type in SHELL_TYPES_LIST},
            DAMAGE_LOG.SHELL_ICONS: {shell: "" for shell in DAMAGE_LOG.SHELL_LIST},
            DAMAGE_LOG.SHELL_COLOR: {
                DAMAGE_LOG.NORMAL: COLORS.NORMAL_TEXT,
                DAMAGE_LOG.GOLD: COLORS.GOLD
            },
            DAMAGE_LOG.AVG_COLOR: {"saturation": 0.5, "brightness": 1.0}
        }
        self.log_input_extended[DAMAGE_LOG.SHELL_TYPES][DAMAGE_LOG.UNDEFINED] = ""
        self.log_input_extended[DAMAGE_LOG.SHELL_ICONS][DAMAGE_LOG.UNDEFINED] = ""
        self.hp_bars = {
            GLOBAL.ENABLED: True,
            HP_BARS.STYLE: HP_BARS.LEGUE_STYLE,
            HP_BARS.WIDTH: 200,
            HP_BARS.DIFF: True,
            HP_BARS.ALIVE: False,
            COLORS.NAME: {
                HP_BARS.C_ALLY: COLORS.GREEN,
                HP_BARS.C_ENEMY: COLORS.RED,
                HP_BARS.C_BLIND: COLORS.BLIND,
                COLORS.C_BG: COLORS.BLACK,
                GLOBAL.ALPHA: 0.6,
                GLOBAL.BG_ALPHA: 0.5
            },
            GLOBAL.OUTLINE: {
                GLOBAL.ENABLED: True,
                GLOBAL.COLOR: COLORS.NORMAL_TEXT
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
            COLORS.NAME: {
                COLORS.C_GREEN: COLORS.GREEN,
                COLORS.C_RED: COLORS.RED,
                COLORS.C_PURPLE: COLORS.PURPLE,
                COLORS.C_BG: COLORS.BLACK,
                GLOBAL.ALPHA: 0.6,
                GLOBAL.BG_ALPHA: 0.5
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
        self.markers = {
            GLOBAL.ENABLED: True,
            MARKERS.HOT_KEY: [Keys.KEY_NUMPAD0],
            MARKERS.CLASS_COLOR: False,
            GLOBAL.X: 5,
            GLOBAL.Y: 31
        }
        self.main_gun = {
            GLOBAL.ENABLED: False,
            MAIN_GUN.DYNAMIC: True,
            MAIN_GUN.TEMPLATE: "%(mainGunIcon)s%(mainGunDoneIcon)s%(mainGunFailureIcon)s"
                               "<font color='%(mainGunColor)s'>%(mainGun)s</font>",
            GLOBAL.SETTINGS: {
                GLOBAL.X: 255,
                GLOBAL.Y: GLOBAL.ZERO,
                GLOBAL.ALIGN: GLOBAL.LEFT
            },
            MAIN_GUN.GUN_ICON: "<img src='{}/achievement/32x32/mainGun.png' width='26' height='25'"
                               " vspace='-7'>".format(icons_dir),
            MAIN_GUN.DONE_ICON: "<img src='{}/library/done.png' width='24' height='24' vspace='-8'>".format(icons_dir),
            MAIN_GUN.FAILURE_ICON: "<img src='{}/library/icon_alert_32x32.png' width='22' height='22'"
                                   " vspace='-6'>".format(icons_dir)
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
        self.panels_icon = {
            GLOBAL.ENABLED: False,
            PANELS.BLACKOUT: -0.8
        }
        self.players_spotted = {
            GLOBAL.ENABLED: False,
            PANELS.STATUS: {
                PANELS.LIGHTS: "<font face='$TitleFont' color='#00FF00' size='24'>*</font>",
                PANELS.NOT_LIGHT: "<font face='$TitleFont' color='#FF0000' size='24'>*</font>"
            },
            GLOBAL.SETTINGS: {GLOBAL.X: -40, GLOBAL.Y: -2, GLOBAL.ALIGN: GLOBAL.CENTER}
        }
        self.players_damages = {
            GLOBAL.ENABLED: False,
            PANELS.DAMAGES_HOT_KEY: [[Keys.KEY_LALT]],
            PANELS.DAMAGES_TEMPLATE: "<font color='#FFFF00'>%(damage)s</font>",
            PANELS.DAMAGES_SETTINGS: {GLOBAL.X: -50, GLOBAL.Y: -2, GLOBAL.ALIGN: GLOBAL.LEFT}
        }
        self.players_bars = {
            GLOBAL.ENABLED: False,
            PANELS.BAR_CLASS_COLOR: False,
            PANELS.ON_KEY_DOWN: False,
            PANELS.BAR_HOT_KEY: [[Keys.KEY_LALT]],
            PANELS.HP_TEMPLATE: "<font face='$TitleFont' color='#FAFAFA' size='15'>%(health)s</font>",
            PANELS.BAR_SETTINGS: {
                PANELS.TEXT_SETTINGS: {GLOBAL.X: 35, GLOBAL.Y: GLOBAL.ZERO, GLOBAL.ALIGN: GLOBAL.CENTER},
                PANELS.BAR: {
                    GLOBAL.X: GLOBAL.ZERO,
                    GLOBAL.Y: 2,
                    GLOBAL.WIDTH: 70,
                    GLOBAL.HEIGHT: 22,
                    COLORS.NAME: {
                        PANELS.ALLY: COLORS.GREEN,
                        PANELS.ENEMY: COLORS.RED,
                        PANELS.BLIND: COLORS.BLIND,
                        COLORS.C_BG: COLORS.BLACK,
                        GLOBAL.ALPHA: 0.6,
                        GLOBAL.BG_ALPHA: 0.5
                    },
                    GLOBAL.OUTLINE: {
                        GLOBAL.ENABLED: True,
                        GLOBAL.COLOR: COLORS.NORMAL_TEXT,
                        GLOBAL.CUSTOM_COLOR: False,
                        GLOBAL.ALPHA: 0.7
                    }
                }
            }
        }
        self.flight_time = {
            GLOBAL.ENABLED: False,
            FLIGHT_TIME.WG_DIST_DISABLE: False,
            GLOBAL.X: -110,
            GLOBAL.Y: GLOBAL.ZERO,
            FLIGHT_TIME.SPG_ONLY: True,
            FLIGHT_TIME.ALIGN: GLOBAL.RIGHT,
            FLIGHT_TIME.TEMPLATE: "<font color='#f5ff8f'>%(flightTime).1f s. - %(distance).1f m.</font>"
        }
        self.save_shoot = {
            GLOBAL.ENABLED: False,
            SAVE_SHOOT.ALIVE_ONLY: True,
            SAVE_SHOOT.MSG: SAVE_SHOOT.TEMPLATE
        }
        self.minimap = {
            GLOBAL.ENABLED: False,
            MINIMAP.DEATH_PERMANENT: False,
            MINIMAP.SHOW_NAMES: False,
            MINIMAP.ZOOM: {
                GLOBAL.ENABLED: False,
                MINIMAP.INDENT: 180,
                MINIMAP.HOT_KEY: [[Keys.KEY_LCONTROL]]
            }
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
        self.postmortem_panel = {GLOBAL.ENABLED: False, POSTMORTEM.HIDE_KILLER: True}


cfg = Config()


class ConfigLoader(object):
    __slots__ = ('cName', 'path', 'configsList')

    def __init__(self):
        self.cName = None
        self.path = os.path.join(m_core.modsDir, "configs", "mod_battle_observer")
        self.configsList = [x for x in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, x))]

    def start(self):
        self.getConfig(self.path)

    def encodeData(self, data):
        """encode dict keys/values to utf-8."""
        if type(data) is dict:
            return {self.encodeData(key): self.encodeData(value) for key, value in data.iteritems()}
        elif type(data) is list:
            return [self.encodeData(element) for element in data]
        elif isinstance(data, basestring):
            return data.encode('utf-8')
        else:
            return data

    def getFileData(self, path):
        """Gets a dict from JSON."""
        try:
            with open(path, 'r') as fh:
                return self.encodeData(json.load(fh))
        except Exception:
            with codecs.open(path, 'r', 'utf-8-sig') as fh:
                return self.encodeData(json.loads(fh.read()))

    def loadError(self, file_name, error):
        with codecs.open(os.path.join(self.path, 'Errors.log'), 'a', 'utf-8-sig') as fh:
            fh.write('%s: %s: %s, %s\n' % (time.asctime(), 'ERROR CONFIG DATA', file_name, error))

    @staticmethod
    def makeDirs(path):
        if not os.path.exists(path):
            os.makedirs(path)
            return True
        return False

    def getConfig(self, path):
        """Loading the main config file with the parameters which config to load next"""
        load_json = os.path.join(path, 'load.json')
        if self.makeDirs(path):
            self.loadError(path, 'CONFIGURATION FILES IS NOT FOUND')
            self.cName = self.createLoadJSON(load_json)
            self.configsList.append(self.cName)
        else:
            if os.path.exists(load_json):
                self.cName = self.getFileData(load_json).get('loadConfig')
            else:
                self.cName = self.createLoadJSON(load_json)
            self.makeDirs(os.path.join(path, self.cName))
        self.readConfig(self.cName)

    def createLoadJSON(self, path):
        cName = 'default'
        self.createFileInDir(path, {'loadConfig': cName})
        self.loadError(path, 'NEW CONFIGURATION FILE load.json IS CREATED')
        return cName

    def updateConfigFile(self, fileName, config):
        path = os.path.join(self.path, self.cName, '{}.json'.format(fileName))
        self.createFileInDir(path, config)

    @staticmethod
    def createFileInDir(path, data):
        """Creates a new file in a folder or replace old."""
        with open(path, 'w') as f:
            json.dump(data, f, skipkeys=True, ensure_ascii=False, indent=2, sort_keys=True)

    @staticmethod
    def isNotEqualLen(data1, data2):
        """
        Returns True if the length of 2 dictionaries is not identical,
        or an error occurs when comparing lengths.
        And the config file needs to be rewritten
        """
        if isinstance(data1, dict) and isinstance(data2, dict):
            return len(data1) != len(data2)
        return type(data1) != type(data2)

    def updateData(self, external_cfg, internal_cfg, file_update=False):
        """recursively updates words from config files"""
        file_update |= self.isNotEqualLen(external_cfg, internal_cfg)
        for key in internal_cfg:
            old_param_type = type(internal_cfg[key])
            if old_param_type is dict:
                file_update |= self.updateData(external_cfg.get(key, {}), internal_cfg[key], file_update)
            else:
                new_param = external_cfg.get(key)
                if new_param is not None:
                    new_param_type = type(new_param)
                    if new_param_type != old_param_type:
                        file_update = True
                        if old_param_type is int and new_param_type is float:
                            internal_cfg[key] = int(round(new_param))
                        elif old_param_type is float and new_param_type is int:
                            internal_cfg[key] = float(new_param)
                    else:
                        internal_cfg[key] = new_param
                else:
                    file_update = True
        return file_update

    def readConfig(self, configName):
        """Read config file from JSON"""
        direct_path = os.path.join(self.path, configName)
        logInfo('START UPDATE USER CONFIGURATION: {}'.format(configName))
        file_list = ['{}.json'.format(name) for name in LOAD_LIST]
        listdir = os.listdir(direct_path)
        for num, module_name in enumerate(LOAD_LIST, GLOBAL.ZERO):
            file_name = file_list[num]
            file_path = os.path.join(direct_path, file_name)
            internal_cfg = getattr(cfg, module_name)
            if file_name in listdir:
                try:
                    if self.updateData(self.getFileData(file_path), internal_cfg):
                        self.createFileInDir(file_path, internal_cfg)
                except Exception as error:
                    self.loadError(file_path, error.message)
                    logWarning('readConfig: {} {}'.format(file_name, repr(error)))
                    continue
            else:
                self.createFileInDir(file_path, internal_cfg)
            g_events.onSettingsChanged(internal_cfg, module_name)
        logInfo('CONFIGURATION UPDATE COMPLETED: {}'.format(configName))
        g_events.onUserConfigUpdateComplete()


c_Loader = ConfigLoader()

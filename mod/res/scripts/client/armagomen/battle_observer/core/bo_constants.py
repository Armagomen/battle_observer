# coding=utf-8
import datetime
import random

from account_helpers.settings_core.settings_constants import GAME
from aih_constants import SHOT_RESULT, CTRL_MODE_NAME
from gui.Scaleform.daapi.view.battle.shared.crosshair.settings import SHOT_RESULT_TO_DEFAULT_COLOR, \
    SHOT_RESULT_TO_ALT_COLOR
from gui.battle_control.battle_constants import FEEDBACK_EVENT_ID
from gui.shared.gui_items.Vehicle import VEHICLE_CLASS_NAME
from helpers import getClientLanguage

today = datetime.date.today()

MOD_NAME = "BATTLE_OBSERVER"
FILE_NAME = "armagomen.battleObserver_{}.wotmod"
MOD_VERSION = "1.32.6"
API_VERSION = "1.10.8"

HEADERS = [('User-Agent', MOD_NAME)]

SOUND_MODES = {'bb21_eu4_Orzanel', 'bb21_ru3_Lebwa', 'eu1_Mailand', 'uniqueCrewSpecialVoice', 'eu4_AwesomeEpicGuys',
               'eu3_Dezgamez', 'bb21_na2_Tragicloss', 'ru1_Lebwa', 'ru3_Amway921', 'bb21_na1_Cabbagemechanic',
               'offspring', 'bb21_ru2_Amway921', 'bb21_ru4_Evilgranny', 'ru4_KorbenDallas', 'bb21_ru2_Korbendailas',
               'bb21_ru1_Yusha', 'celebrity2021_ru', 'buffon', 'bb21_na3_Cmdraf', 'valkyrie1', 'valkyrie2',
               'bb21_eu2_Dakillzor', 'sabaton', 'bb21_ru1_Vspishka', 'bb21_eu3_Newmulti2k', 'racer_ru', 'racer_en',
               'ru2_Yusha', 'bb21_ru4_Nearyou', 'eu2_Skill4ltu', 'bb21_asia2_Summertiger', 'bb21_eu1_Circon',
               'bb21_asia3_Maharlika', 'bb21_ru3_Inspirer', 'bb21_asia1_Mastertortoise', 'celebrity2021_en'}


class SWF:
    def __init__(self):
        pass

    BATTLE = 'modBattleObserver.swf'
    LOBBY = 'modBattleObserverHangar.swf'
    ATTRIBUTE_NAME = 'as_createBattleObserverComp'


class GLOBAL:
    def __init__(self):
        pass

    CONFIG_ERROR = "Incorrect macros in config file."
    ONE_SECOND = 1.0
    ALIGN = "align"
    ALIGN_LIST = ("left", "center", "right")
    ALIGN_LIST_TEST = ("left", "center")
    RU_LOCALIZATION = ('ru', 'uk', 'be')
    ALPHA = "alpha"
    BG_ALPHA = "bgAlpha"
    BLUR_X = "blurX"
    BLUR_Y = "blurY"
    COLOR = "color"
    CUSTOM_COLOR = "customColor"
    DOT = "."
    COMMA_SEP = ", "
    EMPTY_LINE = ""
    ENABLED = "enabled"
    FIRST, LAST = (0, -1)
    GLOW_FILTER = "glowFilter"
    HEIGHT = "height"
    IMG = "img"
    INNER = "inner"
    KNOCKOUT = "knockout"
    LEFT, CENTER, RIGHT = ALIGN_LIST
    SCALE = "scale"
    SETTINGS = "settings"
    SMOOTHING = "smoothing"
    STRENGTH = "strength"
    WIDTH = "width"
    X = "x"
    Y = "y"
    ZERO = FIRST
    F_ZERO = float(FIRST)
    ONE = 1
    TWO = 2
    F_ONE = 1.0
    OUTLINE = "outline"
    ICONS_DIR = "img://gui/maps/icons"
    C_INTERFACE_SPLITTER = "*"
    REPLACE = (("\\t", "<tab>"), ("\\n", "<br>"), ("\\r", "<br>"), ("legue", "league"), ("calcedArmor", "countedArmor"))
    IMG_PARAMS = {"dir": "img://gui/maps/icons/library/efficiency/48x48",
                  "size": "width='24' height='24'",
                  "vspace": "vspace='-13'"}


class URLS:
    def __init__(self):
        pass

    HOST_NAME = "armagomen.bb-t.ru"
    DONATE_UA_URL = "https://donatua.com/@armagomen"
    DONATE_EU_URL = "https://www.donationalerts.com/r/armagomenvs"
    DONATE = {DONATE_UA_URL, DONATE_EU_URL}
    SUPPORT_URL = "https://discord.gg/NuhuhTN"
    UPDATE_GITHUB_API_URL = "https://api.github.com/repos/Armagomen/battle_observer/releases/latest"
    if getClientLanguage().lower() in GLOBAL.RU_LOCALIZATION:
        MESSAGES = ("Поддержите разработку мода. Спасибо что вы с нами.",
                    "Нравится мод ?, не дай автору помереть с голоду.",
                    "Для добавления статистики в мод необходимо собрать деньги на сервер.",
                    "А ты уже поддержал разработку ?",
                    "Мод существует только благодаря вашей поддержке, нет поддержки нет желания что-либо делать.")
    else:
        MESSAGES = ("Please support the development of the 'Battle Observer' mod. Thank you for being with us.",
                    "If you like mod, don't let the author starve to death.",
                    "To add statistics to the mod, you need to rent or buy a server.",
                    "Have you already supported the development?")

    DONATE_MESSAGE = "<b>'Battle Observer'</b><br><br><font color='#ffff73'>{msg}</font><br><br><a href='event:{ua}'>" \
                     "UAH</a> | <a href='event:{all}'>USD/EUR/RUB</a>".format(ua=DONATE_UA_URL, all=DONATE_EU_URL,
                                                                              msg=random.choice(MESSAGES))


class SERVICE_CHANNEL:
    def __init__(self):
        pass

    NAME = "service_channel_filter"
    KEYS = "sys_keys"
    TYPE = "type"
    DATA = "data"
    AUX_DATA = "auxData"
    SYSTEM_CHANNEL_KEYS = {"CustomizationForCredits", "CustomizationForGold", "DismantlingForCredits",
                           "DismantlingForCrystal", "DismantlingForGold", "Information", "MultipleSelling",
                           "PowerLevel", "PurchaseForCredits", "Remove", "Repair", "Restore", "Selling",
                           "autoMaintenance", "customizationChanged", "PurchaseForCrystal",
                           "PurchaseForGold", "GameGreeting"}


class MAIN:
    def __init__(self):
        pass

    AUTO_CLEAR_CACHE = "autoClearCache"
    ENABLE_BARS_ANIMATION = "enableBarsAnimation"
    ENABLE_FPS_LIMITER = "fps_enableFPSLimiter"
    HIDE_BADGES = "hideBadges"
    HIDE_CHAT = "hideChatInRandom"
    HIDE_CLAN_ABBREV = "hideClanAbbrev"
    HIDE_DOG_TAGS = "hide_dog_tags"
    MAX_FRAME_RATE = "fps_maxFrameRate"
    NAME = "main"
    REMOVE_SHADOW_IN_PREBATTLE = "removeShadowInPrebattle"
    SHOW_FRIENDS = "showFriendsAndClanInEars"
    SHOW_ANONYMOUS = "anonymousEnableShow"
    ANONYMOUS_STRING = "anonymousString"
    CHANGE_ANONYMOUS_NAME = "anonymousNameChange"
    USE_KEY_PAIRS = "useKeyPairs"
    REMOVE_HANDBRAKE = "removeHandbrake"
    IGNORE_COMMANDERS = "ignore_commanders_voice"
    DISABLE_SCORE_SOUND = "disable_score_sound"
    HIDE_SERVER_IN_HANGAR = "hide_server_in_hangar"
    DEBUG = "DEBUG_MODE"


class COLORS:
    def __init__(self):
        pass

    NAME = "colors"
    BLACK = "#000000"
    BLIND = "#6F6CD3"
    B_SILVER = "#858585"
    GOLD = "#FFD700"
    GREEN = "#5ACB00"
    NORMAL_TEXT = "#FAFAFA"
    ORANGE = "#FF9900"
    RED = "#F30900"
    S_YELLOW = "#E0E06D"
    YELLOW = "#FFC900"
    C_GREEN = "green"
    C_ORANGE = "orange"
    C_RED = "red"
    C_YELLOW = "yellow"
    C_PURPLE = "purple"
    C_BG = "bgColor"
    GLOBAL = "global"
    ALLY_MAME = "ally"
    ENEMY_MAME = "enemy"
    ENEMY_BLIND_MAME = "enemyColorBlind"
    DEAD_COLOR = "deadColor"


class MAIN_GUN:
    def __init__(self):
        pass

    NAME = "main_gun"
    COLOR = "mainGunColor"
    TEMPLATE = "template"
    GUN_ICON = "mainGunIcon"
    DONE_ICON, FAILURE_ICON = ("mainGunDoneIcon", "mainGunFailureIcon")
    MIN_GUN_DAMAGE = 1000
    DAMAGE_RATE = 0.2


class MINIMAP:
    def __init__(self):
        pass

    DEATH_PERMANENT = "permanentMinimapDeath"
    HOT_KEY = "zoom_hotkey"
    INDENT = "indent"
    NAME = "minimap"
    SHOW_NAMES = "showDeathNames"
    ZOOM = "zoom"


class HP_BARS:
    def __init__(self):
        pass

    NAME = "hp_bars"
    STYLE = "style"
    NORMAL_STYLE = "normal"
    LEAGUE_STYLE = "league"
    WIDTH = "barsWidth"
    DIFF = "differenceHP"
    ALIVE = "showAliveCount"
    STYLE_SELECT = (NORMAL_STYLE, LEAGUE_STYLE)


class CLOCK:
    def __init__(self):
        pass

    NAME = "clock"
    IN_BATTLE = "battle"
    IN_LOBBY = "hangar"
    FORMAT = "format"
    PREMIUM_TIME = "premium_time"
    UPDATE_INTERVAL = 1.0
    DEFAULT_FORMAT_BATTLE = "<textformat tabstops='[120]'>%d %b %Y<tab>%X</textformat>"
    DEFAULT_FORMAT_HANGAR = "<textformat tabstops='[135]'>%d %b %Y<tab>%X</textformat>"
    DEFAULT_FORMAT_PREMIUM = "%(days)d Дн. %(hours)02d:%(minutes)02d:%(seconds)02d"


class SNIPER:
    def __init__(self):
        pass

    ZOOM = "zoom"
    NAME = ZOOM
    DYN_ZOOM = "dynamic_zoom"
    STEPS_ONLY = "steps_only"
    ZOOM_STEPS = "zoomSteps"
    STEPS = "steps"
    GUN_ZOOM = "zoomToGunMarker"
    METERS = "zoomXMeters"
    ZOOMS = "zooms"
    ZOOM_EXPOSURE = "zoomExposure"
    INCREASED_ZOOM = "increasedZoom"
    DEFAULT_STEPS = [2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 16.0, 20.0, 25.0]
    EXPOSURE_FACTOR, MAX_CALIBER = (0.1, 40)
    DISABLE_SNIPER = "disable_cam_after_shoot"
    SKIP_CLIP = "disable_cam_skip_clip"
    CLIP = "clip"
    MAX_DIST = 730.0


class DAMAGE_LOG:
    def __init__(self):
        pass

    NAME = "damage_log"
    ALL_DAMAGES = "allDamages"
    ASSIST_DAMAGE = "assistDamage"
    ASSIST_STUN = "stun"
    ATTACK_REASON = "attackReason"
    AVG_COLOR = "avgColor"
    AVG_DAMAGE = "tankAvgDamage"
    AVG_DAMAGE_DATA = 0.0
    BLOCKED_DAMAGE = "blockedDamage"
    CLASS_COLOR = "tankClassColor"
    MAX_HEALTH = "max_health"
    CLASS_ICON = "classIcon"
    COLOR_MAX_PURPLE, COLOR_MAX_GREEN, COLOR_MULTIPLIER = (0.8333, 0.3333, 255)
    COLOR_FORMAT = "#{:02X}{:02X}{:02X}"
    DAMAGE_AVG_COLOR = "tankDamageAvgColor"
    DAMAGE_LIST = "damageList"
    DONE_EXTENDED = "log_damage_extended"
    D_LOG = "d_log"
    IN_LOG = "in_log"
    TOP_LOG_ASSIST = {FEEDBACK_EVENT_ID.PLAYER_ASSIST_TO_KILL_ENEMY, FEEDBACK_EVENT_ID.PLAYER_ASSIST_TO_STUN_ENEMY,
                      FEEDBACK_EVENT_ID.PLAYER_USED_ARMOR}
    EXTENDED_DAMAGE = {FEEDBACK_EVENT_ID.PLAYER_DAMAGED_HP_ENEMY, FEEDBACK_EVENT_ID.ENEMY_DAMAGED_HP_PLAYER}
    GLOBAL = "log_global"
    HOT_KEY = "logsAltmode_hotkey"
    ICONS = "icons"
    ICON_NAME = "iconName"
    INDEX = "index"
    IN_CENTER = "inCenter"
    KILLED_ICON = "killedIcon"
    KILLS = "kills"
    LAST_DAMAGE = "lastDamage"
    LOG_MAX_LEN = 13
    LOG_MODE = ("extendedLog", "extendedLogALTMODE")
    MAIN_LOG = "main"
    NEW_LINE, COMMA, LIST_SEPARATOR = ("<br>", ", ", " <font color='#FFFF00'>|</font> ")
    PERCENT_AVG_COLOR = "percentDamageAvgColor"
    PLAYER_DAMAGE = "playerDamage"
    RANDOM_MIN_AVG, FRONT_LINE_MIN_AVG = (1200.0, 4000.0)
    RECEIVED_EXTENDED = "log_input_extended"
    REVERSE = "reverse"
    SHELL = ("normal", "gold")
    NORMAL, GOLD = SHELL
    SHELL_COLOR = "shellColor"
    SHELL_TYPE = "shellType"
    SHELL_ICON = "shellIcon"
    SHELL_TYPES = "shellTypes"
    SHELL_ICONS = "shellIcons"
    SHOTS = "shots"
    SPOTTED_TANKS = "spottedTanks"
    STUN_ICON = "stunIcon"
    TANK_LEVEL = "TankLevel"
    TANK_NAME = "tankName"
    TANK_NAMES = "tankNames"
    TEMPLATE_MAIN_DMG = "templateMainDMG"
    TOP_MACROS_NAME = {
        FEEDBACK_EVENT_ID.PLAYER_DAMAGED_HP_ENEMY: PLAYER_DAMAGE,
        FEEDBACK_EVENT_ID.PLAYER_USED_ARMOR: BLOCKED_DAMAGE,
        FEEDBACK_EVENT_ID.PLAYER_ASSIST_TO_KILL_ENEMY: ASSIST_DAMAGE,
        FEEDBACK_EVENT_ID.PLAYER_SPOTTED_ENEMY: SPOTTED_TANKS,
        FEEDBACK_EVENT_ID.PLAYER_ASSIST_TO_STUN_ENEMY: ASSIST_STUN,
        FEEDBACK_EVENT_ID.DESTRUCTIBLE_DAMAGED: PLAYER_DAMAGE
    }
    TOP_LOG = "log_total"
    TOTAL_DAMAGE = "totalDamage"
    UNKNOWN_TAG = "unknown"
    USER_NAME = "userName"
    VEHICLE_CLASS = "vehicleClass"
    VEHICLE_CLASS_COLORS = "vehicleClassColors"
    VEHICLE_CLASS_ICON = "vehicleClassIcon"
    WG_ASSIST = "wg_log_hide_assist"
    WG_BLOCKED = "wg_log_hide_block"
    WG_CRITS = "wg_log_hide_crits"
    WG_POS = "wg_log_pos_fix"
    UNDEFINED = "UNDEFINED"
    PREMIUM = "_PREMIUM"
    PREMIUM_SHELLS = {"ARMOR_PIERCING_CR_PREMIUM", "ARMOR_PIERCING_PREMIUM",
                      "HIGH_EXPLOSIVE_PREMIUM", "HOLLOW_CHARGE_PREMIUM"}
    WARNING_MESSAGE = "incorrect event parameter for the damage log"


class ARCADE:
    def __init__(self):
        pass

    ANGLE = -0.22
    DIST_RANGE = "distRange"
    MAX = "max"
    MIN = "min"
    NAME = "arcade_camera"
    START_ANGLE = "startAngle"
    START_DEAD_DIST = "startDeadDist"
    START_DIST = "startDist"
    SCROLL_MULTIPLE = "scrollMultiple"
    SCROLL_SENSITIVITY = "scrollSensitivity"


class STRATEGIC:
    def __init__(self):
        pass

    NAME = "strategic_camera"
    MIN = "min"
    MAX = "max"
    DIST_RANGE = "distRange"


class POSTMORTEM:
    def __init__(self):
        pass

    DURATION = "transitionDuration"
    PARAMS = "postmortemParams"
    CAM_MATRIX = "camMatrix"
    MODES = {CTRL_MODE_NAME.POSTMORTEM, CTRL_MODE_NAME.DEATH_FREE_CAM}


class ARMOR_CALC:
    def __init__(self):
        pass

    GREAT_PIERCED, NOT_PIERCED = 0.75, 1.25
    HALF = 0.35
    PIERCING_POWER = "piercingPower"
    NORMAL = SHOT_RESULT_TO_DEFAULT_COLOR[SHOT_RESULT.UNDEFINED]
    NAME = "armor_calculator"
    POSITION = "calcPosition"
    MESSAGES = "messages"
    TEMPLATE = "template"
    MACROS_COLOR = "color"
    MACROS_COUNTED_ARMOR = "countedArmor"
    MACROS_ARMOR = "armor"
    MACROS_PIERCING_RESERVE = "piercingReserve"
    MACROS_MESSAGE = "message"
    MACROS_CALIBER = "caliber"
    MACROS_RICOCHET = "ricochet"
    NONE_DATA = (SHOT_RESULT.UNDEFINED, None, None, None, None)
    MESSAGE_COLORS = set(SHOT_RESULT_TO_ALT_COLOR.itervalues())
    MESSAGE_COLORS.update(SHOT_RESULT_TO_DEFAULT_COLOR.itervalues())
    MESSAGES_TEMPLATE = {key: "<font size='20' color='#FAFAFA'>Change me in config.</font>" for key in MESSAGE_COLORS}


class VEHICLE:
    def __init__(self):
        pass

    CUR, MAX, TEAM, PERCENT = ("health", "maxHealth", "team", "percent")


class MARKERS:
    def __init__(self):
        pass

    NAME = "markers"
    HOT_KEY = "showMarkers_hotkey"
    CLASS_COLOR = "markersClassColor"
    TYPE_ICON = {
        VEHICLE_CLASS_NAME.HEAVY_TANK: "H",
        VEHICLE_CLASS_NAME.MEDIUM_TANK: "M",
        VEHICLE_CLASS_NAME.AT_SPG: "J",
        VEHICLE_CLASS_NAME.SPG: "S",
        VEHICLE_CLASS_NAME.LIGHT_TANK: "L",
        "unknown": "U"
    }
    ICON = "<font color='{0}'>{1}</font>"


class CAROUSEL:
    def __init__(self):
        pass

    NAME = "tank_carousel"
    SMALL = "smallDoubleCarousel"
    ROWS = "carouselRows"
    SETTINGS = {GAME.CAROUSEL_TYPE: None, GAME.DOUBLE_CAROUSEL_TYPE: None}


class USER_BACKGROUND:
    def __init__(self):
        pass

    NAME = "user_background"
    LABELS = NAME
    CENTERED_X = "centeredX"
    CENTERED_Y = "centeredY"
    LAYER = "layer"


class FLIGHT_TIME:
    def __init__(self):
        pass

    NAME = "flight_time"
    SPG_ONLY = "spgOnly"
    TEMPLATE = "template"
    M_FLIGHT_TIME = "flightTime"
    M_DISTANCE = "distance"
    ALIGN = "align"


class VEHICLE_TYPES:
    def __init__(self):
        pass

    NAME = "vehicle_types"
    CLASS_COLORS = "vehicleClassColors"
    CLASS_ICON = "vehicleClassIcon"
    UNKNOWN = "unknown"
    TEMPLATE = "<font face='BattleObserver' size='20'>{}</font>"


class SIXTH_SENSE:
    def __init__(self):
        pass

    NAME = "sixth_sense"
    SHOW_TIMER = "showTimer"
    PLAY_TICK_SOUND = "playTickSound"
    TIME = "lampShowTime"
    TIMER = "timer"
    TEMPLATE = "TimerTemplate"
    IMAGE = "image"
    M_TIME = "lampTime"
    M_TIME_LEFT = "timeLeft"


class DISPERSION:
    def __init__(self):
        pass

    NAME = "dispersion_circle"
    CIRCLE_EXTRA_LAP = "circle_extraServerLap"
    CIRCLE_REPLACE = "circle_replaceOriginalCircle"
    CIRCLE_SCALE_CONFIG = "circle_scale"
    CIRCLE_SERVER = "useServerAim"
    ENABLED = "circle_enabled"
    CIRCLE_SCALE = 0.80
    SCALE = 80
    MAX_TIME = 5.0
    SPG_GM_SCALE = 0.8
    GUN_MARKER_MIN_SIZE = 16.0
    MINUS_ONE_F = -1.0

    TIMER_ENABLED = "timer_enabled"
    TIMER_POSITION_X = "timer_position_x"
    TIMER_POSITION_Y = "timer_position_y"
    TIMER_COLOR = "timer_color"
    TIMER_DONE_COLOR = "timer_done_color"
    TIMER_DONE_TEMPLATE = "timer_done_template"
    TIMER_REGULAR_TEMPLATE = "timer_regular_template"
    TIMER_ALIGN = "timer_align"


class DEBUG_PANEL:
    def __init__(self):
        pass

    NAME = "debug_panel"
    TEXT = "debugText"
    TEMPLATE = "text"
    GRAPHICS = "debugGraphics"
    PING_BAR = "pingBar"
    FPS_BAR = "fpsBar"
    FPS_COLOR = "fpsColor"
    PING_COLOR = "pingColor"
    LAG_COLOR = "pingLagColor"
    PING = "PING"
    FPS = "FPS"
    LAG = "PingLagColor"


class BATTLE_TIMER:
    def __init__(self):
        pass

    NAME = "battle_timer"
    TEMPLATE = "timerTemplate"
    COLOR = "timerColor"
    END_COLOR = "timerColorEndBattle"
    M_TIMER = "timer"
    TIME_FORMAT = "%02d:%02d"
    START_STRING = "00:00"
    END_BATTLE_SEC = 120


class EFFECTS:
    def __init__(self):
        pass

    NAME = "effects"
    NO_FLASH_BANG = "noFlashBang"
    NO_SHOCK_WAVE = "noShockWave"
    # NO_LIGHT_EFFECT = "noLightEffect"
    NO_BINOCULARS = "noBinoculars"
    # ENTITY = "entity"
    IS_PLAYER_VEHICLE = "isPlayerVehicle"
    SHOW_FLASH_BANG = "showFlashBang"
    SHOW_SHOCK_WAVE = "showShockWave"


class TEAM_BASES:
    def __init__(self):
        pass

    NAME = "team_bases_panel"
    TEXT_SETTINGS = "text_settings"
    FONT = "font"
    SIZE = "size"
    BOLD = "bold"
    ITALIC = "italic"
    UNDERLINE = "underline"
    BASE_FONT = "$TitleFont"
    FONT_SIZE = 16
    HUNDRED = 100.0


class ALIASES:
    def __init__(self):
        pass

    HP_BARS = "Observer_TeamsHP_UI"
    DAMAGE_LOG = "Observer_DamageLog_UI"
    MAIN_GUN = "Observer_MainGun_UI"
    DEBUG = "Observer_DebugPanel_UI"
    TIMER = "Observer_BattleTimer_UI"
    SIXTH_SENSE = "Observer_SixthSense_UI"
    TEAM_BASES = "Observer_TeamBases_UI"
    ARMOR_CALC = "Observer_ArmorCalculator_UI"
    FLIGHT_TIME = "Observer_FlightTime_UI"
    DISPERSION_TIMER = "Observer_DispersionTimer_UI"
    PANELS = "Observer_PlayersPanels_UI"
    MINIMAP = "Observer_Minimap_UI"
    USER_BACKGROUND = "Observer_UserBackGround_UI"
    WG_COMP = "Observer_WGCompSettings_UI"
    DATE_TIME = "Observer_DateTimes_UI"


class PANELS:
    def __init__(self):
        pass

    PANELS_NAME = "players_panels"
    # icons
    ICONS_BLACKOUT = "panels_icon_filter_strength"
    ICONS_ENABLED = "panels_icon_enabled"
    # hp_bars
    BARS_ENABLED = "players_bars_enabled"
    BAR_SETTINGS = "players_bars_settings"
    TEXT_SETTINGS = "players_bars_text"
    BAR = "players_bars_bar"
    HP_TEMPLATE = "players_bars_hp_text"
    ON_KEY_DOWN = "players_bars_on_key_pressed"
    BAR_HOT_KEY = "players_bars_hotkey"
    BAR_CLASS_COLOR = "players_bars_classColor"
    # players_damages
    DAMAGES_ENABLED = "players_damages_enabled"
    DAMAGES_TEMPLATE = "players_damages_text"
    DAMAGES_SETTINGS = "players_damages_settings"
    DAMAGES_HOT_KEY = "players_damages_hotkey"
    DAMAGES_TF = "DamageTf"
    # another
    SPOTTED_FIX = "panels_spotted_fix"
    DAMAGE = "damage"
    TEAM = ("green", "red")


class SAVE_SHOOT:
    def __init__(self):
        pass

    NAME = "save_shoot"
    MSG = "msg"
    TEMPLATE = "Shot blocked."
    DESTROYED_BLOCK = "block_on_destroyed"
    VEHICLE = "Vehicle"
    TEAM = "team"
    HOT_KEY = "shoot_hotkey"


class ANOTHER:
    def __init__(self):
        pass

    CONFIG_SELECT = "configSelect"
    SHADOW_SETTINGS = "shadow_settings"
    FRIEND_LIST = "friendList"
    ACCOUNT_DBID = "accountDBID"
    USERS = "users"
    DBID = "databaseID"
    BADGES = "badges"
    IS_TEAM_KILLER = "isTeamKiller"
    NAME = "name"
    CLAN_DBID = "clanDBID"
    CLAN_ABBR = "clanAbbrev"


class MASSAGES:
    def __init__(self):
        pass

    START = "START LOADING"
    FINISH = "SHUTTING DOWN"
    LOCKED_BY_FILE_NAME = "ERROR: file {} is not valid, mod locked, please install mod from official site"
    UPDATE_CHECKED = "The update check is completed, you have the current version."
    NEW_VERSION = "An update {} is detected, the client will be restarted at the end of the download."


LOAD_LIST = (
    HP_BARS.NAME, MAIN.NAME, MAIN_GUN.NAME, DEBUG_PANEL.NAME, BATTLE_TIMER.NAME, DISPERSION.NAME,
    VEHICLE_TYPES.NAME, SNIPER.NAME, COLORS.NAME, ARMOR_CALC.NAME, TEAM_BASES.NAME, FLIGHT_TIME.NAME,
    SERVICE_CHANNEL.NAME, ARCADE.NAME, STRATEGIC.NAME, PANELS.PANELS_NAME, MINIMAP.NAME, EFFECTS.NAME,
    DAMAGE_LOG.GLOBAL, DAMAGE_LOG.TOP_LOG, DAMAGE_LOG.DONE_EXTENDED, DAMAGE_LOG.RECEIVED_EXTENDED, SAVE_SHOOT.NAME,
    SIXTH_SENSE.NAME, USER_BACKGROUND.NAME, ANOTHER.SHADOW_SETTINGS, CAROUSEL.NAME, CLOCK.NAME
)

CACHE_DIRS = (
    "account_caches", "battle_results", "clan_cache", "custom_data", "dossier_cache", "messenger_cache",
    "storage_cache", "tutorial_cache", "veh_cmp_cache", "web_cache", "profile"
)


class CONFIG_INTERFACE:
    def __init__(self):
        pass

    DONATE_BUTTONS = ('donate_button_ua', 'donate_button_ru', 'donate_button_eu', 'support_button')
    BLOCK_IDS = (
        ANOTHER.CONFIG_SELECT, MAIN.NAME, DISPERSION.NAME, CAROUSEL.NAME, EFFECTS.NAME, DEBUG_PANEL.NAME,
        BATTLE_TIMER.NAME, CLOCK.NAME, HP_BARS.NAME, ARMOR_CALC.NAME, DAMAGE_LOG.GLOBAL,
        DAMAGE_LOG.TOP_LOG, DAMAGE_LOG.DONE_EXTENDED, DAMAGE_LOG.RECEIVED_EXTENDED, MAIN_GUN.NAME, TEAM_BASES.NAME,
        VEHICLE_TYPES.NAME, PANELS.PANELS_NAME, SNIPER.NAME, ARCADE.NAME, STRATEGIC.NAME, FLIGHT_TIME.NAME,
        SAVE_SHOOT.NAME, MINIMAP.NAME, ANOTHER.SHADOW_SETTINGS, SIXTH_SENSE.NAME, COLORS.NAME, SERVICE_CHANNEL.NAME
    )
    HANDLER_VALUES = {
        SNIPER.NAME: {
            'dynamic_zoom*enabled': (
                'dynamic_zoom*steps_only',
                'dynamic_zoom*zoomXMeters'
            ),
            'zoomSteps*enabled': ('zoomSteps*steps',),
            SNIPER.DISABLE_SNIPER: (SNIPER.SKIP_CLIP,)
        },
        TEAM_BASES.NAME: {
            'outline*enabled': ('outline*color',)
        },
        PANELS.PANELS_NAME: {
            "players_bars_enabled": (
                "players_bars_settings*players_bars_bar*outline*enabled",
                "players_bars_settings*players_bars_bar*outline*customColor",
                "players_bars_settings*players_bars_bar*outline*color",
                "players_bars_settings*players_bars_bar*outline*alpha",
                "players_bars_hotkey",
                "players_bars_classColor",
                "players_bars_on_key_pressed",
            ),
            'players_bars_settings*players_bars_bar*outline*customColor': (
                'players_bars_settings*players_bars_bar*outline*color',
            ),
            'players_bars_settings*players_bars_bar*outline*enabled': (
                'players_bars_settings*players_bars_bar*outline*color',
                'players_bars_settings*players_bars_bar*outline*alpha',
                'players_bars_settings*players_bars_bar*outline*customColor'
            ),
            'players_damages_enabled': (
                'players_damages_hotkey', 'players_damages_settings*x', 'players_damages_settings*y'
            ),
            "panels_icon_enabled": ("panels_icon_filter_strength",)
        },
        ARMOR_CALC.NAME: {
            'showCalcPoints': ('calcPosition*x', 'calcPosition*y', 'template')
        },
        MAIN.NAME: {
            MAIN.ENABLE_FPS_LIMITER: (MAIN.MAX_FRAME_RATE,),
            MAIN.SHOW_ANONYMOUS: (MAIN.CHANGE_ANONYMOUS_NAME,)
        },
        HP_BARS.NAME: {
            'outline*enabled': ('outline*color',),
            'markers*enabled': ("markers*x", "markers*y", "markers*showMarkers_hotkey", "markers*markersClassColor")
        },
        MINIMAP.NAME: {
            'zoom*enabled': ('zoom*zoom_hotkey', 'zoom*indent'),
            MINIMAP.DEATH_PERMANENT: (MINIMAP.SHOW_NAMES,)
        },
        DEBUG_PANEL.NAME: {
            'debugGraphics*enabled': (
                'debugGraphics*pingBar*enabled', 'debugGraphics*fpsBar*enabled', 'debugGraphics*pingBar*color',
                'debugGraphics*fpsBar*color')
        },
        CLOCK.NAME: {
            'hangar*enabled': ('hangar*format', 'hangar*x', 'hangar*y'),
            'battle*enabled': ('battle*format', 'battle*x', 'battle*y')
        },
        SIXTH_SENSE.NAME: {
            SIXTH_SENSE.SHOW_TIMER: (SIXTH_SENSE.PLAY_TICK_SOUND,)
        },
        "reversed_values": {PANELS.BAR_CLASS_COLOR},
        DISPERSION.NAME: {
            DISPERSION.TIMER_ENABLED: (DISPERSION.TIMER_REGULAR_TEMPLATE,
                                       DISPERSION.TIMER_DONE_TEMPLATE,
                                       DISPERSION.TIMER_DONE_COLOR,
                                       DISPERSION.TIMER_COLOR,
                                       DISPERSION.TIMER_POSITION_X,
                                       DISPERSION.TIMER_POSITION_Y,
                                       DISPERSION.TIMER_ALIGN),
            DISPERSION.ENABLED: (DISPERSION.CIRCLE_SCALE_CONFIG,
                                 DISPERSION.CIRCLE_EXTRA_LAP,
                                 DISPERSION.CIRCLE_REPLACE)
        }
    }


ALIAS_TO_PATH = {
    ALIASES.HP_BARS: ".teams_hp",
    ALIASES.DAMAGE_LOG: ".damage_log",
    ALIASES.MAIN_GUN: ".main_gun",
    ALIASES.DEBUG: ".debug_panel",
    ALIASES.TIMER: ".battle_timer",
    ALIASES.SIXTH_SENSE: ".sixth_sense",
    ALIASES.TEAM_BASES: ".team_bases",
    ALIASES.ARMOR_CALC: ".armor_calculator",
    ALIASES.FLIGHT_TIME: ".flight_time",
    ALIASES.DISPERSION_TIMER: ".dispersion_timer",
    ALIASES.PANELS: ".players_panels",
    ALIASES.MINIMAP: ".minimap",
    ALIASES.USER_BACKGROUND: ".user_background",
    ALIASES.WG_COMP: ".wg_comp_settings",
    ALIASES.DATE_TIME: ".date_times"
}

ALIAS_TO_CONFIG_NAME = {
    ALIASES.HP_BARS: HP_BARS.NAME,
    ALIASES.DAMAGE_LOG: DAMAGE_LOG.NAME,
    ALIASES.MAIN_GUN: MAIN_GUN.NAME,
    ALIASES.DEBUG: DEBUG_PANEL.NAME,
    ALIASES.TIMER: BATTLE_TIMER.NAME,
    ALIASES.SIXTH_SENSE: SIXTH_SENSE.NAME,
    ALIASES.TEAM_BASES: TEAM_BASES.NAME,
    ALIASES.ARMOR_CALC: ARMOR_CALC.NAME,
    ALIASES.FLIGHT_TIME: FLIGHT_TIME.NAME,
    ALIASES.DISPERSION_TIMER: DISPERSION.NAME,
    ALIASES.PANELS: PANELS.PANELS_NAME,
    ALIASES.MINIMAP: MINIMAP.NAME,
    ALIASES.USER_BACKGROUND: USER_BACKGROUND.NAME,
    ALIASES.DATE_TIME: CLOCK.NAME,
    ALIASES.WG_COMP: MAIN.NAME
}

SORTED_ALIASES = (
    ALIASES.WG_COMP, ALIASES.MAIN_GUN, ALIASES.HP_BARS, ALIASES.DAMAGE_LOG, ALIASES.DEBUG, ALIASES.TIMER,
    ALIASES.SIXTH_SENSE, ALIASES.TEAM_BASES, ALIASES.ARMOR_CALC, ALIASES.FLIGHT_TIME, ALIASES.DISPERSION_TIMER,
    ALIASES.PANELS, ALIASES.MINIMAP, ALIASES.USER_BACKGROUND, ALIASES.DATE_TIME
)

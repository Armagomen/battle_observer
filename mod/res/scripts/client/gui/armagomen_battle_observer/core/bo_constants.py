# coding=utf-8
from account_helpers.settings_core.settings_constants import GAME
from aih_constants import SHOT_RESULT
from constants import SHELL_TYPES_LIST
from gui.battle_control.battle_constants import FEEDBACK_EVENT_ID as EV_ID
from gui.shared.gui_items.Vehicle import VEHICLE_CLASS_NAME
from vehicle_systems.tankStructure import TankPartIndexes

MOD_NAME = "BATTLE_OBSERVER"
FILE_NAME = "armagomen.battleObserver_{}.wotmod"
MOD_PATH = "gui.armagomen_battle_observer.{}"
MOD_VERSION = "1.32.0"
API_VERSION = "1.10.8"

HEADERS = [('User-Agent', MOD_NAME)]


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
    DEBUG_MODE = False
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
    SPACE = " "
    DOUBLE_UNDERLINE = "__"
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
    F_ONE = 1.0
    OUTLINE = "outline"
    ICONS_DIR = "img://gui/maps/icons"
    C_INTERFACE_SPLITTER = "*"
    REPLACE = (("\\t", "<tab>"), ("\\n", "<br>"), ("\\r", "<br>"))
    IMG_PARAMS = {"dir": "img://gui/maps/icons/library/efficiency/48x48",
                  "size": "width='24' height='24'",
                  "vspace": "vspace='-13'"}


class URLS:
    def __init__(self):
        pass

    HOST_NAME = "armagomen.bb-t.ru"
    DONATE_UA_URL = "https://donatua.com/@armagomen"
    DONATE_EU_URL = "https://www.donationalerts.com/r/armagomenvs"
    SUPPORT_URL = "https://discord.gg/NuhuhTN"
    UPDATE_GITHUB_API_URL = "https://api.github.com/repos/Armagomen/battle_observer/releases/latest"
    DONATE_RU_MESSAGE = "<font color='#ffff73'>" \
                        "Поддержите разработку мода 'Battle Observer'. Спасибо что вы с нами." \
                        "</font><br><br>" \
                        "<a href='event:{ua}'>UAH</a> | <a href='event:{all}'>USD/EUR/RUB</a>" \
                        "<br><br>Если ссылки не работают: откройте меню настроек мода и " \
                        "выбирайте там нужную ссылку.".format(ua=DONATE_UA_URL, all=DONATE_EU_URL)
    DONATE_EU_MESSAGE = "<font color='#ffff73'>" \
                        "Support the development of the 'Battle Observer' mod. Thank you for being with us." \
                        "</font><br><br>" \
                        "<a href='event:{ua}'>UAH</a> | <a href='event:{all}'>USD/EUR/RUB</a>" \
                        "<br><br>If the links do not work: open the mod's settings menu and select the desired" \
                        " link there.".format(ua=DONATE_UA_URL, all=DONATE_EU_URL)


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
    BG = "background"
    BG_TRANSPARENCY = "backgroundTransparency"
    ENABLE_BARS_ANIMATION = "enableBarsAnimation"
    ENABLE_FPS_LIMITER = "fps_enableFPSLimiter"
    HIDE_BADGES = "hideBadges"
    HIDE_CHAT = "hideChatInRandom"
    HIDE_CLAN_ABBREV = "hideClanAbbrev"
    MAX_FRAME_RATE = "fps_maxFrameRate"
    NAME = "main"
    REMOVE_SHADOW_IN_PREBATTLE = "removeShadowInPrebattle"
    SHOW_FRIENDS = "showFriendsAndClanInEars"
    SHOW_ANONYMOUS = "anonymousEnableShow"
    ANONYMOUS_STRING = "anonymousString"
    CHANGE_ANONYMOUS_NAME = "anonymousNameChange"
    USE_KEY_PAIRS = "useKeyPairs"
    REMOVE_HANDBRAKE = "removeHandbrake"
    HIDE_POSTMORTEM_TIPS = "hide_postmortem_tips"


class COLORS:
    def __init__(self):
        pass

    NAME = "colors"
    BLACK = "#000000"
    BLIND = "#6F6CD3"
    PURPLE = "#6A0DAD"
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
    LEGUE_STYLE = "legue"
    WIDTH = "barsWidth"
    DIFF = "differenceHP"
    ALIVE = "showAliveCount"
    C_ALLY = "ally"
    C_ENEMY = "enemy"
    C_BLIND = "enemyColorBlind"
    STYLE_SELECT = (NORMAL_STYLE, LEGUE_STYLE)


class CLOCK:
    def __init__(self):
        pass

    NAME = "clock"
    IN_BATTLE = "battle"
    IN_LOBBY = "hangar"
    FORMAT = "format"
    UPDATE_INTERVAL = 0.5
    DEFAULT_FORMAT_BATTLE = "<textformat tabstops='[120]'>%d %b %Y<tab>%X</textformat>"
    DEFAULT_FORMAT_HANGAR = "<textformat tabstops='[135]'>%d %b %Y<tab>%X</textformat>"


class SNIPER:
    def __init__(self):
        pass

    MIN, MAX, ZMX = (0, 1, 2)
    ZOOM = "zoom"
    NAME = ZOOM
    DYN_ZOOM = "dynamic_zoom"
    ZOOM_STEPS = "zoomSteps"
    STEPS = "steps"
    GUN_ZOOM = "zoomToGunMarker"
    METERS = "zoomXMeters"
    MAX_ZOOM_NUM = "zoom_max"
    MIN_ZOOM_NUM = "zoom_min"
    ZOOMS = "zooms"
    ZOOM_EXPOSURE = "zoomExposure"
    INCREASED_ZOOM = "increasedZoom"
    DEFAULT_STEPS = [2.0, 4.0, 8.0, 12.0, 16.0, 20.0, 24.0, 28.0]
    ONE, EXPOSURE_FACTOR, MAX_CALIBER = (1, 0.1, 40)
    DISABLE_AFTER_SHOOT = "disable_cam_after_shoot"
    SKIP_CLIP = "disable_cam_skip_clip"
    CLIP = "clip"


class DAMAGE_LOG:
    def __init__(self):
        pass

    ALL_DAMAGES = "allDamages"
    ASSIST_DAMAGE = "assistDamage"
    ASSIST_STUN = "stun"
    ATTACK_REASON = "attackReason"
    AVG_COLOR = "avgColor"
    AVG_DAMAGE = "tankAvgDamage"
    BLOCKED_DAMAGE = "blockedDamage"
    CLASS_COLOR = "tankClassColor"
    CLASS_ICON = "classIcon"
    COLOR_MAX_PURPLE, COLOR_MAX_GREEN, COLOR_MULTIPLIER = (0.8333, 0.3333, 255)
    COLOR_FORMAT = "#{:02X}{:02X}{:02X}"
    DAMAGE_AVG_COLOR = "tankDamageAvgColor"
    DAMAGE_LIST = "damageList"
    DONE_EXTENDED = "log_damage_extended"
    D_LOG = "d_log"
    IN_LOG = "in_log"
    E_TYPES = {
        EV_ID.PLAYER_SPOTTED_ENEMY,
        EV_ID.PLAYER_DAMAGED_HP_ENEMY,
        EV_ID.PLAYER_ASSIST_TO_KILL_ENEMY,
        EV_ID.PLAYER_ASSIST_TO_STUN_ENEMY,
        EV_ID.PLAYER_USED_ARMOR,
        EV_ID.DESTRUCTIBLE_DAMAGED
    }
    TOP_LOG_ASSIST = {EV_ID.PLAYER_ASSIST_TO_KILL_ENEMY, EV_ID.PLAYER_ASSIST_TO_STUN_ENEMY, EV_ID.PLAYER_USED_ARMOR}
    EXTENDED_DAMAGE = {EV_ID.PLAYER_DAMAGED_HP_ENEMY, EV_ID.ENEMY_DAMAGED_HP_PLAYER}
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
    RANDOM_MIN_AVG, FRONT_LINE_MIN_AVG = (1000.0, 4000.0)
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
        EV_ID.PLAYER_DAMAGED_HP_ENEMY: PLAYER_DAMAGE,
        EV_ID.PLAYER_USED_ARMOR: BLOCKED_DAMAGE,
        EV_ID.PLAYER_ASSIST_TO_KILL_ENEMY: ASSIST_DAMAGE,
        EV_ID.PLAYER_SPOTTED_ENEMY: SPOTTED_TANKS,
        EV_ID.PLAYER_ASSIST_TO_STUN_ENEMY: ASSIST_STUN,
        EV_ID.DESTRUCTIBLE_DAMAGED: PLAYER_DAMAGE
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
    SHELL_LIST = SHELL_TYPES_LIST + tuple(PREMIUM_SHELLS)
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

    CALLBACK_TIME_SEC = 1.0
    TRANSITION = "postmortemTransition"
    DURATION = "transitionDuration"
    PARAMS = "postmortemParams"
    NAME = "postmortem_panel"


class ARMOR_CALC:
    def __init__(self):
        pass

    BACKWARD_LENGTH = 0.1
    DEFAULT_MESSAGES = {"green": "100%", "orange": "50%", "red": "0%", "yellow": "50%", "purple": "0%"}
    EFFECTIVE_DISTANCE = 400.0
    FORWARD_LENGTH = 10.0
    GREAT_PIERCED = 0.75
    HALF = 0.22
    MESSAGES = "messages"
    MIN_DIST = 100.0
    NAME = "armor_calculator"
    NOT_PIERCED = 1.25
    POSITION = "calcPosition"
    SHOW_MESSAGE = "showTextMessage"
    SHOW_POINTS = "showCalcPoints"
    SKIP_DETAILS = {TankPartIndexes.CHASSIS, TankPartIndexes.GUN}
    TEMPLATE = "template"
    TEXT_POSITION = "textMessagePosition"
    MACROS_COLOR = "color"
    MACROS_CALCED_ARMOR = "calcedArmor"
    MACROS_ARMOR = "armor"
    MACROS_PIERCING_RESERVE = "piercingReserve"
    NONEDATA = (None, None, SHOT_RESULT.UNDEFINED)


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
    LIST_SIZE = 15

    DEAD_COLOR = "deadColor"
    ALLY = "ally"
    ENEMY = "enemy"
    ENEMY_COLOR_BLIND = "enemyColorBlind"
    ALIVE = True
    NOT_ALIVE = False


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
    WG_DIST_DISABLE = "wgDistDisable"
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


class DISPERSION_CIRCLE:
    def __init__(self):
        pass

    NAME = "dispersion_circle"
    CIRCLE_EXTRA_LAP = "circle_extraServerLap"
    CIRCLE_REPLACE = "circle_replaceOriginalCircle"
    CIRCLE_SCALE_CONFIG = "circle_scale"
    CIRCLE_SERVER = "useServerAim"
    CIRCLE_ENABLED = "circle_enabled"
    CIRCLE_SCALE = 0.65
    SCALE = 65
    MAX_TIME = 5.0
    SPG_GM_SCALE = 0.8
    HALF_SIZE = 0.5
    GUN_MARKER_MIN_SIZE = 12.0
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
    NO_LIGHT_EFFECT = "noLightEffect"
    NO_BINOCULARS = "noBinoculars"
    ENTITY = "entity"
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
    BLACKOUT = "panels_icon_filter_strength"
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
    VEHICLE_ID = "vehicleID"
    IS_ENEMY = "isEnemy"
    DAMAGE = "damage"
    ALLY = "ally"
    BLIND = "enemyBlind"
    ENEMY = "enemy"
    TEAM = ("green", "red")


class SCORE_PANEL:
    def __init__(self):
        pass

    TOTAL_STATS = "totalStats"
    RIGHT_SCOPE = "rightScope"
    LEFT_SCOPE = "leftScope"
    RIGHT_CORRELATION_IDS = "rightCorrelationIDs"
    LEFT_CORRELATION_IDS = "leftCorrelationIDs"
    EMPTY_LIST = []


class SAVE_SHOOT:
    def __init__(self):
        pass

    NAME = "save_shoot"
    MSG = "msg"
    TEMPLATE = "Shot blocked."
    ALIVE_ONLY = "aliveOnly"
    VEHICLE = "Vehicle"
    REPEAT = "isRepeat"
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
    VEHICLE_TYPE = "vehicleType"
    CLAN_DBID = "clanDBID"
    CLAN_ABBR = "clanAbbrev"


class MASSAGES:
    def __init__(self):
        pass

    NA = "NA"
    START = "START LOADING"
    FINISH = "SHUTTING DOWN"
    LOCKED = ("Sorry, your region is locked."
              " If you want to use the mod, you need to contact me personally"
              " armagomen.bb-t.ru and purchase a presonal license.")
    LOCKED_BY_FILE_NAME = "ERROR: file {} is not valid, mod locked, please install mod from official site"
    UPDATE_CHECKED = "The update check is completed, you have the current version."
    NEW_VERSION = "An update {} is detected, the client will be restarted at the end of the download."
    UPDATE_ERROR = "Error checking update. CheckUpdate.run, {}"


LOAD_LIST = (
    HP_BARS.NAME, MAIN.NAME, MAIN_GUN.NAME, MARKERS.NAME, DEBUG_PANEL.NAME, BATTLE_TIMER.NAME, DISPERSION_CIRCLE.NAME,
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
        ANOTHER.CONFIG_SELECT, MAIN.NAME, DISPERSION_CIRCLE.NAME, CAROUSEL.NAME, EFFECTS.NAME, DEBUG_PANEL.NAME,
        BATTLE_TIMER.NAME, CLOCK.NAME, HP_BARS.NAME, MARKERS.NAME, ARMOR_CALC.NAME, DAMAGE_LOG.GLOBAL,
        DAMAGE_LOG.TOP_LOG, DAMAGE_LOG.DONE_EXTENDED, DAMAGE_LOG.RECEIVED_EXTENDED, MAIN_GUN.NAME, TEAM_BASES.NAME,
        VEHICLE_TYPES.NAME, PANELS.PANELS_NAME, SNIPER.NAME, ARCADE.NAME, STRATEGIC.NAME, FLIGHT_TIME.NAME,
        SAVE_SHOOT.NAME, MINIMAP.NAME, ANOTHER.SHADOW_SETTINGS, SIXTH_SENSE.NAME, COLORS.NAME, SERVICE_CHANNEL.NAME
    )
    HANDLER_VALUES = {
        SNIPER.NAME: {
            'dynamic_zoom*enabled': (
                'dynamic_zoom*zoom_max', 'dynamic_zoom*zoomToGunMarker', 'dynamic_zoom*zoom_min',
                'dynamic_zoom*zoomXMeters'
            ),
            'zoomSteps*enabled': ('zoomSteps*steps',),
            SNIPER.DISABLE_AFTER_SHOOT: (SNIPER.SKIP_CLIP,)
        },
        TEAM_BASES.NAME: {
            'outline*enabled': ('outline*color',)
        },
        PANELS.PANELS_NAME: {
            "players_bars_enabled": (
                "players_bars_settings*players_bars_bar*colors*ally",
                "players_bars_settings*players_bars_bar*colors*bgColor",
                "players_bars_settings*players_bars_bar*colors*enemy",
                "players_bars_settings*players_bars_bar*colors*enemyBlind",
                "players_bars_settings*players_bars_bar*alpha",
                "players_bars_settings*players_bars_bar*bgAlpha",
                "players_bars_settings*players_bars_bar*outline*enabled",
                "players_bars_settings*players_bars_bar*outline*customColor",
                "players_bars_settings*players_bars_bar*outline*color",
                "players_bars_settings*players_bars_bar*outline*alpha",
                "players_bars_hotkey",
                "players_bars_classColor",
                "players_bars_on_key_pressed",
            ),
            'players_bars_settings*players_bars_bar*outline*enabled': (
                'players_bars_settings*players_bars_bar*outline*color',
                'players_bars_settings*players_bars_bar*outline*alpha',
                'players_bars_settings*players_bars_bar*outline*customColor'
            ),
            'players_bars_settings*players_bars_bar*outline*customColor': (
                'players_bars_settings*players_bars_bar*outline*color',
            ),
            PANELS.BAR_CLASS_COLOR: (
                'players_bars_settings*players_bars_bar*colors*ally',
                'players_bars_settings*players_bars_bar*colors*enemy',
                'players_bars_settings*players_bars_bar*colors*enemyBlind'
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
            MAIN.BG: (MAIN.BG_TRANSPARENCY,),
            MAIN.ENABLE_FPS_LIMITER: (MAIN.MAX_FRAME_RATE,),
            MAIN.SHOW_ANONYMOUS: (MAIN.CHANGE_ANONYMOUS_NAME,)
        },
        HP_BARS.NAME: {
            'outline*enabled': ('outline*color',)
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
        "reversed_values": {'dynamic_zoom*enabled', PANELS.BAR_CLASS_COLOR},
        DISPERSION_CIRCLE.NAME: {
            DISPERSION_CIRCLE.TIMER_ENABLED: (DISPERSION_CIRCLE.TIMER_REGULAR_TEMPLATE,
                                              DISPERSION_CIRCLE.TIMER_DONE_TEMPLATE,
                                              DISPERSION_CIRCLE.TIMER_DONE_COLOR,
                                              DISPERSION_CIRCLE.TIMER_COLOR,
                                              DISPERSION_CIRCLE.TIMER_POSITION_X,
                                              DISPERSION_CIRCLE.TIMER_POSITION_Y,
                                              DISPERSION_CIRCLE.TIMER_ALIGN),
            DISPERSION_CIRCLE.CIRCLE_ENABLED: (DISPERSION_CIRCLE.CIRCLE_SCALE_CONFIG,
                                               DISPERSION_CIRCLE.CIRCLE_EXTRA_LAP,
                                               DISPERSION_CIRCLE.CIRCLE_REPLACE)
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

SORTED_ALIASES = (
    ALIASES.MAIN_GUN, ALIASES.HP_BARS, ALIASES.DAMAGE_LOG, ALIASES.DEBUG, ALIASES.TIMER,
    ALIASES.SIXTH_SENSE, ALIASES.TEAM_BASES, ALIASES.ARMOR_CALC, ALIASES.FLIGHT_TIME, ALIASES.DISPERSION_TIMER,
    ALIASES.PANELS, ALIASES.MINIMAP, ALIASES.USER_BACKGROUND, ALIASES.WG_COMP, ALIASES.DATE_TIME
)

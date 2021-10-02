from collections import namedtuple

from account_helpers.settings_core.settings_constants import GAME
from aih_constants import CTRL_MODE_NAME
from gui.Scaleform.daapi.view.battle.shared.crosshair.settings import SHOT_RESULT_TO_DEFAULT_COLOR, \
    SHOT_RESULT_TO_ALT_COLOR
from gui.battle_control.battle_constants import FEEDBACK_EVENT_ID
from gui.shared.gui_items.Vehicle import VEHICLE_CLASS_NAME
from helpers import getClientLanguage

MOD_NAME = "BATTLE_OBSERVER"
FILE_NAME = "armagomen.battleObserver_{}.wotmod"

HEADERS = [('User-Agent', MOD_NAME)]

SWF = namedtuple("SWF", ("BATTLE", "LOBBY", "ATTRIBUTE_NAME"))(
    'modBattleObserver.swf', 'modBattleObserverHangar.swf', 'as_createBattleObserverComp')

URLS = namedtuple("URLS", ("HOST_NAME", "DONATE_UA_URL", "DONATE_EU_URL", "SUPPORT_URL", "UPDATE_GITHUB_API_URL"))(
    "armagomen.bb-t.ru", "https://donatua.com/@armagomen", "https://www.donationalerts.com/r/armagomenvs",
    "https://discord.gg/NuhuhTN", "https://api.github.com/repos/Armagomen/battle_observer/releases/latest")

VEHICLE = namedtuple("VEHICLE", ("CUR", "MAX", "TEAM", "PERCENT"))("health", "maxHealth", "team", "percent")


class GLOBAL:
    def __init__(self):
        pass

    ALIGN = "align"
    ALIGN_LIST = namedtuple("ALIGN_LIST", ("left", "center", "right"))("left", "center", "right")
    ALPHA = "alpha"
    AVG_COLOR = "avgColor"
    BG_ALPHA = "bgAlpha"
    BLUR_X = "blurX"
    BLUR_Y = "blurY"
    COLOR = "color"
    COMMA_SEP = ", "
    CONFIG_ERROR = "Incorrect macros in config file."
    CUSTOM_COLOR = "customColor"
    C_INTERFACE_SPLITTER = "*"
    DOT = "."
    EMPTY_LINE = ""
    ENABLED = "enabled"
    FIRST, LAST = (0, -1)
    F_ONE = 1.0
    F_ZERO = float(FIRST)
    GLOW_FILTER = "glowFilter"
    HEIGHT = "height"
    ICONS_DIR = "img://gui/maps/icons"
    IMG = "img"
    IMG_PARAMS = {"dir": "img://gui/maps/icons/library/efficiency/48x48", "size": "width='24' height='24'",
                  "vspace": "vspace='-13'"}
    INNER = "inner"
    KNOCKOUT = "knockout"
    ONE = 1
    ONE_SECOND = 1.0
    OUTLINE = "outline"
    REPLACE = ("\n", "<br>")
    RU_LOCALIZATION = getClientLanguage().lower() in ('ru', 'uk', 'be')
    SCALE = "scale"
    SETTINGS = "settings"
    SMOOTHING = "smoothing"
    STRENGTH = "strength"
    TWO = 2
    WIDTH = "width"
    X = "x"
    Y = "y"
    ZERO = FIRST


SERVICE_CHANNEL = namedtuple("SERVICE_CHANNEL", ("NAME", "KEYS", "TYPE", "DATA", "AUX_DATA", "SYSTEM_CHANNEL_KEYS"))(
    "service_channel_filter", "sys_keys", "type", "data", "auxData", (
        "CustomizationForCredits", "CustomizationForGold", "DismantlingForCredits",
        "DismantlingForCrystal", "DismantlingForGold", "Information", "MultipleSelling",
        "PowerLevel", "PurchaseForCredits", "Remove", "Repair", "Restore", "Selling",
        "autoMaintenance", "customizationChanged", "PurchaseForCrystal",
        "PurchaseForGold", "GameGreeting"))

__Main = namedtuple("MAIN", (
    "AUTO_CLEAR_CACHE", "ENABLE_BARS_ANIMATION", "ENABLE_FPS_LIMITER", "HIDE_BADGES", "HIDE_CHAT", "HIDE_CLAN_ABBREV",
    "HIDE_DOG_TAGS", "MAX_FRAME_RATE", "NAME", "REMOVE_SHADOW_IN_PREBATTLE", "SHOW_FRIENDS", "SHOW_ANONYMOUS",
    "ANONYMOUS_STRING", "CHANGE_ANONYMOUS_NAME", "USE_KEY_PAIRS", "IGNORE_COMMANDERS", "DISABLE_SCORE_SOUND",
    "HIDE_SERVER_IN_HANGAR", "DEBUG", "CREW_TRAINING"))
MAIN = __Main(
    "autoClearCache", "enableBarsAnimation", "fps_enableFPSLimiter", "hideBadges", "hideChatInRandom", "hideClanAbbrev",
    "hide_dog_tags", "fps_maxFrameRate", "main", "removeShadowInPrebattle", "showFriendsAndClanInEars",
    "anonymousEnableShow", "anonymousString", "anonymousNameChange", "useKeyPairs", "ignore_commanders_voice",
    "disable_score_sound", "hide_server_in_hangar", "DEBUG_MODE", "auto_crew_training")

COLORS = namedtuple("COLORS", (
    "NAME", "BLACK", "BLIND", "B_SILVER", "GOLD", "GREEN", "NORMAL_TEXT", "ORANGE", "RED", "S_YELLOW", "YELLOW",
    "C_GREEN", "C_ORANGE", "C_RED", "C_YELLOW", "C_PURPLE", "C_BG", "GLOBAL", "ALLY_MAME", "ENEMY_MAME",
    "ENEMY_BLIND_MAME", "DEAD_COLOR"))(
    "colors", "#000000", "#6F6CD3", "#858585", "#FFD700", "#5ACB00", "#FAFAFA", "#FF9900", "#F30900", "#E0E06D",
    "#FFC900", "green", "orange", "red", "yellow", "purple", "bgColor", "global", "ally", "enemy", "enemyColorBlind",
    "deadColor")

MAIN_GUN = namedtuple("MAIN_GUN", (
    "NAME", "COLOR", "TEMPLATE", "GUN_ICON", "DONE_ICON", "FAILURE_ICON", "MIN_GUN_DAMAGE", "DAMAGE_RATE"))(
    "main_gun", "mainGunColor", "template", "mainGunIcon", "mainGunDoneIcon", "mainGunFailureIcon", 1000, 0.2)

MINIMAP = namedtuple("MINIMAP", ("NAME", "DEATH_PERMANENT", "HOT_KEY", "INDENT", "SHOW_NAMES", "ZOOM"))(
    "minimap", "permanentMinimapDeath", "zoom_hotkey", "indent", "showDeathNames", "zoom")

HP_BARS = namedtuple("HP_BARS", ("NAME", "STYLE", "WIDTH", "DIFF", "ALIVE", "STYLES"))(
    "hp_bars", "style", "barsWidth", "differenceHP", "showAliveCount",
    namedtuple("HpStyles", ("normal", "league"))("normal", "league"))

CLOCK = namedtuple("CLOCK", (
    "NAME", "IN_BATTLE", "IN_LOBBY", "FORMAT", "UPDATE_INTERVAL", "DEFAULT_FORMAT_BATTLE", "DEFAULT_FORMAT_HANGAR"))(
    "clock", "battle", "hangar", "format", 1.0, "<textformat tabstops='[120]'>%d %b %Y<tab>%X</textformat>",
    "<textformat tabstops='[135]'>%d %b %Y<tab>%X</textformat>")

PREMIUM = namedtuple("PREMIUM", ("PREMIUM_TIME", "PREMIUM_FORMAT", "DEFAULT_FORMAT_PREMIUM"))(
    "premium_time", "premium_format", "<font face='$TitleFont' size='16' color='#FAFAFA'>%(days)d "
                                      "Days. %(hours)02d:%(minutes)02d:%(seconds)02d</font>")

__Sniper = namedtuple("SNIPER", (
    "ZOOM", "NAME", "DYN_ZOOM", "STEPS_ONLY", "ZOOM_STEPS", "STEPS", "GUN_ZOOM", "METERS", "ZOOMS", "ZOOM_EXPOSURE",
    "INCREASED_ZOOM", "DEFAULT_STEPS", "EXPOSURE_FACTOR", "MAX_CALIBER", "MAX_DIST", "DISABLE_SNIPER",
    "DISABLE_LATENCY", "SKIP_CLIP", "CLIP"))
SNIPER = __Sniper(
    "zoom", "zoom", "dynamic_zoom", "steps_only", "zoomSteps", "steps", "zoomToGunMarker", "zoomXMeters", "zooms",
    "zoomExposure", "increasedZoom", [2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 16.0, 20.0, 25.0], 0.05, 60, 730.0,
    "disable_cam_after_shot", "disable_cam_after_shot_latency", "disable_cam_after_shot_skip_clip", "clip")


class DAMAGE_LOG:
    def __init__(self):
        pass

    NAME = "damage_log"
    ALL_DAMAGES = "allDamages"
    ASSIST_DAMAGE = "assistDamage"
    ASSIST_STUN = "stun"
    ATTACK_REASON = "attackReason"
    AVG_DAMAGE = "tankAvgDamage"
    AVG_DAMAGE_DATA = 0.0
    BLOCKED_DAMAGE = "blockedDamage"
    CLASS_COLOR = "tankClassColor"
    MAX_HEALTH = "max_health"
    CLASS_ICON = "classIcon"
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


ARCADE = namedtuple("ARCADE", (
    "NAME", "ANGLE", "DIST_RANGE", "MAX", "MIN", "START_ANGLE", "START_DEAD_DIST", "START_DIST", "SCROLL_SENSITIVITY"))(
    "arcade_camera", -0.22, "distRange", "max", "min", "startAngle", "startDeadDist", "startDist", "scrollSensitivity")

STRATEGIC = namedtuple("STRATEGIC", ("NAME", "MIN", "MAX", "DIST_RANGE", "SCROLL_SENSITIVITY"))(
    "strategic_camera", "min", "max", "distRange", "scrollSensitivity")
POSTMORTEM = namedtuple("POSTMORTEM", ("DURATION", "PARAMS", "CAM_MATRIX", "MODES"))(
    "transitionDuration", "postmortemParams", "camMatrix", {CTRL_MODE_NAME.POSTMORTEM, CTRL_MODE_NAME.DEATH_FREE_CAM})

ARMOR_CALC = namedtuple("ARMOR_CALC", (
    "PIERCING_POWER", "NAME", "POSITION", "MESSAGES", "TEMPLATE", "MACROS_COLOR", "MACROS_COUNTED_ARMOR",
    "MACROS_PIERCING_RESERVE", "MACROS_MESSAGE", "MACROS_CALIBER", "RICOCHET", "NO_DAMAGE",
    "MESSAGES_TEMPLATE", "RICOCHET_MESSAGE", "NO_DAMAGE_MESSAGE", "DEFAULT_TEMPLATE", "ON_ALLY"))(
    "piercingPower", "armor_calculator", "position", "messages", "template", "color", "countedArmor",
    "piercingReserve", "message", "caliber", "ricochet", "noDamage",
    {key: "<font size='20' color='#FAFAFA'>Change me in config.</font>" for key in
     set(SHOT_RESULT_TO_ALT_COLOR.values() + SHOT_RESULT_TO_DEFAULT_COLOR.values())}, "Ricochet",
    "critical shot, no damage", "<p align='center'>%(ricochet)s%(noDamage)s<br>"
                                "<font color='%(color)s'>%(countedArmor)d | %(piercingPower)d</font></p>",
    "display_on_allies")

MARKERS = namedtuple("MARKERS", ("NAME", "HOT_KEY", "CLASS_COLOR", "TYPE_ICON", "ICON"))(
    "markers", "showMarkers_hotkey", "markersClassColor", {
        VEHICLE_CLASS_NAME.HEAVY_TANK: "H", VEHICLE_CLASS_NAME.MEDIUM_TANK: "M", VEHICLE_CLASS_NAME.AT_SPG: "J",
        VEHICLE_CLASS_NAME.SPG: "S", VEHICLE_CLASS_NAME.LIGHT_TANK: "L", "unknown": "U"}, "<font color='{}'>{}</font>")

CAROUSEL = namedtuple("CAROUSEL", ("NAME", "SMALL", "ROWS", "SETTINGS"))(
    "tank_carousel", "smallDoubleCarousel", "carouselRows", {GAME.CAROUSEL_TYPE: None, GAME.DOUBLE_CAROUSEL_TYPE: None})

USER_BACKGROUND = namedtuple("USER_BACKGROUND", ("NAME", "CENTERED_X", "CENTERED_Y", "LAYER"))(
    "user_background", "centeredX", "centeredY", "layer")

FLIGHT_TIME = namedtuple("FLIGHT_TIME", ("NAME", "SPG_ONLY", "TEMPLATE", "M_FLIGHT_TIME", "M_DISTANCE", "ALIGN"))(
    "flight_time", "spgOnly", "template", "flightTime", "distance", "align")

VEHICLE_TYPES = namedtuple("VEHICLE_TYPES", ("NAME", "CLASS_COLORS", "CLASS_ICON", "UNKNOWN", "TEMPLATE"))(
    "vehicle_types", "vehicleClassColors", "vehicleClassIcon", "unknown",
    "<font face='BattleObserver' size='20'>{}</font>")

SIXTH_SENSE = namedtuple("SIXTH_SENSE", (
    "NAME", "SHOW_TIMER", "PLAY_TICK_SOUND", "TIME", "TIMER", "TEMPLATE", "IMAGE", "M_TIME", "M_TIME_LEFT"))(
    "sixth_sense", "showTimer", "playTickSound", "lampShowTime", "timer", "TimerTemplate", "image", "lampTime",
    "timeLeft")

__Dispersion = namedtuple("DISPERSION", (
    "NAME", "CIRCLE_EXTRA_LAP", "CIRCLE_REPLACE", "CIRCLE_SCALE_CONFIG", "CIRCLE_SERVER", "ENABLED",
    "SCALE", "MAX_TIME", "SPG_GM_SCALE", "GUN_MARKER_MIN_SIZE", "MINUS_ONE_F", "TIMER_ENABLED",
    "TIMER_POSITION_X", "TIMER_POSITION_Y", "TIMER_COLOR", "TIMER_DONE_COLOR", "TIMER_DONE_TEMPLATE",
    "TIMER_REGULAR_TEMPLATE", "TIMER_ALIGN"))
DISPERSION = __Dispersion(
    "dispersion_circle", "circle_extraServerLap", "circle_replaceOriginalCircle", "circle_scale", "useServerAim",
    "circle_enabled", 80, 5.0, 0.8, 16.0, -1.0, "timer_enabled", "timer_position_x", "timer_position_y",
    "timer_color", "timer_done_color", "timer_done_template", "timer_regular_template", "timer_align")

DISPERSION_TIME = namedtuple("DISPERSION_TIME", ("TIMER", "PERCENT"))("timer", "percent")

DEBUG_PANEL = namedtuple("DEBUG_PANEL", (
    "NAME", "TEXT", "TEMPLATE", "GRAPHICS", "PING_BAR", "FPS_BAR", "FPS_COLOR", "PING_COLOR", "LAG_COLOR", "PING",
    "FPS", "LAG"))("debug_panel", "debugText", "text", "debugGraphics", "pingBar", "fpsBar", "fpsColor", "pingColor",
                   "pingLagColor", "PING", "FPS", "PingLagColor")

BATTLE_TIMER = namedtuple("BATTLE_TIMER", (
    "NAME", "TEMPLATE", "COLOR", "END_COLOR", "M_TIMER", "TIME_FORMAT", "START_STRING", "END_BATTLE_SEC"))(
    "battle_timer", "timerTemplate", "timerColor", "timerColorEndBattle", "timer", "%02d:%02d", "00:00", 120)

EFFECTS = namedtuple("EFFECTS", (
    "NAME", "NO_FLASH_BANG", "NO_SHOCK_WAVE", "NO_BINOCULARS", "IS_PLAYER_VEHICLE", "SHOW_FLASH_BANG",
    "SHOW_SHOCK_WAVE", "NO_SNIPER_DYNAMIC"))(
    "effects", "noFlashBang", "noShockWave", "noBinoculars", "isPlayerVehicle", "showFlashBang", "showShockWave",
    "noSniperDynamic"
)

TEAM_BASES = namedtuple("TEAM_BASES", (
    "NAME", "TEXT_SETTINGS", "FONT", "SIZE", "BOLD", "ITALIC", "UNDERLINE", "BASE_FONT", "FONT_SIZE", "HUNDRED"))(
    "team_bases_panel", "text_settings", "font", "size", "bold", "italic", "underline", "$TitleFont", 16, 100.0)

__Aliases = namedtuple("ALIASES", (
    "HP_BARS", "DAMAGE_LOG", "MAIN_GUN", "DEBUG", "TIMER", "SIXTH_SENSE", "TEAM_BASES", "ARMOR_CALC", "FLIGHT_TIME",
    "DISPERSION_TIMER", "PANELS", "MINIMAP", "USER_BACKGROUND", "DATE_TIME", "DISTANCE", "OWN_HEALTH"))
ALIASES = __Aliases(
    "Observer_TeamsHP_UI", "Observer_DamageLog_UI", "Observer_MainGun_UI", "Observer_DebugPanel_UI",
    "Observer_BattleTimer_UI", "Observer_SixthSense_UI", "Observer_TeamBases_UI", "Observer_ArmorCalculator_UI",
    "Observer_FlightTime_UI", "Observer_DispersionTimer_UI", "Observer_PlayersPanels_UI", "Observer_Minimap_UI",
    "Observer_UserBackGround_UI", "Observer_DateTimes_UI", "Observer_Distance_UI",
    "Observer_OwnHealth_UI")

DISTANCE = namedtuple("DISTANCE", ("NAME", "TEMPLATE", "ALIGN", "DIST", "TANK_NAME", "SPOTTED"))(
    "distance_to_enemy", "template", "align", "distance", "name", "spottedOnly")

OWN_HEALTH = namedtuple("OWN_HEALTH", ("NAME", "TEMPLATE", "ALIGN", "COLOR"))("own_health", "template", "align",
                                                                              "color")


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
    BAR_TEXT_SETTINGS = "players_bars_text"
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
    # ststistics
    STATISTIC_ENABLED = "players_statistic_enabled"
    STATISTIC_PATTERN_LEFT = "players_statistic_pattern_left"
    STATISTIC_PATTERN_RIGHT = "players_statistic_pattern_right"
    STATISTIC_SETTINGS = "players_statistic_settings"
    STATISTIC_COLORS = "players_statistic_colors"


SAVE_SHOOT = namedtuple("SAVE_SHOOT", ("NAME", "MSG", "TEMPLATE", "DESTROYED_BLOCK", "VEHICLE", "TEAM", "HOT_KEY"))(
    "save_shoot", "msg", "Shot blocked.", "block_on_destroyed", "Vehicle", "team", "shoot_hotkey")

ANOTHER = namedtuple("ANOTHER", (
    "CONFIG_SELECT", "SHADOW_SETTINGS", "FRIEND_LIST", "ACCOUNT_DBID", "USERS", "DBID", "BADGES", "IS_TEAM_KILLER",
    "NAME", "CLAN_DBID", "CLAN_ABBR"))(
    "configSelect", "shadow_settings", "friendList", "accountDBID", "users", "databaseID", "badges", "isTeamKiller",
    "name", "clanDBID", "clanAbbrev")

MESSAGES = namedtuple("MESSAGES", ("START", "FINISH", "LOCKED_BY_FILE_NAME", "UPDATE_CHECKED", "NEW_VERSION"))(
    "START LOADING", "SHUTTING DOWN", "ERROR: file {} is not valid, mod locked, please install mod from official site",
    "The update check is completed, you have the current version.",
    "An update {} is detected, the client will be restarted at the end of the download.")

LOAD_LIST = (
    HP_BARS.NAME, MAIN.NAME, MAIN_GUN.NAME, DEBUG_PANEL.NAME, BATTLE_TIMER.NAME, DISPERSION.NAME,
    VEHICLE_TYPES.NAME, SNIPER.NAME, COLORS.NAME, ARMOR_CALC.NAME, TEAM_BASES.NAME, FLIGHT_TIME.NAME,
    SERVICE_CHANNEL.NAME, ARCADE.NAME, STRATEGIC.NAME, PANELS.PANELS_NAME, MINIMAP.NAME, EFFECTS.NAME,
    DAMAGE_LOG.GLOBAL, DAMAGE_LOG.TOP_LOG, DAMAGE_LOG.DONE_EXTENDED, DAMAGE_LOG.RECEIVED_EXTENDED, SAVE_SHOOT.NAME,
    SIXTH_SENSE.NAME, USER_BACKGROUND.NAME, ANOTHER.SHADOW_SETTINGS, CAROUSEL.NAME, CLOCK.NAME, DISTANCE.NAME,
    OWN_HEALTH.NAME,
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
        SAVE_SHOOT.NAME, MINIMAP.NAME, ANOTHER.SHADOW_SETTINGS, SIXTH_SENSE.NAME, DISTANCE.NAME, OWN_HEALTH.NAME,
        COLORS.NAME, SERVICE_CHANNEL.NAME
    )
    HANDLER_VALUES = {
        SNIPER.NAME: {
            'dynamic_zoom*enabled': (
                'dynamic_zoom*steps_only',
                'dynamic_zoom*zoomXMeters'
            ),
            'zoomSteps*enabled': ('zoomSteps*steps',),
            SNIPER.DISABLE_SNIPER: (SNIPER.SKIP_CLIP, SNIPER.DISABLE_LATENCY)
        },
        TEAM_BASES.NAME: {
            'outline*enabled': ('outline*color',)
        },
        PANELS.PANELS_NAME: {
            PANELS.BARS_ENABLED: (
                "players_bars_settings*players_bars_bar*outline*enabled",
                "players_bars_settings*players_bars_bar*outline*customColor",
                "players_bars_settings*players_bars_bar*outline*color",
                "players_bars_settings*players_bars_bar*outline*alpha",
                PANELS.BAR_HOT_KEY,
                PANELS.BAR_CLASS_COLOR,
                PANELS.ON_KEY_DOWN,
            ),
            'players_bars_settings*players_bars_bar*outline*customColor': (
                'players_bars_settings*players_bars_bar*outline*color',
            ),
            'players_bars_settings*players_bars_bar*outline*enabled': (
                'players_bars_settings*players_bars_bar*outline*color',
                'players_bars_settings*players_bars_bar*outline*alpha',
                'players_bars_settings*players_bars_bar*outline*customColor'
            ),
            PANELS.DAMAGES_ENABLED: (
                PANELS.DAMAGES_HOT_KEY, 'players_damages_settings*x', 'players_damages_settings*y'
            ),
            PANELS.ICONS_ENABLED: (PANELS.ICONS_BLACKOUT,),
            PANELS.STATISTIC_ENABLED: (PANELS.STATISTIC_PATTERN_RIGHT, PANELS.STATISTIC_PATTERN_LEFT)
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
    ALIASES.DATE_TIME: ".date_times",
    ALIASES.DISTANCE: ".distance_to_enemy",
    ALIASES.OWN_HEALTH: ".own_health",
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
    ALIASES.DISTANCE: DISTANCE.NAME,
    ALIASES.OWN_HEALTH: OWN_HEALTH.NAME,
}

SORTED_ALIASES = (
    ALIASES.MAIN_GUN, ALIASES.HP_BARS, ALIASES.DAMAGE_LOG, ALIASES.DEBUG, ALIASES.TIMER,
    ALIASES.SIXTH_SENSE, ALIASES.TEAM_BASES, ALIASES.ARMOR_CALC, ALIASES.FLIGHT_TIME, ALIASES.DISPERSION_TIMER,
    ALIASES.PANELS, ALIASES.MINIMAP, ALIASES.DATE_TIME, ALIASES.DISTANCE, ALIASES.OWN_HEALTH, ALIASES.USER_BACKGROUND
)

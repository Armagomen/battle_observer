from collections import namedtuple

from aih_constants import CTRL_MODE_NAME
from constants import ARENA_GUI_TYPE, AUTH_REALM

MOD_NAME = "BATTLE_OBSERVER"
IMAGE_DIR = "img://gui/maps/icons/battle_observer"

IS_WG_CLIENT = AUTH_REALM != "RU"


def getLogo(big=True):
    if big:
        return "<img src='{}/logo/big.png' width='500' height='32' vspace='16'>".format(IMAGE_DIR)
    return "<img src='{}/logo/small.png' width='220' height='14' vspace='16'>".format(IMAGE_DIR)


IMG = namedtuple("IMG", "MONO PATREON DONATELLO")(
    "<img src='{}/donate/mono.png' width='16' height='16' vspace='-3'>".format(IMAGE_DIR),
    "<img src='{}/donate/patreon.png' width='16' height='16' vspace='-3'>".format(IMAGE_DIR),
    "<img src='{}/donate/donatello.png' width='16' height='16' vspace='-3'>".format(IMAGE_DIR)
)

URLS = namedtuple("URLS", (
    "UPDATE_GITHUB_API_URL",
    "MONO",
    "PATREON",
    "DISCORD",
    "UPDATE",
    "DONATELLO"
))(
    "https://api.github.com/repos/Armagomen/battle_observer/releases/latest",
    "https://send.monobank.ua/jar/5BZHrPrJwr",
    "https://patreon.com/armagomen",
    "https://discord.gg/Nma5T5snKW",
    "https://github.com/Armagomen/battle_observer/releases/download/",
    "https://donatello.to/ArmagomenUA"
)

VEHICLE = namedtuple("VEHICLE", ("CUR", "MAX", "TEAM", "PERCENT", "VEHICLE"))(
    "health", "maxHealth", "team", "percent", "Vehicle")

API_KEY = "5500d1b937426e47e2b039e4a11990be" if IS_WG_CLIENT else "53352ebb7cd87e994157d0d1e9f360b1"
REGIONS = {"EU": "https://api.worldoftanks.eu/wot/account/info/?application_id={}".format(API_KEY),
           "ASIA": "https://api.worldoftanks.asia/wot/account/info/?application_id={}".format(API_KEY),
           "NA": "https://api.worldoftanks.com/wot/account/info/?application_id={}".format(API_KEY),
           "RU": "https://api.tanki.su/wot/account/info/?application_id={}".format(API_KEY)}
STATISTICS_REGION = REGIONS.get(AUTH_REALM)

VEHICLE_TYPES_COLORS = namedtuple("VEHICLE_TYPES_COLORS", ("NAME", "UNKNOWN"))("vehicle_types_colors", "unknown")


class GLOBAL:
    def __init__(self):
        pass

    ALIGN = "align"
    ALIGN_LIST = namedtuple("ALIGN_LIST", ("left", "center", "right"))("left", "center", "right")
    ALPHA = "alpha"
    AVG_COLOR = "avgColor"
    COLOR = "color"
    COMMA_SEP = ", "
    C_INTERFACE_SPLITTER = "*"
    EMPTY_LINE = ""
    ENABLED = "enabled"
    HEIGHT = "height"
    IMG_PARAMS = {"dir": "img://gui/maps/icons/library/efficiency/48x48", "size": "width='24' height='24'", "vspace": "vspace='-13'"}
    SCALE = "scale"
    SETTINGS = "settings"
    WIDTH = "width"
    X = "x"
    Y = "y"
    NEW_LINE = "\n"


EFFICIENCY_ICONS_SIZE = "width='18' height='18' vspace='-3'"
LOGS_ICONS = "width='16' height='16' vspace='-4'"
EX_LOGS_ICONS = "width='15' height='15' vspace='-4'"

SERVICE_CHANNEL = namedtuple("SERVICE_CHANNEL", ("NAME", "KEYS", "TYPE", "DATA", "AUX_DATA", "SYSTEM_CHANNEL_KEYS"))(
    "service_channel_filter", "sys_keys", "type", "data", "auxData", (
        "CustomizationForCredits", "CustomizationForGold", "DismantlingForCredits",
        "DismantlingForCrystal", "DismantlingForGold", "Information", "MultipleSelling",
        "PowerLevel", "PurchaseForCredits", "Remove", "Repair", "Restore", "Selling",
        "autoMaintenance", "customizationChanged", "PurchaseForCrystal",
        "PurchaseForGold", "GameGreeting"))

__Main = namedtuple("MAIN", (
    "AUTO_CLEAR_CACHE", "HIDE_BADGES", "HIDE_CLAN_ABBREV", "HIDE_DOG_TAGS", "NAME", "SHOW_FRIENDS", "SHOW_ANONYMOUS",
    "USE_KEY_PAIRS", "IGNORE_COMMANDERS", "DISABLE_SCORE_SOUND", "DEBUG", "CREW_TRAINING", "DIRECTIVES", "HIDE_HINT",
    "FIELD_MAIL", "CREW_RETURN", "STUN_SOUND", "HIDE_MAIN_CHAT", "HIDE_BTN_COUNTERS", "PREMIUM_TIME", "SAVE_SHOT",
    "MUTE_BASES_SOUND", "HIDE_PRESTIGE_HANGAR_WIDGET", "HIDE_PRESTIGE_PROFILE_WIDGET",
    "HIDE_PRESTIGE_BATTLE_WIDGET", "EXCLUDED_MAP_SLOTS_NOTIFICATION", "AUTO_CLAIM_CLAN_REWARD", "HIDE_EVENT_BANNER"))
MAIN = __Main(
    "clear_cache_automatically", "hide_badges", "hide_clan_abbrev", "hide_dog_tags", "main", "show_friends",
    "anti_anonymous", "useKeyPairs", "ignore_commanders_voice", "disable_score_sound", "DEBUG_MODE",
    "auto_crew_training", "directives_only_from_storage", "hide_hint_panel", "hide_field_mail",
    "auto_return_crew", "disable_stun_sound", "hide_main_chat_in_hangar", "hide_button_counters_on_top_panel",
    "premium_time", "save_shot", "mute_team_base_sound", "hide_prestige_hangar_widget", "hide_prestige_profile_widget",
    "hide_prestige_battle_widget", "excluded_map_slots_notification", "auto_claim_clan_reward", "hideEventBanner")

COLORS = namedtuple("COLORS", (
    "NAME", "BLACK", "BLIND", "GOLD", "GREEN", "WHITE", "ORANGE", "RED", "S_YELLOW", "YELLOW",
    "C_GREEN", "C_ORANGE", "C_RED", "C_NORMAL", "C_YELLOW", "C_PURPLE", "C_BG", "GLOBAL", "ALLY_MAME", "ENEMY_MAME",
    "ENEMY_BLIND_MAME"))(
    "colors", "#000000", "#6F6CD3", "#FFD700", "#60CB00", "#FFFFFF", "#FF9900", "#ED070A", "#E0E06D", "#FFC900",
    "green", "orange", "red", "normal", "yellow", "purple", "bgColor", "global", "ally", "enemy", "enemyColorBlind")

MAIN_GUN = namedtuple("MAIN_GUN", ("NAME", "MIN_GUN_DAMAGE", "DAMAGE_RATE"))("main_gun", 1000, 0.2)

MINIMAP = namedtuple("MINIMAP", (
    "NAME", "DEATH_PERMANENT", "SHOW_NAMES", "ZOOM", "VIEW_RADIUS", "YAW", "ZOOM_KEY"))(
    "minimap", "permanentMinimapDeath", "showDeathNames", "zoom", "real_view_radius",
    "yaw_limits", "zoom_hotkey")

HP_BARS = namedtuple("HP_BARS", ("NAME", "STYLE", "ALIVE", "STYLES"))(
    "hp_bars", "style", "showAliveCount", namedtuple("HpStyles", ("normal", "league", "league_big"))("normal", "league", "league_big"))

CLOCK = namedtuple("CLOCK", (
    "NAME", "IN_BATTLE", "IN_LOBBY", "FORMAT", "UPDATE_INTERVAL", "DEFAULT_FORMAT_BATTLE", "DEFAULT_FORMAT_HANGAR"))(
    "clock", "battle", "hangar", "format", 1.0, "<textformat tabstops='[120]'>%d %b %Y<tab>%H:%M:%S</textformat>",
    "<textformat tabstops='[135]'>%d %b %Y<tab>%H:%M:%S</textformat>")

__Sniper = namedtuple("SNIPER", (
    "NAME", "DYN_ZOOM", "ZOOM_STEPS", "STEPS", "ZOOM_EXPOSURE", "DEFAULT_STEPS",
    "MAX_CALIBER", "DISABLE_SNIPER", "DISABLE_LATENCY", "SKIP_CLIP"))
SNIPER = __Sniper(
    "zoom", "dynamic_zoom", "steps_enabled", "steps_range", "zoomExposure", map(float, xrange(2, 34, 2)),
    60, "disable_cam_after_shot", "disable_cam_after_shot_latency", "disable_cam_after_shot_skip_clip")


class DAMAGE_LOG:
    def __init__(self):
        pass

    NAME = "damage_log"
    TOP_LOG = "log_total"
    TOP_LOG_SEPARATE = "separate"
    SEPARATE = " "
    WG_LOGS_FIX = "wg_logs"

    EXTENDED_LOG = "log_extended"
    D_DONE, D_RECEIVED = (0, 1)

    D_DONE_ENABLED = "top_enabled"
    D_RECEIVED_ENABLED = "bottom_enabled"

    ALL_DAMAGES = "allDamages"
    ATTACK_REASON = "attackReason"
    CLASS_COLOR = "tankClassColor"
    CLASS_ICON = "classIcon"
    DAMAGE_LIST = "damageList"

    HOT_KEY = "logsAltMode_hotkey"
    ICONS = "icons"
    ICON_NAME = "iconName"
    INDEX = "index"
    IN_CENTER = "inCenter"
    KILLED_ICON = "killedIcon"
    LAST_DAMAGE = "lastDamage"
    TEMPLATES = "templates"
    NOT_SHELL = "--"
    PERCENT_AVG_COLOR = "percentDamageAvgColor"
    REVERSE = "reverse"
    SHELL = ("normal", "gold")
    SHELL_COLOR = "shellColor"
    SHELL_TYPE = "shellType"
    SHOTS = "shots"
    STUN_ICON = "stunIcon"
    TANK_LEVEL = "TankLevel"
    TANK_NAME = "tankName"
    TEMPLATE_MAIN_DMG = "templateMainDMG"
    TOTAL_DAMAGE = "totalDamage"
    USER_NAME = "userName"
    VEHICLE_CLASS = "vehicleClass"
    WARNING_MESSAGE = "log_extended: incorrect event parameter in getLogData module {}"
    WG_ASSIST = "wg_log_hide_assist"
    WG_BLOCKED = "wg_log_hide_block"
    WG_CRITICS = "wg_log_hide_critics"
    WG_POS = "wg_log_pos_fix"
    NORMAL, GOLD = SHELL


ARCADE = namedtuple("ARCADE", (
    "NAME", "DIST_RANGE", "MAX", "MIN", "START_DEAD_DIST", "START_DIST", "SCROLL_SENSITIVITY", "START_ANGLE"))(
    "arcade_camera", "distRange", "max", "min", "startDeadDist", "startDist", "scrollSensitivity", "startAngle")

STRATEGIC = namedtuple("STRATEGIC", ("NAME", "MIN", "MAX", "DIST_RANGE", "SCROLL_SENSITIVITY"))(
    "strategic_camera", "min", "max", "distRange", "scrollSensitivity")

POSTMORTEM_MODES = {CTRL_MODE_NAME.POSTMORTEM, CTRL_MODE_NAME.DEATH_FREE_CAM,
                    CTRL_MODE_NAME.RESPAWN_DEATH, CTRL_MODE_NAME.VEHICLES_SELECTION}
if IS_WG_CLIENT:
    POSTMORTEM_MODES.update((CTRL_MODE_NAME.KILL_CAM, CTRL_MODE_NAME.LOOK_AT_KILLER))

ARMOR_CALC = namedtuple("ARMOR_CALC", (
    "SHOW_PIERCING_POWER", "NAME", "POSITION", "MESSAGES", "TEMPLATE", "MACROS_COLOR", "SHOW_COUNTED_ARMOR",
    "SHOW_PIERCING_RESERVE", "SHOW_CALIBER", "ON_ALLY"))(
    "show_piercing_power", "armor_calculator", "position", "messages", "template", "color", "show_counted_armor",
    "show_piercing_reserve", "show_caliber", "display_on_allies")

FLIGHT_TIME = namedtuple("FLIGHT_TIME", ("NAME", "SPG_ONLY", "TIME", "DISTANCE", "ALIGN"))(
    "flight_time", "spgOnly", "time", "distance", "align")

SIXTH_SENSE = namedtuple("SIXTH_SENSE", (
    "NAME", "PLAY_TICK_SOUND", "TIME", "DEFAULT", "ICON_NAME", "USER_ICON", "SHOW_TIMER", "TIMER_GRAPHICS", "TIMER_GRAPHICS_COLOR",
    "ICON_SIZE", "TIMER_GRAPHICS_RADIUS"))(
    "sixth_sense", "playTickSound", "lampShowTime", "default_icon", "default_icon_name", "user_icon", "show_timer", "show_timer_graphics",
    "show_timer_graphics_color", "icon_size", "show_timer_graphics_radius"
)

__Dispersion = namedtuple("DISPERSION", ("NAME", "SERVER", "SCALE", "REPLACE"))
DISPERSION = __Dispersion("dispersion_circle", "server_aim", "scale", "replace")

__DispersionTimer = namedtuple("dispersion_timer", ("NAME", "TIMER", "PERCENT"))
DISPERSION_TIMER = __DispersionTimer("dispersion_timer", "timer", "percent")

DEBUG_PANEL = namedtuple("DEBUG_PANEL", (
    "NAME", "FPS_COLOR", "PING_COLOR", "STYLES", "STYLE"))(
    "debug_panel", "fpsColor", "pingColor", namedtuple("DebugStyles", ("minimal", "modern", "big_lag"))
    ("minimal", "modern", "big_lag"), "style")

BATTLE_TIMER = namedtuple("BATTLE_TIMER", (
    "NAME", "TEMPLATE", "COLOR", "END_COLOR", "M_TIMER", "TIME_FORMAT", "START_STRING", "END_BATTLE_SEC"))(
    "battle_timer", "timerTemplate", "timerColor", "timerColorEndBattle", "timer", "%02d:%02d", "00:00", 120)

EFFECTS = namedtuple("EFFECTS", (
    "NAME", "NO_FLASH_BANG", "NO_SHOCK_WAVE", "NO_BINOCULARS", "IS_PLAYER_VEHICLE", "SHOW_FLASH_BANG",
    "SHOW_SHOCK_WAVE", "NO_SNIPER_DYNAMIC"))(
    "effects", "noFlashBang", "noShockWave", "noBinoculars", "isPlayerVehicle", "showFlashBang", "showShockWave", "noSniperDynamic")

TEAM_BASES = namedtuple("TEAM_BASES", (
    "NAME", "TEXT_SETTINGS", "FONT", "SIZE", "BOLD", "ITALIC", "UNDERLINE", "BASE_FONT", "FONT_SIZE", "HUNDRED"))(
    "team_bases_panel", "text_settings", "font", "size", "bold", "italic", "underline", "$TitleFont", 16, 100.0)

BATTLE_ALIASES = namedtuple("BATTLE_ALIASES", (
    "WGR_ICONS", "HP_BARS", "MAIN_GUN", "DAMAGE_LOG", "DAMAGE_LOG_EXT", "DEBUG", "TIMER", "TEAM_BASES", "ARMOR_CALC",
    "FLIGHT_TIME", "DISPERSION_TIMER", "DATE_TIME", "DISTANCE", "OWN_HEALTH", "PANELS", "SIXTH_SENSE", "MAP"))(
    "Observer_WGRAndIcons_UI", "Observer_TeamsHP_UI", "Observer_MainGun_UI", "Observer_DamageLog_UI", "Observer_ExtendedDamageLogs_UI",
    "Observer_DebugPanel_UI", "Observer_BattleTimer_UI", "Observer_TeamBases_UI", "Observer_ArmorCalculator_UI", "Observer_FlightTime_UI",
    "Observer_DispersionTimer_UI", "Observer_DateTimes_UI", "Observer_Distance_UI", "Observer_OwnHealth_UI", "Observer_PlayersPanels_UI",
    "Observer_SixthSense_UI", "Observer_MiniMap_UI")

LOBBY_ALIASES = namedtuple("LOBBY_ALIASES", ("DATE_TIME",))("Observer_DateTimes_UI", )

DISTANCE = namedtuple("DISTANCE", ("NAME",))("distance_to_enemy", )

OWN_HEALTH = namedtuple("OWN_HEALTH", ("NAME",))("own_health", )

STATISTICS = namedtuple("STATISTICS", (
    "NAME", "STATISTIC_ENABLED", "CHANGE_VEHICLE_COLOR",
    "FULL_LEFT", "FULL_RIGHT",
    "CUT_LEFT", "CUT_RIGHT",
    "COLORS", "ICON_ENABLED", "ICON_BLACKOUT",
    "PANELS_FULL_WIDTH", "PANELS_CUT_WIDTH"))(
    "statistics", "statistics", "statistics_vehicle_name_color",
    "statistics_pattern_full_left", "statistics_pattern_full_right",
    "statistics_pattern_cut_left", "statistics_pattern_cut_right",
    "statistics_colors", "icons", "icons_blackout",
    "statistics_panels_full_width", "statistics_panels_cut_width"
)


class PANELS:
    def __init__(self):
        pass

    PANELS_NAME = "players_panels"
    # hp_bars
    BARS_ENABLED = "players_bars_enabled"
    BAR_TEXT_SETTINGS = "players_bars_text"
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


ANOTHER = namedtuple("ANOTHER", (
    "CONFIG_SELECT", "ACCOUNT_DBID", "USERS", "DBID", "BADGES", "OVERRIDDEN_BADGE",
    "NAME", "FAKE_NAME", "CLAN_ABBR", "PRESTIGE_LEVEL", "PRESTIGE_GRADE_MARK_ID"))(
    "configSelect", "accountDBID", "users", "databaseID", "badges", "overriddenBadge",
    "name", "fakeName", "clanAbbrev", "prestigeLevel", "prestigeGradeMarkID")

CREW_XP = namedtuple("CREW_XP", (
    "NAME", "NOT_AVAILABLE", "IS_FULL_XP", "IS_FULL_COMPLETE", "NED_TURN_OFF", "ENABLE", "DISABLE"))(
    "crewDialog", "notAvailable", "isFullXp", "isFullComplete", "needTurnOff", "enable", "disable")

EXCLUDED_MAPS = namedtuple("EXCLUDED_MAPS", ("NAME", "HEADER", "MESSAGE"))("excludedMaps", "header", "message")

AVG_EFFICIENCY_HANGAR = namedtuple("AVG_EFFICIENCY_HANGAR", (
    "NAME", "DAMAGE", "ASSIST", "BLOCKED", "STUN", "MARKS_ON_GUN", "WIN_RATE", "BATTLES"))(
    "avg_efficiency_in_hangar", "avg_damage", "avg_assist", "avg_blocked", "avg_stun", "gun_marks", "win_rate", "battles")

# Settings Loader List
LOAD_LIST = (
    MAIN.NAME, HP_BARS.NAME, MAIN_GUN.NAME, DEBUG_PANEL.NAME, BATTLE_TIMER.NAME, DISPERSION.NAME, DISPERSION_TIMER.NAME,
    SNIPER.NAME, COLORS.NAME, ARMOR_CALC.NAME, TEAM_BASES.NAME, FLIGHT_TIME.NAME,
    SERVICE_CHANNEL.NAME, ARCADE.NAME, STRATEGIC.NAME, PANELS.PANELS_NAME, MINIMAP.NAME, EFFECTS.NAME,
    DAMAGE_LOG.WG_LOGS_FIX, DAMAGE_LOG.TOP_LOG, DAMAGE_LOG.EXTENDED_LOG, SIXTH_SENSE.NAME,
    CLOCK.NAME, DISTANCE.NAME, OWN_HEALTH.NAME, STATISTICS.NAME, AVG_EFFICIENCY_HANGAR.NAME
)


class CONFIG_INTERFACE:
    def __init__(self):
        pass

    DONATE_BUTTONS = ('donate_button_ua', 'discord_button')
    BLOCK_IDS = (
        ANOTHER.CONFIG_SELECT, MAIN.NAME, STATISTICS.NAME, DISPERSION.NAME, DISPERSION_TIMER.NAME,
        EFFECTS.NAME, DEBUG_PANEL.NAME, BATTLE_TIMER.NAME, CLOCK.NAME, HP_BARS.NAME, ARMOR_CALC.NAME,
        DAMAGE_LOG.WG_LOGS_FIX, DAMAGE_LOG.TOP_LOG, DAMAGE_LOG.EXTENDED_LOG, MAIN_GUN.NAME, TEAM_BASES.NAME,
        PANELS.PANELS_NAME, SNIPER.NAME, ARCADE.NAME, STRATEGIC.NAME, FLIGHT_TIME.NAME,
        MINIMAP.NAME, SIXTH_SENSE.NAME, DISTANCE.NAME, OWN_HEALTH.NAME,
        SERVICE_CHANNEL.NAME, AVG_EFFICIENCY_HANGAR.NAME, COLORS.NAME
    )
    HANDLER_VALUES = {
        SNIPER.NAME: {
            SNIPER.ZOOM_STEPS: (SNIPER.STEPS,),
            SNIPER.DISABLE_SNIPER: (SNIPER.SKIP_CLIP, SNIPER.DISABLE_LATENCY)
        },
        TEAM_BASES.NAME: {
            'outline*enabled': ('outline*color',)
        },
        PANELS.PANELS_NAME: {
            PANELS.BARS_ENABLED: (
                PANELS.BAR_CLASS_COLOR,
                PANELS.BAR_HOT_KEY,
                PANELS.BAR_CLASS_COLOR,
                PANELS.ON_KEY_DOWN,
            ),
            PANELS.DAMAGES_ENABLED: (
                PANELS.DAMAGES_HOT_KEY, 'players_damages_settings*x', 'players_damages_settings*y'
            ),
        },
        HP_BARS.NAME: {
            'outline*enabled': ('outline*color',),
            'markers*enabled': ("markers*x", "markers*y", "markers*showMarkers_hotkey", "markers*markersClassColor")
        },
        MINIMAP.NAME: {
            'zoom*enabled': ('zoom*zoom_hotkey', 'zoom*indent'),
            MINIMAP.DEATH_PERMANENT: (MINIMAP.SHOW_NAMES,)
        },
        CLOCK.NAME: {
            'hangar*enabled': ('hangar*format', 'hangar*x', 'hangar*y'),
            'battle*enabled': ('battle*format', 'battle*x', 'battle*y')
        },
        SIXTH_SENSE.NAME: {
            SIXTH_SENSE.DEFAULT: (SIXTH_SENSE.ICON_NAME,),
            SIXTH_SENSE.TIMER_GRAPHICS: (SIXTH_SENSE.TIMER_GRAPHICS_COLOR, SIXTH_SENSE.TIMER_GRAPHICS_RADIUS)
        },
        STATISTICS.NAME: {
            STATISTICS.STATISTIC_ENABLED: (
                STATISTICS.PANELS_FULL_WIDTH, STATISTICS.PANELS_CUT_WIDTH, STATISTICS.CHANGE_VEHICLE_COLOR,
                "statistics_colors*bad", "statistics_colors*normal", "statistics_colors*good",
                "statistics_colors*very_good", "statistics_colors*unique", "statistics_colors*very_bad"
            ),
            STATISTICS.ICON_ENABLED: (STATISTICS.ICON_BLACKOUT,)
        }
    }


ALIAS_TO_CONFIG_NAME = {
    BATTLE_ALIASES.HP_BARS: HP_BARS.NAME,
    BATTLE_ALIASES.DAMAGE_LOG: DAMAGE_LOG.TOP_LOG,
    BATTLE_ALIASES.DAMAGE_LOG_EXT: DAMAGE_LOG.EXTENDED_LOG,
    BATTLE_ALIASES.MAIN_GUN: MAIN_GUN.NAME,
    BATTLE_ALIASES.DEBUG: DEBUG_PANEL.NAME,
    BATTLE_ALIASES.TIMER: BATTLE_TIMER.NAME,
    BATTLE_ALIASES.SIXTH_SENSE: SIXTH_SENSE.NAME,
    BATTLE_ALIASES.TEAM_BASES: TEAM_BASES.NAME,
    BATTLE_ALIASES.ARMOR_CALC: ARMOR_CALC.NAME,
    BATTLE_ALIASES.FLIGHT_TIME: FLIGHT_TIME.NAME,
    BATTLE_ALIASES.DISPERSION_TIMER: DISPERSION_TIMER.NAME,
    BATTLE_ALIASES.PANELS: PANELS.PANELS_NAME,
    BATTLE_ALIASES.DATE_TIME: CLOCK.NAME,
    BATTLE_ALIASES.DISTANCE: DISTANCE.NAME,
    BATTLE_ALIASES.OWN_HEALTH: OWN_HEALTH.NAME,
    BATTLE_ALIASES.WGR_ICONS: STATISTICS.NAME,
    BATTLE_ALIASES.MAP: MINIMAP.NAME
}

ALIAS_TO_CONFIG_NAME_LOBBY = {
    LOBBY_ALIASES.DATE_TIME: CLOCK.NAME
}

__battle_types = (
    "BATTLE_ROYALE",
    "COMP7",
    "EPIC_BATTLE",
    "EPIC_RANDOM",
    "EPIC_RANDOM_TRAINING",
    "FORT_BATTLE_2",
    "FUN_RANDOM",
    "LAST_STAND",
    "MAPBOX",
    "RANDOM",
    "RANKED",
    "SORTIE_2",
    "TOURNAMENT_COMP7",
    "TRAINING",
    "UNKNOWN",
)

BATTLES_RANGE = tuple(getattr(ARENA_GUI_TYPE, name) for name in __battle_types if hasattr(ARENA_GUI_TYPE, name))

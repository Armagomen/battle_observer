from collections import defaultdict
from colorsys import hsv_to_rgb

from constants import ATTACK_REASONS
from gui.battle_control.battle_constants import FEEDBACK_EVENT_ID as EV_ID
from gui.shared.gui_items.Vehicle import VEHICLE_CLASS_NAME
from ..core.battle_cache import cache
from ..core.bo_constants import DAMAGE_LOG as CONSTANTS, GLOBAL
from ..core.bw_utils import callback
from ..core.config import cfg
from ..core.core import SafeDict
from ..core.events import g_events
from ..core.keys_parser import g_keysParser
from ..meta.battle.damage_logs_meta import DamageLogsMeta


class DamageLog(DamageLogsMeta):

    def __init__(self):
        super(DamageLog, self).__init__()
        self.input_log = {CONSTANTS.KILLS: set()}
        self.damage_log = {CONSTANTS.KILLS: set()}
        self.shots = defaultdict(list)
        self.topMacro = defaultdict(int, cfg.log_total[CONSTANTS.ICONS])
        self.logsEnabledSetting = {
            EV_ID.PLAYER_DAMAGED_HP_ENEMY: cfg.log_damage_extended[GLOBAL.ENABLED],
            EV_ID.ENEMY_DAMAGED_HP_PLAYER: cfg.log_input_extended[GLOBAL.ENABLED]
        }
        g_keysParser.registerComponent(CONSTANTS.HOT_KEY, cfg.log_global[CONSTANTS.HOT_KEY])
        self.eveToLog = {
            EV_ID.PLAYER_DAMAGED_HP_ENEMY: self.damage_log,
            EV_ID.ENEMY_DAMAGED_HP_PLAYER: self.input_log
        }
        self.eveToLogConfig = {
            EV_ID.PLAYER_DAMAGED_HP_ENEMY: cfg.log_damage_extended,
            EV_ID.ENEMY_DAMAGED_HP_PLAYER: cfg.log_input_extended
        }
        self.isSPG = False

    def onEnterBattlePage(self):
        super(DamageLog, self).onEnterBattlePage()
        self.subscribe()
        if cache.player is not None and cache.player.vehicle is not None:
            self.isSPG = VEHICLE_CLASS_NAME.SPG in cache.player.vehicleTypeDescriptor.type.tags
            extended_log = any(self.logsEnabledSetting.itervalues())
            if extended_log:
                cache.logsEnable = extended_log
                g_events.onKeyPressed += self.keyEvent
                g_events.onVehicleAddUpdate += self.onVehicleAddUpdate
            if cfg.log_total[GLOBAL.ENABLED] or extended_log:
                feedback = self.sessionProvider.shared.feedback
                if feedback:
                    feedback.onPlayerFeedbackReceived += self.__onPlayerFeedbackReceived
            if not self.isSPG:
                self.topMacro.update(stun=GLOBAL.EMPTY_LINE, stunIcon=GLOBAL.EMPTY_LINE)
            self.updateAvgDamage(self.sessionProvider.arenaVisitor.gui.isEpicBattle())
            self.updateTopLog()

    def onExitBattlePage(self):
        if cache.player is not None:
            extended_log = any(self.logsEnabledSetting.itervalues())
            if extended_log:
                g_events.onKeyPressed -= self.keyEvent
                g_events.onVehicleAddUpdate -= self.onVehicleAddUpdate
            if cfg.log_total[GLOBAL.ENABLED] or extended_log:
                feedback = self.sessionProvider.shared.feedback
                if feedback:
                    feedback.onPlayerFeedbackReceived -= self.__onPlayerFeedbackReceived
            self.input_log.clear()
            self.damage_log.clear()
            self.shots.clear()
            self.topMacro.clear()
        self.unsubscribe()
        super(DamageLog, self).onExitBattlePage()

    def subscribe(self):
        self.as_startUpdateS({CONSTANTS.D_LOG: cfg.log_damage_extended[GLOBAL.SETTINGS],
                              CONSTANTS.IN_LOG: cfg.log_input_extended[GLOBAL.SETTINGS],
                              CONSTANTS.MAIN_LOG: cfg.log_total[GLOBAL.SETTINGS]},
                             {CONSTANTS.D_LOG: cfg.log_damage_extended[GLOBAL.ENABLED],
                              CONSTANTS.IN_LOG: cfg.log_input_extended[GLOBAL.ENABLED],
                              CONSTANTS.MAIN_LOG: cfg.log_total[GLOBAL.ENABLED]})
        if cfg.log_input_extended[GLOBAL.ENABLED]:
            g_events.onPlayerVehicleDeath += self.onPlayerVehicleDeath
        if cfg.log_damage_extended[GLOBAL.ENABLED]:
            g_events.onPlayerKilledEnemy += self.onPlayerKilledEnemy

    def unsubscribe(self):
        if cfg.log_input_extended[GLOBAL.ENABLED]:
            g_events.onPlayerVehicleDeath -= self.onPlayerVehicleDeath
        if cfg.log_damage_extended[GLOBAL.ENABLED]:
            g_events.onPlayerKilledEnemy -= self.onPlayerKilledEnemy

    def updateAvgDamage(self, isEpicBattle):
        """sets the average damage of the selected tank"""
        if not cache.tankAvgDamage and not isEpicBattle:
            max_health = cache.player.vehicle.typeDescriptor.maxHealth
            cache.tankAvgDamage = max(CONSTANTS.RANDOM_MIN_AVG, float(max_health))
        elif isEpicBattle:
            cache.tankAvgDamage = CONSTANTS.FRONT_LINE_MIN_AVG
        self.topMacro[CONSTANTS.AVG_DAMAGE] = int(cache.tankAvgDamage)

    def keyEvent(self, key, isKeyDown):
        """hot key event"""
        if key == CONSTANTS.HOT_KEY:
            if cfg.log_damage_extended[GLOBAL.ENABLED]:
                self.updateExtendedLog(self.damage_log, cfg.log_damage_extended, CONSTANTS.D_LOG, altMode=isKeyDown)
            if cfg.log_input_extended[GLOBAL.ENABLED]:
                self.updateExtendedLog(self.input_log, cfg.log_input_extended, CONSTANTS.IN_LOG, altMode=isKeyDown)

    @staticmethod
    def percentToRBG(percent, saturation=0.5, brightness=1.0):
        """percent is float number in range 0 - 2.4"""
        normalized_percent = min(CONSTANTS.COLOR_MAX_PURPLE, percent * CONSTANTS.COLOR_MAX_GREEN)
        tuple_values = hsv_to_rgb(normalized_percent, saturation, brightness)
        r, g, b = (int(i * CONSTANTS.COLOR_MULTIPLIER) for i in tuple_values)
        return CONSTANTS.COLOR_FORMAT.format(r, g, b)

    def __onPlayerFeedbackReceived(self, events, *a, **kw):
        """wg Feedback event parser"""
        for event in events:
            e_type = event.getType()
            extra = event.getExtra()
            data = 0
            if e_type == EV_ID.PLAYER_SPOTTED_ENEMY:
                data += event.getCount()
            elif e_type in CONSTANTS.TOP_LOG_ASSIST or e_type in CONSTANTS.EXTENDED_DAMAGE:
                data += int(extra.getDamage())
            elif e_type == EV_ID.DESTRUCTIBLE_DAMAGED:
                data += int(extra)
            if e_type in CONSTANTS.TOP_MACROS_NAME:
                if e_type == EV_ID.PLAYER_ASSIST_TO_STUN_ENEMY and not self.topMacro[CONSTANTS.STUN_ICON]:
                    self.topMacro[CONSTANTS.STUN_ICON] = cfg.log_total[CONSTANTS.ICONS][CONSTANTS.STUN_ICON]
                    self.topMacro[CONSTANTS.ASSIST_STUN] = 0
                self.topMacro[CONSTANTS.TOP_MACROS_NAME[e_type]] += data
                self.updateTopLog()
            if e_type in CONSTANTS.EXTENDED_DAMAGE and self.logsEnabledSetting.get(e_type):
                self.addToExtendedLog(self.eveToLog[e_type], self.eveToLogConfig[e_type],
                                      CONSTANTS.EXTENDED_DAMAGE[e_type], event.getTargetID(),
                                      extra.getAttackReasonID(), data, extra.getShellType(),
                                      extra.isShellGold())

    def updateTopLog(self):
        """update global sums in log"""
        if cfg.log_total[GLOBAL.ENABLED]:
            value = self.topMacro[CONSTANTS.PLAYER_DAMAGE] / cache.tankAvgDamage
            self.topMacro[CONSTANTS.DAMAGE_AVG_COLOR] = self.percentToRBG(value, **cfg.log_total[CONSTANTS.AVG_COLOR])
            self.as_updateDamageS(cfg.log_total[CONSTANTS.TEMPLATE_MAIN_DMG] % self.topMacro)

    def onVehicleAddUpdate(self, vehicleID, vehicleType):
        """update log item in GM-mode"""
        vehicle = self.input_log.get(vehicleID, {})
        if vehicle and vehicle.get(CONSTANTS.VEHICLE_CLASS) is None:
            vehicle_ci = cfg.vehicle_types[CONSTANTS.VEHICLE_CLASS_ICON]
            vehicle_cc = cfg.vehicle_types[CONSTANTS.VEHICLE_CLASS_COLORS]
            vehicle[CONSTANTS.VEHICLE_CLASS] = vehicleType.classTag
            vehicle[CONSTANTS.TANK_NAMES] = {vehicleType.shortName}
            vehicle[CONSTANTS.TANK_NAME] = vehicleType.shortName
            vehicle[CONSTANTS.ICON_NAME] = vehicleType.iconName
            vehicle[CONSTANTS.TANK_LEVEL] = vehicleType.level
            vehicle[CONSTANTS.CLASS_ICON] = vehicle_ci.get(vehicleType.classTag, vehicle_ci[CONSTANTS.UNKNOWN_TAG])
            vehicle[CONSTANTS.CLASS_COLOR] = vehicle_cc.get(vehicleType.classTag, vehicle_cc[CONSTANTS.UNKNOWN_TAG])
            self.updateExtendedLog(self.input_log, cfg.log_input_extended, CONSTANTS.IN_LOG)

    def onPlayerVehicleDeath(self, killerID):
        self.input_log[CONSTANTS.KILLS].add(killerID)

    def onPlayerKilledEnemy(self, targetID):
        self.damage_log[CONSTANTS.KILLS].add(targetID)
        self.updateExtendedLog(self.damage_log, cfg.log_damage_extended, CONSTANTS.D_LOG)

    def addToExtendedLog(self, *args):
        """add or update log item
        :param args: log_dict, settings, log_name, vehicle_id, attack_reason_id, damage, shell_type, gold
        """
        log_dict, settings, log_name, vehicle_id, attack_reason_id, damage, shell_type, gold = args
        if vehicle_id not in self.shots[log_name]:
            self.shots[log_name].append(vehicle_id)
        is_dlog = log_name == CONSTANTS.D_LOG
        if shell_type is None:
            shell_type = CONSTANTS.UNDEFINED
            if is_dlog and attack_reason_id == GLOBAL.ZERO:
                shell_type = cache.player.getVehicleDescriptor().shot.shell.kind
        shell_icon_name = shell_type + "_PREMIUM" if gold else shell_type
        vehicle = log_dict.setdefault(vehicle_id, SafeDict())
        info = cache.arenaDP.getVehicleInfo(vehicle_id)
        if vehicle:
            vehicle[CONSTANTS.DAMAGE_LIST].append(damage)
            vehicle[CONSTANTS.TANK_NAMES].add(info.vehicleType.shortName)
        else:
            vehicle_ci = cfg.vehicle_types[CONSTANTS.VEHICLE_CLASS_ICON]
            vehicle_cc = cfg.vehicle_types[CONSTANTS.VEHICLE_CLASS_COLORS]
            class_tag = info.vehicleType.classTag
            vehicle[CONSTANTS.INDEX] = len(self.shots[log_name])
            vehicle[CONSTANTS.DAMAGE_LIST] = [damage]
            vehicle[CONSTANTS.VEHICLE_CLASS] = class_tag
            vehicle[CONSTANTS.TANK_NAMES] = {info.vehicleType.shortName}
            vehicle[CONSTANTS.ICON_NAME] = info.vehicleType.iconName
            vehicle[CONSTANTS.USER_NAME] = info.player.name
            vehicle[CONSTANTS.TANK_LEVEL] = info.vehicleType.level
            vehicle[CONSTANTS.KILLED_ICON] = GLOBAL.EMPTY_LINE
            vehicle[CONSTANTS.CLASS_ICON] = vehicle_ci.get(class_tag, vehicle_ci[CONSTANTS.UNKNOWN_TAG])
            vehicle[CONSTANTS.CLASS_COLOR] = vehicle_cc.get(class_tag, vehicle_cc[CONSTANTS.UNKNOWN_TAG])
        vehicle[CONSTANTS.SHOTS] = len(vehicle[CONSTANTS.DAMAGE_LIST])
        vehicle[CONSTANTS.TOTAL_DAMAGE] = sum(vehicle[CONSTANTS.DAMAGE_LIST])
        vehicle[CONSTANTS.ALL_DAMAGES] = CONSTANTS.COMMA.join(str(x) for x in vehicle[CONSTANTS.DAMAGE_LIST])
        vehicle[CONSTANTS.LAST_DAMAGE] = vehicle[CONSTANTS.DAMAGE_LIST][GLOBAL.LAST]
        vehicle[CONSTANTS.ATTACK_REASON] = cfg.log_global[CONSTANTS.ATTACK_REASON][ATTACK_REASONS[attack_reason_id]]
        vehicle[CONSTANTS.SHELL_TYPE] = settings[CONSTANTS.SHELL_TYPES][shell_type]
        vehicle[CONSTANTS.SHELL_ICON] = settings[CONSTANTS.SHELL_ICONS][shell_icon_name]
        vehicle[CONSTANTS.SHELL_COLOR] = settings[CONSTANTS.SHELL_COLOR][CONSTANTS.SHELL[gold]]
        vehicle[CONSTANTS.TANK_NAME] = CONSTANTS.LIST_SEPARATOR.join(sorted(vehicle[CONSTANTS.TANK_NAMES]))
        vehicle_id = cache.player.playerVehicleID if not is_dlog else vehicle_id
        vehicle_max_health = cache.arenaDP.getVehicleInfo(vehicle_id).vehicleType.maxHealth
        percent = float(vehicle[CONSTANTS.TOTAL_DAMAGE]) / vehicle_max_health
        vehicle[CONSTANTS.PERCENT_AVG_COLOR] = self.percentToRBG(percent, **settings[CONSTANTS.AVG_COLOR])
        callback(0.1, lambda: self.updateExtendedLog(log_dict, settings, log_name))

    def updateExtendedLog(self, log_dict, settings, log_name, altMode=False):
        """
        Final log processing and flash output,
        also works when the alt mode is activated by hot key.
        """
        if log_dict:
            template = GLOBAL.EMPTY_LINE.join(settings[CONSTANTS.LOG_MODE[int(altMode)]])
            log = self.shots[log_name]
            if len(log) > CONSTANTS.LOG_MAX_LEN:
                log = log[-CONSTANTS.LOG_MAX_LEN:]
            data = reversed(log) if settings[CONSTANTS.REVERSE] else log
            for vehicleID in log:
                if vehicleID in log_dict[CONSTANTS.KILLS] and not log_dict[vehicleID][CONSTANTS.KILLED_ICON]:
                    log_dict[vehicleID][CONSTANTS.KILLED_ICON] = settings[CONSTANTS.KILLED_ICON]
            self.as_updateLogS(log_name, CONSTANTS.NEW_LINE.join(template % log_dict[key] for key in data))

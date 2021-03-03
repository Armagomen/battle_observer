from collections import defaultdict
from colorsys import hsv_to_rgb

from constants import ATTACK_REASONS
from gui.battle_control.battle_constants import FEEDBACK_EVENT_ID as EV_ID
from gui.shared.gui_items.Vehicle import VEHICLE_CLASS_NAME
from ..core import cfg, cache, keysParser
from ..core.bo_constants import DAMAGE_LOG as CONSTANTS, GLOBAL
from ..core.utils.common import callback, logWarning
from ..meta.battle.damage_logs_meta import DamageLogsMeta


class DamageLog(DamageLogsMeta):

    def __init__(self):
        super(DamageLog, self).__init__()
        self.input_log = {}
        self.damage_log = {}
        self.top_log = defaultdict(int, cfg.log_total[CONSTANTS.ICONS])
        self.isSPG = False

    def _populate(self):
        super(DamageLog, self)._populate()
        self.as_startUpdateS({CONSTANTS.D_LOG: cfg.log_damage_extended[GLOBAL.SETTINGS],
                              CONSTANTS.IN_LOG: cfg.log_input_extended[GLOBAL.SETTINGS],
                              CONSTANTS.MAIN_LOG: cfg.log_total[GLOBAL.SETTINGS]},
                             {CONSTANTS.D_LOG: cfg.log_damage_extended[GLOBAL.ENABLED],
                              CONSTANTS.IN_LOG: cfg.log_input_extended[GLOBAL.ENABLED],
                              CONSTANTS.MAIN_LOG: cfg.log_total[GLOBAL.ENABLED]})

    @staticmethod
    def isLogEnabled(eventType):
        if eventType == EV_ID.PLAYER_DAMAGED_HP_ENEMY:
            return cfg.log_damage_extended[GLOBAL.ENABLED]
        elif eventType == EV_ID.ENEMY_DAMAGED_HP_PLAYER:
            return cfg.log_input_extended[GLOBAL.ENABLED]
        logWarning(CONSTANTS.WARNING_MESSAGE)
        return False

    def getLogDictAndSettings(self, eventType):
        if eventType == EV_ID.PLAYER_DAMAGED_HP_ENEMY:
            return self.damage_log, cfg.log_damage_extended
        elif eventType == EV_ID.ENEMY_DAMAGED_HP_PLAYER:
            return self.input_log, cfg.log_input_extended
        logWarning(CONSTANTS.WARNING_MESSAGE)
        return None, None

    def onEnterBattlePage(self):
        super(DamageLog, self).onEnterBattlePage()
        if self._player is not None and self._player.vehicle is not None:
            self.input_log.update({CONSTANTS.KILLS: set(), CONSTANTS.SHOTS: []})
            self.damage_log.update({CONSTANTS.KILLS: set(), CONSTANTS.SHOTS: []})
            self.isSPG = VEHICLE_CLASS_NAME.SPG in self._player.vehicleTypeDescriptor.type.tags
            extended_log = cfg.log_damage_extended[GLOBAL.ENABLED] or cfg.log_input_extended[GLOBAL.ENABLED]
            if extended_log:
                cache.logsEnable = extended_log
                keysParser.onKeyPressed += self.keyEvent
                arena = self._arenaVisitor.getArenaSubscription()
                if arena is not None:
                    arena.onVehicleAdded += self.onVehicleAddUpdate
                    arena.onVehicleUpdated += self.onVehicleAddUpdate
                    arena.onVehicleKilled += self.onVehicleKilled
                keysParser.registerComponent(CONSTANTS.HOT_KEY, cfg.log_global[CONSTANTS.HOT_KEY])
            if cfg.log_total[GLOBAL.ENABLED] or extended_log:
                feedback = self.sessionProvider.shared.feedback
                if feedback:
                    feedback.onPlayerFeedbackReceived += self.__onPlayerFeedbackReceived
            if not self.isSPG:
                self.top_log.update(stun=GLOBAL.EMPTY_LINE, stunIcon=GLOBAL.EMPTY_LINE)
            self.updateAvgDamage(self.sessionProvider.arenaVisitor.gui.isEpicBattle())
            self.updateTopLog()

    def onExitBattlePage(self):
        if self._player is not None:
            extended_log = cfg.log_damage_extended[GLOBAL.ENABLED] or cfg.log_input_extended[GLOBAL.ENABLED]
            if extended_log:
                keysParser.onKeyPressed -= self.keyEvent
                arena = self._arenaVisitor.getArenaSubscription()
                if arena is not None:
                    arena.onVehicleAdded -= self.onVehicleAddUpdate
                    arena.onVehicleUpdated -= self.onVehicleAddUpdate
                    arena.onVehicleKilled -= self.onVehicleKilled
            if cfg.log_total[GLOBAL.ENABLED] or extended_log:
                feedback = self.sessionProvider.shared.feedback
                if feedback:
                    feedback.onPlayerFeedbackReceived -= self.__onPlayerFeedbackReceived
            self.input_log.clear()
            self.damage_log.clear()
            self.top_log.clear()
        super(DamageLog, self).onExitBattlePage()

    def updateAvgDamage(self, isEpicBattle):
        """sets the average damage of the selected tank"""
        if self._player is not None and not cache.tankAvgDamage and not isEpicBattle:
            max_health = self._player.vehicle.typeDescriptor.maxHealth
            cache.tankAvgDamage = max(CONSTANTS.RANDOM_MIN_AVG, float(max_health))
        elif isEpicBattle:
            cache.tankAvgDamage = CONSTANTS.FRONT_LINE_MIN_AVG
        self.top_log[CONSTANTS.AVG_DAMAGE] = int(cache.tankAvgDamage)

    def keyEvent(self, key, isKeyDown):
        """hot key event"""
        if key == CONSTANTS.HOT_KEY:
            if cfg.log_damage_extended[GLOBAL.ENABLED]:
                self.updateExtendedLog(self.damage_log, cfg.log_damage_extended, altMode=isKeyDown)
            if cfg.log_input_extended[GLOBAL.ENABLED]:
                self.updateExtendedLog(self.input_log, cfg.log_input_extended, altMode=isKeyDown)

    @staticmethod
    def percentToRBG(percent, saturation=0.5, brightness=1.0):
        """percent is float number in range 0 - 2.4"""
        normalized_percent = min(CONSTANTS.COLOR_MAX_PURPLE, percent * CONSTANTS.COLOR_MAX_GREEN)
        tuple_values = hsv_to_rgb(normalized_percent, saturation, brightness)
        r, g, b = (int(i * CONSTANTS.COLOR_MULTIPLIER) for i in tuple_values)
        return CONSTANTS.COLOR_FORMAT.format(r, g, b)

    def __onPlayerFeedbackReceived(self, events, *args, **kwargs):
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
                if e_type == EV_ID.PLAYER_ASSIST_TO_STUN_ENEMY and not self.top_log[CONSTANTS.STUN_ICON]:
                    self.top_log[CONSTANTS.STUN_ICON] = cfg.log_total[CONSTANTS.ICONS][CONSTANTS.STUN_ICON]
                    self.top_log[CONSTANTS.ASSIST_STUN] = 0
                self.top_log[CONSTANTS.TOP_MACROS_NAME[e_type]] += data
                self.updateTopLog()
            if e_type in CONSTANTS.EXTENDED_DAMAGE and self.isLogEnabled(e_type):
                log_dict, settings = self.getLogDictAndSettings(e_type)
                if log_dict is None:
                    return
                self.addToExtendedLog(log_dict, settings, event.getTargetID(),
                                      extra.getAttackReasonID(), data, extra.getShellType(), extra.isShellGold())

    def updateTopLog(self):
        """update global sums in log"""
        if cfg.log_total[GLOBAL.ENABLED]:
            value = self.top_log[CONSTANTS.PLAYER_DAMAGE] / cache.tankAvgDamage
            self.top_log[CONSTANTS.DAMAGE_AVG_COLOR] = self.percentToRBG(value, **cfg.log_total[CONSTANTS.AVG_COLOR])
            self.as_updateDamageS(cfg.log_total[CONSTANTS.TEMPLATE_MAIN_DMG] % self.top_log)

    def onVehicleAddUpdate(self, vehicleID, *args, **kwargs):
        """update log item in GM-mode"""
        vehicleInfoVO = self._arenaDP.getVehicleInfo(vehicleID)
        if vehicleInfoVO:
            vehicleType = vehicleInfoVO.vehicleType
            if vehicleType and vehicleType.maxHealth and vehicleType.classTag:
                vehicle = self.input_log.get(vehicleID, {})
                if vehicle and vehicle.get(CONSTANTS.VEHICLE_CLASS) is None:
                    vehicle_ci = cfg.vehicle_types[CONSTANTS.VEHICLE_CLASS_ICON]
                    vehicle_cc = cfg.vehicle_types[CONSTANTS.VEHICLE_CLASS_COLORS]
                    vehicle[CONSTANTS.VEHICLE_CLASS] = vehicleType.classTag
                    vehicle[CONSTANTS.TANK_NAMES] = {vehicleType.shortName}
                    vehicle[CONSTANTS.TANK_NAME] = vehicleType.shortName
                    vehicle[CONSTANTS.ICON_NAME] = vehicleType.iconName
                    vehicle[CONSTANTS.TANK_LEVEL] = vehicleType.level
                    vehicle[CONSTANTS.CLASS_ICON] = vehicle_ci.get(vehicleType.classTag,
                                                                   vehicle_ci[CONSTANTS.UNKNOWN_TAG])
                    vehicle[CONSTANTS.CLASS_COLOR] = vehicle_cc.get(vehicleType.classTag,
                                                                    vehicle_cc[CONSTANTS.UNKNOWN_TAG])
                    self.updateExtendedLog(self.input_log, cfg.log_input_extended)

    def onVehicleKilled(self, targetID, attackerID, *args, **kwargs):
        if self._player is not None:
            if self._player.playerVehicleID == targetID:
                self.input_log[CONSTANTS.KILLS].add(attackerID)
                self.updateExtendedLog(self.input_log, cfg.log_input_extended)
            elif self._player.playerVehicleID == attackerID:
                self.damage_log[CONSTANTS.KILLS].add(targetID)
                self.updateExtendedLog(self.damage_log, cfg.log_damage_extended)

    def checkShell(self, attack_reason_id, gold, is_dlog, shell_type):
        if is_dlog and attack_reason_id == GLOBAL.ZERO:
            if self._player is not None:
                v_desc = self._player.getVehicleDescriptor()
                shell_type = v_desc.shot.shell.kind
                shell_icon_name = v_desc.shot.shell.iconName
                gold = shell_icon_name in CONSTANTS.PREMIUM_SHELLS
            else:
                shell_type = CONSTANTS.UNDEFINED
                shell_icon_name = CONSTANTS.UNDEFINED
        elif shell_type in CONSTANTS.SHELL_LIST:
            shell_icon_name = shell_type + CONSTANTS.PREMIUM if gold else shell_type
        else:
            shell_type = CONSTANTS.UNDEFINED
            shell_icon_name = CONSTANTS.UNDEFINED
        return gold, shell_icon_name, shell_type

    def addToExtendedLog(self, log_dict, settings, vehicle_id, attack_reason_id, damage, shell_type, gold):
        """add or update log item"""
        is_dlog = log_dict is self.damage_log
        if vehicle_id not in log_dict[CONSTANTS.SHOTS]:
            log_dict[CONSTANTS.SHOTS].append(vehicle_id)
        gold, shell_icon_name, shell_type = self.checkShell(attack_reason_id, gold, is_dlog, shell_type)
        vehicle = log_dict.setdefault(vehicle_id, defaultdict(lambda: GLOBAL.CONFIG_ERROR))
        info = self._arenaDP.getVehicleInfo(vehicle_id)
        if vehicle:
            vehicle[CONSTANTS.DAMAGE_LIST].append(damage)
            vehicle[CONSTANTS.TANK_NAMES].add(info.vehicleType.shortName)
        else:
            vehicle_ci = cfg.vehicle_types[CONSTANTS.VEHICLE_CLASS_ICON]
            vehicle_cc = cfg.vehicle_types[CONSTANTS.VEHICLE_CLASS_COLORS]
            class_tag = info.vehicleType.classTag
            vehicle[CONSTANTS.INDEX] = len(log_dict[CONSTANTS.SHOTS])
            vehicle[CONSTANTS.DAMAGE_LIST] = [damage]
            vehicle[CONSTANTS.VEHICLE_CLASS] = class_tag
            vehicle[CONSTANTS.TANK_NAMES] = {info.vehicleType.shortName}
            vehicle[CONSTANTS.ICON_NAME] = info.vehicleType.iconName
            vehicle[CONSTANTS.USER_NAME] = info.player.name
            vehicle[CONSTANTS.TANK_LEVEL] = info.vehicleType.level
            vehicle[CONSTANTS.KILLED_ICON] = GLOBAL.EMPTY_LINE
            vehicle[CONSTANTS.CLASS_ICON] = vehicle_ci.get(class_tag, vehicle_ci[CONSTANTS.UNKNOWN_TAG])
            vehicle[CONSTANTS.CLASS_COLOR] = vehicle_cc.get(class_tag, vehicle_cc[CONSTANTS.UNKNOWN_TAG])
            vehicle_id = self._player.playerVehicleID if not is_dlog else vehicle_id
            vehicle[CONSTANTS.MAX_HEALTH] = self._arenaDP.getVehicleInfo(vehicle_id).vehicleType.maxHealth
        vehicle[CONSTANTS.SHOTS] = len(vehicle[CONSTANTS.DAMAGE_LIST])
        vehicle[CONSTANTS.TOTAL_DAMAGE] = sum(vehicle[CONSTANTS.DAMAGE_LIST])
        vehicle[CONSTANTS.ALL_DAMAGES] = CONSTANTS.COMMA.join(str(x) for x in vehicle[CONSTANTS.DAMAGE_LIST])
        vehicle[CONSTANTS.LAST_DAMAGE] = vehicle[CONSTANTS.DAMAGE_LIST][GLOBAL.LAST]
        vehicle[CONSTANTS.ATTACK_REASON] = cfg.log_global[CONSTANTS.ATTACK_REASON][ATTACK_REASONS[attack_reason_id]]
        vehicle[CONSTANTS.SHELL_TYPE] = settings[CONSTANTS.SHELL_TYPES][shell_type]
        vehicle[CONSTANTS.SHELL_ICON] = settings[CONSTANTS.SHELL_ICONS][shell_icon_name]
        vehicle[CONSTANTS.SHELL_COLOR] = settings[CONSTANTS.SHELL_COLOR][CONSTANTS.SHELL[gold]]
        vehicle[CONSTANTS.TANK_NAME] = CONSTANTS.LIST_SEPARATOR.join(sorted(vehicle[CONSTANTS.TANK_NAMES]))
        percent = float(vehicle[CONSTANTS.TOTAL_DAMAGE]) / vehicle[CONSTANTS.MAX_HEALTH]
        vehicle[CONSTANTS.PERCENT_AVG_COLOR] = self.percentToRBG(percent, **settings[CONSTANTS.AVG_COLOR])
        callback(0.1, lambda: self.updateExtendedLog(log_dict, settings))

    def updateExtendedLog(self, log_dict, settings, altMode=False):
        """
        Final log processing and flash output,
        also works when the alt mode is activated by hot key.
        """
        if log_dict:
            log_name = CONSTANTS.D_LOG if log_dict is self.damage_log else CONSTANTS.IN_LOG
            template = GLOBAL.EMPTY_LINE.join(settings[CONSTANTS.LOG_MODE[int(altMode)]])
            log = log_dict[CONSTANTS.SHOTS]
            if len(log) > CONSTANTS.LOG_MAX_LEN:
                log = log[-CONSTANTS.LOG_MAX_LEN:]
            data = reversed(log) if settings[CONSTANTS.REVERSE] else log
            for vehicleID in log:
                if vehicleID in log_dict[CONSTANTS.KILLS] and not log_dict[vehicleID][CONSTANTS.KILLED_ICON]:
                    log_dict[vehicleID][CONSTANTS.KILLED_ICON] = settings[CONSTANTS.KILLED_ICON]
            self.as_updateLogS(log_name, CONSTANTS.NEW_LINE.join(template % log_dict[key] for key in data))

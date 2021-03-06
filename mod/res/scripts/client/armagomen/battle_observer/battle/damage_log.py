from collections import defaultdict
from colorsys import hsv_to_rgb

from armagomen.battle_observer.core import config, keysParser
from armagomen.battle_observer.core.constants import DAMAGE_LOG, GLOBAL
from armagomen.battle_observer.meta.battle.damage_logs_meta import DamageLogsMeta
from armagomen.utils.common import callback, logWarning
from constants import ATTACK_REASONS, SHELL_TYPES_LIST
from gui.battle_control.battle_constants import FEEDBACK_EVENT_ID as EV_ID
from gui.shared.gui_items.Vehicle import VEHICLE_CLASS_NAME


class DamageLog(DamageLogsMeta):

    def __init__(self):
        super(DamageLog, self).__init__()
        self.input_log = {}
        self.damage_log = {}
        self.top_log = defaultdict(int, **config.log_total[DAMAGE_LOG.ICONS])
        self.isSPG = False

    def _populate(self):
        super(DamageLog, self)._populate()
        self.as_startUpdateS({DAMAGE_LOG.D_LOG: config.log_damage_extended[GLOBAL.SETTINGS],
                              DAMAGE_LOG.IN_LOG: config.log_input_extended[GLOBAL.SETTINGS],
                              DAMAGE_LOG.MAIN_LOG: config.log_total[GLOBAL.SETTINGS]},
                             {DAMAGE_LOG.D_LOG: config.log_damage_extended[GLOBAL.ENABLED],
                              DAMAGE_LOG.IN_LOG: config.log_input_extended[GLOBAL.ENABLED],
                              DAMAGE_LOG.MAIN_LOG: config.log_total[GLOBAL.ENABLED]})

    def _dispose(self):
        DAMAGE_LOG.AVG_DAMAGE_DATA = 0.0
        super(DamageLog, self)._dispose()

    @staticmethod
    def isLogEnabled(eventType):
        if eventType == EV_ID.PLAYER_DAMAGED_HP_ENEMY:
            return config.log_damage_extended[GLOBAL.ENABLED]
        elif eventType == EV_ID.ENEMY_DAMAGED_HP_PLAYER:
            return config.log_input_extended[GLOBAL.ENABLED]
        logWarning(DAMAGE_LOG.WARNING_MESSAGE)
        return False

    def getLogDictAndSettings(self, eventType):
        if eventType == EV_ID.PLAYER_DAMAGED_HP_ENEMY:
            return self.damage_log, config.log_damage_extended
        elif eventType == EV_ID.ENEMY_DAMAGED_HP_PLAYER:
            return self.input_log, config.log_input_extended
        logWarning(DAMAGE_LOG.WARNING_MESSAGE)
        return None, None

    def onEnterBattlePage(self):
        super(DamageLog, self).onEnterBattlePage()
        if self._player is not None and self._player.vehicle is not None:
            self.input_log.update(kills=set(), shots=list())
            self.damage_log.update(kills=set(), shots=list())
            self.isSPG = VEHICLE_CLASS_NAME.SPG in self._player.vehicleTypeDescriptor.type.tags
            extended_log = config.log_damage_extended[GLOBAL.ENABLED] or config.log_input_extended[GLOBAL.ENABLED]
            if extended_log:
                keysParser.onKeyPressed += self.keyEvent
                arena = self._arenaVisitor.getArenaSubscription()
                if arena is not None:
                    arena.onVehicleAdded += self.onVehicleAddUpdate
                    arena.onVehicleUpdated += self.onVehicleAddUpdate
                    arena.onVehicleKilled += self.onVehicleKilled
                keysParser.registerComponent(DAMAGE_LOG.HOT_KEY, config.log_global[DAMAGE_LOG.HOT_KEY])
            if config.log_total[GLOBAL.ENABLED] or extended_log:
                feedback = self.sessionProvider.shared.feedback
                if feedback:
                    feedback.onPlayerFeedbackReceived += self.__onPlayerFeedbackReceived
            if not self.isSPG:
                self.top_log.update(stun=GLOBAL.EMPTY_LINE, stunIcon=GLOBAL.EMPTY_LINE)
            self.updateAvgDamage(self.sessionProvider.arenaVisitor.gui.isEpicBattle())
            self.updateTopLog()

    def onExitBattlePage(self):
        if self._player is not None:
            extended_log = config.log_damage_extended[GLOBAL.ENABLED] or config.log_input_extended[GLOBAL.ENABLED]
            if extended_log:
                keysParser.onKeyPressed -= self.keyEvent
                arena = self._arenaVisitor.getArenaSubscription()
                if arena is not None:
                    arena.onVehicleAdded -= self.onVehicleAddUpdate
                    arena.onVehicleUpdated -= self.onVehicleAddUpdate
                    arena.onVehicleKilled -= self.onVehicleKilled
            if config.log_total[GLOBAL.ENABLED] or extended_log:
                feedback = self.sessionProvider.shared.feedback
                if feedback:
                    feedback.onPlayerFeedbackReceived -= self.__onPlayerFeedbackReceived
            self.input_log.clear()
            self.damage_log.clear()
            self.top_log.clear()
        super(DamageLog, self).onExitBattlePage()

    def updateAvgDamage(self, isEpicBattle):
        """sets the average damage of the selected tank"""
        if self._player is not None and not DAMAGE_LOG.AVG_DAMAGE_DATA and not isEpicBattle:
            max_health = self._player.vehicle.typeDescriptor.maxHealth
            DAMAGE_LOG.AVG_DAMAGE_DATA = max(DAMAGE_LOG.RANDOM_MIN_AVG, float(max_health))
        elif isEpicBattle:
            DAMAGE_LOG.AVG_DAMAGE_DATA = DAMAGE_LOG.FRONT_LINE_MIN_AVG
        self.top_log[DAMAGE_LOG.AVG_DAMAGE] = int(DAMAGE_LOG.AVG_DAMAGE_DATA)

    def keyEvent(self, key, isKeyDown):
        """hot key event"""
        if key == DAMAGE_LOG.HOT_KEY:
            if config.log_damage_extended[GLOBAL.ENABLED]:
                self.updateExtendedLog(self.damage_log, config.log_damage_extended, altMode=isKeyDown)
            if config.log_input_extended[GLOBAL.ENABLED]:
                self.updateExtendedLog(self.input_log, config.log_input_extended, altMode=isKeyDown)

    @staticmethod
    def percentToRBG(percent, saturation=0.5, brightness=1.0):
        """percent is float number in range 0 - 2.4"""
        normalized_percent = min(DAMAGE_LOG.COLOR_MAX_PURPLE, percent * DAMAGE_LOG.COLOR_MAX_GREEN)
        tuple_values = hsv_to_rgb(normalized_percent, saturation, brightness)
        r, g, b = (int(i * DAMAGE_LOG.COLOR_MULTIPLIER) for i in tuple_values)
        return DAMAGE_LOG.COLOR_FORMAT.format(r, g, b)

    def __onPlayerFeedbackReceived(self, events, *args, **kwargs):
        """wg Feedback event parser"""
        for event in events:
            e_type = event.getType()
            extra = event.getExtra()
            data = 0
            if e_type == EV_ID.PLAYER_SPOTTED_ENEMY:
                data += event.getCount()
            elif e_type in DAMAGE_LOG.TOP_LOG_ASSIST or e_type in DAMAGE_LOG.EXTENDED_DAMAGE:
                data += int(extra.getDamage())
            elif e_type == EV_ID.DESTRUCTIBLE_DAMAGED:
                data += int(extra)
            if e_type in DAMAGE_LOG.TOP_MACROS_NAME:
                if e_type == EV_ID.PLAYER_ASSIST_TO_STUN_ENEMY and not self.top_log[DAMAGE_LOG.STUN_ICON]:
                    self.top_log[DAMAGE_LOG.STUN_ICON] = config.log_total[DAMAGE_LOG.ICONS][DAMAGE_LOG.STUN_ICON]
                    self.top_log[DAMAGE_LOG.ASSIST_STUN] = 0
                self.top_log[DAMAGE_LOG.TOP_MACROS_NAME[e_type]] += data
                self.updateTopLog()
            if e_type in DAMAGE_LOG.EXTENDED_DAMAGE and self.isLogEnabled(e_type):
                log_dict, settings = self.getLogDictAndSettings(e_type)
                if log_dict is None:
                    return
                self.addToExtendedLog(log_dict, settings, event.getTargetID(),
                                      extra.getAttackReasonID(), data, extra.getShellType(), extra.isShellGold())

    def updateTopLog(self):
        """update global sums in log"""
        if config.log_total[GLOBAL.ENABLED]:
            value = self.top_log[DAMAGE_LOG.PLAYER_DAMAGE] / DAMAGE_LOG.AVG_DAMAGE_DATA
            self.top_log[DAMAGE_LOG.DAMAGE_AVG_COLOR] = self.percentToRBG(value, **config.log_total[DAMAGE_LOG.AVG_COLOR])
            self.as_updateDamageS(config.log_total[DAMAGE_LOG.TEMPLATE_MAIN_DMG] % self.top_log)

    def onVehicleAddUpdate(self, vehicleID, *args, **kwargs):
        """update log item in GM-mode"""
        vehicleInfoVO = self._arenaDP.getVehicleInfo(vehicleID)
        if vehicleInfoVO:
            vehicleType = vehicleInfoVO.vehicleType
            if vehicleType and vehicleType.maxHealth and vehicleType.classTag:
                vehicle = self.input_log.get(vehicleID, {})
                if vehicle and vehicle.get(DAMAGE_LOG.VEHICLE_CLASS) is None:
                    vehicle_ci = config.vehicle_types[DAMAGE_LOG.VEHICLE_CLASS_ICON]
                    vehicle_cc = config.vehicle_types[DAMAGE_LOG.VEHICLE_CLASS_COLORS]
                    vehicle[DAMAGE_LOG.VEHICLE_CLASS] = vehicleType.classTag
                    vehicle[DAMAGE_LOG.TANK_NAMES] = {vehicleType.shortName}
                    vehicle[DAMAGE_LOG.TANK_NAME] = vehicleType.shortName
                    vehicle[DAMAGE_LOG.ICON_NAME] = vehicleType.iconName
                    vehicle[DAMAGE_LOG.TANK_LEVEL] = vehicleType.level
                    vehicle[DAMAGE_LOG.CLASS_ICON] = vehicle_ci.get(vehicleType.classTag,
                                                                    vehicle_ci[DAMAGE_LOG.UNKNOWN_TAG])
                    vehicle[DAMAGE_LOG.CLASS_COLOR] = vehicle_cc.get(vehicleType.classTag,
                                                                     vehicle_cc[DAMAGE_LOG.UNKNOWN_TAG])
                    self.updateExtendedLog(self.input_log, config.log_input_extended)

    def onVehicleKilled(self, targetID, attackerID, *args, **kwargs):
        if self._player is not None:
            if self._player.playerVehicleID == targetID:
                self.input_log[DAMAGE_LOG.KILLS].add(attackerID)
                self.updateExtendedLog(self.input_log, config.log_input_extended)
            elif self._player.playerVehicleID == attackerID:
                self.damage_log[DAMAGE_LOG.KILLS].add(targetID)
                self.updateExtendedLog(self.damage_log, config.log_damage_extended)

    def checkShell(self, attack_reason_id, gold, is_dlog, shell_type):
        if is_dlog and attack_reason_id == GLOBAL.ZERO:
            if self._player is not None:
                v_desc = self._player.getVehicleDescriptor()
                shell_type = v_desc.shot.shell.kind
                shell_icon_name = v_desc.shot.shell.iconName
                gold = shell_icon_name in DAMAGE_LOG.PREMIUM_SHELLS
            else:
                shell_type = DAMAGE_LOG.UNDEFINED
                shell_icon_name = DAMAGE_LOG.UNDEFINED
        elif shell_type in DAMAGE_LOG.PREMIUM_SHELLS or shell_type in SHELL_TYPES_LIST:
            shell_icon_name = shell_type + DAMAGE_LOG.PREMIUM if gold else shell_type
        else:
            shell_type = DAMAGE_LOG.UNDEFINED
            shell_icon_name = DAMAGE_LOG.UNDEFINED
        return gold, shell_icon_name, shell_type

    def addToExtendedLog(self, log_dict, settings, vehicle_id, attack_reason_id, damage, shell_type, gold):
        """add or update log item"""
        is_dlog = log_dict is self.damage_log
        if vehicle_id not in log_dict[DAMAGE_LOG.SHOTS]:
            log_dict[DAMAGE_LOG.SHOTS].append(vehicle_id)
        gold, shell_icon_name, shell_type = self.checkShell(attack_reason_id, gold, is_dlog, shell_type)
        vehicle = log_dict.setdefault(vehicle_id, defaultdict(lambda: GLOBAL.CONFIG_ERROR))
        info = self._arenaDP.getVehicleInfo(vehicle_id)
        if vehicle:
            vehicle[DAMAGE_LOG.DAMAGE_LIST].append(damage)
            vehicle[DAMAGE_LOG.TANK_NAMES].add(info.vehicleType.shortName)
        else:
            vehicle_ci = config.vehicle_types[DAMAGE_LOG.VEHICLE_CLASS_ICON]
            vehicle_cc = config.vehicle_types[DAMAGE_LOG.VEHICLE_CLASS_COLORS]
            class_tag = info.vehicleType.classTag
            vehicle[DAMAGE_LOG.INDEX] = len(log_dict[DAMAGE_LOG.SHOTS])
            vehicle[DAMAGE_LOG.DAMAGE_LIST] = [damage]
            vehicle[DAMAGE_LOG.VEHICLE_CLASS] = class_tag
            vehicle[DAMAGE_LOG.TANK_NAMES] = {info.vehicleType.shortName}
            vehicle[DAMAGE_LOG.ICON_NAME] = info.vehicleType.iconName
            vehicle[DAMAGE_LOG.USER_NAME] = info.player.name
            vehicle[DAMAGE_LOG.TANK_LEVEL] = info.vehicleType.level
            vehicle[DAMAGE_LOG.KILLED_ICON] = GLOBAL.EMPTY_LINE
            vehicle[DAMAGE_LOG.CLASS_ICON] = vehicle_ci.get(class_tag, vehicle_ci[DAMAGE_LOG.UNKNOWN_TAG])
            vehicle[DAMAGE_LOG.CLASS_COLOR] = vehicle_cc.get(class_tag, vehicle_cc[DAMAGE_LOG.UNKNOWN_TAG])
            vehicle_id = self._player.playerVehicleID if not is_dlog else vehicle_id
            vehicle[DAMAGE_LOG.MAX_HEALTH] = self._arenaDP.getVehicleInfo(vehicle_id).vehicleType.maxHealth
        vehicle[DAMAGE_LOG.SHOTS] = len(vehicle[DAMAGE_LOG.DAMAGE_LIST])
        vehicle[DAMAGE_LOG.TOTAL_DAMAGE] = sum(vehicle[DAMAGE_LOG.DAMAGE_LIST])
        vehicle[DAMAGE_LOG.ALL_DAMAGES] = DAMAGE_LOG.COMMA.join(str(x) for x in vehicle[DAMAGE_LOG.DAMAGE_LIST])
        vehicle[DAMAGE_LOG.LAST_DAMAGE] = vehicle[DAMAGE_LOG.DAMAGE_LIST][GLOBAL.LAST]
        vehicle[DAMAGE_LOG.ATTACK_REASON] = config.log_global[DAMAGE_LOG.ATTACK_REASON][ATTACK_REASONS[attack_reason_id]]
        vehicle[DAMAGE_LOG.SHELL_TYPE] = settings[DAMAGE_LOG.SHELL_TYPES][shell_type]
        vehicle[DAMAGE_LOG.SHELL_ICON] = settings[DAMAGE_LOG.SHELL_ICONS][shell_icon_name]
        vehicle[DAMAGE_LOG.SHELL_COLOR] = settings[DAMAGE_LOG.SHELL_COLOR][DAMAGE_LOG.SHELL[gold]]
        vehicle[DAMAGE_LOG.TANK_NAME] = DAMAGE_LOG.LIST_SEPARATOR.join(sorted(vehicle[DAMAGE_LOG.TANK_NAMES]))
        percent = float(vehicle[DAMAGE_LOG.TOTAL_DAMAGE]) / vehicle[DAMAGE_LOG.MAX_HEALTH]
        vehicle[DAMAGE_LOG.PERCENT_AVG_COLOR] = self.percentToRBG(percent, **settings[DAMAGE_LOG.AVG_COLOR])
        callback(0.1, lambda: self.updateExtendedLog(log_dict, settings))

    def updateExtendedLog(self, log_dict, settings, altMode=False):
        """
        Final log processing and flash output,
        also works when the alt mode is activated by hot key.
        """
        if log_dict:
            log_name = DAMAGE_LOG.D_LOG if log_dict is self.damage_log else DAMAGE_LOG.IN_LOG
            template = GLOBAL.EMPTY_LINE.join(settings[DAMAGE_LOG.LOG_MODE[int(altMode)]])
            log = log_dict[DAMAGE_LOG.SHOTS]
            if len(log) > DAMAGE_LOG.LOG_MAX_LEN:
                log = log[-DAMAGE_LOG.LOG_MAX_LEN:]
            data = reversed(log) if settings[DAMAGE_LOG.REVERSE] else log
            for vehicleID in log:
                if vehicleID in log_dict[DAMAGE_LOG.KILLS] and not log_dict[vehicleID][DAMAGE_LOG.KILLED_ICON]:
                    log_dict[vehicleID][DAMAGE_LOG.KILLED_ICON] = settings[DAMAGE_LOG.KILLED_ICON]
            self.as_updateLogS(log_name, DAMAGE_LOG.NEW_LINE.join(template % log_dict[key] for key in data))

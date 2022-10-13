from collections import defaultdict, namedtuple

from armagomen.battle_observer.meta.battle.damage_logs_meta import DamageLogsMeta
from armagomen.constants import DAMAGE_LOG, GLOBAL, VEHICLE_TYPES
from armagomen.utils.common import logDebug, logWarning, percentToRGB, getPercent
from armagomen.utils.keys_listener import g_keysListener
from constants import ATTACK_REASONS, BATTLE_LOG_SHELL_TYPES, SHELL_TYPES
from gui.battle_control.battle_constants import FEEDBACK_EVENT_ID

_BATTLE_LOG_SHELL_TYPES_TO_SHELL_TYPE = {
    BATTLE_LOG_SHELL_TYPES.ARMOR_PIERCING: SHELL_TYPES.ARMOR_PIERCING,
    BATTLE_LOG_SHELL_TYPES.ARMOR_PIERCING_HE: SHELL_TYPES.ARMOR_PIERCING_HE,
    BATTLE_LOG_SHELL_TYPES.ARMOR_PIERCING_CR: SHELL_TYPES.ARMOR_PIERCING_CR,
    BATTLE_LOG_SHELL_TYPES.HOLLOW_CHARGE: SHELL_TYPES.HOLLOW_CHARGE,
    BATTLE_LOG_SHELL_TYPES.HE_MODERN: SHELL_TYPES.HIGH_EXPLOSIVE,
    BATTLE_LOG_SHELL_TYPES.HE_LEGACY_STUN: 'HIGH_EXPLOSIVE_SPG_STUN',
    BATTLE_LOG_SHELL_TYPES.HE_LEGACY_NO_STUN: 'HIGH_EXPLOSIVE_SPG',
    BATTLE_LOG_SHELL_TYPES.SMOKE: SHELL_TYPES.SMOKE
}

LogData = namedtuple('LogData', 'kills id_list vehicles')


class DamageLog(DamageLogsMeta):

    def __init__(self):
        super(DamageLog, self).__init__()
        self.input_log = None
        self.damage_log = None
        self.top_log = None
        self.top_log_enabled = False
        self.extended_log_enabled = False
        self.vehicle_colors = defaultdict(lambda: self.vehicle_types[VEHICLE_TYPES.CLASS_COLORS][VEHICLE_TYPES.UNKNOWN],
                                          **self.vehicle_types[VEHICLE_TYPES.CLASS_COLORS])
        self.vehicle_icons = defaultdict(lambda: self.vehicle_types[VEHICLE_TYPES.CLASS_ICON][VEHICLE_TYPES.UNKNOWN],
                                         **self.vehicle_types[VEHICLE_TYPES.CLASS_ICON])

    def _populate(self):
        super(DamageLog, self)._populate()
        self.top_log = defaultdict(int, **self.settings.log_total[DAMAGE_LOG.ICONS])
        self.as_startUpdateS({DAMAGE_LOG.D_LOG: self.settings.log_damage_extended[GLOBAL.SETTINGS],
                              DAMAGE_LOG.IN_LOG: self.settings.log_input_extended[GLOBAL.SETTINGS],
                              DAMAGE_LOG.MAIN_LOG: self.settings.log_total[GLOBAL.SETTINGS]},
                             {DAMAGE_LOG.D_LOG: self.settings.log_damage_extended[GLOBAL.ENABLED],
                              DAMAGE_LOG.IN_LOG: self.settings.log_input_extended[GLOBAL.ENABLED],
                              DAMAGE_LOG.MAIN_LOG: self.settings.log_total[GLOBAL.ENABLED]})
        self.top_log_enabled = self.settings.log_total[GLOBAL.ENABLED]
        self.extended_log_enabled = (self.settings.log_damage_extended[GLOBAL.ENABLED] or
                                     self.settings.log_input_extended[GLOBAL.ENABLED])
        if self.extended_log_enabled:
            g_keysListener.registerComponent(self.onLogsAltMode, keyList=self.settings.log_global[DAMAGE_LOG.HOT_KEY])

    def isLogEnabled(self, eventType):
        if eventType == FEEDBACK_EVENT_ID.PLAYER_DAMAGED_HP_ENEMY:
            return self.settings.log_damage_extended[GLOBAL.ENABLED]
        elif eventType == FEEDBACK_EVENT_ID.ENEMY_DAMAGED_HP_PLAYER:
            return self.settings.log_input_extended[GLOBAL.ENABLED]
        return False

    def getLogDataAndSettings(self, eventType):
        if eventType == FEEDBACK_EVENT_ID.PLAYER_DAMAGED_HP_ENEMY:
            return self.damage_log, self.settings.log_damage_extended
        elif eventType == FEEDBACK_EVENT_ID.ENEMY_DAMAGED_HP_PLAYER:
            return self.input_log, self.settings.log_input_extended
        logWarning(DAMAGE_LOG.WARNING_MESSAGE)
        raise ValueError("eventType %s NOT FOUND" % eventType)

    def onEnterBattlePage(self):
        super(DamageLog, self).onEnterBattlePage()
        feedback = self.sessionProvider.shared.feedback
        if feedback:
            feedback.onPlayerFeedbackReceived += self.__onPlayerFeedbackReceived
            if self.extended_log_enabled:
                self.input_log = LogData(set(), list(), dict())
                self.damage_log = LogData(set(), list(), dict())
                arena = self._arenaVisitor.getArenaSubscription()
                if arena is not None:
                    arena.onVehicleUpdated += self.onVehicleUpdated
                    arena.onVehicleKilled += self.onVehicleKilled
            if self.top_log_enabled:
                if not self._arenaDP.getVehicleInfo().isSPG():
                    self.top_log.update(stun=GLOBAL.EMPTY_LINE, stunIcon=GLOBAL.EMPTY_LINE)
                self.updateAvgDamage()
                self.updateTopLog()

    def onExitBattlePage(self):
        feedback = self.sessionProvider.shared.feedback
        if feedback:
            feedback.onPlayerFeedbackReceived -= self.__onPlayerFeedbackReceived
            if self.extended_log_enabled:
                arena = self._arenaVisitor.getArenaSubscription()
                if arena is not None:
                    arena.onVehicleUpdated -= self.onVehicleUpdated
                    arena.onVehicleKilled -= self.onVehicleKilled
            if self.top_log_enabled:
                self.top_log.clear()
        super(DamageLog, self).onExitBattlePage()

    def updateAvgDamage(self):
        """sets the average damage to the selected tank"""
        if self._player is not None and not DAMAGE_LOG.AVG_DAMAGE_DATA:
            max_health = self._player.vehicle.typeDescriptor.maxHealth
            DAMAGE_LOG.AVG_DAMAGE_DATA = max(DAMAGE_LOG.RANDOM_MIN_AVG, max_health)
        self.top_log[DAMAGE_LOG.AVG_DAMAGE] = DAMAGE_LOG.AVG_DAMAGE_DATA
        self.top_log[DAMAGE_LOG.AVG_ASSIST] = DAMAGE_LOG.AVG_ASSIST_DATA

    def onLogsAltMode(self, isKeyDown):
        """hot key event"""
        if self.settings.log_damage_extended[GLOBAL.ENABLED]:
            self.updateExtendedLog(self.damage_log, self.settings.log_damage_extended, altMode=isKeyDown)
        if self.settings.log_input_extended[GLOBAL.ENABLED]:
            self.updateExtendedLog(self.input_log, self.settings.log_input_extended, altMode=isKeyDown)

    def parseEvent(self, event):
        """wg Feedback event parser"""
        e_type = event.getType()
        extra = event.getExtra()
        if self.top_log_enabled and e_type in DAMAGE_LOG.TOP_MACROS_NAME:
            if e_type == FEEDBACK_EVENT_ID.PLAYER_ASSIST_TO_STUN_ENEMY and not self.top_log[DAMAGE_LOG.STUN_ICON]:
                self.top_log[DAMAGE_LOG.STUN_ICON] = self.settings.log_total[DAMAGE_LOG.ICONS][DAMAGE_LOG.STUN_ICON]
                self.top_log[DAMAGE_LOG.ASSIST_STUN] = GLOBAL.ZERO
            self.top_log[DAMAGE_LOG.TOP_MACROS_NAME[e_type]] += self.unpackTopLogValue(e_type, event, extra)
            self.updateTopLog()
        if self.isLogEnabled(e_type):
            self.addToExtendedLog(e_type, event.getTargetID(), extra)

    @staticmethod
    def unpackTopLogValue(e_type, event, extra):
        if e_type == FEEDBACK_EVENT_ID.PLAYER_SPOTTED_ENEMY:
            return event.getCount()
        return extra.getDamage()

    def isSwitchToVehicle(self):
        observedVehID = self.sessionProvider.shared.vehicleState.getControllingVehicleID()
        playerVehicleID = self._arenaDP.getPlayerVehicleID()
        return playerVehicleID != observedVehID

    def __onPlayerFeedbackReceived(self, events):
        """shared.feedback player events"""
        if self.isSwitchToVehicle():
            return
        for event in events:
            self.parseEvent(event)

    def updateTopLog(self):
        """update global sums in log"""
        percentDamage = getPercent(self.top_log[DAMAGE_LOG.PLAYER_DAMAGE], DAMAGE_LOG.AVG_DAMAGE_DATA)
        percentAssist = getPercent(self.top_log[DAMAGE_LOG.ASSIST_DAMAGE], DAMAGE_LOG.AVG_ASSIST_DATA)
        self.top_log[DAMAGE_LOG.DAMAGE_AVG_COLOR] = percentToRGB(percentDamage, **self.settings.log_total[
            GLOBAL.AVG_COLOR])
        self.top_log[DAMAGE_LOG.ASSIST_AVG_COLOR] = percentToRGB(percentAssist, **self.settings.log_total[
            GLOBAL.AVG_COLOR])
        self.as_updateDamageS(self.settings.log_total[DAMAGE_LOG.TEMPLATE_MAIN_DMG] % self.top_log)

    def onVehicleUpdated(self, vehicleID, *args, **kwargs):
        """update log item in GM-mode"""
        vehicleInfoVO = self._arenaDP.getVehicleInfo(vehicleID)
        if vehicleInfoVO:
            vehicleType = vehicleInfoVO.vehicleType
            if vehicleType and vehicleType.maxHealth and vehicleType.classTag:
                log_data, settings = self.getLogDataAndSettings(FEEDBACK_EVENT_ID.ENEMY_DAMAGED_HP_PLAYER)
                vehicle = log_data.vehicles.get(vehicleID)
                if vehicle and vehicle.get(DAMAGE_LOG.VEHICLE_CLASS) is None:
                    self.createVehicle(vehicleInfoVO, vehicle, update=True)
                    self.updateExtendedLog(log_data, settings)

    def onVehicleKilled(self, targetID, attackerID, *args, **kwargs):
        if self._player is None or self._player.playerVehicleID not in (targetID, attackerID):
            return
        if self._player.playerVehicleID == targetID:
            eventID = FEEDBACK_EVENT_ID.ENEMY_DAMAGED_HP_PLAYER
            target = attackerID
        else:
            eventID = FEEDBACK_EVENT_ID.PLAYER_DAMAGED_HP_ENEMY
            target = targetID
        log_data, settings = self.getLogDataAndSettings(eventID)
        log_data.kills.add(target)
        self.updateExtendedLog(log_data, settings)

    def checkPlayerShell(self, extra):
        shell_name = DAMAGE_LOG.UNDEFINED
        shell_icon_name = DAMAGE_LOG.UNDEFINED
        gold = extra.isShellGold()
        if self._player is not None and extra.isShot():
            shell = self._player.getVehicleDescriptor().shot.shell
            shell_name = shell.kind
            shell_icon_name = shell.iconName
            gold = shell_icon_name in DAMAGE_LOG.PREMIUM_SHELLS or gold
        return shell_name, shell_icon_name, gold

    @staticmethod
    def checkShell(extra):
        shell_name = _BATTLE_LOG_SHELL_TYPES_TO_SHELL_TYPE.get(extra.getShellType(), DAMAGE_LOG.UNDEFINED)
        shell_icon_name = shell_name
        gold = extra.isShellGold()
        if gold:
            gold_name = shell_name + DAMAGE_LOG.PREMIUM
            if gold_name in DAMAGE_LOG.PREMIUM_SHELLS:
                shell_icon_name = gold_name
        return shell_name, shell_icon_name, gold

    def addToExtendedLog(self, e_type, target_id, extra):
        """add to log item"""
        is_player = e_type == FEEDBACK_EVENT_ID.PLAYER_DAMAGED_HP_ENEMY
        log_data, settings = self.getLogDataAndSettings(e_type)
        if target_id not in log_data.id_list:
            log_data.id_list.append(target_id)
        shell_name, shell_icon_name, gold = self.checkPlayerShell(extra) if is_player else self.checkShell(extra)
        logDebug("Shell type: {}, shell icon: {}, gold: {}, player: {}", shell_name, shell_icon_name, gold, is_player)
        vehicle = log_data.vehicles.setdefault(target_id, defaultdict(lambda: GLOBAL.CONFIG_ERROR))
        vehicleInfoVO = self._arenaDP.getVehicleInfo(target_id)
        maxHealth = vehicleInfoVO.vehicleType.maxHealth if is_player else self._player.vehicle.typeDescriptor.maxHealth
        if not vehicle:
            self.createVehicle(vehicleInfoVO, vehicle, logLen=len(log_data.id_list))
        self.updateVehicleData(extra, gold, settings, shell_icon_name, shell_name, vehicle, maxHealth)
        self.updateExtendedLog(log_data, settings)

    def updateVehicleData(self, extra, gold, settings, shell_icon_name, shell_name, vehicle, maxHealth):
        vehicle[DAMAGE_LOG.DAMAGE_LIST].append(extra.getDamage())
        vehicle[DAMAGE_LOG.SHOTS] = len(vehicle[DAMAGE_LOG.DAMAGE_LIST])
        vehicle[DAMAGE_LOG.TOTAL_DAMAGE] = sum(vehicle[DAMAGE_LOG.DAMAGE_LIST])
        vehicle[DAMAGE_LOG.ALL_DAMAGES] = DAMAGE_LOG.COMMA.join(str(x) for x in vehicle[DAMAGE_LOG.DAMAGE_LIST])
        vehicle[DAMAGE_LOG.LAST_DAMAGE] = vehicle[DAMAGE_LOG.DAMAGE_LIST][GLOBAL.LAST]
        vehicle[DAMAGE_LOG.ATTACK_REASON] = self.settings.log_global[DAMAGE_LOG.ATTACK_REASON][
            ATTACK_REASONS[extra.getAttackReasonID()]]
        vehicle[DAMAGE_LOG.SHELL_TYPE] = settings[DAMAGE_LOG.SHELL_TYPES][shell_name]
        vehicle[DAMAGE_LOG.SHELL_ICON] = settings[DAMAGE_LOG.SHELL_ICONS][shell_icon_name]
        vehicle[DAMAGE_LOG.SHELL_COLOR] = settings[DAMAGE_LOG.SHELL_COLOR][DAMAGE_LOG.SHELL[gold]]
        percent = getPercent(vehicle[DAMAGE_LOG.TOTAL_DAMAGE], maxHealth)
        vehicle[DAMAGE_LOG.PERCENT_AVG_COLOR] = percentToRGB(percent, **settings[GLOBAL.AVG_COLOR])

    def createVehicle(self, vehicleInfoVO, vehicle, update=False, logLen=1):
        if not update:
            vehicle[DAMAGE_LOG.INDEX] = logLen
            vehicle[DAMAGE_LOG.DAMAGE_LIST] = list()
            vehicle[DAMAGE_LOG.KILLED_ICON] = GLOBAL.EMPTY_LINE
            vehicle[DAMAGE_LOG.USER_NAME] = vehicleInfoVO.player.name
        vehicle[DAMAGE_LOG.VEHICLE_CLASS] = vehicleInfoVO.vehicleType.classTag
        vehicle[DAMAGE_LOG.TANK_NAME] = vehicleInfoVO.vehicleType.shortName
        vehicle[DAMAGE_LOG.ICON_NAME] = vehicleInfoVO.vehicleType.iconName
        vehicle[DAMAGE_LOG.TANK_LEVEL] = vehicleInfoVO.vehicleType.level
        vehicle[DAMAGE_LOG.CLASS_ICON] = self.vehicle_icons[vehicleInfoVO.vehicleType.classTag]
        vehicle[DAMAGE_LOG.CLASS_COLOR] = self.vehicle_colors[vehicleInfoVO.vehicleType.classTag]

    @staticmethod
    def getLogLines(log_data, settings, altMode):
        template = GLOBAL.EMPTY_LINE.join(settings[DAMAGE_LOG.LOG_MODE[int(altMode)]])
        for vehicleID in reversed(log_data.id_list) if settings[DAMAGE_LOG.REVERSE] else log_data.id_list:
            if vehicleID in log_data.kills and not log_data.vehicles[vehicleID][DAMAGE_LOG.KILLED_ICON]:
                log_data.vehicles[vehicleID][DAMAGE_LOG.KILLED_ICON] = settings[DAMAGE_LOG.KILLED_ICON]
            yield template % log_data.vehicles[vehicleID]

    def updateExtendedLog(self, log_data, settings, altMode=False):
        """
        Final log processing and flash output,
        also works when the alt mode is activated by hot key.
        """
        if not log_data.id_list:
            return
        result = DAMAGE_LOG.NEW_LINE.join(self.getLogLines(log_data, settings, altMode))
        self.as_updateLogS(DAMAGE_LOG.D_LOG if log_data is self.damage_log else DAMAGE_LOG.IN_LOG, result)

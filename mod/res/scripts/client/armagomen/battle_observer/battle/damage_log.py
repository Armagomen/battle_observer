from collections import defaultdict, namedtuple

from armagomen.battle_observer.core import cachedVehicleData
from armagomen.battle_observer.meta.battle.damage_logs_meta import DamageLogsMeta
from armagomen.constants import DAMAGE_LOG, GLOBAL, VEHICLE_TYPES, COLORS
from armagomen.utils.common import logDebug, percentToRGB, getPercent
from armagomen.utils.keys_listener import g_keysListener
from constants import ATTACK_REASONS, BATTLE_LOG_SHELL_TYPES
from gui.Scaleform.locale.INGAME_GUI import INGAME_GUI
from gui.battle_control.avatar_getter import getVehicleTypeDescriptor
from gui.battle_control.battle_constants import FEEDBACK_EVENT_ID
from helpers import i18n

_SHELL_TYPES_TO_STR = {
    BATTLE_LOG_SHELL_TYPES.ARMOR_PIERCING: INGAME_GUI.DAMAGELOG_SHELLTYPE_ARMOR_PIERCING,
    BATTLE_LOG_SHELL_TYPES.ARMOR_PIERCING_HE: INGAME_GUI.DAMAGELOG_SHELLTYPE_ARMOR_PIERCING_HE,
    BATTLE_LOG_SHELL_TYPES.ARMOR_PIERCING_CR: INGAME_GUI.DAMAGELOG_SHELLTYPE_ARMOR_PIERCING_CR,
    BATTLE_LOG_SHELL_TYPES.HOLLOW_CHARGE: INGAME_GUI.DAMAGELOG_SHELLTYPE_HOLLOW_CHARGE,
    BATTLE_LOG_SHELL_TYPES.HE_MODERN: INGAME_GUI.DAMAGELOG_SHELLTYPE_HIGH_EXPLOSIVE,
    BATTLE_LOG_SHELL_TYPES.HE_LEGACY_STUN: INGAME_GUI.DAMAGELOG_SHELLTYPE_HIGH_EXPLOSIVE,
    BATTLE_LOG_SHELL_TYPES.HE_LEGACY_NO_STUN: INGAME_GUI.DAMAGELOG_SHELLTYPE_HIGH_EXPLOSIVE
}
EXTENDED_FEEDBACK = (FEEDBACK_EVENT_ID.PLAYER_DAMAGED_HP_ENEMY, FEEDBACK_EVENT_ID.ENEMY_DAMAGED_HP_PLAYER)
PREMIUM_SHELL_END = "_PREMIUM"

_EVENT_TO_TOP_LOG_MACROS = {
    FEEDBACK_EVENT_ID.PLAYER_DAMAGED_HP_ENEMY: "playerDamage",
    FEEDBACK_EVENT_ID.PLAYER_USED_ARMOR: "blockedDamage",
    FEEDBACK_EVENT_ID.PLAYER_ASSIST_TO_KILL_ENEMY: "assistDamage",
    FEEDBACK_EVENT_ID.PLAYER_SPOTTED_ENEMY: "spottedTanks",
    FEEDBACK_EVENT_ID.PLAYER_ASSIST_TO_STUN_ENEMY: "stun"
}

_EVENT_TO_TOP_LOG_AVG_MACROS = {
    FEEDBACK_EVENT_ID.PLAYER_DAMAGED_HP_ENEMY: ("tankAvgDamage", "tankDamageAvgColor"),
    FEEDBACK_EVENT_ID.PLAYER_USED_ARMOR: ("tankAvgBlocked", "tankBlockedAvgColor"),
    FEEDBACK_EVENT_ID.PLAYER_ASSIST_TO_KILL_ENEMY: ("tankAvgAssist", "tankAssistAvgColor"),
    FEEDBACK_EVENT_ID.PLAYER_ASSIST_TO_STUN_ENEMY: ("tankAvgStun", "tankStunAvgColor")
}

LogData = namedtuple('LogData', ('kills', 'id_list', 'vehicles', 'name', 'is_player'))


def getI18nShellName(shellType):
    return i18n.makeString(_SHELL_TYPES_TO_STR[shellType])


def isShellGold(shell):
    return shell.iconName.endswith(PREMIUM_SHELL_END)


class DamageLog(DamageLogsMeta):

    def __init__(self):
        super(DamageLog, self).__init__()
        self.__damage_log = None
        self.__input_log = None
        self.__isExtended = False
        self.__isKeyDown = GLOBAL.ZERO
        self.top_log = defaultdict(int)
        self.top_log_enabled = False
        self.vehicle_colors = defaultdict(lambda: self.vehicle_types[VEHICLE_TYPES.CLASS_COLORS][VEHICLE_TYPES.UNKNOWN],
                                          **self.vehicle_types[VEHICLE_TYPES.CLASS_COLORS])
        self.vehicle_icons = defaultdict(lambda: self.vehicle_types[VEHICLE_TYPES.CLASS_ICON][VEHICLE_TYPES.UNKNOWN],
                                         **self.vehicle_types[VEHICLE_TYPES.CLASS_ICON])

    def _populate(self):
        super(DamageLog, self)._populate()
        self.top_log_enabled = self.settings.log_total[GLOBAL.ENABLED]
        if self.top_log_enabled:
            self.top_log.update(self.settings.log_total[DAMAGE_LOG.ICONS],
                                tankDamageAvgColor=COLORS.NORMAL_TEXT,
                                tankAssistAvgColor=COLORS.NORMAL_TEXT,
                                tankBlockedAvgColor=COLORS.NORMAL_TEXT,
                                tankStunAvgColor=COLORS.NORMAL_TEXT)
            if self.gui.isRandomBattle():
                self.top_log.update(tankAvgDamage=cachedVehicleData.efficiencyAvgData.damage,
                                    tankAvgAssist=cachedVehicleData.efficiencyAvgData.assist,
                                    tankAvgStun=cachedVehicleData.efficiencyAvgData.stun,
                                    tankAvgBlocked=cachedVehicleData.efficiencyAvgData.blocked)
            self.as_createTopLogS(self.settings.log_total[GLOBAL.SETTINGS])
        self.__isExtended = self.settings.log_extended[GLOBAL.ENABLED]
        if self.__isExtended:
            self.as_createExtendedLogsS(self.settings.log_extended[GLOBAL.SETTINGS])
            g_keysListener.registerComponent(self.onLogsAltMode, keyList=self.settings.log_extended[DAMAGE_LOG.HOT_KEY])

    def isExtendedLogEventEnabled(self, eventType):
        return self.__isExtended and eventType in EXTENDED_FEEDBACK

    def isTopLogEventEnabled(self, eventType):
        return self.top_log_enabled and eventType in _EVENT_TO_TOP_LOG_MACROS

    def getLogData(self, eventType):
        if eventType == FEEDBACK_EVENT_ID.PLAYER_DAMAGED_HP_ENEMY:
            return self.__damage_log
        elif eventType == FEEDBACK_EVENT_ID.ENEMY_DAMAGED_HP_PLAYER:
            return self.__input_log
        raise ValueError(DAMAGE_LOG.WARNING_MESSAGE.format(eventType))

    def onBattleSessionStart(self):
        super(DamageLog, self).onBattleSessionStart()
        feedback = self.sessionProvider.shared.feedback
        if feedback:
            feedback.onPlayerFeedbackReceived += self.__onPlayerFeedbackReceived
            if self.__isExtended:
                self.__input_log = LogData(set(), list(), dict(), DAMAGE_LOG.IN_LOG, False)
                self.__damage_log = LogData(set(), list(), dict(), DAMAGE_LOG.D_LOG, True)
                arena = self._arenaVisitor.getArenaSubscription()
                if arena is not None:
                    arena.onVehicleUpdated += self.onVehicleUpdated
                    arena.onVehicleKilled += self.onVehicleKilled
            if self.top_log_enabled:
                self.top_log.update(stun=GLOBAL.EMPTY_LINE, stunIcon=GLOBAL.EMPTY_LINE)
                self.as_updateTopLogS(self.settings.log_total[DAMAGE_LOG.TEMPLATE_MAIN_DMG] % self.top_log)

    def onBattleSessionStop(self):
        feedback = self.sessionProvider.shared.feedback
        if feedback:
            feedback.onPlayerFeedbackReceived -= self.__onPlayerFeedbackReceived
            if self.__isExtended:
                arena = self._arenaVisitor.getArenaSubscription()
                if arena is not None:
                    arena.onVehicleUpdated -= self.onVehicleUpdated
                    arena.onVehicleKilled -= self.onVehicleKilled
            if self.top_log_enabled:
                self.top_log.clear()
        super(DamageLog, self).onBattleSessionStop()

    def onLogsAltMode(self, isKeyDown):
        """Hot key event"""
        self.__isKeyDown = int(isKeyDown)
        self.updateExtendedLog(self.__damage_log)
        self.updateExtendedLog(self.__input_log)

    def parseEvent(self, event):
        """wg Feedback event parser"""
        e_type = event.getType()
        extra = event.getExtra()
        if self.isTopLogEventEnabled(e_type):
            self.addToTopLog(e_type, event, extra)
        if self.isExtendedLogEventEnabled(e_type):
            self.addToExtendedLog(e_type, event.getTargetID(), extra)

    def addToTopLog(self, e_type, event, extra):
        macros = _EVENT_TO_TOP_LOG_MACROS[e_type]
        if e_type == FEEDBACK_EVENT_ID.PLAYER_ASSIST_TO_STUN_ENEMY and not self.top_log[DAMAGE_LOG.STUN_ICON]:
            self.top_log[DAMAGE_LOG.STUN_ICON] = self.settings.log_total[DAMAGE_LOG.ICONS][DAMAGE_LOG.STUN_ICON]
            self.top_log[macros] = GLOBAL.ZERO
        self.top_log[macros] += self.unpackTopLogValue(e_type, event, extra)
        if e_type in _EVENT_TO_TOP_LOG_AVG_MACROS:
            avgValueMacros, avgColorMacros = _EVENT_TO_TOP_LOG_AVG_MACROS[e_type]
            value = self.top_log[macros]
            avgValue = self.top_log[avgValueMacros]
            self.top_log[avgColorMacros] = self.getAVGColor(getPercent(value, avgValue))
        self.as_updateTopLogS(self.settings.log_total[DAMAGE_LOG.TEMPLATE_MAIN_DMG] % self.top_log)

    @staticmethod
    def unpackTopLogValue(e_type, event, extra):
        if e_type == FEEDBACK_EVENT_ID.PLAYER_SPOTTED_ENEMY:
            return event.getCount()
        return extra.getDamage()

    def isPostmortemSwitchedToAnotherVehicle(self):
        observedVehID = self.sessionProvider.shared.vehicleState.getControllingVehicleID()
        return self.playerVehicleID != observedVehID

    def __onPlayerFeedbackReceived(self, events):
        """Shared feedback player events"""
        if self.isPostmortemSwitchedToAnotherVehicle():
            return
        for event in events:
            self.parseEvent(event)

    def getAVGColor(self, percent):
        return percentToRGB(percent, **self.settings.log_total[GLOBAL.AVG_COLOR]) if percent else COLORS.NORMAL_TEXT

    def onVehicleUpdated(self, vehicleID, *args, **kwargs):
        """update log item in GM-mode"""
        vehicleInfoVO = self._arenaDP.getVehicleInfo(vehicleID)
        if vehicleInfoVO:
            vehicleType = vehicleInfoVO.vehicleType
            if vehicleType and vehicleType.maxHealth and vehicleType.classTag:
                log_data = self.getLogData(FEEDBACK_EVENT_ID.ENEMY_DAMAGED_HP_PLAYER)
                vehicle = log_data.vehicles.get(vehicleID)
                if vehicle and vehicle.get(DAMAGE_LOG.VEHICLE_CLASS) is None:
                    self.createVehicle(vehicleInfoVO, vehicle, update=True)
                    self.updateExtendedLog(log_data)

    def onVehicleKilled(self, targetID, attackerID, *args, **kwargs):
        if self.playerVehicleID in (targetID, attackerID):
            if self.playerVehicleID == targetID:
                log_data = self.getLogData(FEEDBACK_EVENT_ID.ENEMY_DAMAGED_HP_PLAYER)
                log_data.kills.add(attackerID)
            else:
                log_data = self.getLogData(FEEDBACK_EVENT_ID.PLAYER_DAMAGED_HP_ENEMY)
                log_data.kills.add(targetID)
            self.updateExtendedLog(log_data)

    @staticmethod
    def checkPlayerShell():
        typeDescriptor = getVehicleTypeDescriptor()
        if typeDescriptor is None:
            return DAMAGE_LOG.NOT_SHELL, False
        shell_name = getI18nShellName(BATTLE_LOG_SHELL_TYPES.getType(typeDescriptor.shot.shell))
        return shell_name, isShellGold(typeDescriptor.shot.shell)

    @staticmethod
    def checkShell(extra):
        return getI18nShellName(extra.getShellType()), extra.isShellGold()

    def addToExtendedLog(self, e_type, target_id, extra):
        """add to log item"""
        log_data = self.getLogData(e_type)
        if target_id not in log_data.id_list:
            log_data.id_list.append(target_id)
        if extra.isShot():
            shell_name, gold = self.checkPlayerShell() if log_data.is_player else self.checkShell(extra)
        else:
            shell_name, gold = DAMAGE_LOG.NOT_SHELL, False
        logDebug("Shell type: {}, gold: {}, is_player: {}", shell_name, gold, log_data.is_player)
        vehicle = log_data.vehicles.setdefault(target_id, defaultdict(lambda: GLOBAL.CONFIG_ERROR))
        vehicleInfoVO = self._arenaDP.getVehicleInfo(target_id)
        if log_data.is_player:
            maxHealth = vehicleInfoVO.vehicleType.maxHealth
        else:
            maxHealth = self._arenaDP.getVehicleInfo().vehicleType.maxHealth
        if not vehicle:
            self.createVehicle(vehicleInfoVO, vehicle, index=len(log_data.id_list))
        self.updateVehicleData(extra, gold, shell_name, vehicle, maxHealth, log_data.is_player)
        self.updateExtendedLog(log_data)

    def updateVehicleData(self, extra, gold, shell_name, vehicle, maxHealth, isPlayer):
        vehicle[DAMAGE_LOG.DAMAGE_LIST].append(extra.getDamage())
        vehicle[DAMAGE_LOG.SHOTS] = len(vehicle[DAMAGE_LOG.DAMAGE_LIST])
        vehicle[DAMAGE_LOG.TOTAL_DAMAGE] = sum(vehicle[DAMAGE_LOG.DAMAGE_LIST])
        vehicle[DAMAGE_LOG.ALL_DAMAGES] = DAMAGE_LOG.COMMA.join(str(x) for x in vehicle[DAMAGE_LOG.DAMAGE_LIST])
        vehicle[DAMAGE_LOG.LAST_DAMAGE] = vehicle[DAMAGE_LOG.DAMAGE_LIST][GLOBAL.LAST]
        vehicle[DAMAGE_LOG.ATTACK_REASON] = self.settings.log_extended[DAMAGE_LOG.ATTACK_REASON][
            ATTACK_REASONS[extra.getAttackReasonID()]]
        vehicle[DAMAGE_LOG.SHELL_TYPE] = shell_name
        vehicle[DAMAGE_LOG.SHELL_COLOR] = self.settings.log_extended[DAMAGE_LOG.SHELL_COLOR][DAMAGE_LOG.SHELL[gold]]
        percent = getPercent(vehicle[DAMAGE_LOG.TOTAL_DAMAGE], maxHealth)
        if not isPlayer:
            percent = max((1.0 - percent) * 0.7, 0.01)
        vehicle[DAMAGE_LOG.PERCENT_AVG_COLOR] = self.getAVGColor(percent)

    def createVehicle(self, vehicleInfoVO, vehicle, update=False, index=1):
        if not update:
            vehicle[DAMAGE_LOG.INDEX] = index
            vehicle[DAMAGE_LOG.DAMAGE_LIST] = list()
            vehicle[DAMAGE_LOG.KILLED_ICON] = GLOBAL.EMPTY_LINE
            vehicle[DAMAGE_LOG.USER_NAME] = vehicleInfoVO.player.name
        vehicle[DAMAGE_LOG.VEHICLE_CLASS] = vehicleInfoVO.vehicleType.classTag
        vehicle[DAMAGE_LOG.TANK_NAME] = vehicleInfoVO.vehicleType.shortName
        vehicle[DAMAGE_LOG.ICON_NAME] = vehicleInfoVO.vehicleType.iconName
        vehicle[DAMAGE_LOG.TANK_LEVEL] = vehicleInfoVO.vehicleType.level
        vehicle[DAMAGE_LOG.CLASS_ICON] = self.vehicle_icons[vehicleInfoVO.vehicleType.classTag]
        vehicle[DAMAGE_LOG.CLASS_COLOR] = self.vehicle_colors[vehicleInfoVO.vehicleType.classTag]

    def getLogLines(self, log_data):
        settings = self.settings.log_extended
        template = GLOBAL.EMPTY_LINE.join(settings[DAMAGE_LOG.LOG_MODE[self.__isKeyDown]])
        for vehicleID in reversed(log_data.id_list) if settings[DAMAGE_LOG.REVERSE] else log_data.id_list:
            if vehicleID in log_data.kills and not log_data.vehicles[vehicleID][DAMAGE_LOG.KILLED_ICON]:
                log_data.vehicles[vehicleID][DAMAGE_LOG.KILLED_ICON] = settings[DAMAGE_LOG.KILLED_ICON]
            yield template % log_data.vehicles[vehicleID]

    def updateExtendedLog(self, log_data):
        """
        Final log processing and flash output,
        also works when the alt mode activated by hot key.
        """
        if log_data is None or not log_data.id_list:
            return
        result = DAMAGE_LOG.NEW_LINE.join(self.getLogLines(log_data))
        self.as_updateExtendedLogS(log_data.name, result)

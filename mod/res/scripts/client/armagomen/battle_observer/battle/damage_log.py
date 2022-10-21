from collections import defaultdict, namedtuple

from armagomen.battle_observer.meta.battle.damage_logs_meta import DamageLogsMeta
from armagomen.constants import DAMAGE_LOG, GLOBAL, VEHICLE_TYPES
from armagomen.utils.common import logDebug, percentToRGB, getPercent
from armagomen.utils.keys_listener import g_keysListener
from constants import ATTACK_REASONS, BATTLE_LOG_SHELL_TYPES
from gui.Scaleform.locale.INGAME_GUI import INGAME_GUI
from gui.battle_control.battle_constants import FEEDBACK_EVENT_ID
from gui.battle_control.controllers.prebattle_setups_ctrl import IPrebattleSetupsListener
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
LogData = namedtuple('LogData', ('kills', 'id_list', 'vehicles', 'name', 'is_player'))


def getI18nShellName(shellType):
    return i18n.makeString(_SHELL_TYPES_TO_STR[shellType])


class DamageLog(DamageLogsMeta, IPrebattleSetupsListener):

    def __init__(self):
        super(DamageLog, self).__init__()
        self.__damage_log = None
        self.__input_log = None
        self.__maxHealth = GLOBAL.ZERO
        self.__isExtended = False
        self.top_log = None
        self.top_log_enabled = False
        self.vehicle_colors = defaultdict(lambda: self.vehicle_types[VEHICLE_TYPES.CLASS_COLORS][VEHICLE_TYPES.UNKNOWN],
                                          **self.vehicle_types[VEHICLE_TYPES.CLASS_COLORS])
        self.vehicle_icons = defaultdict(lambda: self.vehicle_types[VEHICLE_TYPES.CLASS_ICON][VEHICLE_TYPES.UNKNOWN],
                                         **self.vehicle_types[VEHICLE_TYPES.CLASS_ICON])

    def _populate(self):
        super(DamageLog, self)._populate()
        self.top_log = defaultdict(int, **self.settings.log_total[DAMAGE_LOG.ICONS])
        self.as_startUpdateS(self.settings.log_total, self.settings.log_extended)
        self.top_log_enabled = self.settings.log_total[GLOBAL.ENABLED]
        self.__isExtended = self.settings.log_extended[GLOBAL.ENABLED]
        if self.__isExtended:
            g_keysListener.registerComponent(self.onLogsAltMode, keyList=self.settings.log_global[DAMAGE_LOG.HOT_KEY])

    def updateVehicleParams(self, vehicle, *args):
        if self.__maxHealth != vehicle.descriptor.maxHealth:
            self.__maxHealth = vehicle.descriptor.maxHealth

    def __onVehicleControlling(self, vehicle):
        if self.isPostmortemSwitched():
            return
        if self.__maxHealth != vehicle.maxHealth:
            self.__maxHealth = vehicle.maxHealth

    def isExtendedLogEnabled(self, eventType):
        return self.__isExtended and eventType in EXTENDED_FEEDBACK

    def getLogData(self, eventType):
        if eventType == FEEDBACK_EVENT_ID.PLAYER_DAMAGED_HP_ENEMY:
            return self.__damage_log
        elif eventType == FEEDBACK_EVENT_ID.ENEMY_DAMAGED_HP_PLAYER:
            return self.__input_log
        raise ValueError(DAMAGE_LOG.WARNING_MESSAGE.format(eventType))

    def onEnterBattlePage(self):
        super(DamageLog, self).onEnterBattlePage()
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
                if not self._arenaDP.getVehicleInfo().isSPG():
                    self.top_log.update(stun=GLOBAL.EMPTY_LINE, stunIcon=GLOBAL.EMPTY_LINE)
                self.updateAvgDamage()
                self.updateTopLog()
        ctrl = self.sessionProvider.shared.vehicleState
        if ctrl is not None:
            ctrl.onVehicleControlling += self.__onVehicleControlling

    def onExitBattlePage(self):
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
        ctrl = self.sessionProvider.shared.vehicleState
        if ctrl is not None:
            ctrl.onVehicleControlling -= self.__onVehicleControlling
        super(DamageLog, self).onExitBattlePage()

    def updateAvgDamage(self):
        """Sets the average damage to the selected tank"""
        if self._player is not None and not DAMAGE_LOG.AVG_DAMAGE_DATA:
            max_health = self._player.vehicle.typeDescriptor.maxHealth
            DAMAGE_LOG.AVG_DAMAGE_DATA = max(DAMAGE_LOG.RANDOM_MIN_AVG, max_health)
        self.top_log[DAMAGE_LOG.AVG_DAMAGE] = DAMAGE_LOG.AVG_DAMAGE_DATA
        self.top_log[DAMAGE_LOG.AVG_ASSIST] = DAMAGE_LOG.AVG_ASSIST_DATA

    def onLogsAltMode(self, isKeyDown):
        """Hot key event"""
        self.updateExtendedLog(self.__damage_log, altMode=isKeyDown)
        self.updateExtendedLog(self.__input_log, altMode=isKeyDown)

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
        if self.isExtendedLogEnabled(e_type):
            self.addToExtendedLog(e_type, event.getTargetID(), extra)

    @staticmethod
    def unpackTopLogValue(e_type, event, extra):
        if e_type == FEEDBACK_EVENT_ID.PLAYER_SPOTTED_ENEMY:
            return event.getCount()
        return extra.getDamage()

    def isPostmortemSwitched(self):
        observedVehID = self.sessionProvider.shared.vehicleState.getControllingVehicleID()
        playerVehicleID = self._arenaDP.getPlayerVehicleID()
        return playerVehicleID != observedVehID

    def __onPlayerFeedbackReceived(self, events):
        """shared.feedback player events"""
        if self.isPostmortemSwitched():
            return
        for event in events:
            self.parseEvent(event)

    def getAVGColor(self, percent):
        return percentToRGB(percent, **self.settings.log_total[GLOBAL.AVG_COLOR])

    def updateTopLog(self):
        """update global sums in log"""
        percentDamage = getPercent(self.top_log[DAMAGE_LOG.PLAYER_DAMAGE], DAMAGE_LOG.AVG_DAMAGE_DATA)
        percentAssist = getPercent(self.top_log[DAMAGE_LOG.ASSIST_DAMAGE], DAMAGE_LOG.AVG_ASSIST_DATA)
        self.top_log[DAMAGE_LOG.DAMAGE_AVG_COLOR] = self.getAVGColor(percentDamage)
        self.top_log[DAMAGE_LOG.ASSIST_AVG_COLOR] = self.getAVGColor(percentAssist)
        self.as_updateDamageS(self.settings.log_total[DAMAGE_LOG.TEMPLATE_MAIN_DMG] % self.top_log)

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
        if self._player is None or self._player.playerVehicleID not in (targetID, attackerID):
            return
        if self._player.playerVehicleID == targetID:
            eventID = FEEDBACK_EVENT_ID.ENEMY_DAMAGED_HP_PLAYER
            target = attackerID
        else:
            eventID = FEEDBACK_EVENT_ID.PLAYER_DAMAGED_HP_ENEMY
            target = targetID
        log_data = self.getLogData(eventID)
        log_data.kills.add(target)
        self.updateExtendedLog(log_data)

    def checkPlayerShell(self):
        shell = self._player.getVehicleDescriptor().shot.shell
        shell_name = getI18nShellName(BATTLE_LOG_SHELL_TYPES.getType(shell))
        return shell_name, shell.isGold

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
            shell_name, gold = GLOBAL.EMPTY_LINE, False
        logDebug("Shell type: {}, gold: {}, is_player: {}", shell_name, gold, log_data.is_player)
        vehicle = log_data.vehicles.setdefault(target_id, defaultdict(lambda: GLOBAL.CONFIG_ERROR))
        vehicleInfoVO = self._arenaDP.getVehicleInfo(target_id)
        maxHealth = vehicleInfoVO.vehicleType.maxHealth if log_data.is_player else self.__maxHealth
        if not vehicle:
            self.createVehicle(vehicleInfoVO, vehicle, logLen=len(log_data.id_list))
        self.updateVehicleData(extra, gold, shell_name, vehicle, maxHealth)
        self.updateExtendedLog(log_data)

    def updateVehicleData(self, extra, gold, shell_name, vehicle, maxHealth):
        vehicle[DAMAGE_LOG.DAMAGE_LIST].append(extra.getDamage())
        vehicle[DAMAGE_LOG.SHOTS] = len(vehicle[DAMAGE_LOG.DAMAGE_LIST])
        vehicle[DAMAGE_LOG.TOTAL_DAMAGE] = sum(vehicle[DAMAGE_LOG.DAMAGE_LIST])
        vehicle[DAMAGE_LOG.ALL_DAMAGES] = DAMAGE_LOG.COMMA.join(str(x) for x in vehicle[DAMAGE_LOG.DAMAGE_LIST])
        vehicle[DAMAGE_LOG.LAST_DAMAGE] = vehicle[DAMAGE_LOG.DAMAGE_LIST][GLOBAL.LAST]
        vehicle[DAMAGE_LOG.ATTACK_REASON] = self.settings.log_global[DAMAGE_LOG.ATTACK_REASON][
            ATTACK_REASONS[extra.getAttackReasonID()]]
        vehicle[DAMAGE_LOG.SHELL_TYPE] = shell_name
        vehicle[DAMAGE_LOG.SHELL_COLOR] = self.settings.log_extended[DAMAGE_LOG.SHELL_COLOR][DAMAGE_LOG.SHELL[gold]]
        percent = getPercent(vehicle[DAMAGE_LOG.TOTAL_DAMAGE], maxHealth)
        vehicle[DAMAGE_LOG.PERCENT_AVG_COLOR] = self.getAVGColor(percent)

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

    def getLogLines(self, log_data, altMode):
        settings = self.settings.log_extended
        template = GLOBAL.EMPTY_LINE.join(settings[DAMAGE_LOG.LOG_MODE[int(altMode)]])
        for vehicleID in reversed(log_data.id_list) if settings[DAMAGE_LOG.REVERSE] else log_data.id_list:
            if vehicleID in log_data.kills and not log_data.vehicles[vehicleID][DAMAGE_LOG.KILLED_ICON]:
                log_data.vehicles[vehicleID][DAMAGE_LOG.KILLED_ICON] = settings[DAMAGE_LOG.KILLED_ICON]
            yield template % log_data.vehicles[vehicleID]

    def updateExtendedLog(self, log_data, altMode=False):
        """
        Final log processing and flash output,
        also works when the alt mode is activated by hot key.
        """
        if log_data is None or not log_data.id_list:
            return
        result = DAMAGE_LOG.NEW_LINE.join(self.getLogLines(log_data, altMode))
        self.as_updateLogS(log_data.name, result)

from collections import defaultdict, namedtuple

from armagomen._constants import DAMAGE_LOG, GLOBAL, COLORS, IMAGE_DIR
from armagomen.battle_observer.core import cachedVehicleData
from armagomen.battle_observer.meta.battle.damage_logs_meta import DamageLogsMeta
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
PREMIUM_SHELL_END = "PREMIUM"

_EVENT_TO_TOP_LOG_MACROS = {
    FEEDBACK_EVENT_ID.PLAYER_DAMAGED_HP_ENEMY: ("tankAvgDamage", "tankDamageAvgColor", "playerDamage"),
    FEEDBACK_EVENT_ID.PLAYER_USED_ARMOR: ("tankAvgBlocked", "tankBlockedAvgColor", "blockedDamage"),
    FEEDBACK_EVENT_ID.PLAYER_ASSIST_TO_KILL_ENEMY: ("tankAvgAssist", "tankAssistAvgColor", "assistDamage"),
    FEEDBACK_EVENT_ID.PLAYER_ASSIST_TO_STUN_ENEMY: ("tankAvgStun", "tankStunAvgColor", "stun"),
    FEEDBACK_EVENT_ID.PLAYER_SPOTTED_ENEMY: (None, None, "spottedTanks")
}

LogData = namedtuple('LogData', ('kills', 'id_list', 'vehicles', 'log_id'))


def getI18nShellName(shellType):
    return i18n.makeString(_SHELL_TYPES_TO_STR[shellType])


def getVehicleClassIcon(classTag):
    if not classTag:
        return GLOBAL.EMPTY_LINE
    return "<img src='{}/vehicle_types/{}.png' width='20' height='20' vspace='-6'>".format(IMAGE_DIR, classTag)


class DamageLog(DamageLogsMeta):

    def __init__(self):
        super(DamageLog, self).__init__()
        self._damage_done = None
        self._damage_received = None
        self._is_extended_log_enabled = False
        self._is_key_down = GLOBAL.ZERO
        self._is_top_log_enabled = False
        self._playerShell = (DAMAGE_LOG.NOT_SHELL, False)
        self.top_log = defaultdict(int)
        self.last_shell = defaultdict(lambda: (DAMAGE_LOG.NOT_SHELL, False))
        self.top_log_template = ""

    def _populate(self):
        super(DamageLog, self)._populate()
        feedback = self.sessionProvider.shared.feedback
        if feedback is None:
            return
        feedback.onPlayerFeedbackReceived += self.__onPlayerFeedbackReceived
        self._is_top_log_enabled = self.settings.log_total[GLOBAL.ENABLED]
        if self._is_top_log_enabled:
            self.as_createTopLogS(self.settings.log_total[GLOBAL.SETTINGS])
            self.update_top_log_start_params()
            self.as_updateTopLogS(self.top_log_template % self.top_log)
        self._is_extended_log_enabled = self.settings.log_extended[GLOBAL.ENABLED] and not self.gui.isEpicBattle()
        if self._is_extended_log_enabled:
            position = self.settings.log_extended[GLOBAL.SETTINGS]
            top_enabled = self.settings.log_extended[DAMAGE_LOG.D_DONE_ENABLED]
            bottom_enabled = self.settings.log_extended[DAMAGE_LOG.D_RECEIVED_ENABLED]
            self.as_createExtendedLogsS(position, top_enabled, bottom_enabled)
            g_keysListener.registerComponent(self.onLogsAltMode, keyList=self.settings.log_extended[DAMAGE_LOG.HOT_KEY])
            self._damage_done = LogData(set(), list(), dict(), DAMAGE_LOG.D_DONE)
            self._damage_received = LogData(set(), list(), dict(), DAMAGE_LOG.D_RECEIVED)
            arena = self._arenaVisitor.getArenaSubscription()
            if arena is not None:
                arena.onVehicleUpdated += self.onVehicleUpdated
                arena.onVehicleKilled += self.onVehicleKilled
            ammo_ctrl = self.sessionProvider.shared.ammo
            if ammo_ctrl is not None:
                ammo_ctrl.onGunReloadTimeSet += self._onGunReloadTimeSet

    def update_top_log_start_params(self):
        template = self.settings.log_total[DAMAGE_LOG.TEMPLATE_MAIN_DMG]
        self.top_log.update(self.settings.log_total[DAMAGE_LOG.ICONS],
                            tankDamageAvgColor=COLORS.WHITE,
                            tankAssistAvgColor=COLORS.WHITE,
                            tankBlockedAvgColor=COLORS.WHITE,
                            tankStunAvgColor=COLORS.WHITE,
                            tankAvgDamage=cachedVehicleData.efficiencyAvgData.damage,
                            tankAvgAssist=cachedVehicleData.efficiencyAvgData.assist,
                            tankAvgStun=cachedVehicleData.efficiencyAvgData.stun,
                            tankAvgBlocked=cachedVehicleData.efficiencyAvgData.blocked)
        if not self.isSPG():
            self.top_log.update(stun=GLOBAL.EMPTY_LINE, stunIcon=GLOBAL.EMPTY_LINE)
            template = [line for line in template if DAMAGE_LOG.STUN_ICON not in line]
        self.top_log_template = self.settings.log_total[DAMAGE_LOG.TOP_LOG_SEPARATE].join(template)

    def isExtendedLogEventEnabled(self, eventType):
        return self._is_extended_log_enabled and eventType in EXTENDED_FEEDBACK

    def isTopLogEventEnabled(self, eventType):
        return self._is_top_log_enabled and eventType in _EVENT_TO_TOP_LOG_MACROS

    def getLogData(self, eventType):
        if eventType == FEEDBACK_EVENT_ID.PLAYER_DAMAGED_HP_ENEMY:
            return self._damage_done
        elif eventType == FEEDBACK_EVENT_ID.ENEMY_DAMAGED_HP_PLAYER:
            return self._damage_received
        raise ValueError(DAMAGE_LOG.WARNING_MESSAGE.format(eventType))

    def _dispose(self):
        feedback = self.sessionProvider.shared.feedback
        if feedback is not None:
            feedback.onPlayerFeedbackReceived -= self.__onPlayerFeedbackReceived
            if self._is_extended_log_enabled:
                arena = self._arenaVisitor.getArenaSubscription()
                if arena is not None:
                    arena.onVehicleUpdated -= self.onVehicleUpdated
                    arena.onVehicleKilled -= self.onVehicleKilled
                ammo_ctrl = self.sessionProvider.shared.ammo
                if ammo_ctrl is not None:
                    ammo_ctrl.onGunReloadTimeSet -= self._onGunReloadTimeSet
            if self._is_top_log_enabled:
                self.top_log.clear()
        super(DamageLog, self)._dispose()

    def _onGunReloadTimeSet(self, _, state, *args, **kwargs):
        if state.isReloadingFinished():
            type_descriptor = getVehicleTypeDescriptor()
            if type_descriptor is None:
                self._playerShell = (DAMAGE_LOG.NOT_SHELL, False)
            shell = type_descriptor.shot.shell
            shell_name = getI18nShellName(BATTLE_LOG_SHELL_TYPES.getType(shell))
            is_shell_gold = shell.isGold or PREMIUM_SHELL_END in shell.iconName
            self._playerShell = (shell_name, is_shell_gold)

    def onLogsAltMode(self, isKeyDown):
        """Hot key event"""
        self._is_key_down = int(isKeyDown)
        self.updateExtendedLog(self._damage_done)
        self.updateExtendedLog(self._damage_received)

    def parseEvent(self, event):
        """wg Feedback event parser"""
        e_type = event.getType()
        extra = event.getExtra()
        if self.isTopLogEventEnabled(e_type):
            self.addToTopLog(e_type, event, extra)
        if self.isExtendedLogEventEnabled(e_type):
            self.addToExtendedLog(e_type, event.getTargetID(), extra)

    def addToTopLog(self, e_type, event, extra):
        avg_value_macros, avg_color_macros, value_macros = _EVENT_TO_TOP_LOG_MACROS[e_type]
        if e_type == FEEDBACK_EVENT_ID.PLAYER_ASSIST_TO_STUN_ENEMY and not self.top_log[DAMAGE_LOG.STUN_ICON]:
            self.top_log_template = self.settings.log_total[DAMAGE_LOG.TOP_LOG_SEPARATE].join(
                self.settings.log_total[DAMAGE_LOG.TEMPLATE_MAIN_DMG])
            self.top_log[DAMAGE_LOG.STUN_ICON] = self.settings.log_total[DAMAGE_LOG.ICONS][DAMAGE_LOG.STUN_ICON]
            self.top_log[value_macros] = GLOBAL.ZERO
        self.top_log[value_macros] += self.unpackTopLogValue(e_type, event, extra)
        if avg_value_macros is not None:
            value = self.top_log[value_macros]
            avg_value = self.top_log[avg_value_macros]
            self.top_log[avg_color_macros] = self.getAVGColor(getPercent(value, avg_value))
        self.as_updateTopLogS(self.top_log_template % self.top_log)

    @staticmethod
    def unpackTopLogValue(e_type, event, extra):
        if e_type == FEEDBACK_EVENT_ID.PLAYER_SPOTTED_ENEMY:
            return event.getCount()
        return extra.getDamage()

    def __onPlayerFeedbackReceived(self, events):
        """Shared feedback player events"""
        if self.isPlayerVehicle:
            for event in events:
                self.parseEvent(event)

    def getAVGColor(self, percent):
        return percentToRGB(percent, **self.settings.log_total[GLOBAL.AVG_COLOR]) if percent else COLORS.WHITE

    def onVehicleUpdated(self, vehicleID, *args, **kwargs):
        """update log item in GM-mode"""
        vehicle_info_vo = self.getVehicleInfo(vehicleID)
        if vehicle_info_vo:
            vehicle_type = vehicle_info_vo.vehicleType
            if vehicle_type and vehicle_type.maxHealth and vehicle_type.classTag:
                log_data = self.getLogData(FEEDBACK_EVENT_ID.ENEMY_DAMAGED_HP_PLAYER)
                vehicle = log_data.vehicles.get(vehicleID)
                if vehicle and vehicle.get(DAMAGE_LOG.VEHICLE_CLASS) is None:
                    self.createVehicle(vehicle_info_vo, vehicle, update=True)
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

    def checkShell(self, extra, target_id):
        shell_type = extra.getShellType()
        is_gold = extra.isShellGold()
        if shell_type is not None:
            self.last_shell[target_id] = (getI18nShellName(shell_type), is_gold)
        return self.last_shell[target_id]

    def addToExtendedLog(self, e_type, target_id, extra):
        """add to log item"""
        log_data = self.getLogData(e_type)
        is_player = log_data.log_id == DAMAGE_LOG.D_DONE
        if target_id not in log_data.id_list:
            log_data.id_list.append(target_id)
        if extra.isShot() or extra.isFire():
            shell_name, gold = self._playerShell if is_player else self.checkShell(extra, target_id)
        else:
            shell_name, gold = DAMAGE_LOG.NOT_SHELL, False
        logDebug("Shell type: {}, gold: {}, is_player: {}", shell_name, gold, is_player)
        vehicle = log_data.vehicles.setdefault(target_id, defaultdict(lambda: GLOBAL.CONFIG_ERROR))
        vehicle_info_vo = self.getVehicleInfo(target_id)
        if is_player:
            max_health = vehicle_info_vo.vehicleType.maxHealth
        else:
            max_health = self.getVehicleInfo().vehicleType.maxHealth
        if not vehicle:
            self.createVehicle(vehicle_info_vo, vehicle, index=len(log_data.id_list))
        self.updateVehicleData(extra, gold, shell_name, vehicle, max_health, is_player)
        self.updateExtendedLog(log_data)

    def updateVehicleData(self, extra, gold, shell_name, vehicle, maxHealth, isPlayer):
        vehicle[DAMAGE_LOG.DAMAGE_LIST].append(extra.getDamage())
        vehicle[DAMAGE_LOG.SHOTS] = len(vehicle[DAMAGE_LOG.DAMAGE_LIST])
        vehicle[DAMAGE_LOG.TOTAL_DAMAGE] = sum(vehicle[DAMAGE_LOG.DAMAGE_LIST])
        vehicle[DAMAGE_LOG.ALL_DAMAGES] = GLOBAL.COMMA_SEP.join(str(x) for x in vehicle[DAMAGE_LOG.DAMAGE_LIST])
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
        vehicle[DAMAGE_LOG.TANK_NAME] = vehicleInfoVO.vehicleType.guiName
        vehicle[DAMAGE_LOG.ICON_NAME] = vehicleInfoVO.vehicleType.iconName
        vehicle[DAMAGE_LOG.TANK_LEVEL] = vehicleInfoVO.vehicleType.level
        vehicle[DAMAGE_LOG.CLASS_ICON] = getVehicleClassIcon(vehicleInfoVO.vehicleType.classTag)
        vehicle[DAMAGE_LOG.CLASS_COLOR] = self.getVehicleClassColor(vehicleInfoVO.vehicleType.classTag)

    def getLogLines(self, log_data):
        extended = self.settings.log_extended
        template = GLOBAL.EMPTY_LINE.join(extended[DAMAGE_LOG.TEMPLATES][self._is_key_down])
        for vehicleID in reversed(log_data.id_list) if extended[DAMAGE_LOG.REVERSE] else log_data.id_list:
            if vehicleID in log_data.kills and not log_data.vehicles[vehicleID][DAMAGE_LOG.KILLED_ICON]:
                log_data.vehicles[vehicleID][DAMAGE_LOG.KILLED_ICON] = extended[DAMAGE_LOG.KILLED_ICON]
            yield template % log_data.vehicles[vehicleID]

    def updateExtendedLog(self, log_data):
        """
        Final log processing and flash output,
        also works when the alt mode activated by hot key.
        """
        if log_data is None or not log_data.id_list:
            return
        result = GLOBAL.NEW_LINE.join(self.getLogLines(log_data))
        self.as_updateExtendedLogS(log_data.log_id, result)

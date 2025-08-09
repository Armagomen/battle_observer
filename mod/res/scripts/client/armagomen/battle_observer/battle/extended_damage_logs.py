from collections import defaultdict, namedtuple

from armagomen._constants import COLORS, DAMAGE_LOG, EX_LOGS_ICONS, GLOBAL, IMAGE_DIR
from armagomen.battle_observer.meta.battle.extended_damage_logs_meta import ExtendedDamageLogsMeta
from armagomen.utils.common import getPercent, percentToRGB
from armagomen.utils.keys_listener import g_keysListener
from armagomen.utils.logging import logDebug
from constants import ATTACK_REASONS, BATTLE_LOG_SHELL_TYPES
from gui.battle_control.avatar_getter import getVehicleTypeDescriptor
from gui.battle_control.battle_constants import FEEDBACK_EVENT_ID
from gui.Scaleform.locale.INGAME_GUI import INGAME_GUI
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
NOT_SHELL = (DAMAGE_LOG.NOT_SHELL, False)
DEFAULT_REASON = "<img src='{}/efficiency/module.png' {}>".format(IMAGE_DIR, EX_LOGS_ICONS)
LogData = namedtuple('LogData', ('kills', 'id_list', 'vehicles', 'log_id'))


def getI18nShellName(shellType):
    if shellType is not None and shellType in _SHELL_TYPES_TO_STR:
        return i18n.makeString(_SHELL_TYPES_TO_STR[shellType])
    else:
        return DAMAGE_LOG.NOT_SHELL


def getVehicleClassIcon(classTag):
    if not classTag:
        classTag = "unknown"
    return "<img src='{}/vehicle_types/{}.png' width='20' height='20' vspace='-6'>".format(IMAGE_DIR, classTag)


class ExtendedDamageLogs(ExtendedDamageLogsMeta):

    def __init__(self):
        super(ExtendedDamageLogs, self).__init__()
        self._damage_done = LogData(set(), list(), dict(), DAMAGE_LOG.D_DONE)
        self._damage_received = LogData(set(), list(), dict(), DAMAGE_LOG.D_RECEIVED)
        self._is_key_down = 0
        self._playerShell = NOT_SHELL
        self.attack_reasons = defaultdict(lambda: DEFAULT_REASON)
        self.last_shell = defaultdict(lambda: NOT_SHELL)

    def _populate(self):
        super(ExtendedDamageLogs, self)._populate()
        feedback = self.sessionProvider.shared.feedback
        if feedback is None:
            return
        feedback.onPlayerFeedbackReceived += self.__onPlayerFeedbackReceived
        self.attack_reasons.update(self.settings[DAMAGE_LOG.ATTACK_REASON])
        g_keysListener.registerComponent(self.onLogsAltMode, keyList=self.settings[DAMAGE_LOG.HOT_KEY])
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onVehicleUpdated += self.onVehicleUpdated
            arena.onVehicleKilled += self.onVehicleKilled
        ammo_ctrl = self.sessionProvider.shared.ammo
        if ammo_ctrl is not None:
            ammo_ctrl.onGunReloadTimeSet += self._onGunReloadTimeSet

    def _dispose(self):
        feedback = self.sessionProvider.shared.feedback
        if feedback is not None:
            feedback.onPlayerFeedbackReceived -= self.__onPlayerFeedbackReceived
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onVehicleUpdated -= self.onVehicleUpdated
            arena.onVehicleKilled -= self.onVehicleKilled
        ammo_ctrl = self.sessionProvider.shared.ammo
        if ammo_ctrl is not None:
            ammo_ctrl.onGunReloadTimeSet -= self._onGunReloadTimeSet
        self._damage_done = None
        self._damage_received = None
        super(ExtendedDamageLogs, self)._dispose()

    def getLogData(self, eventType):
        if eventType == FEEDBACK_EVENT_ID.PLAYER_DAMAGED_HP_ENEMY:
            return self._damage_done
        elif eventType == FEEDBACK_EVENT_ID.ENEMY_DAMAGED_HP_PLAYER:
            return self._damage_received
        raise ValueError(DAMAGE_LOG.WARNING_MESSAGE.format(eventType))

    def _onGunReloadTimeSet(self, _, state, *args, **kwargs):
        if state.isReloadingFinished():
            type_descriptor = getVehicleTypeDescriptor()
            if type_descriptor is None:
                self._playerShell = NOT_SHELL
            else:
                shell = type_descriptor.shot.shell
                shell_name = getI18nShellName(BATTLE_LOG_SHELL_TYPES.getType(shell))
                is_shell_gold = shell.isGold or PREMIUM_SHELL_END in shell.iconName
                self._playerShell = (shell_name, is_shell_gold)

    def onLogsAltMode(self, isKeyDown):
        """Hot key event"""
        self._is_key_down = int(isKeyDown)
        self.updateExtendedLog(self._damage_done)
        self.updateExtendedLog(self._damage_received)

    def __onPlayerFeedbackReceived(self, events):
        """Shared feedback player events"""
        if self.isPlayerVehicle():
            for event in events:
                self.addToExtendedLog(event)

    def getAVGColor(self, percent):
        return percentToRGB(percent, color_blind=self._isColorBlind, **self.settings[GLOBAL.AVG_COLOR]) if percent else COLORS.WHITE

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
        if self.playerVehicleID not in (targetID, attackerID):
            return
        event_id, vehicle_id = (
            (FEEDBACK_EVENT_ID.ENEMY_DAMAGED_HP_PLAYER, attackerID)
            if self.playerVehicleID == targetID else
            (FEEDBACK_EVENT_ID.PLAYER_DAMAGED_HP_ENEMY, targetID)
        )
        log_data = self.getLogData(event_id)
        log_data.kills.add(vehicle_id)
        self.updateExtendedLog(log_data)

    def checkShell(self, extra, target_id):
        shell_type = extra.getShellType()
        is_gold = extra.isShellGold()
        if shell_type is not None:
            self.last_shell[target_id] = (getI18nShellName(shell_type), is_gold)
        return self.last_shell[target_id]

    def addToExtendedLog(self, event):
        """add to log item"""
        e_type = event.getType()
        if e_type not in EXTENDED_FEEDBACK:
            return
        log_data = self.getLogData(e_type)
        is_player = log_data.log_id == DAMAGE_LOG.D_DONE
        target_id = event.getTargetID()
        extra = event.getExtra()
        if target_id not in log_data.id_list:
            log_data.id_list.append(target_id)
        if extra.isShot() or extra.isFire():
            shell_name, gold = self._playerShell if is_player else self.checkShell(extra, target_id)
        else:
            shell_name, gold = DAMAGE_LOG.NOT_SHELL, False
        logDebug("Shell type: {}, gold: {}, is_player: {}", shell_name, gold, is_player)
        vehicle = log_data.vehicles.setdefault(target_id, defaultdict(lambda: "ERROR"))
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
        vehicle[DAMAGE_LOG.LAST_DAMAGE] = vehicle[DAMAGE_LOG.DAMAGE_LIST][-1]
        vehicle[DAMAGE_LOG.ATTACK_REASON] = self.attack_reasons[ATTACK_REASONS[extra.getAttackReasonID()]]
        vehicle[DAMAGE_LOG.SHELL_TYPE] = shell_name
        vehicle[DAMAGE_LOG.SHELL_COLOR] = self.settings[DAMAGE_LOG.SHELL_COLOR][DAMAGE_LOG.SHELL[gold]]
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
        template = GLOBAL.EMPTY_LINE.join(self.settings[DAMAGE_LOG.TEMPLATES][self._is_key_down])
        for vehicleID in reversed(log_data.id_list) if self.settings[DAMAGE_LOG.REVERSE] else log_data.id_list:
            if vehicleID in log_data.kills and not log_data.vehicles[vehicleID][DAMAGE_LOG.KILLED_ICON]:
                log_data.vehicles[vehicleID][DAMAGE_LOG.KILLED_ICON] = self.settings[DAMAGE_LOG.KILLED_ICON]
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

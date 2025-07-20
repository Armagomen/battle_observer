from collections import defaultdict

from armagomen._constants import COLORS, DAMAGE_LOG, GLOBAL
from armagomen.battle_observer.components.controllers import cachedVehicleData
from armagomen.battle_observer.meta.battle.damage_logs_meta import DamageLogsMeta
from armagomen.utils.common import getPercent, percentToRGB
from gui.battle_control.battle_constants import FEEDBACK_EVENT_ID

_EVENT_TO_TOP_LOG_MACROS = {
    FEEDBACK_EVENT_ID.PLAYER_DAMAGED_HP_ENEMY: ("tankAvgDamage", "tankDamageAvgColor", "playerDamage"),
    FEEDBACK_EVENT_ID.PLAYER_USED_ARMOR: ("tankAvgBlocked", "tankBlockedAvgColor", "blockedDamage"),
    FEEDBACK_EVENT_ID.PLAYER_ASSIST_TO_KILL_ENEMY: ("tankAvgAssist", "tankAssistAvgColor", "assistDamage"),
    FEEDBACK_EVENT_ID.PLAYER_ASSIST_TO_STUN_ENEMY: ("tankAvgStun", "tankStunAvgColor", "stun"),
    FEEDBACK_EVENT_ID.PLAYER_SPOTTED_ENEMY: (None, None, "spottedTanks")
}


class DamageLog(DamageLogsMeta):

    def __init__(self):
        super(DamageLog, self).__init__()
        self.top_log = defaultdict(int)
        self.top_log_template = ""
        self.stun_added = False

    def _populate(self):
        super(DamageLog, self)._populate()
        feedback = self.sessionProvider.shared.feedback
        if feedback is None:
            return
        feedback.onPlayerFeedbackReceived += self.__onPlayerFeedbackReceived
        if self._arenaVisitor.gui.isRandomBattle():
            avg_data = cachedVehicleData.efficiencyAvgData
        else:
            avg_data = cachedVehicleData.default
        template_list = self.settings[DAMAGE_LOG.TEMPLATE_MAIN_DMG]
        if not self.isSPG():
            template_list = (line for line in template_list if DAMAGE_LOG.STUN_ICON not in line)
        else:
            self.stun_added = True
        self.top_log.update(self.settings[DAMAGE_LOG.ICONS],
                            tankDamageAvgColor=COLORS.WHITE,
                            tankAssistAvgColor=COLORS.WHITE,
                            tankBlockedAvgColor=COLORS.WHITE,
                            tankStunAvgColor=COLORS.WHITE,
                            tankAvgDamage=avg_data.tankAvgDamage,
                            tankAvgAssist=avg_data.tankAvgAssist,
                            tankAvgStun=avg_data.tankAvgStun,
                            tankAvgBlocked=avg_data.tankAvgBlocked)
        self.top_log_template = self.settings[DAMAGE_LOG.TOP_LOG_SEPARATE].join(template_list)
        self.as_updateTopLogS(self.top_log_template % self.top_log)

    def _dispose(self):
        feedback = self.sessionProvider.shared.feedback
        if feedback is not None:
            feedback.onPlayerFeedbackReceived -= self.__onPlayerFeedbackReceived
        self.top_log.clear()
        super(DamageLog, self)._dispose()

    def addToTopLog(self, event):
        e_type = event.getType()
        if e_type not in _EVENT_TO_TOP_LOG_MACROS:
            return
        avg_value_macros, avg_color_macros, value_macros = _EVENT_TO_TOP_LOG_MACROS[e_type]
        if e_type == FEEDBACK_EVENT_ID.PLAYER_ASSIST_TO_STUN_ENEMY and not self.stun_added:
            self.stun_added = True
            self.top_log_template = self.settings[DAMAGE_LOG.TOP_LOG_SEPARATE].join(self.settings[DAMAGE_LOG.TEMPLATE_MAIN_DMG])
        self.top_log[value_macros] += self.unpackTopLogValue(e_type, event)
        if avg_value_macros is not None:
            value = self.top_log[value_macros]
            avg_value = self.top_log[avg_value_macros]
            self.top_log[avg_color_macros] = self.getAVGColor(getPercent(value, avg_value))
        self.as_updateTopLogS(self.top_log_template % self.top_log)

    @staticmethod
    def unpackTopLogValue(e_type, event):
        if e_type == FEEDBACK_EVENT_ID.PLAYER_SPOTTED_ENEMY:
            return event.getCount()
        return event.getExtra().getDamage()

    def __onPlayerFeedbackReceived(self, events):
        """Shared feedback player events"""
        if self.isPlayerVehicle():
            for event in events:
                self.addToTopLog(event)

    def getAVGColor(self, percent):
        return percentToRGB(percent, color_blind=self._isColorBlind, **self.settings[GLOBAL.AVG_COLOR]) if percent else COLORS.WHITE

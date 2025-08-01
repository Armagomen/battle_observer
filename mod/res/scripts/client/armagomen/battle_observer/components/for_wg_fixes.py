from armagomen._constants import DAMAGE_LOG, GLOBAL
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import cancelOverride, overrideMethod
from gui.battle_control.battle_constants import PERSONAL_EFFICIENCY_TYPE
from gui.Scaleform.daapi.view.battle.shared.damage_log_panel import _LogViewComponent, DamageLogPanel


class WG_Logs_Fix(object):
    BASE_WG_LOGS = (DamageLogPanel._addToTopLog, DamageLogPanel._updateTopLog,
                    DamageLogPanel._updateBottomLog, DamageLogPanel._addToBottomLog)

    def __init__(self):
        self.validated = {}
        user_settings.onModSettingsChanged += self.onModSettingsChanged

    def fini(self):
        user_settings.onModSettingsChanged -= self.onModSettingsChanged

    def addToLog(self, base, component, event):
        return base(component, [e for e in event if not self.validated.get(e.getType(), False)])

    def onModSettingsChanged(self, config, blockID):
        if blockID == DAMAGE_LOG.WG_LOGS_FIX:
            if config[GLOBAL.ENABLED]:
                overrideMethod(_LogViewComponent, "addToLog")(self.addToLog)
                self.validated.update(self.validateSettings(config))
            else:
                cancelOverride(_LogViewComponent, "addToLog", "addToLog")
            self.updatePositions(config)

    def updatePositions(self, config):
        DamageLogPanel._addToTopLog, DamageLogPanel._updateTopLog, DamageLogPanel._updateBottomLog, DamageLogPanel._addToBottomLog = \
            reversed(self.BASE_WG_LOGS) if config[GLOBAL.ENABLED] and config[DAMAGE_LOG.WG_POS] else self.BASE_WG_LOGS

    @staticmethod
    def validateSettings(config):
        return {PERSONAL_EFFICIENCY_TYPE.RECEIVED_CRITICAL_HITS: config[DAMAGE_LOG.WG_CRITICS],
                PERSONAL_EFFICIENCY_TYPE.BLOCKED_DAMAGE: config[DAMAGE_LOG.WG_BLOCKED],
                PERSONAL_EFFICIENCY_TYPE.ASSIST_DAMAGE: config[DAMAGE_LOG.WG_ASSIST],
                PERSONAL_EFFICIENCY_TYPE.STUN: config[DAMAGE_LOG.WG_ASSIST]}


logs_fix = WG_Logs_Fix()


def fini():
    logs_fix.fini()

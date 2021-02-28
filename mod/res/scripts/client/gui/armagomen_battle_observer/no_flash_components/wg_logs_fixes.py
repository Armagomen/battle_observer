from gui.Scaleform.daapi.view.battle.shared.damage_log_panel import _LogViewComponent, DamageLogPanel
from gui.battle_control.battle_constants import PERSONAL_EFFICIENCY_TYPE as _ETYPE
from ..core import cache
from ..core.bo_constants import DAMAGE_LOG
from ..core.utils.common import overrideMethod


class WGLogsFixes(object):
    __slots__ = ("validated",)
    BASE_WG_LOGS = (DamageLogPanel._addToTopLog, DamageLogPanel._updateTopLog,
                    DamageLogPanel._updateBottomLog, DamageLogPanel._addToBottomLog)

    def __init__(self):
        self.validated = {}
        cache.onModSettingsChanged += self.onModSettingsChanged

        @overrideMethod(DamageLogPanel, "_setSettings")
        def setSettings(base, panel, vis, cb):
            return base(panel, vis or cache.logsEnable, cb)

        @overrideMethod(_LogViewComponent, "addToLog")
        def addToLog(base, component, event):
            return base(component, [e for e in event if not self.validated.get(e.getType(), False)])

    def onModSettingsChanged(self, config, blockID):
        if blockID == DAMAGE_LOG.GLOBAL:
            self.validated = self.validateSettings(config)
            DamageLogPanel._addToTopLog, DamageLogPanel._updateTopLog, \
            DamageLogPanel._updateBottomLog, DamageLogPanel._addToBottomLog = \
                reversed(self.BASE_WG_LOGS) if config[DAMAGE_LOG.WG_POS] else self.BASE_WG_LOGS

    @staticmethod
    def validateSettings(config):
        return {_ETYPE.RECEIVED_CRITICAL_HITS: config[DAMAGE_LOG.WG_CRITS],
                _ETYPE.BLOCKED_DAMAGE: config[DAMAGE_LOG.WG_BLOCKED],
                _ETYPE.ASSIST_DAMAGE: config[DAMAGE_LOG.WG_ASSIST],
                _ETYPE.STUN: config[DAMAGE_LOG.WG_ASSIST]}


wg_logs_fixes = WGLogsFixes()

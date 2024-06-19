from armagomen._constants import DAMAGE_LOG, GLOBAL
from armagomen.battle_observer.settings import user
from armagomen.utils.common import overrideMethod
from gui.battle_control.battle_constants import PERSONAL_EFFICIENCY_TYPE as _ETYPE
from gui.Scaleform.daapi.view.battle.shared.damage_log_panel import _LogViewComponent, DamageLogPanel

BASE_WG_LOGS = (DamageLogPanel._addToTopLog, DamageLogPanel._updateTopLog,
                DamageLogPanel._updateBottomLog, DamageLogPanel._addToBottomLog)

validated = {}


@overrideMethod(_LogViewComponent, "addToLog")
def addToLog(base, component, event):
    if user.wg_logs[GLOBAL.ENABLED]:
        return base(component, [e for e in event if not validated.get(e.getType(), False)])
    return base(component, event)


def onModSettingsChanged(config, blockID):
    if blockID == DAMAGE_LOG.WG_LOGS_FIX:
        validated.update(validateSettings(config))
        DamageLogPanel._addToTopLog, DamageLogPanel._updateTopLog, \
            DamageLogPanel._updateBottomLog, DamageLogPanel._addToBottomLog = \
            reversed(BASE_WG_LOGS) if config[DAMAGE_LOG.WG_POS] else BASE_WG_LOGS


def validateSettings(config):
    return {_ETYPE.RECEIVED_CRITICAL_HITS: config[DAMAGE_LOG.WG_CRITICS],
            _ETYPE.BLOCKED_DAMAGE: config[DAMAGE_LOG.WG_BLOCKED],
            _ETYPE.ASSIST_DAMAGE: config[DAMAGE_LOG.WG_ASSIST],
            _ETYPE.STUN: config[DAMAGE_LOG.WG_ASSIST]}


user.onModSettingsChanged += onModSettingsChanged

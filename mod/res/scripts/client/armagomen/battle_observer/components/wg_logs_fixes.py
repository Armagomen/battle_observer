from armagomen.battle_observer.core import config
from armagomen.battle_observer.core.bo_constants import DAMAGE_LOG, GLOBAL
from armagomen.utils.common import overrideMethod
from gui.Scaleform.daapi.view.battle.shared.damage_log_panel import _LogViewComponent, DamageLogPanel
from gui.battle_control.battle_constants import PERSONAL_EFFICIENCY_TYPE as _ETYPE

BASE_WG_LOGS = (DamageLogPanel._addToTopLog, DamageLogPanel._updateTopLog,
                DamageLogPanel._updateBottomLog, DamageLogPanel._addToBottomLog)

validated = {}


@overrideMethod(DamageLogPanel, "_setSettings")
def setSettings(base, panel, vis, cb):
    return base(panel, vis or config.log_damage_extended[GLOBAL.ENABLED] or config.log_input_extended[GLOBAL.ENABLED], cb)


@overrideMethod(_LogViewComponent, "addToLog")
def addToLog(base, component, event):
    return base(component, [e for e in event if not validated.get(e.getType(), False)])


def onModSettingsChanged(config, blockID):
    if blockID == DAMAGE_LOG.GLOBAL:
        validated.update(validateSettings(config))
        DamageLogPanel._addToTopLog, DamageLogPanel._updateTopLog, \
        DamageLogPanel._updateBottomLog, DamageLogPanel._addToBottomLog = \
            reversed(BASE_WG_LOGS) if config[DAMAGE_LOG.WG_POS] else BASE_WG_LOGS


def validateSettings(config):
    return {_ETYPE.RECEIVED_CRITICAL_HITS: config[DAMAGE_LOG.WG_CRITS],
            _ETYPE.BLOCKED_DAMAGE: config[DAMAGE_LOG.WG_BLOCKED],
            _ETYPE.ASSIST_DAMAGE: config[DAMAGE_LOG.WG_ASSIST],
            _ETYPE.STUN: config[DAMAGE_LOG.WG_ASSIST]}


config.onModSettingsChanged += onModSettingsChanged

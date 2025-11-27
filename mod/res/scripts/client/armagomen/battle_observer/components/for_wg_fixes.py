import BigWorld
from _weakref import weakref
from armagomen._constants import DAMAGE_LOG, GLOBAL
from armagomen.utils.common import overrideMethod, toggleOverride
from armagomen.utils.events import g_events
from gui.battle_control.battle_constants import PERSONAL_EFFICIENCY_TYPE
from gui.Scaleform.daapi.view.battle.shared.damage_log_panel import _LogViewComponent, DamageLogPanel
from visual_script_client.vehicle_blocks import OnVehicleShaked


class WG_Logs_Fix(object):
    BASE_WG_LOGS = (DamageLogPanel._addToTopLog, DamageLogPanel._updateTopLog,
                    DamageLogPanel._updateBottomLog, DamageLogPanel._addToBottomLog)

    EFFICIENCY_TYPE_TO_CONFIG_KEY = {
        PERSONAL_EFFICIENCY_TYPE.RECEIVED_CRITICAL_HITS: DAMAGE_LOG.WG_CRITICS,
        PERSONAL_EFFICIENCY_TYPE.BLOCKED_DAMAGE: DAMAGE_LOG.WG_BLOCKED,
        PERSONAL_EFFICIENCY_TYPE.ASSIST_DAMAGE: DAMAGE_LOG.WG_ASSIST,
        PERSONAL_EFFICIENCY_TYPE.STUN: DAMAGE_LOG.WG_ASSIST
    }

    def __init__(self):
        self.config = {}
        g_events.onModSettingsChanged += self.onModSettingsChanged

    def fini(self):
        g_events.onModSettingsChanged -= self.onModSettingsChanged

    def filterEvents(self, events):
        for event in events:
            e_type = event.getType()
            if e_type in self.EFFICIENCY_TYPE_TO_CONFIG_KEY and self.config[self.EFFICIENCY_TYPE_TO_CONFIG_KEY[e_type]]:
                continue
            yield event

    def addToLog(self, base, component, events):
        return base(component, list(self.filterEvents(events)))

    def onModSettingsChanged(self, name, data):
        if name == DAMAGE_LOG.WG_LOGS_FIX:
            self.config = data
            toggleOverride(_LogViewComponent, "addToLog", self.addToLog, data[GLOBAL.ENABLED])
            self.updatePositions(data[GLOBAL.ENABLED] and data[DAMAGE_LOG.WG_POS])

    def updatePositions(self, enabled):
        DamageLogPanel._addToTopLog, DamageLogPanel._updateTopLog, DamageLogPanel._updateBottomLog, DamageLogPanel._addToBottomLog = \
            reversed(self.BASE_WG_LOGS) if enabled else self.BASE_WG_LOGS


logs_fix = WG_Logs_Fix()


def fini():
    logs_fix.fini()


@overrideMethod(OnVehicleShaked, '_onVehicleShaked')
def onVehicleShaken(base, shake, vehicleId, shakeReason):
    entity = BigWorld.entity(vehicleId)
    if entity is None:
        return
    shake._vehicle.setValue(weakref.proxy(entity))
    shake._shakeReason.setValue(shakeReason)
    shake._out.call()

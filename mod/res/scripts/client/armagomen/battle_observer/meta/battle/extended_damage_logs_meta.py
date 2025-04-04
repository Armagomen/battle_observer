from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class ExtendedDamageLogsMeta(BaseModMeta):

    def __init__(self):
        super(ExtendedDamageLogsMeta, self).__init__()

    def as_createExtendedLogsS(self, position, top_enabled, bottom_enabled):
        return self.flashObject.as_createExtendedLogs(position, top_enabled, bottom_enabled) if self._isDAAPIInited() else None

    def as_updateExtendedLogS(self, name, text):
        return self.flashObject.as_updateExtendedLog(name, text) if self._isDAAPIInited() else None

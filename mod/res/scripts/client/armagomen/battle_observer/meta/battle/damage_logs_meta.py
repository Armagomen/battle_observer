from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class DamageLogsMeta(BaseModMeta):

    def __init__(self):
        super(DamageLogsMeta, self).__init__()

    def as_createExtendedLogsS(self, position, top_enabled, bottom_enabled, isComp7):
        return self.flashObject.as_createExtendedLogs(position, top_enabled,
                                                      bottom_enabled, isComp7) if self._isDAAPIInited() else None

    def as_createTopLogS(self, settings):
        return self.flashObject.as_createTopLog(settings) if self._isDAAPIInited() else None

    def as_updateExtendedLogS(self, name, text):
        return self.flashObject.as_updateExtendedLog(name, text) if self._isDAAPIInited() else None

    def as_updateTopLogS(self, text):
        return self.flashObject.as_updateTopLog(text) if self._isDAAPIInited() else None

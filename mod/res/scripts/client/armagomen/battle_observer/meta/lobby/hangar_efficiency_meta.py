from armagomen.battle_observer.meta.lobby.base_mod_meta import BaseModMeta


class HangarEfficiencyMeta(BaseModMeta):

    def __init__(self):
        super(HangarEfficiencyMeta, self).__init__()

    def as_onSettingsChanged(self, config):
        return self.flashObject.as_onSettingsChanged(config) if self._isDAAPIInited() else None

    def as_updateValue(self, value):
        return self.flashObject.as_updateValue(value) if self._isDAAPIInited() else None

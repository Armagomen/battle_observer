from armagomen.battle_observer.meta.lobby.base_mod_meta import BaseModMeta


class DateTimesMeta(BaseModMeta):

    def __init__(self):
        super(DateTimesMeta, self).__init__()

    def getTimeString(self):
        return 'TEST STRING'

    def as_onSettingsChanged(self, config):
        return self.flashObject.as_onSettingsChanged(config) if self._isDAAPIInited() else None

    def setVisible(self, visible):
        return self.flashObject.as_setVisible(visible) if self._isDAAPIInited() else None

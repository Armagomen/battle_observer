from armagomen._constants import GLOBAL
from armagomen.battle_observer.meta.lobby.base_mod_meta import BaseModMeta


class DateTimesMeta(BaseModMeta):

    def __init__(self):
        super(DateTimesMeta, self).__init__()

    def as_setDateTimeS(self, text=GLOBAL.EMPTY_LINE):
        return self.flashObject.as_setDateTime(text) if self._isDAAPIInited() else None

    def as_clearSceneS(self):
        return self.flashObject.as_clearScene() if self._isDAAPIInited() else None

    def as_onSettingsChanged(self, config):
        return self.flashObject.as_onSettingsChanged(config) if self._isDAAPIInited() else None

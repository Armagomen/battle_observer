from armagomen.battle_observer.settings import user_settings
from armagomen.utils.logging import logDebug
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent


class BaseModMeta(BaseDAAPIComponent):

    def __init__(self):
        super(BaseModMeta, self).__init__()
        self.settings = None

    def _populate(self):
        super(BaseModMeta, self)._populate()
        logDebug("hangar module '{}' loaded", self.getAlias())

    def _dispose(self):
        logDebug("hangar module '{}' dispose", self.getAlias())
        super(BaseModMeta, self)._dispose()

    def setAlias(self, alias):
        super(BaseModMeta, self).setAlias(alias)
        self.settings = user_settings.getSettingDictByAliasLobby(alias)

    def as_startUpdateS(self, *args):
        return self.flashObject.as_startUpdate(*args) if self._isDAAPIInited() else None

    def getSettings(self):
        return self.settings

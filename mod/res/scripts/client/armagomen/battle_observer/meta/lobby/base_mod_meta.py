from armagomen.battle_observer.settings.default_settings import settings
from armagomen.utils.common import logDebug
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent


class BaseModMeta(BaseDAAPIComponent):

    def __init__(self):
        super(BaseModMeta, self).__init__()

    @staticmethod
    def getShadowSettings():
        return settings.shadow_settings

    def _populate(self):
        super(BaseModMeta, self)._populate()
        logDebug("hangar module '{}' loaded", self.getAlias())

    def _dispose(self):
        logDebug("hangar module '{}' dispose", self.getAlias())
        super(BaseModMeta, self)._dispose()

    def as_startUpdateS(self, *args):
        return self.flashObject.as_startUpdate(*args) if self._isDAAPIInited() else None

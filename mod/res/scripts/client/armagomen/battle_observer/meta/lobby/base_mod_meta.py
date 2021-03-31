from armagomen.battle_observer.core import settings
from armagomen.battle_observer.core.bo_constants import MAIN
from armagomen.utils.common import logInfo
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent


class BaseModMeta(BaseDAAPIComponent):

    def __init__(self):
        super(BaseModMeta, self).__init__()

    @staticmethod
    def getShdowSettings():
        return settings.shadow_settings

    def _populate(self):
        super(BaseModMeta, self)._populate()
        if settings.main[MAIN.DEBUG] and self._isDAAPIInited():
            logInfo("hangar module '%s' loaded" % self.getAlias())

    def _dispose(self):
        if settings.main[MAIN.DEBUG] and self._isDAAPIInited():
            logInfo("hangar module '%s' dispose" % self.getAlias())
        super(BaseModMeta, self)._dispose()

    def as_startUpdateS(self, *args):
        return self.flashObject.as_startUpdate(*args) if self._isDAAPIInited() else None

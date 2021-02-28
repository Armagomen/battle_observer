from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent
from ...core import cfg
from ...core.bo_constants import GLOBAL
from ...core.utils.bw_utils import logInfo


class BaseModMeta(BaseDAAPIComponent):

    def __init__(self):
        super(BaseModMeta, self).__init__()

    @staticmethod
    def getShdowSettings():
        return cfg.shadow_settings

    def _populate(self):
        super(BaseModMeta, self)._populate()
        if GLOBAL.DEBUG_MODE and self._isDAAPIInited():
            moduleName = self.flashObject.name.split("_")[1]
            logInfo("hangar module '%s' loaded" % moduleName)

    def _dispose(self):
        if GLOBAL.DEBUG_MODE and self._isDAAPIInited():
            moduleName = self.flashObject.name.split("_")[1]
            logInfo("hangar module '%s' dispose" % moduleName)
        super(BaseModMeta, self)._dispose()

    def as_startUpdateS(self, *args):
        return self.flashObject.as_startUpdate(*args) if self._isDAAPIInited() else None

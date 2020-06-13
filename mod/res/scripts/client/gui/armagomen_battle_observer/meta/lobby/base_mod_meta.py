from BigWorld import logInfo
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent
from ...core.config import cfg
from ...core.bo_constants import MOD_NAME, GLOBAL

class BaseModMeta(BaseDAAPIComponent):

    def __init__(self):
        super(BaseModMeta, self).__init__()

    def getShdowSettings(self):
        return cfg.shadow_settings

    def _populate(self):
        super(BaseModMeta, self)._populate()
        if GLOBAL.DEBUG_MODE and self._isDAAPIInited():
            moduleName = self.flashObject.name.split("_")[1]
            logInfo(MOD_NAME, "hangar module '%s' loaded" % moduleName, None)

    def _dispose(self):
        if GLOBAL.DEBUG_MODE and self._isDAAPIInited():
            moduleName = self.flashObject.name.split("_")[1]
            logInfo(MOD_NAME, "hangar module '%s' dispose" % moduleName, None)
        super(BaseModMeta, self)._dispose()

    def as_startUpdateS(self, *args):
        return self.flashObject.as_startUpdate(*args) if self._isDAAPIInited() else None
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.logging import logDebug
from frameworks.wulf.gui_constants import ShowingStatus
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent
from helpers import dependency
from skeletons.gui.impl import IGuiLoader


class BaseModMeta(BaseDAAPIComponent):
    SHOWING_STATUS_TO_VALUE = {ShowingStatus.SHOWN.value: True, ShowingStatus.HIDING.value: False}
    gui = dependency.descriptor(IGuiLoader)

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

    def getSettings(self):
        return self.settings

    def setVisible(self, visible):
        if self._isDAAPIInited():
            self.flashObject.visible = visible
